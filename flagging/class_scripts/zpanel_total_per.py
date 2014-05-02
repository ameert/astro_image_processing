from mysql.mysql_class import *
from flag_defs import *
import pylab as pl
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt

def print_flags(autoflag, test_flag, print_gals = False):
    if test_flag == 10:
        flag_vals = np.where(autoflag&2**test_flag>0, 1,0)*np.where(autoflag&2**14==0, 1,0)
    else:
        flag_vals = np.where(autoflag&2**test_flag>0, 1,0)
    flag_num = np.sum(flag_vals)/float(len(flag_vals))
    if np.isnan(flag_num):
        flag_num = 0.0
    #print "%d: %.4f" %(test_flag, flag_num)
    #if print_gals:
    #    print np.extract(flag_vals==1, galcount)
    return flag_num

class MyLocator(mticker.MaxNLocator):
    def __init__(self, *args, **kwargs):
        mticker.MaxNLocator.__init__(self, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return mticker.MaxNLocator.__call__(self, *args, **kwargs)

def get_flag_props(flags_to_use, autoflag, binval, bins):
    props = dict([(f, []) for f in flags_to_use])
    props['total'] = []

    binpos = np.digitize(binval, bins)
    
    for scanval in range(1, bins.size):
        new_arr = np.extract(binpos == scanval, autoflag)
        
        
        for flag in flags_to_use:
            props[flag].append(print_flags(new_arr, flag))
        props['total'].append(new_arr.size)
    return props

def get_vals(binval): 
#    cmd = """select a.galcount, a.flag, %s from Flags_optimize as a, M2010 as b, CAST as c, DERT as d, r_band_serexp as f, SSDR6 as z   where a.flag >=0 and a.band = 'r' and a.model = 'serexp' and a.ftype = 'u' and a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and a.galcount = f.galcount and a.galcount = z.galcount order by a.galcount limit 1000000;""" %binval

    cmd = """select a.galcount, IF(a.flag&pow(2,10)>0, IF(f.n_bulge>7.95, a.flag^(pow(2,10)+pow(2,27)),a.flag),a.flag) , %s from Flags_optimize as a, M2010 as b, CAST as c, DERT as d, r_band_serexp as f where a.flag >=0 and a.band = 'r' and a.model = 'serexp' and a.ftype = 'u' and a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and a.galcount = f.galcount order by a.galcount limit 1000000;""" %binval

    galcount, flags, binvals = cursor.get_data(cmd)
    galcount = np.array(galcount, dtype=int)
    autoflag = np.array(flags, dtype=int)
    binvals = np.array(binvals, dtype=float)
    
    return galcount, autoflag, binvals

def plot_props(xlab, props, magbins, delta, flags_to_use,plot_info):
    magbinctr = (magbins[1:]+magbins[0:-1])/2

    ax1 = pl.gca()
    pl.xlabel(xlab)

    ax2 = pl.twinx()

    max_yticksl = 6
    max_yticksr = 5
    max_xticks = 5
    ylocl = plt.MaxNLocator(max_yticksl,prune='lower')
    ylocr = plt.MaxNLocator(max_yticksr,prune='lower')
    xloc = plt.MaxNLocator(max_xticks)

    for flag in flags_to_use:
        ax2.plot(magbinctr, np.array(props[flag])*np.array(props['total'])/np.sum(np.array(props['total'])), 
                 marker = plot_info[flag]['marker'],
                 ms = plot_info[flag]['ms'], ls = plot_info[flag]['ls'], 
                 color = plot_info[flag]['color'], 
                 label = plot_info[flag]['label'])


        ax2.set_ylabel('fraction of galaxies', fontsize=8)
        ax1.set_ylabel('Total galaxies', fontsize=8)

        ax1.yaxis.tick_right()
        ax1.yaxis.set_label_position("right")
        ax2.yaxis.tick_left()
        ax2.yaxis.set_label_position("left")

        #ax2.set_ylim(0,1.0)

    ax1.bar(magbins[:-1], props['total'], width = delta, color = plot_info['total']['color'], log = False, zorder = -100) 

    ax1.xaxis.set_major_locator(xloc)
    ax2.xaxis.set_major_locator(xloc)
    ax1.yaxis.set_major_locator(ylocr)
    ax2.yaxis.set_major_locator(ylocl)
        
    #for tick in ax1.yaxis.get_major_ticks():
    #    tick.set_label('%2.1e' %float(tick.get_label())) 
            
        #ticklabs = ax1.get_yticklabels()
        #print ticklabs
        #print ['%2.1e' %float(x.get_text()) for x in ticklabs]
        #ax1.set_yticklabels( ['%2.1e' %float(x) for x in ticklabs] )
    return ax1, ax2

cursor = mysql_connect('catalog','pymorph','pymorph','')

band = 'r'
model = 'serexp'

flags_to_use = [1,4,10,27,14,19]

plot_info = {1:{'color':'r', 'label':'bulges', 'ms':3, 'marker':'o', 'ls':'-'},
             4:{'color':'b', 'label':'disks', 'ms':3, 'marker':'s', 'ls':'-'},
             10:{'color':'g', 'label':'2com', 'ms':3, 'marker':'d', 'ls':'-'},
             14:{'color':'y', 'label':'bad 2com', 'ms':3, 'marker':'o', 'ls':'--'},
             27:{'color':'c', 'label':'n8', 'ms':3, 'marker':'s', 'ls':'--'},
             19:{'color':'k', 'label':'bad', 'ms':3, 'marker':'d', 'ls':'--'},
             'total': {'color':"#D0D0D0",'label':'total'}
             }

fig = pl.figure(figsize=(8,6))
pl.subplots_adjust(right = 0.85, left =0.1, hspace = 0.5, wspace = 0.75)


print "appmag" 
pl.subplot(3,2,1)

delta = 0.25
magbins = np.arange(13.25, 18.76, delta)
#galcount, autoflag, mag = get_vals('c.petromag_r-c.extinction_r')
galcount, autoflag, mag = get_vals('f.m_tot-c.extinction_r')
props = get_flag_props(flags_to_use, autoflag, mag, magbins)
plot_props('m$_r$', props, magbins, delta, flags_to_use,plot_info)


print "apprad" 
pl.subplot(3,2,3)

delta = 0.5
radbins = np.arange(0.0, 8.0, delta)
#galcount, autoflag, rad = get_vals('c.petror50_r')
galcount, autoflag, rad = get_vals("f.Hrad_corr")
props = get_flag_props(flags_to_use, autoflag, rad, radbins)
plot_props('r$_{hl, arcsec}$', props, radbins, delta, flags_to_use,plot_info)

print "ba" 
pl.subplot(3,2,5)

delta = 0.05
radbins = np.arange(0.0, 1.01, delta)
#galcount, autoflag, rad = get_vals("c.petror50_r*d.kpc_per_arcsec")
galcount, autoflag, rad = get_vals("f.ba_tot_corr")
props = get_flag_props(flags_to_use, autoflag, rad, radbins)
ax1, ax2 = plot_props('b/a$_{tot}$', props, radbins, delta, flags_to_use,plot_info)

print "absmag" 
pl.subplot(3,2,2)

delta = 0.5
magbins = np.arange(-25.0, -17.0, delta)
#galcount, autoflag, mag = get_vals("c.petromag_r-d.dismod-d.kcorr_r-c.extinction_r")
galcount, autoflag, mag = get_vals("f.m_tot-d.dismod-d.kcorr_r-c.extinction_r")
props = get_flag_props(flags_to_use, autoflag, mag, magbins)
plot_props('M$_r$', props, magbins, delta, flags_to_use,plot_info)


print "ABSrad" 
pl.subplot(3,2,4)

delta = 2.5
radbins = np.arange(0.0, 20.01, delta)
#galcount, autoflag, rad = get_vals("c.petror50_r*d.kpc_per_arcsec")
galcount, autoflag, rad = get_vals("f.Hrad_corr*d.kpc_per_arcsec")
props = get_flag_props(flags_to_use, autoflag, rad, radbins)
ax1, ax2 = plot_props('R$_{hl, kpc}$', props, radbins, delta, flags_to_use,plot_info)
print "ABSrad" 

if 0:
    pl.subplot(3,2,7)

    delta = 0.5
    magbins = np.arange(-25.0, -17.0, delta)
    #galcount, autoflag, mag = get_vals("c.petromag_r-d.dismod-d.kcorr_r-c.extinction_r")
    galcount, autoflag, mag = get_vals("f.m_tot-d.dismod-d.kcorr_r-c.extinction_r")
    props = get_flag_props(flags_to_use, autoflag, mag, magbins)
    plot_inflag_prop('M$_r$', props, magbins, delta, flags_to_use,plot_info)

    pl.subplot(3,2,6)

    delta = 2.5
    radbins = np.arange(0.0, 20.01, delta)
    #galcount, autoflag, rad = get_vals("c.petror50_r*d.kpc_per_arcsec")
    galcount, autoflag, rad = get_vals("f.Hrad_corr*d.kpc_per_arcsec")
    props = get_flag_props(flags_to_use, autoflag, rad, radbins)
    plot_inflag_prop('R$_{hl, kpc}$', props, radbins, delta, flags_to_use,plot_info)

#print "z" 
#pl.subplot(3,2,6)

#delta = 0.025
#zbins = np.arange(0.0, 0.3, delta)
#galcount, autoflag, z = get_vals("c.z")
#props = get_flag_props(flags_to_use, autoflag, z, zbins)
#plot_props('z', props, zbins, delta, flags_to_use,plot_info)


l = ax2.legend(loc='center', bbox_to_anchor=(0.5, -1.05), fontsize='10')


#pl.show()
pl.savefig('./dist_obs_total_per.eps')
#pl.savefig('./dist_obs_petro.eps')
#pl.savefig('./dist_obs_small_petro.eps')

