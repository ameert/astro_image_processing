from astro_image_processing.mysql.mysql_class import *
from flag_defs import *
import pylab as pl
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt

plot_info = {1:{'color':'r', 'label':'bulges', 'ms':3, 'marker':'o', 'ls':'-'},
             2:{'color':'b', 'label':'disks', 'ms':3, 'marker':'s', 'ls':'-'},
             3:{'color':'g', 'label':'2com', 'ms':3, 'marker':'d', 'ls':'-'},
             4:{'color':'y', 'label':'bad 2com', 'ms':3, 'marker':'o', 'ls':'--'},
             5:{'color':'k', 'label':'bad', 'ms':3, 'marker':'d', 'ls':'--'},
             6:{'color':'c', 'label':'n8', 'ms':3, 'marker':'s', 'ls':'--'},
             
             7:{'color':'r', 'label':'dvc', 'ms':3, 'marker':'o', 'ls':'-'},
             8:{'color':'b', 'label':'exp', 'ms':3, 'marker':'s', 'ls':'-'},
             9:{'color':'y', 'label':'nb1', 'ms':3, 'marker':'d', 'ls':':'},
             10:{'color':'g', 'label':'nb4', 'ms':3, 'marker':'d', 'ls':'-'},
             11:{'color':'c', 'label':'ser, n$<$2', 'ms':3, 'marker':'s', 'ls':'-'},
             12:{'color':'#FF6600', 'label':'ser, n$\geq$2', 'ms':3, 'marker':'o', 'ls':'--'},
             13:{'color':'g', 'label':'devexp', 'ms':3, 'marker':'d', 'ls':'--'},
             14:{'color':'y', 'label':'serexp', 'ms':3, 'marker':'d', 'ls':'-'},
             15:{'color':'r', 'label':'dev', 'ms':3, 'marker':'o', 'ls':'-'},
             16:{'color':'b', 'label':'exp', 'ms':3, 'marker':'s', 'ls':'-'},
             17:{'color':'g', 'label':'devexp', 'ms':3, 'marker':'d', 'ls':'-'},
             18:{'color':'k', 'label':'unknown', 'ms':3, 'marker':'o', 'ls':'--'},
             19:{'color':'r', 'label':'bulges', 'ms':3, 'marker':'o', 'ls':'-'},
             20:{'color':'b', 'label':'disks', 'ms':3, 'marker':'s', 'ls':'-'},
             21:{'color':'g', 'label':'2com small bulge', 'ms':3, 'marker':'d', 'ls':'-'},
             22:{'color':'y', 'label':'2com obvi', 'ms':3, 'marker':'o', 'ls':'--'},
             23:{'color':'k', 'label':'2com domin', 'ms':3, 'marker':'d', 'ls':'--'},             
             24:{'color':'c', 'label':'edge', 'ms':3, 'marker':'d', 'ls':'--'},             
             'total': {'color':"#D0D0D0",'label':'total'},

             'ylims':{'flagclass':{'ba':(0.0,0.13), 'mtot':(0.0,0.25),
                                   'rad':(0.0,0.25), 'absmtot':(0.0,0.25),
                                   'absrad':(0.0,0.15),'nbulge':(0.0,0.15)},
                      'total':{'ba':(0.0,0.045), 'mtot':(0.0,0.09),
                                   'rad':(0.0,0.1), 'absmtot':(0.0,0.09),
                                   'absrad':(0.0,0.04),'nbulge':(0.0,0.075)}
                      }

             }


