from mysql.mysql_class import *
from flag_defs import *
import pylab as pl
import matplotlib.ticker as mticker
import scikits.bootstrap as bootstrap  
import matplotlib 

def print_flags(autoflag, test_flag, print_gals = False):
    #if test_flag == 10:
    #    flag_vals = np.where(autoflag&2**test_flag>0, 1,0)*np.where(autoflag&2**14==0, 1,0)
    #else:
    flag_vals = np.where(autoflag==test_flag, 1,0)
    flag_num = np.sum(flag_vals)
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

def get_ci(data, ci):
    try:
        ci_vals = bootstrap.ci(data=data, alpha = ci, statfunction=print_flags, 
                               n_samples = 5)
    except:
        ci_vals = [-1.0,1.0]
    return ci_vals
        

def get_flag_props(flags_to_use, autoflag, binval, bins):
    props = dict([(f, []) for f in flags_to_use])
    props['total'] = []

    binpos = np.digitize(binval, bins)
    
    for scanval in range(1, bins.size):
        new_arr = np.extract(binpos == scanval, autoflag)
        print new_arr
        print new_arr.shape
        for flag in flags_to_use:
            props[flag].append(float(print_flags(new_arr, flag)))
        props['total'].append(new_arr.size)
    return props

def get_vals(binval):
 
    if binval == 'lackner':
        cmd = """select d.galcount,IF(d.model='dvc',7,0)+ IF(d.model='ser' and z.n_bulge>=2.0, 12,0)+IF(d.model='exp',8,0)+ IF(d.model='ser' and z.n_bulge<2.0, 11,0)+IF(d.model='nb1',9,0)+IF(d.model = 'nb4', 10,0),m.petromag_r-m.extinction_r-x.dismod-x.kcorr_r from catalog.CAST as m,catalog.DERT as x, catalog.r_lackner_fit as d, catalog.r_lackner_ser as z where m.galcount = x.galcount and m.galcount=d.galcount and d.galcount = z.galcount order by d.galcount  limit 1000000;"""
    elif binval == 'simard':
        cmd = """select d.galcount, IF(d.Prob_pS>0.32 and z.n_bulge>=2.0, 12,0)+IF(d.Prob_pS>0.32 and z.n_bulge<2.0, 11,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4>0.32, 13,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4<=0.32, 14,0),  m.petromag_r-m.extinction_r-x.dismod-x.kcorr_r from catalog.CAST as m,catalog.DERT as x, catalog.r_simard_fit as d, catalog.r_simard_ser as z where  m.galcount = x.galcount and m.galcount= d.galcount and m.galcount = z.galcount order by d.galcount  limit 1000000;"""
    elif binval == 'mendel':
        cmd = """select d.galcount, IF(d.Proftype=1, 15,0)+IF(d.Proftype=2, 16,0)+IF(d.Proftype=3, 17,0)+IF(d.Proftype=4 or d.Proftype<0,18,0),  m.petromag_r-m.extinction_r-x.dismod-x.kcorr_r from catalog.CAST as m,catalog.DERT as x,  catalog.r_simard_fit as d, catalog.r_simard_ser as z where  m.galcount = x.galcount and m.galcount = d.galcount and m.galcount = z.galcount order by d.galcount  limit 1000000;"""
    elif binval == 'meert':
        cmd = """select c.galcount,IF(c.flag&pow(2,1)>0,1,0)+ IF(c.flag&pow(2,4)>0,2,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge<7.95,3,0)+ IF(c.flag&pow(2,14)>0,4,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge>=7.95,6,0)+IF(c.flag&pow(2,19)>0,5,0)  ,m.petromag_r-m.extinction_r-x.dismod-x.kcorr_r from catalog.CAST as m,catalog.DERT as x, catalog.Flags_optimize as c, catalog.r_band_serexp as d  where  m.galcount = x.galcount and m.galcount = c.galcount and d.galcount = c.galcount  and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by c.galcount  limit 1000000;""".format(model = 'serexp', band = 'r')
    elif binval == 'simard_lackner':
        cmd = """select d.galcount, IF(d.Prob_pS>0.32 and z.n_bulge>=2.0, 12,0)+IF(d.Prob_pS>0.32 and z.n_bulge<2.0, 11,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4>0.32, 13,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4<=0.32, 14,0),  m.petromag_r-m.extinction_r-x.dismod-x.kcorr_r from catalog.CAST as m,catalog.DERT as x,  catalog.r_lackner_fit as c, catalog.r_simard_fit as d, catalog.r_simard_ser as z where  m.galcount = x.galcount and m.galcount = c.galcount and c.galcount = d.galcount and c.galcount = z.galcount order by d.galcount  limit 1000000;"""
    elif binval == 'mendel_lackner':
        cmd = """select d.galcount, IF(d.Proftype=1, 15,0)+IF(d.Proftype=2, 16,0)+IF(d.Proftype=3, 17,0)+IF(d.Proftype=4 or d.Proftype<0,18,0),  m.petromag_r-m.extinction_r-x.dismod-x.kcorr_r from catalog.CAST as m,catalog.DERT as x,  catalog.r_lackner_fit as c, catalog.r_simard_fit as d, catalog.r_simard_ser as z where  m.galcount = x.galcount and m.galcount = c.galcount and c.galcount = d.galcount and c.galcount = z.galcount order by d.galcount  limit 1000000;"""
    elif binval == 'meert_lackner':
        cmd = """select c.galcount,IF(c.flag&pow(2,1)>0,1,0)+ IF(c.flag&pow(2,4)>0,2,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge<7.95,3,0)+ IF(c.flag&pow(2,14)>0,4,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge>=7.95,6,0)+IF(c.flag&pow(2,19)>0,5,0)  ,m.petromag_r-m.extinction_r-x.dismod-x.kcorr_r from catalog.CAST as m,catalog.DERT as x, catalog.Flags_optimize as c, catalog.r_lackner_fit as z, catalog.r_band_serexp as d  where  m.galcount = x.galcount and m.galcount = c.galcount and d.galcount = c.galcount and c.galcount = z.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by c.galcount  limit 1000000;""".format(model = 'serexp', band = 'r')
    elif binval == 'nair_lackner':
        cmd = """select d.galcount,IF(d.model='dvc',7,0)+ IF(d.model='ser' and z.n_bulge>=2.0, 12,0)+IF(d.model='exp',8,0)+ IF(d.model='ser' and z.n_bulge<2.0, 11,0)+IF(d.model='nb1',9,0)+IF(d.model = 'nb4', 10,0),n.ttype from catalog.M2010 as m, catalog.r_lackner_fit as d, catalog.r_lackner_ser as z, catalog.Nair as n where m.galcount=d.galcount and n.galcount = d.galcount and d.galcount = z.galcount order by d.galcount  limit 1000000;"""
    elif binval == 'nair_simard':
        cmd = """select d.galcount, IF(d.Prob_pS>0.32 and z.n_bulge>=2.0, 12,0)+IF(d.Prob_pS>0.32 and z.n_bulge<2.0, 11,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4>0.32, 13,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4<=0.32, 14,0),  n.ttype from catalog.M2010 as m,  catalog.r_lackner_fit as c, catalog.r_simard_fit as d, catalog.r_simard_ser as z, catalog.Nair as n where m.galcount = c.galcount and n.galcount = c.galcount  and c.galcount = d.galcount and c.galcount = z.galcount order by d.galcount  limit 1000000;"""
    elif binval == 'nair_meert':
        cmd = """select c.galcount,IF(c.flag&pow(2,1)>0,1,0)+ IF(c.flag&pow(2,4)>0,2,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge<7.95,3,0)+ IF(c.flag&pow(2,14)>0,4,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge>=7.95,6,0)+IF(c.flag&pow(2,19)>0,5,0)  ,n.ttype  from catalog.M2010 as m, catalog.Flags_optimize as c, catalog.r_lackner_fit as z, catalog.r_band_serexp as d, catalog.Nair as n  where m.galcount = c.galcount and n.galcount = c.galcount and d.galcount = c.galcount and c.galcount = z.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by c.galcount  limit 1000000;""".format(model = 'serexp', band = 'r')
    galcount, flags, flag2 = cursor.get_data(cmd)
    galcount = np.array(galcount, dtype=int)
    autoflag = np.array(flags, dtype=int)

    flag2 = np.array(flag2)

    return galcount, autoflag, flag2

