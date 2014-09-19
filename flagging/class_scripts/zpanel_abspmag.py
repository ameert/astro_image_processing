from astro_image_processing.mysql.mysql_class import *
from flag_defs import *
import pylab as pl
import matplotlib.ticker as mticker
import scikits.bootstrap as bootstrap  
import matplotlib 

        
def get_vals(binval):
    # , catalog.gz2_flags as z where z.galcount = m.galcount and  
    galnumlim = 1000000
    if binval == 'lackner':
        cmd = """select d.galcount,IF(d.model='dvc',7,0)+ IF(d.model='ser' and z.n_bulge>=2.0, 12,0)+IF(d.model='exp',8,0)+ IF(d.model='ser' and z.n_bulge<2.0, 11,0)+IF(d.model='nb1',9,0)+IF(d.model = 'nb4', 10,0),m.petromag_{band}-m.extinction_{band}-x.dismod-x.kcorr_{band} from catalog.CAST as m,catalog.DERT as x, catalog.{band}_lackner_fit as d, catalog.{band}_lackner_ser as z where m.galcount = x.galcount and m.galcount=d.galcount and d.galcount = z.galcount order by d.galcount  limit {galnumlim};""".format(band=band, model=model, galnumlim=galnumlim)
    elif binval == 'simard':
        cmd = """select d.galcount, IF(d.Prob_pS>0.32 and z.n_bulge>=2.0, 12,0)+IF(d.Prob_pS>0.32 and z.n_bulge<2.0, 11,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4>0.32, 13,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4<=0.32, 14,0),  m.petromag_{band}-m.extinction_{band}-x.dismod-x.kcorr_{band} from catalog.CAST as m,catalog.DERT as x, catalog.{band}_simard_fit as d, catalog.{band}_simard_ser as z where  m.galcount = x.galcount and m.galcount= d.galcount and m.galcount = z.galcount order by d.galcount  limit {galnumlim};""".format(band=band, model=model, galnumlim=galnumlim)
    elif binval == 'mendel':
        cmd = """select d.galcount, IF(d.Proftype=1, 15,0)+IF(d.Proftype=2, 16,0)+IF(d.Proftype=3, 17,0)+IF(d.Proftype=4 or d.Proftype<0,18,0),  m.petromag_{band}-m.extinction_{band}-x.dismod-x.kcorr_{band} from catalog.CAST as m,catalog.DERT as x,  catalog.{band}_simard_fit as d, catalog.{band}_simard_ser as z where  m.galcount = x.galcount and m.galcount = d.galcount and m.galcount = z.galcount order by d.galcount  limit {galnumlim};""".format(band=band, model=model, galnumlim=galnumlim)
    elif binval == 'meert':
        cmd = """select c.galcount,IF(c.flag&pow(2,1)>0,1,0)+ IF(c.flag&pow(2,4)>0,2,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge<7.95,3,0)+ IF(c.flag&pow(2,14)>0,4,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge>=7.95,6,0)+IF(c.flag&pow(2,20)>0,5,0)  ,m.petromag_{band}-m.extinction_{band}-x.dismod-x.kcorr_{band} from catalog.CAST as m,catalog.DERT as x, catalog.Flags_catalog as c, catalog.{band}_band_{model} as d where m.galcount = x.galcount and m.galcount = c.galcount and d.galcount = c.galcount  and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by c.galcount  limit {galnumlim};""".format(band=band, model=model, galnumlim=galnumlim)#and  t01_smooth*19+ (t09_no_bulge+t05_no_bulge)*20+t05_just_noticeable*21+(t05_obvious+t09_bulge_rounded+t09_bulge_boxy)*IF((t08_ring+t08_disturbed+t08_irregular+t08_merger+t08_dust_lane)>0,0,1)*22+t05_dominant*23>0
    elif binval == 'galzoo':
        cmd = """select c.galcount, t01_smooth*19+ (t09_no_bulge+t05_no_bulge)*20+t05_just_noticeable*21+(t05_obvious+t09_bulge_rounded+t09_bulge_boxy)*IF((t08_ring+t08_disturbed+t08_irregular+t08_merger+t08_dust_lane)>0,0,1)*22+t05_dominant*23, m.petromag_{band}-m.extinction_{band}-x.dismod-x.kcorr_{band} from catalog.CAST as m,catalog.DERT as x, catalog.gz2_flags as c, catalog.{band}_band_{model} as d  where  m.galcount = x.galcount and m.galcount = c.galcount and d.galcount = c.galcount and  t01_smooth*19+ (t09_no_bulge+t05_no_bulge)*20+t05_just_noticeable*21+(t05_obvious+t09_bulge_rounded+t09_bulge_boxy)*IF((t08_ring+t08_disturbed+t08_irregular+t08_merger+t08_dust_lane)>0,0,1)*22+t05_dominant*23>0  order by c.galcount  limit {galnumlim};""".format(band=band, model=model, galnumlim=galnumlim)
    elif binval == 'galzoo_lackner':
        cmd = """select  c.galcount,t01_smooth*19+ (t09_no_bulge+t05_no_bulge)*20+t05_just_noticeable*21+(t05_obvious+t09_bulge_rounded+t09_bulge_boxy)*IF((t08_ring+t08_disturbed+t08_irregular+t08_merger+t08_dust_lane)>0,0,1)*22+t05_dominant*23, m.petromag_{band}-m.extinction_{band}-x.dismod-x.kcorr_{band} from catalog.CAST as m,catalog.DERT as x, catalog.gz2_flags as c, catalog.{band}_band_{model} as d,catalog.{band}_lackner_fit as z  where  m.galcount = x.galcount and  m.galcount = z.galcount and m.galcount = c.galcount and d.galcount = c.galcount  and  t01_smooth*19+ (t09_no_bulge+t05_no_bulge)*20+t05_just_noticeable*21+(t05_obvious+t09_bulge_rounded+t09_bulge_boxy)*IF((t08_ring+t08_disturbed+t08_irregular+t08_merger+t08_dust_lane)>0,0,1)*22+t05_dominant*23>0 order by c.galcount  limit {galnumlim};""".format(band=band, model=model, galnumlim=galnumlim)
    elif binval == 'simard_lackner':
        cmd = """select d.galcount, IF(d.Prob_pS>0.32 and z.n_bulge>=2.0, 12,0)+IF(d.Prob_pS>0.32 and z.n_bulge<2.0, 11,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4>0.32, 13,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4<=0.32, 14,0),  m.petromag_{band}-m.extinction_{band}-x.dismod-x.kcorr_{band} from catalog.CAST as m,catalog.DERT as x,  catalog.{band}_lackner_fit as c, catalog.{band}_simard_fit as d, catalog.{band}_simard_ser as z where  m.galcount = x.galcount and m.galcount = c.galcount and c.galcount = d.galcount and c.galcount = z.galcount order by d.galcount  limit {galnumlim};""".format(band=band, model=model, galnumlim=galnumlim)
    elif binval == 'mendel_lackner':
        cmd = """select d.galcount, IF(d.Proftype=1, 15,0)+IF(d.Proftype=2, 16,0)+IF(d.Proftype=3, 17,0)+IF(d.Proftype=4 or d.Proftype<0,18,0),  m.petromag_{band}-m.extinction_{band}-x.dismod-x.kcorr_{band} from catalog.CAST as m,catalog.DERT as x,  catalog.{band}_lackner_fit as c, catalog.{band}_simard_fit as d, catalog.{band}_simard_ser as z where  m.galcount = x.galcount and m.galcount = c.galcount and c.galcount = d.galcount and c.galcount = z.galcount order by d.galcount  limit {galnumlim};""".format(band=band, model=model, galnumlim=galnumlim)
    elif binval == 'meert_lackner':
        cmd = """select c.galcount,IF(c.flag&pow(2,1)>0,1,0)+ IF(c.flag&pow(2,4)>0,2,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge<7.95,3,0)+ IF(c.flag&pow(2,14)>0,4,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge>=7.95,6,0)+IF(c.flag&pow(2,20)>0,5,0)  ,m.petromag_{band}-m.extinction_{band}-x.dismod-x.kcorr_{band} from catalog.CAST as m,catalog.DERT as x, catalog.Flags_catalog as c, catalog.{band}_lackner_fit as z, catalog.{band}_band_{model} as d where  m.galcount = x.galcount and m.galcount = c.galcount and d.galcount = c.galcount and c.galcount = z.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by c.galcount  limit {galnumlim};""".format(band=band, model=model, galnumlim=galnumlim)#  and  t01_smooth*19+ (t09_no_bulge+t05_no_bulge)*20+t05_just_noticeable*21+(t05_obvious+t09_bulge_rounded+t09_bulge_boxy)*IF((t08_ring+t08_disturbed+t08_irregular+t08_merger+t08_dust_lane)>0,0,1)*22+t05_dominant*23>0
    elif binval == 'nair_lackner':
        cmd = """select d.galcount,IF(d.model='dvc',7,0)+ IF(d.model='ser' and z.n_bulge>=2.0, 12,0)+IF(d.model='exp',8,0)+ IF(d.model='ser' and z.n_bulge<2.0, 11,0)+IF(d.model='nb1',9,0)+IF(d.model = 'nb4', 10,0),n.ttype from catalog.M2010 as m, catalog.{band}_lackner_fit as d, catalog.{band}_lackner_ser as z, catalog.Nair as n where m.galcount=d.galcount and n.galcount = d.galcount and d.galcount = z.galcount order by d.galcount  limit {galnumlim};""".format(band=band, model=model, galnumlim=galnumlim)
    elif binval == 'nair_simard':
        cmd = """select d.galcount, IF(d.Prob_pS>0.32 and z.n_bulge>=2.0, 12,0)+IF(d.Prob_pS>0.32 and z.n_bulge<2.0, 11,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4>0.32, 13,0)+IF(d.Prob_pS<=0.32 and d.Prob_n4<=0.32, 14,0),  n.ttype from catalog.M2010 as m,  catalog.{band}_lackner_fit as c, catalog.{band}_simard_fit as d, catalog.{band}_simard_ser as z, catalog.Nair as n where m.galcount = c.galcount and n.galcount = c.galcount  and c.galcount = d.galcount and c.galcount = z.galcount order by d.galcount  limit {galnumlim};""".format(band=band, model=model, galnumlim=galnumlim)
    elif binval == 'nair_meert':
        cmd = """select c.galcount,IF(c.flag&pow(2,1)>0,1,0)+ IF(c.flag&pow(2,4)>0,2,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge<7.95,3,0)+ IF(c.flag&pow(2,14)>0,4,0)+ IF(c.flag&pow(2,10)>0 and d.n_bulge>=7.95,6,0)+IF(c.flag&pow(2,20)>0,5,0)  ,n.ttype  from catalog.M2010 as m, catalog.Flags_catalog as c, catalog.{band}_lackner_fit as z, catalog.{band}_band_{model} as d, catalog.Nair as n  where m.galcount = c.galcount and n.galcount = c.galcount and d.galcount = c.galcount and c.galcount = z.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by c.galcount  limit {galnumlim};""".format(band=band, model=model, galnumlim=galnumlim)
    galcount, flags, flag2 = cursor.get_data(cmd)
    galcount = np.array(galcount, dtype=int)
    autoflag = np.array(flags, dtype=int)

    flag2 = np.array(flag2)

    return galcount, autoflag, flag2


