from mysql.mysql_class import *
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
    try:
        ci_vals = bootstrap.ci(data=data, alpha = ci, statfunction=print_flags, 
                               n_samples = 10)
    except:
        ci_vals = [-1.0,1.0]
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


def get_vals(binval):
 
    if binval == 'lackner':
        cmd = """select d.galcount,IF(d.model='dvc',7,0)+ IF(d.model='ser' and z.n_bulge>=2.0, 12,0)+IF(d.model='exp',8,0)+ IF(d.model='ser' and z.n_bulge<2.0, 11,0)+IF(d.model='nb1',9,0)+IF(d.model = 'nb4', 10,0),m.BT from catalog.r_band_serexp as m, catalog.r_lackner_fit as d, catalog.r_lackner_ser as z where m.galcount=d.galcount and d.galcount = z.galcount order by d.galcount  limit 1000000;"""
    elif binval == 'simard':
        cmd = """select d.galcount, IF(d.Prob_pS>0.32 and z.n_bulge>=2.0, 12,0)+IF(d.Prob_pS>0.32 and z.n_bulge<2.0, 11,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4>0.32, 13,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4<=0.32, 14,0),  m.BT from catalog.r_band_serexp  as m,  catalog.r_lackner_fit as c, catalog.r_simard_fit as d, catalog.r_simard_ser as z where m.galcount = c.galcount and c.galcount = d.galcount and c.galcount = z.galcount order by d.galcount  limit 1000000;"""
    elif binval == 'mendel':
        cmd = """select d.galcount, IF(d.Proftype=1, 15,0)+IF(d.Proftype=2, 16,0)+IF(d.Proftype=3, 17,0)+IF(d.Proftype=4 or d.Proftype<0,18,0),  m.BT from catalog.r_band_serexp  as m,  catalog.r_lackner_fit as c, catalog.r_simard_fit as d, catalog.r_simard_ser as z where m.galcount = c.galcount and c.galcount = d.galcount and c.galcount = z.galcount order by d.galcount  limit 1000000;"""
    elif binval == 'meert':
        cmd = """select c.galcount,IF(c.flag&pow(2,1)>0,1,0)+ IF(c.flag&pow(2,4)>0,2,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge<7.95,3,0)+ IF(c.flag&pow(2,14)>0,4,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge>=7.95,6,0)+IF(c.flag&pow(2,19)>0,5,0)  ,m.BT from catalog.r_band_serexp  as m, catalog.Flags_optimize as c, catalog.r_lackner_fit as z, catalog.r_band_serexp as d  where m.galcount = c.galcount and d.galcount = c.galcount and c.galcount = z.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by c.galcount  limit 1000000;""".format(model = 'serexp', band = 'r')
    elif binval == 'nair_lackner':
        cmd = """select d.galcount,IF(d.model='dvc',7,0)+ IF(d.model='ser' and z.n_bulge>=2.0, 12,0)+IF(d.model='exp',8,0)+ IF(d.model='ser' and z.n_bulge<2.0, 11,0)+IF(d.model='nb1',9,0)+IF(d.model = 'nb4', 10,0),n.ttype from catalog.M2010 as m, catalog.r_lackner_fit as d, catalog.r_lackner_ser as z, catalog.Nair as n where m.galcount=d.galcount and n.galcount = d.galcount and d.galcount = z.galcount order by d.galcount  limit 10000000;"""
    elif binval == 'nair_simard':
        cmd = """select d.galcount, IF(d.Prob_pS>0.32 and z.n_bulge>=2.0, 12,0)+IF(d.Prob_pS>0.32 and z.n_bulge<2.0, 11,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4>0.32, 13,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4<=0.32, 14,0),  n.ttype from catalog.M2010 as m,  catalog.r_lackner_fit as c, catalog.r_simard_fit as d, catalog.r_simard_ser as z, catalog.Nair as n where m.galcount = c.galcount and n.galcount = c.galcount  and c.galcount = d.galcount and c.galcount = z.galcount order by d.galcount  limit 10000000;"""
    elif binval == 'nair_meert':
        cmd = """select c.galcount,IF(c.flag&pow(2,1)>0,1,0)+ IF(c.flag&pow(2,4)>0,2,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge<7.95,3,0)+ IF(c.flag&pow(2,14)>0,4,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge>=7.95,6,0)+IF(c.flag&pow(2,19)>0,5,0)  ,n.ttype  from catalog.M2010 as m, catalog.Flags_optimize as c, catalog.r_lackner_fit as z, catalog.r_band_serexp as d, catalog.Nair as n  where m.galcount = c.galcount and n.galcount = c.galcount and d.galcount = c.galcount and c.galcount = z.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by c.galcount  limit 10000000;""".format(model = 'serexp', band = 'r')
    galcount, flags, flag2 = cursor.get_data(cmd)
    galcount = np.array(galcount, dtype=int)
    autoflag = np.array(flags, dtype=int)

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
    #l = ax2.legend(loc=3, bbox_to_anchor=(0.75, 0.9), prop={'size':6})

    return ax2

cursor = mysql_connect('catalog','pymorph','pymorph','')

band = 'r'
model = 'serexp'


