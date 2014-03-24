import numpy as np
import os
import sys
import pylab as pl
import matplotlib.cm as cm
from mysql_class import *
from utilities import *

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

#cmd = 'select c.galcount, b.ProbaE, x.m_tot - d.kcorr_r - c.extinction_r-d.dismod,y.m_tot - d.kcorr_r - c.extinction_r-d.dismod,z.m_tot - d.kcorr_r - c.extinction_r-d.dismod, x.n_bulge,y.n_bulge,z.n_bulge, x.Hrad_corr*d.kpc_per_arcsec,y.Hrad_corr*d.kpc_per_arcsec,z.Hrad_corr*d.kpc_per_arcsec, x.BT,y.BT,z.BT from g_band_serexp as x ,r_band_serexp as y ,i_band_serexp as z, DERT as d, M2010 as b , CAST as c where c.galcount = b.galcount and x.galcount = c.galcount and c.galcount = d.galcount and c.galcount = y.galcount and c.galcount = z.galcount and d.kcorr_r > -900 order by rand() limit 10000;' 

#select * from ((select c.galcount, a.p_ser as prob, b.ProbaE, x.m_tot - d.kcorr_r - c.extinction_r-d.dismod as absmag_g,y.m_tot - d.kcorr_r - c.extinction_r-d.dismod as absmag_r,z.m_tot - d.kcorr_r - c.extinction_r-d.dismod, x.n_bulge,y.n_bulge,z.n_bulge, x.Hrad_corr*d.kpc_per_arcsec,y.Hrad_corr*d.kpc_per_arcsec,z.Hrad_corr*d.kpc_per_arcsec, x.BT,y.BT,z.BT from g_band_ser as x ,r_band_serexp as y ,i_band_serexp as z, DERT as d, M2010 as b , CAST as c, svm_probs as a where c.galcount = b.galcount and x.galcount = c.galcount and c.galcount = d.galcount and c.galcount = y.galcount and c.galcount = z.galcount and c.galcount = a.galcount and d.kcorr_r > -900) union (select c.galcount, 1.0-a.p_ser as prob, b.ProbaE, x.m_tot - d.kcorr_r - c.extinction_r-d.dismod,y.m_tot - d.kcorr_r - c.extinction_r-d.dismod,z.m_tot - d.kcorr_r - c.extinction_r-d.dismod, x.n_bulge,y.n_bulge,z.n_bulge, x.Hrad_corr*d.kpc_per_arcsec,y.Hrad_corr*d.kpc_per_arcsec,z.Hrad_corr*d.kpc_per_arcsec, x.BT,y.BT,z.BT from g_band_serexp as x ,r_band_serexp as y ,i_band_serexp as z, DERT as d, M2010 as b , CAST as c, svm_probs as a where c.galcount = b.galcount and x.galcount = c.galcount and c.galcount = d.galcount and c.galcount = y.galcount and c.galcount = z.galcount and c.galcount = a.galcount and d.kcorr_r > -900)) as tmptab where prob > 0.5;

#cmd = 'select * from ((select c.galcount, a.p_ser-1.0 as prob, b.ProbaE, x.m_tot- d.kcorr_r - c.extinction_r-d.dismod as mag_g,y.m_tot- d.kcorr_r - c.extinction_r-d.dismod as mag_r,z.m_tot- d.kcorr_r - c.extinction_r-d.dismod as mag_i, x.n_bulge as n_g, y.n_bulge as n_r,z.n_bulge as n_i, x.Hrad_corr*d.kpc_per_arcsec as rad_g,y.Hrad_corr*d.kpc_per_arcsec as rad_r,z.Hrad_corr*d.kpc_per_arcsec as rad_i, x.BT as BT_r,y.BT as BT_i,z.BT as BT_z from g_band_ser as x ,r_band_ser as y ,i_band_ser as z, DERT as d, M2010 as b , CAST as c, svm_probs as a where c.galcount = b.galcount and x.galcount = c.galcount and c.galcount = d.galcount and c.galcount = y.galcount and c.galcount = z.galcount and c.galcount = a.galcount and d.kcorr_r > -900) union (select c.galcount, a.p_ser as prob, b.ProbaE, x.m_tot- d.kcorr_r - c.extinction_r-d.dismod as mag_g,y.m_tot- d.kcorr_r - c.extinction_r-d.dismod as mag_r,z.m_tot- d.kcorr_r - c.extinction_r-d.dismod as mag_i, x.n_bulge as n_g, y.n_bulge as n_r,z.n_bulge as n_i, x.Hrad_corr*d.kpc_per_arcsec as rad_g,y.Hrad_corr*d.kpc_per_arcsec as rad_r,z.Hrad_corr*d.kpc_per_arcsec as rad_i, x.BT as BT_r,y.BT as BT_i,z.BT as BT_z from g_band_serexp as x ,r_band_serexp as y ,i_band_serexp as z, DERT as d, M2010 as b , CAST as c, svm_probs as a where c.galcount = b.galcount and x.galcount = c.galcount and c.galcount = d.galcount and c.galcount = y.galcount and c.galcount = z.galcount and c.galcount = a.galcount and d.kcorr_r > -900)) as tmptab where abs(prob) > 0.5 order by rand() limit 10000;'

cmd = "select c.galcount, -6.0*m.probaEll -3.0*m.probaS0+4.0*m.probaSab+8.0*m.probaScd, u.flag , x.m_tot- d.kcorr_r - c.extinction_r-d.dismod as mag_g,y.m_tot- d.kcorr_r - c.extinction_r-d.dismod as mag_r,z.m_tot- d.kcorr_r - c.extinction_r-d.dismod as mag_i, x.n_bulge as n_g, y.n_bulge as n_r,z.n_bulge as n_i, x.Hrad_corr*d.kpc_per_arcsec as rad_g,y.Hrad_corr*d.kpc_per_arcsec as rad_r,z.Hrad_corr*d.kpc_per_arcsec as rad_i, x.BT as BT_r,y.BT as BT_i,z.BT as BT_z from g_band_serexp as x ,r_band_serexp as y ,i_band_serexp as z, DERT as d, M2010 as m , CAST as c, Flags_optimize as u where c.galcount = m.galcount and x.galcount = c.galcount and c.galcount = d.galcount and c.galcount = y.galcount and c.galcount = z.galcount and d.kcorr_r > -900 and c.galcount = u.galcount and u.ftype = 'u' and u.band = 'r' and u.model = 'serexp' and u.flag>=0 order by rand() limit 10000;"


data = cursor.get_data(cmd)

gal = {}
gal['galcount'] = np.array(data[0], dtype = int)
gal['flag'] = np.array(data[2], dtype = int)
gal['ttype'] = np.array(data[1], dtype = float)
names = ['absmag', 'n', 'rad', 'BT']
count = 2
print len(data)
for name in names:
    if not gal.has_key(name):
        gal[name] = {}
    for band in 'gri':
        count+=1
        gal[name][band] = np.array(data[count], dtype = float)

pl.subplot(1,1,1)
pl.scatter(gal['absmag']['i'],gal['absmag']['g'] - gal['absmag']['r'], c =gal['ttype'] , s = 3, edgecolor = 'none', vmin=-8, vmax=10.0, cmap = cm.jet_r)
pl.xlim(-27, -16)
pl.ylim(-0.20, 2.2)
pl.xlabel('M$_i$')
pl.ylabel('M$_g$-M$_r$')
pl.title('colored by ttype')
pl.colorbar()

pl.show()
