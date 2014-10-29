import numpy as np
import os
import pylab as pl
from mysql_class import *
from cosmocal import *

usr = 'pymorph'
pwd = 'pymorph'
dba = 'catalog'

cursor = cursor = mysql_connect(dba, usr, pwd)

cmd = 'select a.galcount, a.devmag_r, a.extinction_r, b.dismod, b.kcorr_r, a.z, a.devrad_r, a.devrad_g, a.devab_r, a.devab_g, kpc_per_arcsec from CAST as a, DERT as b, M2010 as c where a.galcount = b.galcount and a.galcount = c.galcount;'

galcount, mag, extinction, dismod, kcorr,z, devrad_r, devrad_g, devab_r, devab_g, kpc_per_arcsec = cursor.get_data(cmd)

galcount = np.array(galcount, dtype = int)
mag = np.array(mag, dtype = float)
extinction= np.array(extinction, dtype = float)
dismod= np.array(dismod, dtype = float)
kcorr= np.array(kcorr, dtype = float)
devrad_r= np.array(devrad_r, dtype = float)
devrad_g= np.array(devrad_g, dtype = float)
devab_r= np.array(devab_r, dtype = float)
devab_g= np.array(devab_g, dtype = float)
z= np.array(z, dtype = float)
kpc_per_arcsec= np.array(kpc_per_arcsec, dtype = float)
 
r_sdss = devrad_r*np.sqrt(devab_r)
g_sdss = devrad_g*np.sqrt(devab_g)

mag = mag + 0.024279 - r_sdss/71.1734 + (r_sdss/26.5)**2.0
r_r = r_sdss + 0.181571-r_sdss/4.5213 + (r_sdss/3.9165)**2.0
r_g = g_sdss + 0.181571-g_sdss/4.5213 + (g_sdss/3.9165)**2.0

absmag = mag - dismod - kcorr + 0.9*z

r_kpc = r_r * kpc_per_arcsec
g_kpc = r_g * kpc_per_arcsec

print absmag
print r_kpc

mag_line = np.arange(-24, -18, 0.2)
rad_line = 0.020*mag_line*mag_line + 0.63*mag_line + 4.72

print mag_line
print rad_line

pl.scatter(absmag, np.log10(r_kpc), edgecolor = 'none', s = 2)
pl.plot(mag_line, rad_line, 'r-')
pl.xlim((-18, -25))
pl.ylim((-0.5,1.5))
pl.show()