cursor = mysql_connect('catalog','pymorph','pymorph','')

band = 'r'
model = 'devexp'


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
             'total': {'color':"#D0D0D0",'label':'total'}
             }

names=[ plot_info[key]['label'] for key in plot_info.keys()] 
matplotlib.rc('xtick', labelsize=8)
fig = pl.figure(figsize=(6,8))
pl.subplots_adjust(right = 0.92, top = 0.97, left =0.1, bottom=0.1,
                   hspace = 0.65, wspace = 0.95)


delta = 0.5
typebins = np.arange(-24.0, -16.49, delta)
typebins_lg12 = np.arange(-23.0, -16.49, delta)
#x_names= [str(int(a)) for a in typebins+0.5]
#x_names = [ x_names[a] if (a+1)%4 ==0 else "" for a in range(len(x_names))] 

print "meert" 
pl.subplot(5,2,2)
flags_to_use = np.array([1,2,3,4,5,6])
galcount, autoflag, stype = get_vals('meert')
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
ax1, ax2 =plot_props('M$_{petro}$', props, typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names)
pl.title('This Work (full sample)', fontsize=8)
pl.xticks(fontsize=8)
#l = ax2.legend(loc=2, bbox_to_anchor=(1.01, 0.1), prop={'size':6})
pl.xlim(-16.5,-24.0)
ax1.yaxis.set_tick_params(labelsize=6)
ax2.yaxis.set_tick_params(labelsize=6)

