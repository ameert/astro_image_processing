import pylab as pl
import numpy as np
from mysql.mysql_class import *
from is_good import distance
import statistics.bin_stats as bin_stats

pstem = 'good'
model = 'ser'

if pstem == 'good':
    secondrun_poll = 0
elif pstem == 'bad':
    secondrun_poll = 1

cursor = mysql_connect('catalog','pymorph','pymorph')

cmd = 'select a.galcount, a.m_bulge, a.n_bulge, a.r_bulge, a.ba_bulge, b.PetroR50_r, b.Petromag_r, b.modelmag_r from {table} as a, DERT as x, CAST as b, r_band_badfits as c, r_sampledeep_{model} as rser where x.galcount = b.galcount and rser.galcount = a.galcount and a.galcount = b.galcount and a.galcount = c.galcount and c.is_polluted = 0 and c.is_fractured = 0 and rser.n_bulge>0 and rser.flag&pow(2,8)=0;' 
#cmd = 'select a.galcount, a.m_bulge, a.n_bulge, a.r_bulge, a.ba_bulge, b.PetroR50_r, b.Petromag_r, b.modelmag_r from {table} as a, DERT as x, CAST as b, r_band_badfits as c, r_deep_badfits as d, r_deep_{model} as rser where x.galcount = b.galcount and rser.galcount = a.galcount and a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and c.is_polluted = 1 and d.is_polluted = %d and rser.n_bulge>0;' %secondrun_poll
#cmd = 'select a.galcount, a.m_disk, a.n_bulge, a.r_disk, a.ba_disk, b.PetroR50_r, b.Petromag_r, b.modelmag_r from {table} as a, DERT as x, CAST as b, r_band_badfits as c, r_deep_badfits as d, r_deep_{model} as rser where x.galcount = b.galcount and rser.galcount = a.galcount and a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and c.is_polluted = 1 and d.is_polluted = %d and rser.n_bulge>0;' %secondrun_poll
#cmd = 'select a.galcount, a.m_tot, a.n_bulge, a.Hrad_corr, a.BT, b.PetroR50_r, b.Petromag_r, b.modelmag_r from {table} as a, DERT as x, CAST as b, r_band_badfits as c, r_deep_badfits as d, r_deep_{model} as rser where x.galcount = b.galcount and rser.galcount = a.galcount and a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and c.is_polluted = 1 and d.is_polluted = %d and rser.n_bulge>0;' %secondrun_poll

#-b.extinction_r-x.dismod

def plot_bars(nstats, plotnum):
    pl.subplot(2,2,plotnum)
    pl.errorbar(nstats.bin_median,1.0-0.3, xerr=nstats.bin_med95ci, ecolor = 'm', marker='s', markersize=2)
    pl.errorbar(nstats.bin_mean,1.0-0.2, xerr=nstats.bin_stdev, ecolor = 'm', marker='s', markersize=2)
    pl.errorbar(nstats.bin_median,1.0-0.1, xerr=nstats.bin_68[0:2], ecolor = 'r', marker='s', markersize=2)
    pl.errorbar(nstats.bin_median,1, xerr=nstats.bin_95[0:2], ecolor = 'b', marker='s', markersize=2)
    pl.errorbar(nstats.bin_median,1+0.1, xerr=nstats.bin_99[0:2], ecolor = 'g', marker='s', markersize=2)
    pl.ylim(0.6,1.2)
    ax = pl.gca()
    pl.yticks((0.7,0.8,0.9,1.0,1.1),
              ('med/95ci','mean/std','med/68','med/95','med/99'))
    return



def do_scaplots(distance_dict, after_dict, before_dict, bins, xtext, option=0):
    for count, name,ylims in ((0,'m_diff', (-0.5,0.5)),(1,'n diff', (-1,0.5)),(2,'r diff', (-0.5,0.5)),(3, 'ba diff', (-0.05,0.05))): 
        pl.subplot(2,2,count+1)
        if 0:#count ==2:
            ns = np.array([after_dict[a][count]/np.max([before_dict[a][count],0.0000001])-1.0 for a in before_dict.keys()]).T
        else:
            ns = np.array([after_dict[a][count]-before_dict[a][count] for a in before_dict.keys()]).T
        bars, edges=np.histogram(ns, bins=100,range=ylims)
        bars = bars/float(ns.size)
        print ns
        #pl.step(bars, edges, *args, **kwargs)
        pl.barh((edges[0:-1]+edges[1:])/2, bars, align='center', height = (edges[1:]-edges[0:-1]),alpha=0.4)
        #pl.scatter(ns[0,:], ns[1,:], s =3, edgecolor='none', zorder = -900)
        nstats = bin_stats.bin_stats(0.25*np.ones_like(ns), ns, (0.0,0.5), -1000.0, 1000.0)
        nstats.lay_bounds(color='r', sigma_choice = [68,95])
        nstats.plot_ebar('median','med95ci',color='r',ecolor='r',
                         marker='s', markersize=3, lw=2, linestyle='none')
        pl.xlabel(xtext)
        pl.ylabel(name)
        pl.ylim(ylims)
        pl.xlim(0,0.5)


    #ax = pl.subplot(2,2,3)
    #pl.ylim(-10,10)
    pl.subplots_adjust(wspace=0.4, hspace=0.4)
    return


 
data_before = cursor.get_data(cmd.format(table='r_band_%s'%model, model=model))
data_after = cursor.get_data(cmd.format(table='r_sampledeep_%s'%model, model=model))

before_dict = dict([(a[0], (a[1:])) for a in zip(*data_before)])
after_dict = dict([(a[0], (a[1:])) for a in zip(*data_after)])

