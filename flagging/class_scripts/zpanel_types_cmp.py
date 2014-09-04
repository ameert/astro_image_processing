from mysql_class import *
from flag_defs import *
import pylab as pl
import matplotlib.ticker as mticker

def print_flags(autoflag, test_flag, print_gals = False):
    flag_vals = np.where(np.abs(autoflag-test_flag)<0.1, 1,0)
    flag_num = np.sum(flag_vals)/float(len(flag_vals))
    if np.isnan(flag_num):
        flag_num = 0.0
    print "%d: %.4f" %(test_flag, flag_num)
    if print_gals:
        print np.extract(flag_vals==1, galcount)
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
    if binval == 'lackner':
        cmd = """select d.galcount,c.flag, IF(d.model='dvc' or (d.model='ser' and z.n_bulge>=2.0), 1,0)+IF(d.model='exp' or (d.model='ser' and z.n_bulge<2.0), 2,0)+IF(d.model='nb1'or d.model = 'nb4', 3,0) from catalog.Flags_catalog as c, catalog.{band}_lackner_fit as d, catalog.{band}_lackner_ser as z where c.galcount = d.galcount  and c.galcount = z.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by d.galcount;""".format(model = model, band = band)
    elif binval == 'simard':
        cmd = """select d.galcount,c.flag, IF(d.Prob_pS>0.32 and z.n_bulge>=2.0, 1,0)+IF(d.Prob_pS>0.32 and z.n_bulge<2.0, 2,0)+IF(d.Prob_pS<=0.32, 3,0) from catalog.Flags_catalog as c, catalog.{band}_simard_fit as d, catalog.{band}_simard_ser as z where c.galcount = d.galcount and c.galcount = z.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by d.galcount;""".format(model = model, band = band)
    elif binval == 'mendel':
        cmd = """select d.galcount,c.flag, IF(d.ProfType=1 or (d.ProfType=4 and z.n_bulge >=2.0) , 1,0)+IF(d.ProfType=2 or (d.ProfType=4 and z.n_bulge <2.0), 2,0)+IF(d.ProfType=3, 3,0) from catalog.Flags_catalog as c, simard.Mendel_masses as d,  catalog.{band}_simard_ser as z where c.galcount = d.galcount and c.galcount = z.galcount  and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by d.galcount;""".format(model = model, band = band)
    elif binval == 'nair':
        cmd = """select d.galcount,c.flag, d.Ttype from catalog.Flags_catalog as c, catalog.Nair as d where c.galcount = d.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by d.galcount;""".format(model = model, band = band)
    elif binval == 'nair_lackner':
        cmd = """select d.galcount, IF(d.model='dvc' or (d.model='ser' and z.n_bulge>=2.0), 2,0)+IF(d.model='exp' or (d.model='ser' and z.n_bulge<2.0), 16,0)+IF(d.model='nb1'or d.model = 'nb4', pow(2,10),0),  c.Ttype from catalog.{band}_lackner_fit as d, catalog.{band}_lackner_ser as z, catalog.Nair as c  where c.galcount = d.galcount  and c.galcount = z.galcount  order by d.galcount;""".format(model = model, band = band)
    elif binval == 'nair_simard':
        cmd = """select d.galcount, IF(d.Prob_pS>0.32 and z.n_bulge>=2.0, 2,0)+IF(d.Prob_pS>0.32 and z.n_bulge<2.0, 16,0)+IF(d.Prob_pS<=0.32, pow(2,10),0),  c.Ttype  from  catalog.Nair as c, catalog.{band}_simard_fit as d, catalog.{band}_simard_ser as z where c.galcount = d.galcount and c.galcount = z.galcount order by d.galcount;""".format(model = model, band = band)
    elif binval == 'nair_mendel':
        cmd = """select d.galcount, IF(d.ProfType=1 or (d.ProfType=4 and z.n_bulge >=2.0) ,2,0)+IF(d.ProfType=2 or (d.ProfType=4 and z.n_bulge <2.0), 16,0)+IF(d.ProfType=3, pow(2,10),0) ,  c.Ttype from catalog.Nair as c, simard.Mendel_masses as d,  catalog.{band}_simard_ser as z where c.galcount = d.galcount and c.galcount = z.galcount order by d.galcount;""".format(model = model, band = band)
    elif binval == 'nair_lackner_meert':
        cmd = """select d.galcount, c.flag,  d.Ttype from catalog.Flags_catalog as c, catalog.{band}_lackner_fit as z, catalog.Nair as d  where c.galcount = d.galcount  and c.galcount = z.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by d.galcount;""".format(model = model, band = band)
    elif binval == 'meert':
        cmd = """select c.galcount,c.flag,  -6.0*m.probaEll -3.0*m.probaS0+4.0*m.probaSab+8.0*m.probaScd from catalog.Flags_catalog as c, catalog.M2010 as m where c.galcount = m.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by c.galcount;""".format(model = model, band = band)
    galcount, flags, flag2 = cursor.get_data(cmd)
    galcount = np.array(galcount, dtype=int)
    autoflag = np.array(flags, dtype=int)
    autoflag = np.where(autoflag&2**1>0,1,0)+np.where(autoflag&2**4>0,2,0)+np.where(autoflag&2**10>0,3,0)+np.where(autoflag&2**14>0,4,0)+np.where(autoflag&2**19>0,5,0)
    autoflag = autoflag.astype(int)

    flag2 = np.array(flag2, dtype=int)

    return galcount, autoflag, flag2

