import os
import numpy as np

os.system("""mysql -u pymorph -ppymorph catalog -e "select b.galcount, b.bt, b.m_tot - c.extinction_r , b.hrad_corr,  b.m_bulge - c.extinction_r ,  b.n_bulge, IFNULL(b.r_bulge*sqrt(b.ba_bulge),-999),b.ba_bulge,  b.m_disk - c.extinction_r ,  b.ba_disk, IFNULL(b.r_disk*sqrt(b.ba_disk),-999), -4.5775*m.probaEll -2.35723*m.probaS0+2.48028*m.probaSab+6.0815*m.probaScd, u.flag,d.kpc_per_arcsec, d.kcorr_r - d.dismod from M2010 as m, Flags_catalog as u, CAST as c, DERT as d, r_band_serexp as b where c.galcount = m.galcount and c.galcount = b.galcount and c.galcount = d.galcount and c.galcount = u.galcount and u.ftype = 'u' and u.band = 'r' and u.model = 'serexp' and u.flag>=0;" > test.txt """)  

data = np.loadtxt('./test.txt', skiprows=1, unpack=True)
names = ['galcount', 'BT', 'm_tot', 'r_tot', 'm_bulge', 'n_bulge', 
         'r_bulge', 'ba_bulge', ' m_disk', 'ba_disk', 'r_disk', 
         'ttype', 'flags','kpc_per_arcsec','dismod']
data = dict([a for a in zip(names,data)])
os.system('/bin/rm test.txt')

data['flags'] = data['flags'].astype(int)
data['galcount'] = data['galcount'].astype(int)

np.savez('ba_data_serexp.npz', **data)
