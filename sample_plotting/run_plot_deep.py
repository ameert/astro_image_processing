from mysql.mysql_class import *
import numpy as np
from plot_sample import *
import scipy.stats as stats

import sys
sys.path.append('/home/ameert/git_projects/alans-image-processing-pipeline/chitou_scripts/')
from ks_test import *


dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)

cmd = 'select b.galcount, b.z, f.Vmax, b.petromag_r - b.extinction_r - f.kcorr_r - f.dismod, b.petromag_r - b.extinction_r, b.petroR50_r, b.petromag_r  from catalog.CAST as b , catalog.DERT as f where f.galcount = b.galcount and f.Vmax > 0;'

galcount, z, Vmax, absmag, petromag_r, halflight_rad,ucorr_mag = cursor.get_data(cmd)

galcount1 = np.array(galcount)
z1 = np.array(z)
Vmax1 = np.array(Vmax)
petromag_r1 = np.array(petromag_r)
halflight_rad1 = np.array(halflight_rad)
absmag1 = np.array(absmag)
ucorr_mag1 = np.array(ucorr_mag)

surf_bright1 = -2.5*np.log10(10**(-0.4*ucorr_mag1)/(2*np.pi*halflight_rad1**2.0))

cmd = 'select b.galcount, b.z, f.Vmax, b.petromag_r - b.extinction_r - f.kcorr_r - f.dismod, b.petromag_r - b.extinction_r, b.petroR50_r, b.petromag_r  from CAST as b , DERT as f, r_band_badfits as x left join r_deep_badfits as z on x.galcount=z.galcount  where b.galcount=x.galcount and f.galcount = b.galcount and f.Vmax > 0 and ((x.is_polluted = 0 and x.is_fractured = 0 ) or (z.is_fractured = 0 and z.is_polluted=0 and z.galcount is not null));'

galcount, z, Vmax, absmag, petromag_r, halflight_rad,ucorr_mag = cursor.get_data(cmd)

galcount2 = np.array(galcount)
z2 = np.array(z)
Vmax2 = np.array(Vmax)
petromag_r2 = np.array(petromag_r)
halflight_rad2 = np.array(halflight_rad)
absmag2 = np.array(absmag)
ucorr_mag2 = np.array(ucorr_mag)

surf_bright2 = -2.5*np.log10(10**(-0.4*ucorr_mag2)/(2*np.pi*halflight_rad2**2.0))

cmd = 'select b.galcount, b.z, f.Vmax, b.petromag_r - b.extinction_r - f.kcorr_r - f.dismod, b.petromag_r - b.extinction_r, b.petroR50_r, b.petromag_r  from CAST as b , DERT as f, r_band_badfits as x left join r_deep_badfits as z on x.galcount=z.galcount  where b.galcount=x.galcount and f.galcount = b.galcount and f.Vmax > 0 and (x.is_polluted = 1 and x.is_fractured = 0 and (z.is_fractured = 1 or z.is_polluted=1));'

galcount, z, Vmax, absmag, petromag_r, halflight_rad,ucorr_mag = cursor.get_data(cmd)

galcount3 = np.array(galcount)
z3 = np.array(z)
Vmax3 = np.array(Vmax)
petromag_r3 = np.array(petromag_r)
halflight_rad3 = np.array(halflight_rad)
absmag3 = np.array(absmag)
ucorr_mag3 = np.array(ucorr_mag)

surf_bright3 = -2.5*np.log10(10**(-0.4*ucorr_mag3)/(2*np.pi*halflight_rad3**2.0))

cmd = 'select b.galcount, b.z, f.Vmax, b.petromag_r - b.extinction_r - f.kcorr_r - f.dismod, b.petromag_r - b.extinction_r, b.petroR50_r, b.petromag_r  from CAST as b , DERT as f, r_band_badfits as x left join r_deep_badfits as z on x.galcount=z.galcount  where b.galcount=x.galcount and f.galcount = b.galcount and f.Vmax > 0 and (x.is_fractured = 1 and (z.is_fractured = 1 or z.galcount is null));'

galcount, z, Vmax, absmag, petromag_r, halflight_rad,ucorr_mag = cursor.get_data(cmd)

galcount4 = np.array(galcount)
z4 = np.array(z)
Vmax4 = np.array(Vmax)
petromag_r4 = np.array(petromag_r)
halflight_rad4 = np.array(halflight_rad)
absmag4 = np.array(absmag)
ucorr_mag4 = np.array(ucorr_mag)

surf_bright4 = -2.5*np.log10(10**(-0.4*ucorr_mag4)/(2*np.pi*halflight_rad4**2.0))

z = [z1,z2,z3,z4]
absmag = [absmag1,absmag2, absmag3, absmag4]
petromag_r = [petromag_r1,petromag_r2,petromag_r3,petromag_r4]
halflight_rad =[halflight_rad1,halflight_rad2,halflight_rad3,halflight_rad4]
surf_bright = [surf_bright1,surf_bright2,surf_bright3,surf_bright4]
Vmax = [Vmax1, Vmax2, Vmax3, Vmax4]

plot_sample(z, absmag, petromag_r, halflight_rad, surf_bright, Vmax, plot_stem = './sample', colors = ['k','r','g','b','m'])

print 'raw absmag'
print stats.ks_2samp(absmag1, absmag2)
print stats.ks_2samp(absmag1, absmag3)
print stats.ks_2samp(absmag1, absmag4)
print 'appmag'
print stats.ks_2samp(petromag_r1, petromag_r2)
print stats.ks_2samp(petromag_r1, petromag_r3)
print stats.ks_2samp(petromag_r1, petromag_r4)
print 'rad'
print stats.ks_2samp(halflight_rad1, halflight_rad2)
print stats.ks_2samp(halflight_rad1, halflight_rad3)
print stats.ks_2samp(halflight_rad1, halflight_rad4)
print 'mu'
print stats.ks_2samp(surf_bright1, surf_bright2)
print stats.ks_2samp(surf_bright1, surf_bright3)
print stats.ks_2samp(surf_bright1, surf_bright4)
print 'z'
print stats.ks_2samp(z1, z2)
print stats.ks_2samp(z1, z3)
print stats.ks_2samp(z1, z4)

#def ks_weighted(absmag1, vmax1, absmag2, vmax2):
#    Vw1 = 1.0/vmax1
#    Vw2 = 1.0/vmax2

#    n1, bins1, patches1 = pl.hist(absmag1, bins = 180, weights = Vw1/np.sum(Vw1), range=(-25,-16), normed = True, log = True)
      
#    pl.show()

#    return

ks_weighted(absmag1, Vmax1,absmag2, Vmax2)
ks_weighted(absmag1, Vmax1,absmag3, Vmax3)
ks_weighted(absmag1, Vmax1,absmag4, Vmax4)

