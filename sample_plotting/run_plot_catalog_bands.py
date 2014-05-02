from mysql.mysql_class import *
import numpy as np
from plot_sample_data import *
import scipy.stats as stats
#from ks_test import *

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)


def get_alldat(band):
    cmd = 'select b.z, f.Vmax, b.petromag_{band} - b.extinction_{band} - f.kcorr_{band} - f.dismod, b.petromag_{band} - b.extinction_{band}, b.petroR50_{band}, b.petromag_{band}  from catalog.CAST as b , catalog.DERT as f where f.galcount = b.galcount and f.Vmax > 0;'.format(band=band)

    z, V_max, absmag, petromag, halflight_rad,ucorr_mag = cursor.get_data(cmd)

    z1 = np.array(z)
    V_max1 = np.array(V_max)
    petromag_1 = np.array(petromag)
    halflight_rad1 = np.array(halflight_rad)
    absmag1 = np.array(absmag)
    ucorr_mag1 = np.array(ucorr_mag)

    surf_bright1 = -2.5*np.log10(10**(-0.4*ucorr_mag1)/(2*np.pi*halflight_rad1**2.0))
    
    return z1, V_max1, petromag_1, halflight_rad1, absmag1, surf_bright1

z = []
absmag = []
petromag = []
halflight_rad =[]
surf_bright = []
V_max = []

ztmp, vmaxtmp, petrotmp, hradtmp, abtmp, sbtmp  = get_alldat('g')
z.append(ztmp)
absmag.append(abtmp)
petromag.append(petrotmp)
halflight_rad.append(hradtmp)
surf_bright.append(sbtmp)
V_max.append(vmaxtmp)
ztmp, vmaxtmp, petrotmp, hradtmp, abtmp, sbtmp  = get_alldat('r')
z.append(ztmp)
absmag.append(abtmp)
petromag.append(petrotmp)
halflight_rad.append(hradtmp)
surf_bright.append(sbtmp)
V_max.append(vmaxtmp)
ztmp, vmaxtmp, petrotmp, hradtmp, abtmp, sbtmp  = get_alldat('i')
z.append(ztmp)
absmag.append(abtmp)
petromag.append(petrotmp)
halflight_rad.append(hradtmp)
surf_bright.append(sbtmp)
V_max.append(vmaxtmp)

print z, absmag, petromag, halflight_rad, surf_bright, V_max

plot_sample(z, absmag, petromag, halflight_rad, surf_bright, V_max, plot_stem = './data_cmp', colors = ['g','r','k'])

#print 'raw absmag'
#print stats.ks_2samp(absmag1, absmag2)
#print 'Vmax absmag'
#ks_weighted(absmag1, V_max1,absmag2, V_max2)
#print 'appmag'
#print stats.ks_2samp(petromag_r1, petromag_r2)
#print 'rad'
#print stats.ks_2samp(halflight_rad1, halflight_rad2)
#print 'mu'
#print stats.ks_2samp(surf_bright1, surf_bright2)
#print 'z'
#print stats.ks_2samp(z1, z2)
