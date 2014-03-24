from mysql_class import *
import pylab as pl
import numpy as np


cursor = mysql_connect('catalog','pymorph','pymorph')

cmd = 'select a.galcount, a.n, a.re_kpc, a.hrad_pix_corr*a.re_kpc/a.re_pix from CAST as c, full_dr7_r_ser as a  where a.Ie - a.magzp-c.aa_r -c.kk_r*c.airmass_r -a.dis_modu < -24.0 and a.galcount = c.galcount;'


dnames = ['galcount', 'n', 're_kpc', 'hrad_kpc']
data = cursor.get_data(cmd)

data_dict = {}
for a, d in zip(data, dnames):
    data_dict[d] = np.array(a, dtype = float)

print min(data_dict['n']), max(data_dict['n'])
print min(data_dict['re_kpc']), max(data_dict['re_kpc'])
print min(data_dict['hrad_kpc']), max(data_dict['hrad_kpc'])
 
pl.subplot(2,2,1)
pl.hist(data_dict['n'], bins = 32, range = (0,8))

pl.subplot(2,2,2)
pl.hist(data_dict['re_kpc'], bins = 80, range = (0, 400))

pl.subplot(2,2,3)
pl.hist(data_dict['hrad_kpc'], bins = 80, range = (0, 400))
pl.show()




