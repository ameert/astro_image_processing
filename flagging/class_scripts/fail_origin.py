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

def get_flag_props(flags_to_use, autoflag, binvalx, binvaly, bins):
    props = dict([(f, []) for f in flags_to_use])
    props['total'] = []

    binpos, xedge, yedge = np.histogram2d(binvalx, binvaly, bins=bins) 

    colsum = np.sum(binpos, axis=0)

    print binpos
    print colsum
    binpos = binpos /colsum
    print binpos
    
#    for scanval in range(1, bins.size):
#        new_arr = np.extract(binpos == scanval, autoflag)
        
        
#        for flag in flags_to_use:
#            props[flag].append(print_flags(new_arr, flag))
#        props['total'].append(new_arr.size)
    return binpos



def get_vals(binval1, binval2): 
    cmd = """select a.galcount, a.flag, %s, %s from Flags_catalog as a, M2010 as b, CAST as c, DERT as d, r_band_serexp as f, SSDR6 as z   where a.flag >=0 and a.band = 'r' and a.model = 'serexp' and a.ftype = 'u' and a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and a.galcount = f.galcount and a.galcount = z.galcount and a.flag&pow(2,20)>0 order by a.galcount limit 1000000;""" %(binval1, binval2)

    galcount, flags, binval1, binval2 = cursor.get_data(cmd)
    galcount = np.array(galcount, dtype=int)
    autoflag = np.array(flags, dtype=int)
    binval1 = np.array(binval1, dtype=float)
    binval2 = np.array(binval2, dtype=float)
    
    return galcount, autoflag, binval1, binval2

cursor = mysql_connect('catalog','pymorph','pymorph','')

band = 'r'
model = 'serexp'

flags_to_use = [1,4,10,14,20]

plot_info = {1:{'color':'r', 'label':'bulges', 'ms':3},
             4:{'color':'b', 'label':'disks', 'ms':3},
             10:{'color':'g', 'label':'2com', 'ms':3},
             14:{'color':'y', 'label':'bad 2com', 'ms':3},
             20:{'color':'k', 'label':'bad', 'ms':3},
             'total': {'color':"#D0D0D0",'label':'total'}
             }

fig = pl.figure(figsize=(8,6))
pl.subplots_adjust(right = 0.85, left =0.1, hspace = 0.5, wspace = 0.75)

print "absmag" 
#pl.subplot(3,2,2)

delta = 0.25
magbins = np.arange(-25.0, -17.0, delta)
galcount, autoflag, mag_petro, mag_serexp = get_vals("c.petromag_r-d.dismod-d.kcorr_r-c.extinction_r","f.m_tot-d.dismod-d.kcorr_r-c.extinction_r")
props = get_flag_props(flags_to_use, autoflag, mag_petro, mag_serexp, magbins)
#plot_props('M$_r$', props, magbins, delta, flags_to_use,plot_info)

pl.imshow(props, extent = (magbins[0], magbins[-1], magbins[0], magbins[-1]), vmin = 0, interpolation = 'nearest', origin = 'lower')
xlim = pl.xlim()
ylim = pl.ylim()
pl.ylabel('M$_{petro}$')
pl.xlabel('M$_{serexp}$')
pl.colorbar()
pl.plot([-25,-17],[-25,-17], 'r-')
pl.xlim(xlim)
pl.ylim(ylim)
pl.savefig('failed_origin_petro.eps')