def plot_props(xlab, props, magbins, delta, flags_to_use,plot_info):
    magbinctr = (magbins[1:]+magbins[0:-1])/2

    ax1 = pl.gca()
    pl.xlabel(xlab)

    ax2 = pl.twinx()

    max_yticksl = 6
    max_yticksr = 5
    max_xticks = 5
    ylocl = pl.MaxNLocator(max_yticksl,prune='lower')
    ylocr = pl.MaxNLocator(max_yticksr,prune='lower')
    xloc = pl.MaxNLocator(max_xticks, prune='lower')

    for flag in flags_to_use:
        ax2.plot(magbinctr, np.array(props[flag])/np.array(props['total']), 
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

        ax2.set_ylim(0,1.0)

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


plot_info = {1:{'color':'r', 'label':'bulges', 'ms':3, 'marker':'o', 'ls':'-'},
             2:{'color':'b', 'label':'disks', 'ms':3, 'marker':'s', 'ls':'-'},
             3:{'color':'g', 'label':'2com', 'ms':3, 'marker':'d', 'ls':'-'},
             4:{'color':'y', 'label':'bad 2com', 'ms':3, 'marker':'o', 'ls':'--'},
             5:{'color':'k', 'label':'bad', 'ms':3, 'marker':'d', 'ls':'--'},
             6:{'color':'c', 'label':'n8', 'ms':3, 'marker':'s', 'ls':'--'},
             
             7:{'color':'r', 'label':'dvc', 'ms':3, 'marker':'o', 'ls':'-'},
             8:{'color':'b', 'label':'exp', 'ms':3, 'marker':'s', 'ls':'-'},
             9:{'color':'g', 'label':'nb1', 'ms':3, 'marker':'d', 'ls':':'},
             10:{'color':'y', 'label':'nb4', 'ms':3, 'marker':'d', 'ls':'-'},
             11:{'color':'c', 'label':'ser, n<2', 'ms':3, 'marker':'s', 'ls':'-'},
             12:{'color':'k', 'label':'ser, n>=2', 'ms':3, 'marker':'o', 'ls':'-'},
             13:{'color':'g', 'label':'devexp', 'ms':3, 'marker':'d', 'ls':'--'},
             14:{'color':'y', 'label':'serexp', 'ms':3, 'marker':'d', 'ls':'-'},
             15:{'color':'r', 'label':'dev', 'ms':3, 'marker':'o', 'ls':'-'},
             16:{'color':'b', 'label':'exp', 'ms':3, 'marker':'s', 'ls':'-'},
             17:{'color':'g', 'label':'devexp', 'ms':3, 'marker':'d', 'ls':'-'},
             18:{'color':'k', 'label':'unknown', 'ms':3, 'marker':'o', 'ls':'--'},
             'total': {'color':"#D0D0D0",'label':'total'}
             }

names=[ plot_info[key]['label'] for key in plot_info.keys()] 
matplotlib.rc('xtick', labelsize=8)
fig = pl.figure(figsize=(6,8))
pl.subplots_adjust(right = 0.85, top = 0.85, left =0.1, bottom=0.3,
                   hspace = 1.2, wspace = 0.8)


delta = 0.5
typebins = np.arange(-24.0, -16.49, delta)
#x_names= [str(int(a)) for a in typebins+0.5]
#x_names = [ x_names[a] if (a+1)%4 ==0 else "" for a in range(len(x_names))] 

print "meert" 
pl.subplot(4,2,2)
flags_to_use = np.array([1,2,3,4,5,6])
galcount, autoflag, stype = get_vals('meert')
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
ax1, ax2 =plot_props('M$_{petro}$', props, typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names)
pl.title('This Work (full sample)', fontsize=8)
pl.xticks(fontsize=8)
l = ax2.legend(loc=2, bbox_to_anchor=(1.025, 0.09), prop={'size':6})
pl.xlim(-16.5,-24.0)


print "simard" 
pl.subplot(4,2,4)
flags_to_use = np.array([11,12,13,14])
galcount, autoflag, stype = get_vals('simard')
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
ax1,ax2=plot_props('M$_{petro}$', props, typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('S11 (full sample)', fontsize=8)
l = ax2.legend(loc=2, bbox_to_anchor=(1.025, 0.09), prop={'size':6})
pl.xticks(fontsize=8)
pl.xlim(-16.5,-24.0)

print "mendel" 
pl.subplot(4,2,6)
flags_to_use = np.array([15,16,17,18])
galcount, autoflag, stype = get_vals('mendel')
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
ax1,ax2=plot_props('M$_{petro}$', props, typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('Men14 (full sample)', fontsize=8)
l = ax2.legend(loc=2, bbox_to_anchor=(1.025, 0.09), prop={'size':6})
pl.xticks(fontsize=8)
pl.xlim(-16.5,-24.0)

print "meert" 
pl.subplot(4,2,1)
flags_to_use = np.array([1,2,3,4,5,6])
galcount, autoflag, stype = get_vals('meert_lackner')
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
ax1, ax2 =plot_props('M$_{petro}$', props, typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('This Work (LG12 sample)', fontsize=8)
pl.xticks(fontsize=8)
l = ax2.legend(loc=2, bbox_to_anchor=(1.025, 0.09), prop={'size':6})
pl.xlim(-16.5,-23.0)

print "simard" 
pl.subplot(4,2,3)
flags_to_use = np.array([11,12,13,14])
galcount, autoflag, stype = get_vals('simard_lackner')
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
ax1,ax2=plot_props('M$_{petro}$', props, typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('S11 (LG12 sample)', fontsize=8)
l = ax2.legend(loc=2, bbox_to_anchor=(1.025, 0.09), prop={'size':6})
pl.xticks(fontsize=8)
pl.xlim(-16.5,-23.0)

print "mendel" 
pl.subplot(4,2,5)
flags_to_use = np.array([15,16,17,18])
galcount, autoflag, stype = get_vals('mendel_lackner')
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
ax1,ax2=plot_props('M$_{petro}$', props, typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('Men14 (LG12 sample)', fontsize=8)
l = ax2.legend(loc=2, bbox_to_anchor=(1.025, 0.09), prop={'size':6})
pl.xticks(fontsize=8)
pl.xlim(-16.5,-23.0)

print "lackner" 
pl.subplot(4,2,7)
flags_to_use = np.array([7,8,9,10,11,12])
galcount, autoflag, stype = get_vals('lackner')
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
ax1,ax2=plot_props('M$_{petro}$', props, typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('LG12 (LG12 sample)', fontsize=8)
l = ax2.legend(loc=2, bbox_to_anchor=(1.025, 0.09), prop={'size':6})
pl.xticks(fontsize=8)
pl.xlim(-16.5,-23.0)


pl.savefig('./types_dist_abspmag.eps', bbox_inches = 'tight')
#pl.show()
