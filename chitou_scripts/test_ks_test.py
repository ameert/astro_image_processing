from mysql_class import *
import numpy as np
from plot_sample import *
from ks_test import *


dba = 'simard'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)

cmd = "select b.galcount, b.z, a.V_max, b.petromag_r - b.extinction_r - f.kcorr_r - f.dismod, b.petromag_r - b.extinction_r, b.petroR50_r, b.petromag_r  from simard_sample as a, catalog.CAST as b, simulations.sim_input as c , catalog.DERT as f where f.galcount = b.galcount and  b.galcount = a.galcount and b.galcount = c.galcount and a.V_max > 0 and c.model = 'ser';"

galcount, z, V_max, absmag, petromag_r, halflight_rad,ucorr_mag = cursor.get_data(cmd)

galcount3 = np.array(galcount)
z3 = np.array(z)
V_max3 = np.array(V_max)
petromag_r3 = np.array(petromag_r)
halflight_rad3 = np.array(halflight_rad)
absmag3 = np.array(absmag)
ucorr_mag3 = np.array(ucorr_mag)

surf_bright3 = -2.5*np.log10(10**(-0.4*ucorr_mag3)/(2*np.pi*halflight_rad3**2.0))

V_weight = 1.0/V_max3
n, bins, patches = pl.hist(absmag3, bins = 18, weights = V_weight/np.sum(V_weight), range=(-25,-16), color = 'k', linestyle = 'solid', histtype = 'step', cumulative = True)
pl.xlim((-16,-25))

#n,bins,patches= pl.hist(petromag_r3, bins = 10, range=(13,18), weights =  np.ones_like(petromag_r3)/float(len(petromag_r3)),   histtype = 'step', color = 'b', cumulative = True)

#bin_ends, wECDF = weighted_ECDF(absmag3, np.ones_like(petromag_r3), bins = 100, dat_range=(13,18))
bin_ends, wECDF = weighted_ECDF(absmag3, V_weight, bins = 1000, dat_range=(-25,-16))

pl.plot(bin_ends, wECDF, 'g--')

pl.show()

print n, bins
print wECDF, bin_ends
