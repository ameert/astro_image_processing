import pylab as pl
import numpy as np
from astro_image_processing.mysql import *
from is_good import distance
import astro_image_processing.statistics.bin_stats as bin_stats
from astro_image_processing.MatplotRc import *
from scipy import ndimage

pstem = 'good'
model = 'ser'

if pstem == 'good':
    secondrun_poll = 0
elif pstem == 'bad':
    secondrun_poll = 1

cursor = mysql_connect('catalog','pymorph','pymorph')

#cmd = 'select a.galcount, a.m_bulge, a.n_bulge, a.r_bulge, a.ba_bulge, b.PetroR50_r, b.Petromag_r, b.modelmag_r from {table} as a, DERT as x, CAST as b, r_band_badfits as c, r_sampledeep_{model} as rser where x.galcount = b.galcount and rser.galcount = a.galcount and a.galcount = b.galcount and a.galcount = c.galcount and c.is_polluted = 0 and c.is_fractured = 0 and rser.n_bulge>0;' 
cmd = 'select a.galcount, a.m_bulge, a.n_bulge, a.r_bulge, a.ba_bulge, b.PetroR50_r, b.Petromag_r, b.modelmag_r from {table} as a, DERT as x, CAST as b, r_band_badfits as c, r_deep_badfits as d, r_deep_{model} as rser where x.galcount = b.galcount and rser.galcount = a.galcount and a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and c.is_polluted = 1 and d.is_polluted = %d and rser.n_bulge>0;' %secondrun_poll
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

def get_distance():
    cmd = """select  a.galcount,b.colc_r, a.colc_r, b.rowc_r,a.rowc_r, 
a.petroR50_r, c.Hrad_corr, b.petroR50_r, 
a.PetroMag_r, c.m_tot, b.PetroMag_r, a.flags_r,c.ba_bulge, c.pa_bulge
from CAST_neighbors as a, CAST as b, r_band_{model} as c,
r_band_badfits as rbf, r_deep_badfits as rdf
where a.galcount = b.galcount and a.galcount = c.galcount and 
rbf.galcount = b.galcount  and rdf.galcount = b.galcount and 
rbf.is_polluted = 1 and rdf.is_polluted = {ispoll2} and 
a.is_polluter = 1 and a.is_polluter_deep={ispoll2} group by a.galcount;""".format(ispoll2= secondrun_poll, model = model)


#flag condition prevents "nopeaks" from being considered
    data = np.array(cursor.get_data(cmd))

    galcount, xt,xn, yt,yn, rn, rf,rcas,mn, mf, mcas,flag, ba_t, pa_t = data  
    
    userad = np.max(np.array([rf,rcas]), axis=0)
    dis = distance(xt, xn, yt, yn, ba_t, pa_t)

    return galcount, dis, userad, mn-mf


def do_scaplots(distance_dict, after_dict, before_dict, bins, xtext, option=0):
    for count, name,ylims in ((0,'$\Delta$m', (-1,1)),):#,(2,'r diff', (-1,1))):
#,(1,'n diff', (-2,2)),(3, 'ba diff', (-0.2,0.2))): 
        pl.subplot(1,1,count+1)
        if option==0:
            if count ==2:
                ns = np.array([(distance_dict[a][0]/distance_dict[a][1], after_dict[a][count]/np.max([before_dict[a][count],0.0000001])-1.0) for a in keys_to_use]).T
            else:
                ns = np.array([(distance_dict[a][0]/distance_dict[a][1], after_dict[a][count]-before_dict[a][count]) for a in keys_to_use]).T
        elif option == 1:
            if count ==2:
                ns = np.array([(distance_dict[a][2], after_dict[a][count]/np.max([before_dict[a][count],0.0000001])-1.0) for a in keys_to_use]).T
            else:
                ns = np.array([(distance_dict[a][2], after_dict[a][count]-before_dict[a][count]) for a in keys_to_use]).T
        elif option ==2:
            if count ==2:
                ns = np.array([(distance_dict[a][2]+distance_dict[a][0]/distance_dict[a][1], after_dict[a][count]/np.max([before_dict[a][count],0.0000001])-1.0) for a in keys_to_use]).T
            else:
                ns = np.array([(distance_dict[a][2]+distance_dict[a][0]/distance_dict[a][1], after_dict[a][count]-before_dict[a][count]) for a in keys_to_use]).T

        if option==0:
            xlims=(0,3.1)
        elif option == 1:
            xlims=(0,4)
        elif option ==2:
            xlims=(0,4)



        H, xedges, yedges = np.histogram2d(ns[0,:], ns[1,:], 
                                           range = [xlims,ylims], 
                                           bins = 50)
        Hpic = ndimage.rotate(H, 90.0)
        extent = [xlims[0], xlims[1], ylims[0], ylims[1]]
        img = pl.imshow(Hpic,  interpolation='nearest', extent = extent,
                        zorder = -900)
        img.set_cmap(pl.cm.gray_r)
        #pl.scatter(ns[0,:], ns[1,:], s =3, edgecolor='none', zorder = -900, 
        #           c='#BABABA')
        nstats = bin_stats.bin_stats(ns[0,:], ns[1,:], bins, -1000.0, 1000.0)
        nstats.lay_bounds(color='r', sigma_choice = [68,95,99])
        nstats.plot_ebar('median','med95ci',color='r',ecolor='r',
                         marker='s', markersize=3, lw=2, linestyle='none')
        pl.xlabel(xtext)
        pl.ylabel(name)
        pl.ylim(ylims)
        if option==0:
            pl.xlim(0,3.1)
        elif option == 1:
            pl.xlim(0,4)
        elif option ==2:
            pl.xlim(0,4)

    pl.plot(pl.xlim(), (0.0,0.0), 'k-')
    #ax = pl.subplot(2,2,3)
    #pl.ylim(-10,10)
    pl.subplots_adjust(wspace=0.4, hspace=0.4)
    return


