import pylab as pl
from mysql_class import *
import numpy as np
from svm_functs import *
from matplotlib import cm

dba = 'simulations'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

cmd = 'select a.galcount, b.n_bulge, d.BT, a.r_bulge, a.n_bulge, a.ba_bulge, a.pa_bulge, a.r_disk, a.ba_disk, a.pa_disk, a.BT, a.r_bulge/a.r_disk, c.Ttype, c.Bar, c.Ring, c.Lens, c.Pairs, c.tails, f.p_serexp from catalog.svm_probs as f, catalog.r_band_serexp as a,catalog.r_band_ser as b,catalog.r_band_devexp as d, catalog.Nair as c where f.galcount = a.galcount and c.galcount = a.galcount and a.galcount = b.galcount and a.galcount = d.galcount and a.r_bulge>0 and b.r_bulge>0 and d.r_bulge >0;' 

galcount, n_ser, BT_devexp, re_serexp, n_serexp, eb_serexp, bpa, rd_serexp, ed_serexp, dpa, BT, rerd_serexp, Ttype, Bar, Ring, Lens, Pairs, tails, p_serexp  = cursor.get_data(cmd)
    
diff_pa = angdiff(np.array(bpa),np.array(dpa),np.array(eb_serexp),np.array(ed_serexp))

Ttype = np.array(Ttype)
BT = np.array(BT)
p_serexp = np.array(p_serexp)
n_ser = np.array(n_ser)

plotcount = 0

output = np.array([ -452.90002401,1364.31502333,-1677.8076632,
                     1075.92230354,-382.59809833,72.53241043,-5.14678387])
p = np.poly1d(output)
bt_out = np.arange(0.1, 0.801, 0.001)
yvals_out =p(bt_out)

fig = pl.figure(figsize=(15.0,10.0))
pl.subplots_adjust(wspace = 0.4, hspace =0.5 )
for typename in range(-5, 11):
    if typename in [-4, -1]:
        continue

    BT_ex = np.extract(Ttype == typename, BT)
    p_serexp_ex = np.extract(Ttype == typename, p_serexp)
    n_ser_ex = np.extract(Ttype == typename, n_ser)

    total = BT_ex.size
    bad_zone = float(np.sum(np.where(p_serexp_ex - p(BT_ex) <=0, 1, 0)))

    plotcount +=1
    pl.subplot(4,4,plotcount)
    ax = pl.scatter(BT_ex, p_serexp_ex, s = 4, edgecolor = 'none', c = n_ser_ex, vmin = 0, vmax = 8, cmap = cm.jet)
    pl.ylabel('P(serexp)')
    pl.xlabel('BT')
    pl.title('T=%d' %typename)
    pl.text(0.2, 0.2,'%.2f, %d, %d' %(bad_zone/total, bad_zone, total), transform=pl.gca().transAxes)
    pl.plot(bt_out, yvals_out, 'k-')
    

    pl.xlim(0,1)
    pl.ylim(0,1)

colorbar_ax = fig.add_axes([0.6, 0.1, 0.05, 0.15])
fig.colorbar(ax, cax=colorbar_ax)
pl.savefig('nair_pserexp_by_t.eps')
