from mysql_class import *
import numpy as np
from plot_sample import *
import scipy.stats as stats
from ks_test import *

dba = 'simard'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)

cmd = 'select b.galcount, b.z, a.V_max, b.petromag_r - b.extinction_r - f.kcorr_r - f.dismod, b.petromag_r - b.extinction_r, b.petroR50_r, b.petromag_r  from simard_sample as a, catalog.CAST as b , catalog.DERT as f where f.galcount = b.galcount and  b.galcount = a.galcount and a.V_max > 0;'

galcount, z, V_max, absmag, petromag_r, halflight_rad,ucorr_mag = cursor.get_data(cmd)

galcount1 = np.array(galcount)
z1 = np.array(z)
V_max1 = np.array(V_max)
petromag_r1 = np.array(petromag_r)
halflight_rad1 = np.array(halflight_rad)
absmag1 = np.array(absmag)
ucorr_mag1 = np.array(ucorr_mag)

surf_bright1 = -2.5*np.log10(10**(-0.4*ucorr_mag1)/(2*np.pi*halflight_rad1**2.0))

cmd = 'select b.galcount, b.z, a.V_max, b.petromag_r - b.extinction_r - f.kcorr_r - f.dismod, b.petromag_r - b.extinction_r, b.petroR50_r, b.petromag_r  from simard_sample as a, catalog.CAST as b , catalog.DERT as f, catalog.r_lackner_ser as d where f.galcount = b.galcount and  b.galcount = a.galcount and  b.galcount = d.galcount and a.V_max > 0;'

galcount, z, V_max, absmag, petromag_r, halflight_rad,ucorr_mag = cursor.get_data(cmd)

galcount3 = np.array(galcount)
z3 = np.array(z)
V_max3 = np.array(V_max)
petromag_r3 = np.array(petromag_r)
halflight_rad3 = np.array(halflight_rad)
absmag3 = np.array(absmag)
ucorr_mag3 = np.array(ucorr_mag)

surf_bright3 = -2.5*np.log10(10**(-0.4*ucorr_mag3)/(2*np.pi*halflight_rad3**2.0))

z = [z1,z3]
absmag = [absmag1, absmag3]
petromag_r = [petromag_r1,petromag_r3]
halflight_rad =[halflight_rad1,halflight_rad3]
surf_bright = [surf_bright1,surf_bright3]
V_max = [V_max1, V_max3]

plot_sample(z, absmag, petromag_r, halflight_rad, surf_bright, V_max, plot_stem = './lackner_sample', colors = ['k','r'])

plot_2d_sample(petromag_r1, halflight_rad1, plot_stem = './CAST_sample')
plot_2d_sample(petromag_r3, halflight_rad3, plot_stem = './lackner_sample')


print 'raw absmag'
print stats.ks_2samp(absmag1, absmag3)
print 'appmag'
print stats.ks_2samp(petromag_r1, petromag_r3)
print 'rad'
print stats.ks_2samp(halflight_rad1, halflight_rad3)
print 'mu'
print stats.ks_2samp(surf_bright1, surf_bright3)
print 'z'
print stats.ks_2samp(z1, z3)

#def ks_weighted(absmag1, vmax1, absmag2, vmax2):
#    Vw1 = 1.0/vmax1
#    Vw2 = 1.0/vmax2

#    n1, bins1, patches1 = pl.hist(absmag1, bins = 180, weights = Vw1/np.sum(Vw1), range=(-25,-16), normed = True, log = True)
      
#    pl.show()

#    return

ks_weighted(absmag1, V_max1,absmag3, V_max3)


