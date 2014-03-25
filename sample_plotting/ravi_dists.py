from mysql_class import *
import numpy as np
from plot_sample import *
import scipy.stats as stats
from ks_test import *

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)


cmd = 'select b.galcount, b.z, a.V_max, b.petromag_r - b.extinction_r - f.kcorr_r - f.dismod, b.petromag_r - b.extinction_r, b.petroR50_r, b.petromag_r  from simard_sample as a, catalog.CAST as b , catalog.DERT as f  where f.galcount = b.galcount and b.galcount = a.galcount and a.V_max > 0 and b.z < 0.1;'

galcount, z, V_max, absmag, petromag_r, halflight_rad,ucorr_mag = cursor.get_data(cmd)

galcount2 = np.array(galcount)
z2 = np.array(z)
V_max2 = np.array(V_max)
petromag_r2 = np.array(petromag_r)
halflight_rad2 = np.array(halflight_rad)
absmag2 = np.array(absmag)
ucorr_mag2 = np.array(ucorr_mag)

surf_bright2 = -2.5*np.log10(10**(-0.4*ucorr_mag2)/(2*np.pi*halflight_rad2**2.0))

n, bins, patches = pl.hist(absmag2, bins = 18, log = True, range=(-25,-16), normed = True, color = 'b', linestyle = 'solid', histtype = 'step', label = 'incomplete')

V_weight = 1.0/V_max2
n2, bins2, patches2 = pl.hist(absmag2, bins = 18, weights = V_weight/np.sum(V_weight), range=(-25,-16), log = True, color = 'g', linestyle = 'solid', histtype = 'step', normed = True, label='complete')

pl.legend(loc=4)
pl.show()
