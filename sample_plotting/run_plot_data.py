from mysql.mysql_class import *
import numpy as np
from plot_sample_data import *
import scipy.stats as stats
#from ks_test import *

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)

cmd = 'select b.z, f.Vmax, b.petromag_r - b.extinction_r - f.kcorr_r - f.dismod, b.petromag_r - b.extinction_r, b.petroR50_r, b.petromag_r  from catalog.CAST as b , catalog.DERT as f where f.galcount = b.galcount and f.Vmax > 0;'

z, V_max, absmag, petromag_r, halflight_rad,ucorr_mag = cursor.get_data(cmd)

z1 = np.array(z)
V_max1 = np.array(V_max)
petromag_r1 = np.array(petromag_r)
halflight_rad1 = np.array(halflight_rad)
absmag1 = np.array(absmag)
ucorr_mag1 = np.array(ucorr_mag)

surf_bright1 = -2.5*np.log10(10**(-0.4*ucorr_mag1)/(2*np.pi*halflight_rad1**2.0))

cmd = 'select b.redshift, b.Vmax, b.petromag_r - b.extinction_r - b.kcorr_r - b.dismod, b.petromag_r - b.extinction_r, b.petroR50_r, b.petromag_r  from catalog.CAST_raw as b where b.Vmax > 0 and b.redshift >0.005 and b.disqual_flag <=3;'#(b.disqual_flag & 0) = 0 and (b.disqual_flag & 16) = 0 and (b.disqual_flag & 8) = 0 ;'

#z, V_max, absmag, petromag_r, halflight_rad,ucorr_mag = cursor.get_data(cmd)

z2 = np.array(z)
V_max2 = np.array(V_max)
petromag_r2 = np.array(petromag_r)
halflight_rad2 = np.array(halflight_rad)
absmag2 = np.array(absmag)
ucorr_mag2 = np.array(ucorr_mag)

surf_bright2 = -2.5*np.log10(10**(-0.4*ucorr_mag2)/(2*np.pi*halflight_rad2**2.0))

z = [z2]#,z1]
absmag = [absmag2]#, absmag1]
petromag_r = [petromag_r2]#,petromag_r1]
halflight_rad =[halflight_rad2]#,halflight_rad1]
surf_bright = [surf_bright2]#,surf_bright1]
V_max = [V_max2]#, V_max1]

plot_sample(z, absmag, petromag_r, halflight_rad, surf_bright, V_max, plot_stem = './data_cmp', colors = ['k','r'])

print 'raw absmag'
#print stats.ks_2samp(absmag1, absmag2)
print 'Vmax absmag'
#ks_weighted(absmag1, V_max1,absmag2, V_max2)
print 'appmag'
#print stats.ks_2samp(petromag_r1, petromag_r2)
print 'rad'
#print stats.ks_2samp(halflight_rad1, halflight_rad2)
print 'mu'
#print stats.ks_2samp(surf_bright1, surf_bright2)
print 'z'
#print stats.ks_2samp(z1, z2)