distance_dict = before_dict

keys_to_use = set(before_dict.keys())&set(after_dict.keys())&set(distance_dict.keys())
fig1 = pl.figure('changes')
#pl.figtitle()
ns = np.array([(before_dict[a][1],after_dict[a][1]) for a in keys_to_use]).T
ns = np.array([(before_dict[a][1],after_dict[a][1]) for a in before_dict.keys()]).T
print [(before_dict[a][1],after_dict[a][1]) for a in keys_to_use]
nstats = bin_stats.bin_stats(ns[0,:], ns[1,:]- ns[0,:], np.array([0,100]), -8.0, 8.0)
plot_bars(nstats,1)
pl.title('n_ser')
pl.xlabel('$\Delta$n')

ms = np.array([(before_dict[a][0],after_dict[a][0]) for a in keys_to_use]).T 
ms = np.array([(before_dict[a][0],after_dict[a][0]) for a in before_dict.keys()]).T
nstats = bin_stats.bin_stats(ms[0,:], ms[1,:]- ms[0,:], np.array([0,100]), -8.0, 8.0)
plot_bars(nstats,2)
pl.title('m_ser')
pl.xlabel('$\Delta$m')


rs = np.array([(before_dict[a][2],after_dict[a][2]) for a in keys_to_use]).T
rs = np.array([(before_dict[a][2],after_dict[a][2]) for a in before_dict.keys()]).T
nstats = bin_stats.bin_stats(rs[0,:], (rs[1,:]- rs[0,:])/(0.0*rs[0,:]+1), np.array([0,1000]), -1000.0, 1000.0)
plot_bars(nstats, 3)
pl.title('r_ser')
pl.xlabel('$\Delta$r')

bs = np.array([(before_dict[a][3],after_dict[a][3]) for a in keys_to_use]).T 
bs = np.array([(before_dict[a][3],after_dict[a][3]) for a in before_dict.keys()]).T
nstats = bin_stats.bin_stats(bs[0,:], bs[1,:]- bs[0,:], np.array([0,1000]), -1000.0, 1000.0)
plot_bars(nstats, 4)
pl.title('ba_ser')
pl.xlabel('$\Delta$ba')

#pl.show()
pl.subplots_adjust(wspace=0.4, hspace=0.4)



fig2 = pl.figure('vs d/r')
do_scaplots(distance_dict, after_dict, before_dict, np.arange(0,3.01,0.5), 'dis/rad', option=0)
fig2.savefig('dr_%s_bad%s.eps' %(model,pstem))
pl.show()
sys.exit()
fig3 = pl.figure('vs. mn-mt')
do_scaplots(distance_dict, after_dict, before_dict, np.arange(-2.0,4.01,0.5), 'mn-mt', option=1)
fig3.savefig('dm_%s_bad%s.eps' %(model,pstem))

fig4 = pl.figure('vs. mn-mt+dis/rad')
do_scaplots(distance_dict, after_dict, before_dict, np.arange(-2.0,4.01,0.5), 'mn-mt+dis/rad', option=2)
fig4.savefig('dmdr_%s_good%s.eps' %(model,pstem))

pl.show()
sys.exit()





ms = np.array([(before_dict[a][0],after_dict[a][0]) for a in keys_to_use]).T
 
ms = np.where(ms >100, 21.0, ms)

pl.scatter(ms[0,:], ms[1,:], s =3, edgecolor='none')
pl.xlabel('m before')
pl.ylabel('m after')
pl.xlim(12,21.1)
pl.ylim(12,21.1)
pl.show()

ms = np.array([(before_dict[a][5]-before_dict[a][0],before_dict[a][5]-after_dict[a][0]) for a in keys_to_use]).T
 
#ms = np.where(ms >100, 21.0, ms)

pl.scatter(ms[0,:], ms[1,:], s =3, edgecolor='none')
pl.xlabel('m petro-m before')
pl.ylabel('m petro -m after')
pl.xlim(-5,5)
pl.ylim(-5,5)
pl.show()

ms = np.array([(before_dict[a][6]-before_dict[a][0],before_dict[a][6]-after_dict[a][0]) for a in keys_to_use]).T
 
#ms = np.where(ms >100, 21.0, ms)

pl.scatter(ms[0,:], ms[1,:], s =3, edgecolor='none')
pl.xlabel('m model-m before')
pl.ylabel('m model -m after')
pl.xlim(-5,5)
pl.ylim(-5,5)
pl.show()

ms = np.array([(before_dict[a][6],after_dict[a][0]) for a in keys_to_use]).T
 
ms = np.where(ms >100, 21.0, ms)

pl.scatter(ms[0,:], ms[1,:], s =3, edgecolor='none')
pl.xlabel('m model')
pl.ylabel('m after')
pl.xlim(12,21.1)
pl.ylim(12,21.1)
pl.show()

rs = np.array([(before_dict[a][2],after_dict[a][2]) for a in keys_to_use]).T
 
rs = np.where(rs <0, -1.0, rs)

pl.scatter(rs[0,:], rs[1,:], s =3, edgecolor='none')
pl.xlabel('r before')
pl.ylabel('r after')
pl.xlim(-1.1,20)
pl.ylim(-1.1,20)
pl.show()

bs = np.array([(before_dict[a][3],after_dict[a][3]) for a in keys_to_use]).T
 
bs = np.where(bs <0, -0.10, bs)

pl.scatter(bs[0,:], bs[1,:], s =3, edgecolor='none')
pl.xlabel('ba before')
pl.ylabel('ba after')
pl.xlim(-0.1,1.0)
pl.ylim(-0.1,1.0)
pl.show()