distance_data = get_distance()
print distance_data
distance_dict = dict([(a[0], (a[1:])) for a in zip(*distance_data)])
print 'glas ', len(distance_dict.keys()) 
#raw_input()
data_before = cursor.get_data(cmd.format(table='r_predeep_%s'%model, model=model))
data_after = cursor.get_data(cmd.format(table='r_band_%s'%model, model=model))

before_dict = dict([(a[0], (a[1:])) for a in zip(*data_before)])
after_dict = dict([(a[0], (a[1:])) for a in zip(*data_after)])

keys_to_use = set(before_dict.keys())&set(after_dict.keys())&set(distance_dict.keys())
fig1 = pl.figure('changes')
#pl.figtitle()
ns = np.array([(before_dict[a][1],after_dict[a][1]) for a in keys_to_use]).T
#ns = np.array([(before_dict[a][1],after_dict[a][1]) for a in before_dict.keys()]).T
print [(before_dict[a][1],after_dict[a][1]) for a in keys_to_use]
nstats = bin_stats.bin_stats(ns[0,:], ns[1,:]- ns[0,:], np.array([0,100]), -8.0, 8.0)
plot_bars(nstats,1)
pl.title('n_ser')
pl.xlabel('$\Delta$n')

ms = np.array([(before_dict[a][0],after_dict[a][0]) for a in keys_to_use]).T 
#ms = np.array([(before_dict[a][0],after_dict[a][0]) for a in before_dict.keys()]).T
nstats = bin_stats.bin_stats(ms[0,:], ms[1,:]- ms[0,:], np.array([0,100]), -8.0, 8.0)
plot_bars(nstats,2)
pl.title('m_ser')
pl.xlabel('$\Delta$m')


rs = np.array([(before_dict[a][2],after_dict[a][2]) for a in keys_to_use]).T
#rs = np.array([(before_dict[a][2],after_dict[a][2]) for a in before_dict.keys()]).T
nstats = bin_stats.bin_stats(rs[0,:], rs[1,:]- rs[0,:], np.array([0,1000]), -1000.0, 1000.0)
plot_bars(nstats, 3)
pl.title('r_ser')
pl.xlabel('$\Delta$r')

bs = np.array([(before_dict[a][3],after_dict[a][3]) for a in keys_to_use]).T 
#bs = np.array([(before_dict[a][3],after_dict[a][3]) for a in before_dict.keys()]).T
nstats = bin_stats.bin_stats(bs[0,:], bs[1,:]- bs[0,:], np.array([0,1000]), -1000.0, 1000.0)
plot_bars(nstats, 4)
pl.title('ba_ser')
pl.xlabel('$\Delta$ba')

pl.subplots_adjust(wspace=0.4, hspace=0.4)

fig2 = pl.figure('vs d/r')
do_scaplots(distance_dict, after_dict, before_dict, np.arange(0,3.01,0.5), 'dis/rad', option=0)
fig2.savefig('dr_%s_bad%s.eps' %(model,pstem), bbox_inches='tight')

fig3 = pl.figure('vs. mn-mt', figsize=get_fig_size())
dat = pub_plots(xmaj = 1, xmin = 0.5, xstr = '%d', ymaj = 0.5, ymin = 0.1, 
          ystr = '%02.1f')
do_scaplots(distance_dict, after_dict, before_dict, np.arange(-2.0,4.01,0.5), 'm$_{neighbor}$ - m$_{target}$', option=1)
pl.subplots_adjust(left=0.2,bottom=0.16, top=0.99, right=0.97)
dat.set_plot(pl.subplot(1,1,1))
fig3.savefig('dm_%s_bad%s.eps' %(model,pstem))#, bbox_inches='tight')

fig4 = pl.figure('vs. mn-mt+dis/rad')
do_scaplots(distance_dict, after_dict, before_dict, np.arange(-2.0,4.01,0.5), 'mn-mt+dis/rad', option=2)
fig4.savefig('dmdr_%s_bad%s.eps' %(model,pstem), bbox_inches='tight')

#pl.show()
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



