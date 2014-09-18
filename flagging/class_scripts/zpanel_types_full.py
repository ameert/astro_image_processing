from mysql_class import *
from flag_defs import *
import pylab as pl
import matplotlib.ticker as mticker
import scikits.bootstrap as bootstrap  

def print_flags(flag_vals):
    flag_num = np.sum(flag_vals)/float(len(flag_vals))
    if np.isnan(flag_num):
        flag_num = 0.0
    return flag_num

class MyLocator(mticker.MaxNLocator):
    def __init__(self, *args, **kwargs):
        mticker.MaxNLocator.__init__(self, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return mticker.MaxNLocator.__call__(self, *args, **kwargs)


def get_ci(data, ci):
    ci_vals = bootstrap.ci(data=data, alpha = ci, statfunction=print_flags, 
                           n_samples = 10)
    return ci_vals
        

def get_flag_props(flags_to_use, autoflag, binval, bins):
    props = dict([(f, []) for f in flags_to_use] + [(str(f)+'_err', []) for f in flags_to_use])
    props['total'] = []

    binpos = np.digitize(binval, bins)
    
    for scanval in range(1, bins.size):
        print scanval
        new_arr = np.extract(binpos == scanval, autoflag)
        for flag in flags_to_use:
            print "flag ", flag
            flag_vals = np.where(np.abs(new_arr-flag)<0.1, 1,0)
            props[flag].append(print_flags(flag_vals))
            print "percent ", props[flag][-1]
            if props[flag][-1]>0.01:
                props[str(flag)+'_err'].append((get_ci(flag_vals, 0.05)- props[flag][-1])*np.array([-1,1]))
            else:
                props[str(flag)+'_err'].append((np.nan,np.nan))
            print "CI ", props[str(flag)+'_err'][-1]
        props['total'].append(new_arr.size)
    return props

def get_vals(): 
    cmd = """select c.galcount,c.flag, """
    
    if choice =='nair':
        cmd +="""IF(n.ttype>20,12,n.ttype), """
    else:
        cmd += """-4.5775*m.probaEll -2.35723*m.probaS0+2.48028*m.probaSab+6.0815*m.probaScd, """
        
    cmd += """a.n_bulge from catalog.Flags_catalog as c, catalog.M2010 as m, r_band_serexp as a """
    if choice == 'full':
        cmd += """ where """
    else:

        cmd += """, catalog.Nair as n where c.galcount = n.galcount and """
    
    cmd += """c.galcount = a.galcount and c.galcount = m.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by c.galcount;""".format(model = model, band = band)

    galcount, flags, flag2, nbulge = cursor.get_data(cmd)
    galcount = np.array(galcount, dtype=int)
    autoflag = np.array(flags, dtype=int)
    nbulge= np.array(nbulge, dtype=float)
    autoflag = np.where(autoflag&2**1>0,1,0)+np.where(autoflag&2**4>0,2,0)+np.where(autoflag&2**10>0,3,0)*np.where(nbulge<7.95,1,0)+np.where(autoflag&2**14>0,4,0)+np.where(autoflag&2**20>0,5,0)+np.where(autoflag&2**10>0,6,0)*np.where(nbulge>=7.95,1,0)
    autoflag = autoflag.astype(int)

    flag2 = np.array(flag2)

    return galcount, autoflag, flag2

def plot_props(xlab, props, magbins, flags_to_use,plot_info):
    print "plotting"
    print "mask"
    print props['datamask']
    print 'data'
    magbinctr = (magbins[1:]+magbins[0:-1])/2

    ax2 = pl.gca()
    pl.xlabel(xlab)

#    ax2 = pl.twinx()

    for flag in flags_to_use:
        print magbinctr
        print props[flag]
        print props[str(flag)+'_err']
        print magbinctr[props['datamask']]
        print np.array(props[flag])[props['datamask']]
        print np.array(props[str(flag)+'_err'])[props['datamask'],:].T
#        ax2.plot(magbinctr, props[flag], marker = 'o', ms = plot_info[flag]['ms'], ls = '-', color = plot_info[flag]['color'], label = plot_info[flag]['label'])
        ax2.errorbar(magbinctr[props['datamask']],  np.array(props[flag])[props['datamask']], yerr=np.array(props[str(flag)+'_err'])[props['datamask'],:].T,
                 fmt='-', ecolor=plot_info[flag]['color'], elinewidth=1, 
                 capsize=3, marker = 'o', ms = plot_info[flag]['ms'], 
                 label = plot_info[flag]['label'], color =plot_info[flag]['color'] )

        ax2.set_ylabel('fraction of galaxies', fontsize=8)
        #ax2.set_ylabel('Total galaxies', fontsize=8)

        #ax1.yaxis.tick_right()
        #ax1.yaxis.set_label_position("right")
        #ax2.yaxis.tick_left()
        #ax2.yaxis.set_label_position("left")

        ax2.set_ylim(0,1.0)

    #ax1.bar(magbins[:-1], props['total'],width = 0.5,  color = plot_info['total']['color'], log = False, zorder = -100) 

    
    #for tick in ax1.yaxis.get_major_ticks():
    #    tick.set_label('%2.1e' %float(tick.get_label())) 
    
        #ticklabs = ax1.get_yticklabels()
        #print ticklabs
        #print ['%2.1e' %float(x.get_text()) for x in ticklabs]
        #ax1.set_yticklabels( ['%2.1e' %float(x) for x in ticklabs] )
    return ax2

cursor = mysql_connect('catalog','pymorph','pymorph','')

band = 'r'
model = 'serexp'
choice = 'full'
flags_to_use = np.array([1,2,3,4,5,6])

plot_info = {1:{'color':'r', 'label':'bulges', 'ms':3},
             2:{'color':'b', 'label':'disks', 'ms':3},
             3:{'color':'g', 'label':'2com', 'ms':3},
             4:{'color':'y', 'label':'bad 2com', 'ms':3},
             5:{'color':'k', 'label':'bad', 'ms':3},
             6:{'color':'c', 'label':'2nh', 'ms':3},
             'total': {'color':"#D0D0D0",'label':'total'}
             }

names=[ plot_info[key]['label'] for key in plot_info.keys()] 
fig = pl.figure(figsize=(6,6))
pl.subplots_adjust(right = 0.95, left =0.1, hspace = 0.5, wspace = 0.75)

typebins = np.arange(-6.5, 12.51, 1.0)

print "meert" 
pl.subplot(1,1,1)

galcount, autoflag, stype = get_vals()

nair_typebins = typebins
nair_names= [str(a) for a in typebins]
props = get_flag_props(flags_to_use, autoflag, stype,nair_typebins)
print props['total']
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
print props.keys()
print props
ax2 =plot_props('T', props, nair_typebins, flags_to_use,plot_info)
#pl.xticks(np.arange(len(nair_names))-3, nair_names, fontsize = 8)
pl.title('Meert types by TType')
#pl.xticks(rotation=90)
pl.xlim(-6,12.5)
l = ax2.legend(loc='center', bbox_to_anchor=(-1.5, 0.5))


#pl.show()
if choice =='nair_marc':
    pl.savefig('./types_dist_nair_marc_{band}_{model}.eps'.format(band=band, model=model))
elif choice =='nair':
    pl.savefig('./types_dist_nair_{band}_{model}.eps'.format(band=band, model=model))
elif choice =='full':
    pl.savefig('./types_dist_full_{band}_{model}.eps'.format(band=band, model=model))