def get_vals(binval, sql_values, cursor):
    if binval == 'lackner':
        cmd = """select d.galcount,IF(d.model='dvc',7,0)+ IF(d.model='ser' and z.n_bulge>=2.0, 12,0)+IF(d.model='exp',8,0)+ IF(d.model='ser' and z.n_bulge<2.0, 11,0)+IF(d.model='nb1',9,0)+IF(d.model = 'nb4', 10,0), {add_param} from catalog.M2010 as m, catalog.CAST as r,catalog.DERT as s, catalog.r_lackner_fit as d, catalog.r_lackner_ser as z, catalog.{band}_lackner_fit as b where b.galcount = r.galcount and r.galcount=s.galcount and r.galcount = m.galcount and  m.galcount=d.galcount and d.galcount = z.galcount order by d.galcount limit {galnumlim};""".format(**sql_values)
    elif binval == 'simard_lackner':
        cmd = """select d.galcount, IF(d.Prob_pS>0.32 and z.n_bulge>=2.0, 12,0)+IF(d.Prob_pS>0.32 and z.n_bulge<2.0, 11,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4>0.32, 13,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4<=0.32, 14,0), {add_param} from catalog.CAST as r,catalog.DERT as s, catalog.M2010 as m,  catalog.r_lackner_fit as c, catalog.r_simard_fit as d, catalog.r_simard_ser as z , catalog.{band}_simard_{model} as b where b.galcount = r.galcount and  r.galcount=s.galcount and r.galcount = m.galcount and  m.galcount = c.galcount and c.galcount = d.galcount and c.galcount = z.galcount order by d.galcount  limit {galnumlim};""".format(**sql_values)
    elif binval == 'simard':
        cmd = """select d.galcount, IF(d.Prob_pS>0.32 and z.n_bulge>=2.0, 12,0)+IF(d.Prob_pS>0.32 and z.n_bulge<2.0, 11,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4>0.32, 13,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4<=0.32, 14,0), {add_param} from catalog.CAST as r,catalog.DERT as s, catalog.M2010 as m, catalog.r_simard_fit as d, catalog.r_simard_ser as z , catalog.{band}_simard_{model} as b where b.galcount = r.galcount and  r.galcount=s.galcount and r.galcount = m.galcount and  m.galcount = d.galcount and d.galcount = z.galcount order by d.galcount  limit {galnumlim};""".format(**sql_values)
    elif binval == 'meert_lackner':
        cmd = """select c.galcount,IF(c.flag&pow(2,1)>0,1,0)+ IF(c.flag&pow(2,4)>0,2,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge<7.95,3,0)+ IF(c.flag&pow(2,14)>0,4,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge>=7.95,6,0)+IF(c.flag&pow(2,20)>0,5,0)  , {add_param} from   catalog.CAST as r,catalog.DERT as s,catalog.M2010 as m, catalog.Flags_catalog as c, catalog.r_lackner_fit as z, catalog.r_band_serexp as d  , catalog.{band}_band_{model} as b where b.galcount = r.galcount and  r.galcount=s.galcount and r.galcount = m.galcount and  m.galcount = c.galcount and d.galcount = c.galcount and c.galcount = z.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by c.galcount  limit {galnumlim};""".format(**sql_values)
    elif binval == 'meert':
        cmd = """select c.galcount,IF(c.flag&pow(2,1)>0,1,0)+ IF(c.flag&pow(2,4)>0,2,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge<7.95,3,0)+ IF(c.flag&pow(2,14)>0,4,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge>=7.95,6,0)+IF(c.flag&pow(2,20)>0,5,0)  ,   {add_param} from   catalog.CAST as r,catalog.DERT as s,catalog.M2010 as m, catalog.Flags_catalog as c, catalog.{band}_band_{model} as d  , catalog.{band}_band_{model} as b where b.galcount = r.galcount and  r.galcount=s.galcount and r.galcount = m.galcount and  m.galcount = c.galcount and d.galcount = c.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by c.galcount  limit {galnumlim};""".format(**sql_values)
    elif binval == 'mendel_lackner':
        cmd = """select d.galcount, IF(d.Proftype=1, 15,0)+IF(d.Proftype=2, 16,0)+IF(d.Proftype=3, 17,0)+IF(d.Proftype=4 or d.Proftype<0,18,0), {add_param} from  catalog.CAST as r,catalog.DERT as s, catalog.M2010 as m,  catalog.r_lackner_fit as c, catalog.r_simard_fit as d, catalog.r_simard_ser as z , catalog.{band}_simard_{model} as b where b.galcount = r.galcount and  r.galcount=s.galcount and r.galcount = m.galcount and   m.galcount = s.galcount and m.galcount = c.galcount and c.galcount = d.galcount and c.galcount = z.galcount order by d.galcount   limit {galnumlim};""".format(**sql_values)
    elif binval == 'mendel':
        cmd = """select d.galcount, IF(d.Proftype=1, 15,0)+IF(d.Proftype=2, 16,0)+IF(d.Proftype=3, 17,0)+IF(d.Proftype=4 or d.Proftype<0,18,0), {add_param} from  catalog.CAST as r,catalog.DERT as s, catalog.M2010 as m, catalog.r_simard_fit as d, catalog.r_simard_ser as z , catalog.{band}_simard_{model} as b where b.galcount = r.galcount and  r.galcount=s.galcount and r.galcount = m.galcount and   m.galcount = s.galcount and m.galcount = d.galcount and d.galcount = z.galcount order by d.galcount   limit {galnumlim};""".format(**sql_values)
    elif binval == 'nair_lackner':
        cmd = """select d.galcount,IF(d.model='dvc',7,0)+ IF(d.model='ser' and z.n_bulge>=2.0, 12,0)+IF(d.model='exp',8,0)+ IF(d.model='ser' and z.n_bulge<2.0, 11,0)+IF(d.model='nb1',9,0)+IF(d.model = 'nb4', 10,0), {add_param} from   catalog.CAST as r,catalog.DERT as s,catalog.M2010 as m, catalog.r_lackner_fit as d, catalog.r_lackner_ser as z, catalog.Nair as n , catalog.{band}_lackner_fit as b where b.galcount = r.galcount and  r.galcount=s.galcount and r.galcount = m.galcount and  m.galcount=d.galcount and n.galcount = d.galcount and d.galcount = z.galcount order by d.galcount  limit {galnumlim};""".format(**sql_values)
    elif binval == 'nair_simard':
        cmd = """select d.galcount, IF(d.Prob_pS>0.32 and z.n_bulge>=2.0, 12,0)+IF(d.Prob_pS>0.32 and z.n_bulge<2.0, 11,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4>0.32, 13,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4<=0.32, 14,0),  {add_param} from   catalog.CAST as r,catalog.DERT as s,catalog.M2010 as m,  catalog.r_lackner_fit as c, catalog.r_simard_fit as d, catalog.r_simard_ser as z, catalog.Nair as n , catalog.{band}_simard_fit as b where b.galcount = r.galcount and  r.galcount=s.galcount and r.galcount = m.galcount and  m.galcount = c.galcount and n.galcount = c.galcount  and c.galcount = d.galcount and c.galcount = z.galcount order by d.galcount   limit {galnumlim};""".format(**sql_values)
    elif binval == 'nair_mendel':
        cmd = """select d.galcount, IF(d.Proftype=1, 15,0)+IF(d.Proftype=2, 16,0)+IF(d.Proftype=3, 17,0)+IF(d.Proftype=4 or d.Proftype<0,18,0), {add_param} from  catalog.CAST as r,catalog.DERT as s, catalog.M2010 as m,  catalog.r_lackner_fit as c, catalog.r_simard_fit as d, catalog.r_simard_ser as z , catalog.Nair as n, catalog.{band}_simard_fit as b where b.galcount = r.galcount and  r.galcount=s.galcount and r.galcount = m.galcount and   m.galcount = s.galcount and n.galcount=c.galcount and m.galcount = c.galcount and c.galcount = d.galcount and c.galcount = z.galcount order by d.galcount   limit {galnumlim};""".format(**sql_values)
    elif binval == 'nair_meert':
        cmd = """select c.galcount,IF(c.flag&pow(2,1)>0,1,0)+ IF(c.flag&pow(2,4)>0,2,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge<7.95,3,0)+ IF(c.flag&pow(2,14)>0,4,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge>=7.95,6,0)+IF(c.flag&pow(2,20)>0,5,0)  , {add_param} from   catalog.CAST as r,catalog.DERT as s,catalog.M2010 as m, catalog.Flags_catalog as c, catalog.r_lackner_fit as z, catalog.r_band_serexp as d, catalog.Nair as n  , catalog.{band}_band_fit as b where b.galcount = r.galcount and  r.galcount=s.galcount and r.galcount = m.galcount and m.galcount = c.galcount and n.galcount = c.galcount and d.galcount = c.galcount and c.galcount = z.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by c.galcount  limit {galnumlim};""".format(**sql_values)
    elif binval == 'galzoo':
        cmd = """select c.galcount, t01_smooth*19+ (t09_no_bulge+t05_no_bulge)*20+t05_just_noticeable*21+(t05_obvious+t09_bulge_rounded+t09_bulge_boxy)*IF((t08_ring+t08_disturbed+t08_irregular+t08_merger+t08_dust_lane)>0,0,1)*22+t05_dominant*23, m.petromag_{band}-m.extinction_{band}-x.dismod-x.kcorr_{band} from catalog.CAST as m,catalog.DERT as x, catalog.gz2_flags as c, catalog.{band}_band_{model} as d  where  m.galcount = x.galcount and m.galcount = c.galcount and d.galcount = c.galcount and  t01_smooth*19+ (t09_no_bulge+t05_no_bulge)*20+t05_just_noticeable*21+(t05_obvious+t09_bulge_rounded+t09_bulge_boxy)*IF((t08_ring+t08_disturbed+t08_irregular+t08_merger+t08_dust_lane)>0,0,1)*22+t05_dominant*23>0  order by c.galcount  limit {galnumlim};""".format(band=band, model=model, galnumlim=galnumlim)
    elif binval == 'galzoo_lackner':
        cmd = """select  c.galcount,t01_smooth*19+ (t09_no_bulge+t05_no_bulge)*20+t05_just_noticeable*21+(t05_obvious+t09_bulge_rounded+t09_bulge_boxy)*IF((t08_ring+t08_disturbed+t08_irregular+t08_merger+t08_dust_lane)>0,0,1)*22+t05_dominant*23, m.petromag_{band}-m.extinction_{band}-x.dismod-x.kcorr_{band} from catalog.CAST as m,catalog.DERT as x, catalog.gz2_flags as c, catalog.{band}_band_{model} as d,catalog.{band}_lackner_fit as z  where m.galcount = x.galcount and  m.galcount = z.galcount and m.galcount = c.galcount and d.galcount = c.galcount  and  t01_smooth*19+ (t09_no_bulge+t05_no_bulge)*20+t05_just_noticeable*21+(t05_obvious+t09_bulge_rounded+t09_bulge_boxy)*IF((t08_ring+t08_disturbed+t08_irregular+t08_merger+t08_dust_lane)>0,0,1)*22+t05_dominant*23>0 order by c.galcount  limit {galnumlim};""".format(band=band, model=model, galnumlim=galnumlim)

    galcount, flags, add_param = cursor.get_data(cmd)
    galcount = np.array(galcount, dtype=int)
    autoflag = np.array(flags, dtype=int)
    
    add_param = np.array(add_param)

    return galcount, autoflag, add_param


try:
    import scikits.bootstrap as bootstrap  

    def get_ci(data, ci):
        try:
            ci_vals = bootstrap.ci(data=data, alpha = ci, 
                                   statfunction=print_class, 
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

def print_class(autoclass, test_class, print_gals = False):
    class_vals = np.where(autoclass==test_class, 1,0)
    class_num = float(np.sum(class_vals))
    if np.isnan(class_num):
        class_num = 0.0
    if print_gals:
        print "class %d: %.4f" %(test_class, class_num)
    return class_num

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
            props[flag].append(print_class(new_arr, flag))
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
    ax1.yaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)
    return ax1, ax2
