from astro_image_processing.mysql.mysql_class import *
from flag_defs import *
import pylab as pl
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt

try:
    import scikits.bootstrap as bootstrap  

    def get_ci(data, ci):
        try:
            ci_vals = bootstrap.ci(data=data, alpha = ci, 
                                   statfunction=print_flags, 
                                   n_samples = 10)
        except:
            ci_vals = [-1.0,1.0]
        return ci_vals
except ImportError:
    print "Failed to import scikits.bootstrap!!!"
    print "Error bars will not be correct!!!"
    def get_ci(data, ci):
        return [-1.0,1.0]

def print_flags(autoflag, test_flag, print_gals = False):
    if test_flag == 10:
        flag_vals = np.where(autoflag&2**test_flag>0, 1,0)*np.where(autoflag&2**14==0, 1,0)
    else:
        flag_vals = np.where(autoflag&2**test_flag>0, 1,0)
    flag_num = float(np.sum(flag_vals))
    if np.isnan(flag_num):
        flag_num = 0.0
    if print_gals:
        print "flag %d: %.4f" %(test_flag, flag_num)
    return flag_num

class MyLocator(mticker.MaxNLocator):
    def __init__(self, *args, **kwargs):
        mticker.MaxNLocator.__init__(self, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return mticker.MaxNLocator.__call__(self, *args, **kwargs)

def get_flag_props(flags_to_use, autoflag, binval, bins, do_ci=False):
    props = dict([(f, []) for f in flags_to_use] + 
                 [(str(f)+'_err', []) for f in flags_to_use])
    props['total'] = []

    binpos = np.digitize(binval, bins)
    
    for scanval in range(1, bins.size):
        new_arr = np.extract(binpos == scanval, autoflag)
                
        for flag in flags_to_use:
            props[flag].append(print_flags(new_arr, flag))
            # this part may not be correct....
            if do_ci:
                if props[flag][-1]>0.01:
                    props[str(flag)+'_err'].append((get_ci(flag_vals, 0.05)- props[flag][-1])*np.array([-1,1]))
                else:
                    props[str(flag)+'_err'].append((np.nan,np.nan))
        props['total'].append(new_arr.size)
    return props

def flag_norm(flags_to_use, props, normtype):
    """normalizes flags in one of several ways:
    xbin: normalizes by bin count so that flag fraction sums bin-wise to 1
    flagclass:normalizes by flag so that flag fraction sums to 1 across all xbins for each flag
    total: normalize by total galaxy count
    """
    props['total'] = np.array(props['total'], dtype=float)
    for flag in flags_to_use:
        props[flag] = np.array(props[flag], dtype=float)        
        if normtype=='xbin':
            props[flag] = props[flag]/props['total']
        elif normtype=='flagclass':
            props[flag] = props[flag]/np.sum(props[flag])
        elif normtype=='total':
            props[flag] = props[flag]/np.sum(props['total'])
    return props

def plot_props(xlab, props, magbins, delta, flags_to_use,plot_info,do_ci=False):
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
        if do_ci:
            ax2.errorbar(magbinctr, np.array(props[flag]),
                yerr=np.array(props[str(flag)+'_err']).T,
                ecolor=plot_info[flag]['color'], elinewidth=1, 
                capsize=3, marker = plot_info[flag]['marker'],
                ms = plot_info[flag]['ms'], ls = plot_info[flag]['ls'], 
                color = plot_info[flag]['color'], 
                label = plot_info[flag]['label'])
        else:
            ax2.plot(magbinctr, np.array(props[flag]), 
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


    ax1.bar(magbins[:-1], props['total'], width = delta, color = plot_info['total']['color'], log = False, zorder = -100) 

    ax1.xaxis.set_major_locator(xloc)
    ax2.xaxis.set_major_locator(xloc)
    ax1.yaxis.set_major_locator(ylocr)
    ax2.yaxis.set_major_locator(ylocl)
    ax2.set_ylim(0,1.0)

    #for tick in ax1.yaxis.get_major_ticks():
    #    tick.set_label('%2.1e' %float(tick.get_label())) 
            
        #ticklabs = ax1.get_yticklabels()
        #print ticklabs
        #print ['%2.1e' %float(x.get_text()) for x in ticklabs]
        #ax1.set_yticklabels( ['%2.1e' %float(x) for x in ticklabs] )
    return ax1, ax2
