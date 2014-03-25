from mysql_class import *
import os
import sys
import pylab as pl
import numpy as np

from utilities import *
from faber_jackson import *
from kormendy import *
from fund_plane import *
#from photo_fund_plane import *

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

cmd = "select a.galcount, c.veldisp, c.veldispErr, a.m_tot - d.kcorr_r - c.extinction_r-d.dismod, a.m_bulge_err, a.n_bulge, a.n_bulge_err, a.Hrad_corr*d.kpc_per_arcsec, a.r_bulge_err*d.dismod, ifnull(a.BT, -999) from Flags_optimize as u, r_band_serexp as a , DERT as d , M2010 as m , CAST as c where a.galcount = m.galcount and a.galcount = c.galcount and a.galcount = d.galcount and c.galcount = u.galcount and u.ftype = 'u' and u.band = 'r' and u.model = 'serexp' and u.flag>=0 and -6.0*m.probaEll -3.0*m.probaS0+4.0*m.probaSab+8.0*m.probaScd<0 and c.veldisp < 400.0 and c.veldisp > -1 and d.kcorr_r > -900 and a.m_tot>0 and a.Hrad_corr*d.kpc_per_arcsec>0  and u.flag&pow(2,1) order by a.galcount limit 10000;" #and a.m_tot - d.kcorr_r - c.extinction_r-d.dismod +4*log10(a.Hrad_corr*d.kpc_per_arcsec)<-22 

galcount, veldisp, veldispErr, Absmag, magErr, nser, nser_err, Rkpc, Rkpc_err, BT = cursor.get_data(cmd)

galcount = np.array(galcount, dtype = int)
veldisp = np.array(veldisp, dtype = float)
veldispErr = np.array(veldispErr, dtype = float)
Absmag = np.array(Absmag, dtype = float)
magErr = np.array(magErr, dtype = float)
nser = np.array(nser, dtype = float)
nser_err = np.array(nser_err, dtype = float)
Rkpc = np.array(Rkpc, dtype = float)
Rkpc_err = np.array(Rkpc_err, dtype = float)
BT = np.array(BT, dtype = float)

pl.scatter(Absmag,np.log10(Rkpc),  s = 3.0, edgecolor = 'none', c = BT, vmin=0.0, vmax = 1.0)
pl.ylim((-2.0,2.5))
pl.xlim((-14.0, -27.0))
pl.xlabel('r-band Absmag')
pl.ylabel('Size(kpc)')

print np.log10(Rkpc)
print Absmag
print min(np.log10(Rkpc))
print max(np.log10(Rkpc))
print min(Absmag)
print max(Absmag)

pl.savefig('./size_mag.eps') 

Lgal, Lerr = absmag_to_LSun(Absmag,magErr, 'r')
for a in zip(galcount, Absmag, Lgal, Rkpc):
    if np.isinf(a[2]) or np.isnan(a[2]) or np.isinf(a[3]) or np.isnan(a[3]):
        print a
print Absmag
print Lgal
axes = faber_jackson(veldisp, veldispErr, Lgal, Lerr, nser)
pl.savefig('./faber_jackson.eps')
pl.close('all')

axes = kormendy(Rkpc, Rkpc_err, Lgal, Lerr, nser)
pl.savefig('./kormendy.eps')
pl.close('all')

axes = fund_plane(Rkpc, Rkpc_err, veldisp, veldispErr, Lgal, Lerr, nser)
pl.savefig('./fund_plane.eps')
pl.close('all')

#axes = photo_fund_plane(Rkpc, Rkpc_err, nser, nser_err, Lgal, Lerr, BT)
#pl.savefig('/home/ameert/photo_fund_plane.eps')
#pl.close('all')





