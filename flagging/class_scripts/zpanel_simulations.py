from mysql_class import *
from flag_defs import *
import pylab as pl
import matplotlib.ticker as mticker

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
    cmd = """select a.galcount, x.flag, a.flag, %s from Flags_optimize as a,catalog.Flags_optimize as x, M2010 as b, CAST as c, DERT as d, r_sims_serexp as f   where x.galcount = c.true_galcount and  x.band = 'r' and x.model = 'serexp' and x.ftype = 'u' and a.flag >=0 and a.band = 'r' and a.model = 'serexp' and a.ftype = 'u' and a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and a.galcount = f.galcount and a.galcount > 20000 order by a.galcount limit 1000000;""" %binval

    galcount, flags_before, flags_after, binvals = cursor.get_data(cmd)
    galcount = np.array(galcount, dtype=int)
    autoflag_before = np.array(flags_before, dtype=int)
    autoflag_after = np.array(flags_after, dtype=int)
    binvals = np.array(binvals, dtype=float)
    
    return galcount, autoflag_before, binvals

def plot_props(xlab, props, magbins, delta, flags_to_use,plot_info):
    magbinctr = (magbins[1:]+magbins[0:-1])/2

    ax1 = pl.gca()
    pl.xlabel(xlab)

    ax2 = pl.twinx()

    for flag in flags_to_use:
        ax2.plot(magbinctr, props[flag], marker = 'o', ms = plot_info[flag]['ms'], ls = '-', color = plot_info[flag]['color'], label = plot_info[flag]['label'])


        ax2.set_ylabel('fraction of galaxies', fontsize=8)
        ax1.set_ylabel('Total galaxies', fontsize=8)

        ax1.yaxis.tick_right()
        ax1.yaxis.set_label_position("right")
        ax2.yaxis.tick_left()
        ax2.yaxis.set_label_position("left")

        ax2.set_ylim(0,1.0)

    ax1.bar(magbins[:-1], props['total'], width = delta, color = plot_info['total']['color'], log = False, zorder = -100) 

        
    #for tick in ax1.yaxis.get_major_ticks():
    #    tick.set_label('%2.1e' %float(tick.get_label())) 
            
        #ticklabs = ax1.get_yticklabels()
        #print ticklabs
        #print ['%2.1e' %float(x.get_text()) for x in ticklabs]
        #ax1.set_yticklabels( ['%2.1e' %float(x) for x in ticklabs] )
    return ax1, ax2

cursor = mysql_connect('simulations','pymorph','pymorph','')

band = 'r'
model = 'serexp'

flags_to_use = [1,4,10,14,19]

plot_info = {1:{'color':'r', 'label':'bulges', 'ms':3},
             4:{'color':'b', 'label':'disks', 'ms':3},
             10:{'color':'g', 'label':'2com', 'ms':3},
             14:{'color':'y', 'label':'bad 2com', 'ms':3},
             19:{'color':'k', 'label':'bad', 'ms':3},
             'total': {'color':"#D0D0D0",'label':'total'}
             }

fig = pl.figure(figsize=(8,6))
pl.subplots_adjust(right = 0.85, left =0.1, hspace = 0.5, wspace = 0.75)


print "appmag" 
pl.subplot(3,2,1)

delta = 0.25
magbins = np.arange(13.25, 18.76, delta)
galcount, autoflag, mag = get_vals("f.m_tot")
props = get_flag_props(flags_to_use, autoflag, mag, magbins)
plot_props('m$_r$', props, magbins, delta, flags_to_use,plot_info)


print "apprad" 
pl.subplot(3,2,3)

delta = 0.5
radbins = np.arange(0.0, 8.0, delta)
galcount, autoflag, rad = get_vals("f.Hrad_corr")
props = get_flag_props(flags_to_use, autoflag, rad, radbins)
plot_props('r$_{hl, arcsec}$', props, radbins, delta, flags_to_use,plot_info)

print "z" 
pl.subplot(3,2,5)

delta = 0.025
zbins = np.arange(0.0, 0.3, delta)
galcount, autoflag, z = get_vals("c.z")
props = get_flag_props(flags_to_use, autoflag, z, zbins)
plot_props('z', props, zbins, delta, flags_to_use,plot_info)

print "absmag" 
pl.subplot(3,2,2)

delta = 0.5
magbins = np.arange(-25.0, -17.0, delta)
galcount, autoflag, mag = get_vals("f.m_tot-d.dismod-d.kcorr_r-c.extinction_r")
props = get_flag_props(flags_to_use, autoflag, mag, magbins)
plot_props('M$_r$', props, magbins, delta, flags_to_use,plot_info)


print "ABSrad" 
pl.subplot(3,2,4)

delta = 2.5
radbins = np.arange(0.0, 20.01, delta)
galcount, autoflag, rad = get_vals("f.Hrad_corr*d.kpc_per_arcsec")
props = get_flag_props(flags_to_use, autoflag, rad, radbins)
ax1, ax2 = plot_props('R$_{hl, kpc}$', props, radbins, delta, flags_to_use,plot_info)

l = ax2.legend(loc='center', bbox_to_anchor=(0.5, -1.05))


#pl.show()
pl.savefig('./dist_obs_simulation.eps')