if band in 'gr':
    print "simard" 
    pl.subplot(5,2,4)
    flags_to_use = np.array([11,12,13,14])
    galcount, autoflag, stype = get_vals('simard')
    props = get_flag_props(flags_to_use, autoflag, stype,typebins)
    ax1,ax2=plot_props('M$_{petro}$', props, typebins, delta, flags_to_use,plot_info)
    #pl.xticks(typebins+0.5, x_names, fontsize = 8)
    pl.title('S11 (full sample)', fontsize=8)
    #l = ax2.legend(loc=2, bbox_to_anchor=(1.01, 0.1), prop={'size':6})
    pl.xticks(fontsize=8)
    pl.xlim(-16.5,-24.0)
    ax1.yaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)

    print "mendel" 
    pl.subplot(5,2,6)
    flags_to_use = np.array([15,16,17,18])
    galcount, autoflag, stype = get_vals('mendel')
    props = get_flag_props(flags_to_use, autoflag, stype,typebins)
    ax1,ax2=plot_props('M$_{petro}$', props, typebins, delta, flags_to_use,plot_info)
    #pl.xticks(typebins+0.5, x_names, fontsize = 8)
    pl.title('Men14 (full sample)', fontsize=8)
    #l = ax2.legend(loc=2, bbox_to_anchor=(1.01, 0.1), prop={'size':6})
    pl.xticks(fontsize=8)
    pl.xlim(-16.5,-24.0)
    ax1.yaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)

