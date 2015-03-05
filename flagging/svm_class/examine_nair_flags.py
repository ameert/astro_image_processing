import pylab as pl
from mysql_class import *
import numpy as np
from svm_functs import *
from matplotlib import cm

dba = 'simulations'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

cmd = """select a.galcount, IF(d.flag&(pow(2,6)+pow(2,7)+pow(2,13))>0, 1.0, b.n_bulge),  IF(d.flag&(pow(2,6)+pow(2,7)+pow(2,13))>0, 1.0-a.BT, a.BT), c.Ttype, c.Bar, c.Ring, c.Lens, c.Pairs, c.tails, f.p_serexp, d.flag from catalog.svm_probs as f, catalog.r_band_serexp as a,catalog.r_band_ser as b,catalog.Flags_optimize as d, catalog.Nair as c  where f.galcount = a.galcount and c.galcount = a.galcount and a.galcount = b.galcount and a.galcount = d.galcount and a.r_bulge>0 and b.r_bulge>0  and d.flag >=0 and d.band = 'r' and d.model = 'serexp' and d.ftype = 'u'
;""" 

galcount, n_ser, BT, Ttype, Bar, Ring, Lens, Pairs, tails, p_serexp, flag  = cursor.get_data(cmd)

galcount = np.array(galcount, dtype = int)
Ttype = np.array(Ttype)
BT = np.array(BT)
p_serexp = np.array(p_serexp)
n_ser = np.array(n_ser)
flag = np.array(flag, dtype=int)

plotcount = 0

output = np.array([ -452.90002401,1364.31502333,-1677.8076632,
                     1075.92230354,-382.59809833,72.53241043,-5.14678387])
p = np.poly1d(output)
bt_out = np.arange(0.1, 0.801, 0.001)
yvals_out =p(bt_out)

fig = pl.figure(figsize=(8.0,6.0))
pl.subplots_adjust(wspace = 0.4, hspace =0.5 )
for typename in [(-6, -4),(-3, 0), (1,4), (4,10)]:
    
    good_gals = np.where(Ttype >= typename[0], 1,0)*np.where(Ttype <= typename[1], 1,0)

    BT_ex = np.extract(good_gals==1, BT)
    p_serexp_ex = np.extract(good_gals==1, p_serexp)
    n_ser_ex = np.extract(good_gals==1, n_ser)
    galcount_ex = np.extract(good_gals==1, galcount)
    ttype_ex = np.extract(good_gals==1, Ttype)
    flags_ex = np.extract(good_gals==1, flag)
    
    com_type = np.zeros_like(flags_ex)

    com_type = np.where(flags_ex&2**1>0, 1,com_type)
    com_type = np.where(flags_ex&2**4>0, 2,com_type)
    com_type = np.where(flags_ex&2**10>0, 3,com_type)
    com_type = np.where(flags_ex&2**14>0, 4,com_type)
    com_type = np.where(flags_ex&2**9>0, 5,com_type)

    colors = ['k','r','b','g', 'm', 'y']

    point_color = [ colors[a] for a in com_type]

    print zip(galcount_ex,ttype_ex,n_ser_ex, BT_ex ,p_serexp_ex)

    total = BT_ex.size
    bad_zone = np.where(p_serexp_ex - p(BT_ex) <=0, 1, 0)
    bad_zone1 = np.where(p_serexp_ex - p(BT_ex) <=0, 1, 0)*np.where(flags_ex&2**10>0, 1,0)*np.where(flags_ex&2**14>0, 0,1)
    #print "ttype %d" %typename
    #print np.extract(bad_zone==1, galcount_ex)
    
    bad_zone = float(np.sum(bad_zone))
    bad_zone1 = float(np.sum(bad_zone1))
    plotcount +=1
    pl.subplot(2,2,plotcount)
    ax = pl.scatter(BT_ex, p_serexp_ex, s = 4, edgecolor = 'none', c = n_ser_ex, vmin = 0, vmax = 8, cmap = cm.jet)
    #ax = pl.scatter(BT_ex, p_serexp_ex, s = 4, edgecolor = 'none', c = point_color)
    
    pl.ylabel('P(serexp)')
    pl.xlabel('BT')
    pl.title('%d<=T<=%d' %(typename[0],typename[1]))
    pl.text(0.2, 0.2,'%.2f, %d, %d' %(bad_zone/total, bad_zone, total), transform=pl.gca().transAxes)
    pl.text(0.2, 0.1,'%.2f, %d, %d' %(bad_zone1/total, bad_zone1, total), transform=pl.gca().transAxes)
    pl.plot(bt_out, yvals_out, 'k-')
    pl.xlim(0,1)
    pl.ylim(0,1)

#colorbar_ax = fig.add_axes([0.6, 0.1, 0.05, 0.15])
#fig.colorbar(ax, cax=colorbar_ax)
pl.savefig('nair_pserexp_by_t_uflag_nser.eps')