def plot_props(xlab, props, magbins, flags_to_use,plot_info):
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

    ax1.bar(magbins[:-1], props['total'],width = 1,  color = plot_info['total']['color'], log = False, zorder = -100) 

    
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

flags_to_use = np.array([1,2,3,4,5])

plot_info = {1:{'color':'r', 'label':'bulges', 'ms':3},
             2:{'color':'b', 'label':'disks', 'ms':3},
             3:{'color':'g', 'label':'2com', 'ms':3},
             4:{'color':'y', 'label':'bad 2com', 'ms':3},
             5:{'color':'k', 'label':'bad', 'ms':3},
             'total': {'color':"#D0D0D0",'label':'total'}
             }

names=[ plot_info[key]['label'] for key in plot_info.keys()] 
fig = pl.figure(figsize=(8,10))
pl.subplots_adjust(right = 0.85, left =0.1, hspace = 0.5, wspace = 0.75)

typebins = np.array([0.5,1.5, 2.5, 3.5, 4.5, 5.5])[:4]

print "simard" 
pl.subplot(4,2,1)

galcount, autoflag, stype = get_vals('simard')
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
plot_props('', props, typebins, flags_to_use,plot_info)
pl.xticks(np.arange(len(names[:3]))+1, names, fontsize = 8, rotation=90)
pl.title('Simard types')
#pl.xticks(rotation=90)
print "lackner" 
pl.subplot(4,2,5)

galcount, autoflag, stype = get_vals('lackner')
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
plot_props('', props, typebins, flags_to_use,plot_info)
pl.xticks(np.arange(len(names[:3]))+1, names, fontsize = 8)
pl.title('Lackner types')
#pl.xticks(rotation=90)

print "mendel" 
pl.subplot(4,2,3)

galcount, autoflag, stype = get_vals('mendel')
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
ax1, ax2 =plot_props('', props, typebins, flags_to_use,plot_info)
pl.xticks(np.arange(len(names[:3]))+1, names, fontsize = 8)
pl.title('mendel types')
pl.xticks(rotation=90)

print "nair" 
pl.subplot(4,2,7)

galcount, autoflag, stype = get_vals('nair')
for vals in [(99,13), (-2, -1), (-3, -2), (-5,-3)]:
    stype = np.where(stype==vals[0], vals[1], stype)

nair_typebins = np.arange(-3.5, 13.51,1.0)
nair_names= [str(a) for a in ([-5,-3,-2] + range(0,14))]
props = get_flag_props(flags_to_use, autoflag, stype,nair_typebins)
ax1, ax2 =plot_props('T', props, nair_typebins, flags_to_use,plot_info)
pl.xticks(np.arange(len(nair_names))-3, nair_names, fontsize = 8)
pl.title('Meert types')
pl.xticks(rotation=90)
#l = ax2.legend(loc='center', bbox_to_anchor=(-1.5, 0.5))

print "meert" 
pl.subplot(4,2,8)

galcount, autoflag, stype = get_vals('meert')
for vals in [(99,13), (-2, -1), (-3, -2), (-5,-3)]:
    stype = np.where(stype==vals[0], vals[1], stype)

nair_typebins = np.arange(-3.5, 13.51,1.0)
nair_names= [str(a) for a in ([-5,-3,-2] + range(0,14))]
props = get_flag_props(flags_to_use, autoflag, stype,nair_typebins)
ax1, ax2 =plot_props('T', props, nair_typebins, flags_to_use,plot_info)
pl.xticks(np.arange(len(nair_names))-3, nair_names, fontsize = 8)
pl.title('Meert types')
pl.xticks(rotation=90)
#l = ax2.legend(loc='center', bbox_to_anchor=(-1.5, 0.5))



print "simard" 
pl.subplot(4,2,2)

galcount, autoflag, stype = get_vals('nair_simard')
for vals in [(99,13), (-2, -1), (-3, -2), (-5,-3)]:
    stype = np.where(stype==vals[0], vals[1], stype)
props = get_flag_props(flags_to_use, autoflag, stype,nair_typebins)
plot_props('T', props, nair_typebins, flags_to_use,plot_info)
pl.xticks(np.arange(len(nair_names))-3, nair_names, fontsize = 8)
pl.title('Simard types')
#pl.xticks(rotation=90)



print "lackner" 
pl.subplot(4,2,6)

galcount, autoflag, stype = get_vals('nair_lackner')
for vals in [(99,13), (-2, -1), (-3, -2), (-5,-3)]:
    stype = np.where(stype==vals[0], vals[1], stype)
props = get_flag_props(flags_to_use, autoflag, stype,nair_typebins)
plot_props('T', props, nair_typebins, flags_to_use,plot_info)
pl.xticks(np.arange(len(nair_names))-3, nair_names, fontsize = 8)
pl.title('Lackner types')
#pl.xticks(rotation=90)

print "mendel" 
pl.subplot(4,2,4)

galcount, autoflag, stype = get_vals('nair_mendel')
for vals in [(99,13), (-2, -1), (-3, -2), (-5,-3)]:
    stype = np.where(stype==vals[0], vals[1], stype)
props = get_flag_props(flags_to_use, autoflag, stype,nair_typebins)
plot_props('T', props, nair_typebins, flags_to_use,plot_info)
pl.xticks(np.arange(len(nair_names))-3, nair_names, fontsize = 8)
pl.title('mendel types')
pl.xticks(rotation=90)


#pl.show()
pl.savefig('./types_dist.eps')
#pl.savefig('./dist_obs_petro.eps')
#pl.savefig('./dist_obs_small_petro.eps')