print "meert" 
pl.subplot(5,2,1)
flags_to_use = np.array([1,2,3,4,5,6])
galcount, autoflag, stype = get_vals('meert_lackner')
props = get_flag_props(flags_to_use, autoflag, stype,typebins_lg12)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
ax1, ax2 =plot_props('M$_{petro}$', props, typebins_lg12, delta, flags_to_use,plot_info)
#pl.xticks(typebins_lg12+0.5, x_names, fontsize = 8)
pl.title('This Work (LG12 sample)', fontsize=8)
pl.xticks(fontsize=8)
l = ax2.legend(loc=10, bbox_to_anchor=(1.5, 0.5), prop={'size':6})
pl.xlim(-16.5,-24.0)
ax1.yaxis.set_tick_params(labelsize=6)
ax2.yaxis.set_tick_params(labelsize=6)

if band in 'gr':
    print "simard" 
    pl.subplot(5,2,3)
    flags_to_use = np.array([11,12,13,14])
    galcount, autoflag, stype = get_vals('simard_lackner')
    props = get_flag_props(flags_to_use, autoflag, stype,typebins_lg12)
    props['datamask'] = np.where(np.array(props['total'])>0,True,False)
    ax1,ax2=plot_props('M$_{petro}$', props, typebins_lg12, delta, flags_to_use,plot_info)
    #pl.xticks(typebins_lg12+0.5, x_names, fontsize = 8)
    pl.title('S11 (LG12 sample)', fontsize=8)
    l = ax2.legend(loc=10, bbox_to_anchor=(1.5, 0.5), prop={'size':6})
    pl.xticks(fontsize=8)
    pl.xlim(-16.5,-24.0)
    ax1.yaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)

    print "mendel" 
    pl.subplot(5,2,5)
    flags_to_use = np.array([15,16,17,18])
    galcount, autoflag, stype = get_vals('mendel_lackner')
    props = get_flag_props(flags_to_use, autoflag, stype,typebins_lg12)
    props['datamask'] = np.where(np.array(props['total'])>0,True,False)
    ax1,ax2=plot_props('M$_{petro}$', props, typebins_lg12, delta, flags_to_use,plot_info)
    #pl.xticks(typebins_lg12+0.5, x_names, fontsize = 8)
    pl.title('Men14 (LG12 sample)', fontsize=8)
    l = ax2.legend(loc=10, bbox_to_anchor=(1.5, 0.5), prop={'size':6})
    pl.xticks(fontsize=8)
    pl.xlim(-16.5,-24.0)
    ax1.yaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)