plot_info = {1:{'color':'r', 'label':'bulges', 'ms':3},
             2:{'color':'b', 'label':'disks', 'ms':3},
             3:{'color':'g', 'label':'2com', 'ms':3},
             4:{'color':'y', 'label':'bad 2com', 'ms':3},
             5:{'color':'k', 'label':'bad', 'ms':3},
             6:{'color':'c', 'label':'2nh', 'ms':3},
             7:{'color':'r', 'label':'dvc', 'ms':3},
             8:{'color':'b', 'label':'exp', 'ms':3},
             9:{'color':'g', 'label':'nb1', 'ms':3},
             10:{'color':'y', 'label':'nb4', 'ms':3},
             11:{'color':'c', 'label':'ser, n<2', 'ms':3},
             12:{'color':'k', 'label':'ser, n>=2', 'ms':3},
             13:{'color':'g', 'label':'devexp', 'ms':3},
             14:{'color':'y', 'label':'serexp', 'ms':3},
             15:{'color':'r', 'label':'dev', 'ms':3},
             16:{'color':'b', 'label':'exp', 'ms':3},
             17:{'color':'g', 'label':'devexp', 'ms':3},
             18:{'color':'k', 'label':'unknown', 'ms':3},
             'total': {'color':"#D0D0D0",'label':'total'}
             }

names=[ plot_info[key]['label'] for key in plot_info.keys()] 
fig = pl.figure(figsize=(8,6))
pl.subplots_adjust(right = 0.95, top = 0.8, left =0.1, bottom=0.13,
                   hspace = 0.38, wspace = 0.5)

typebins = np.arange(0.0, 1.01, 0.1)
x_names= [str(int(a)) for a in typebins+0.5]
#x_names = [ x_names[a] if a%2 ==0 else "" for a in range(len(x_names))] 


print "meert" 
pl.subplot(2,2,1)
flags_to_use = np.array([1,2,3,4,5,6])
galcount, autoflag, stype = get_vals('meert')
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
ax2 =plot_props('BT', props, typebins, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('Meert', fontsize=8)
#pl.xticks(rotation=90)
l = ax2.legend(loc=3, bbox_to_anchor=(1.0, 0.6), prop={'size':6})
pl.xlim(0.0,1.0)

print "simard" 
pl.subplot(2,2,2)
flags_to_use = np.array([11,12,13,14])
galcount, autoflag, stype = get_vals('simard')
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
ax2=plot_props('BT', props, typebins, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('S11', fontsize=8)
l = ax2.legend(loc=3, bbox_to_anchor=(0.05, 0.7), prop={'size':6})
#pl.xticks(rotation=90)
pl.xlim(0.0,1.0)

print "lackner" 
pl.subplot(2,2,3)
flags_to_use = np.array([7,8,9,10,11,12])
galcount, autoflag, stype = get_vals('lackner')
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
ax2=plot_props('BT', props, typebins, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('L12', fontsize=8)
l = ax2.legend(loc=3, bbox_to_anchor=(0.05, 0.6), prop={'size':6})
#pl.xticks(rotation=90)
pl.xlim(0.0,1.0)

print props.keys()
print props[12]
print props[10]
print np.array(props[12])/np.array(props[10])

print "mendel" 
pl.subplot(2,2,4)
flags_to_use = np.array([15,16,17,18])
galcount, autoflag, stype = get_vals('mendel')
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
ax2=plot_props('BT', props, typebins, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('Mendel', fontsize=8)
l = ax2.legend(loc=3, bbox_to_anchor=(0.7, 0.7), prop={'size':6})
#pl.xticks(rotation=90)
pl.xlim(0.0,1.0)


if 0:
    print "meert" 
    pl.subplot(2,3,4)
    flags_to_use = np.array([1,2,3,4,5,6])
    galcount, autoflag, stype = get_vals('nair_meert')
    props = get_flag_props(flags_to_use, autoflag, stype,typebins)
    props['datamask'] = np.where(np.array(props['total'])>0,True,False)
    ax2 =plot_props('T', props, typebins, flags_to_use,plot_info)
    pl.xticks(typebins+0.5, x_names, fontsize = 8)
    pl.title('Meert  (Nair)', fontsize=8)
    pl.xticks(rotation=90)
    #l = ax2.legend(loc='center', bbox_to_anchor=(-1.5, 0.5))
    pl.xlim(-6,14)

    print "simard" 
    pl.subplot(2,3,5)
    flags_to_use = np.array([11,12,13,14])
    galcount, autoflag, stype = get_vals('nair_simard')
    props = get_flag_props(flags_to_use, autoflag, stype,typebins)
    props['datamask'] = np.where(np.array(props['total'])>0,True,False)
    plot_props('T', props, typebins, flags_to_use,plot_info)
    pl.xticks(typebins+0.5, x_names, fontsize = 8)
    pl.title('Simard  (Nair)', fontsize=8)
    #pl.xticks(rotation=90)
    pl.xlim(-6,14)

    print "lackner" 
    pl.subplot(2,3,6)
    flags_to_use = np.array([7,8,9,10,11,12])
    galcount, autoflag, stype = get_vals('nair_lackner')
    props = get_flag_props(flags_to_use, autoflag, stype,typebins)
    props['datamask'] = np.where(np.array(props['total'])>0,True,False)
    plot_props('T', props, typebins, flags_to_use,plot_info)
    pl.xticks(typebins+0.5, x_names, fontsize = 8)
    pl.title('Lackner (Nair)', fontsize=8)
    #pl.xticks(rotation=90)
    pl.xlim(-6,14)


#pl.show()
pl.savefig('./types_dist_BT.eps', bbox_inches = 'tight')
#pl.savefig('./dist_obs_petro.eps')
#pl.savefig('./dist_obs_small_petro.eps')