if 0:
    print 'galzoo lackner'
    pl.subplot(5,2,7)
    flags_to_use = np.array([19,20,21,22,23])
    galcount, autoflag, stype = get_vals('galzoo_lackner')
    props = get_flag_props(flags_to_use, autoflag, stype,typebins_lg12)
    props['datamask'] = np.where(np.array(props['total'])>0,True,False)
    ax1,ax2=plot_props('M$_{petro}$', props, typebins_lg12, delta, flags_to_use,plot_info)
    #pl.xticks(typebins_lg12+0.5, x_names, fontsize = 8)
    pl.title('Galaxy Zoo (LG12 sample)', fontsize=8)
    l = ax2.legend(loc=10, bbox_to_anchor=(1.5, 0.5), prop={'size':6})
    pl.xticks(fontsize=8)
    pl.xlim(-16.5,-24.0)

    print 'galzoo'
    pl.subplot(5,2,8)
    flags_to_use = np.array([19,20,21,22,23])
    galcount, autoflag, stype = get_vals('galzoo')
    props = get_flag_props(flags_to_use, autoflag, stype,typebins)
    props['datamask'] = np.where(np.array(props['total'])>0,True,False)
    ax1,ax2=plot_props('M$_{petro}$', props, typebins, delta, flags_to_use,plot_info)
    #pl.xticks(typebins+0.5, x_names, fontsize = 8)
    pl.title('Galaxy Zoo (full sample)', fontsize=8)
#    l = ax2.legend(loc=2, bbox_to_anchor=(1.01, 0.1), prop={'size':6})
    pl.xticks(fontsize=8)
    pl.xlim(-16.5,-24.0)


print "lackner" 
pl.subplot(5,2,7)
flags_to_use = np.array([7,8,9,10,11,12])
galcount, autoflag, stype = get_vals('lackner')
props = get_flag_props(flags_to_use, autoflag, stype,typebins_lg12)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
ax1,ax2=plot_props('M$_{petro}$', props, typebins_lg12, delta, flags_to_use,plot_info)
#pl.xticks(typebins_lg12+0.5, x_names, fontsize = 8)
pl.title('LG12 (LG12 sample)', fontsize=8)
l = ax2.legend(loc=10, bbox_to_anchor=(1.5, 0.5), prop={'size':6})
pl.xticks(fontsize=8)
pl.xlim(-16.5,-24.0)
ax1.yaxis.set_tick_params(labelsize=6)
ax2.yaxis.set_tick_params(labelsize=6)

pl.savefig('./types_dist_abspmag_{band}_{model}.eps'.format(band=band, model=model), bbox_inches = 'tight')
#pl.show()
