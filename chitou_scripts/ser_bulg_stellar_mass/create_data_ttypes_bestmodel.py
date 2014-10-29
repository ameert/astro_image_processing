import os
import numpy as np

os.system("""mysql -u pymorph -ppymorph catalog -e "select b.galcount, b.m_tot - c.extinction_r, b.hrad_corr,  b.BT, b.m_bulge - c.extinction_r,  b.n_bulge, IFNULL(b.r_bulge*sqrt(b.ba_bulge),-999),  b.m_disk - c.extinction_r,  IFNULL(b.r_disk*sqrt(b.ba_disk),-999),d.kcorr_r + d.dismod, d.kpc_per_arcsec, -4.5775*m.probaEll -2.35723*m.probaS0+2.48028*m.probaSab+6.0815*m.probaScd, u.flag, c.z, c.petromag_g-c.petromag_r-c.extinction_g+c.extinction_r-d.kcorr_g+d.kcorr_r, petroR90_r/petroR50_r from M2010 as m, Flags_catalog as u, CAST as c, DERT as d, r_band_serexp as b where c.galcount = m.galcount and c.galcount = b.galcount and c.galcount = d.galcount and c.galcount = u.galcount and u.ftype = 'u' and u.band = 'r' and u.model = 'serexp' and u.flag>=0;" > test.txt """)  

#gz2_flags as gz2 
# c.galcount=gz2.galcount
#and gz2.t03_bar>0
# and gz2.t03_no_bar>0


galcount, m_tot, r_tot, BT, m_bulge, n_bulge, r_bulge,  m_disk, r_disk, mcorr, kpc_per_arcsec, ttype, flags,z,grcolor, concentration = np.loadtxt('./test.txt', skiprows=1, unpack=True)

n_disk = np.ones_like(n_bulge)

os.system('/bin/rm test.txt')

flags = flags.astype(int)

galcount = galcount.astype(int)

BT = np.where( flags&2**6>0, 1-BT, BT)
BT = np.where( flags&2**7>0, 1-BT, BT)
BT = np.where( flags&2**13>0, 1-BT, BT)

tmp_m_bulge = m_bulge[:]
tmp_m_disk = m_disk[:]
tmp_r_bulge = r_bulge[:]
tmp_r_disk = r_disk[:]
tmp_n_bulge = n_bulge[:]
tmp_n_disk = n_disk[:]

m_bulge = np.where( flags&2**6>0, tmp_m_disk, m_bulge)
m_bulge = np.where( flags&2**7>0, tmp_m_disk, m_bulge)
m_bulge = np.where( flags&2**13>0, tmp_m_disk, m_bulge)

m_disk = np.where( flags&2**6>0, tmp_m_bulge, m_disk)
m_disk = np.where( flags&2**7>0, tmp_m_bulge, m_disk)
m_disk = np.where( flags&2**13>0, tmp_m_bulge, m_disk)

r_bulge = np.where( flags&2**6>0, tmp_r_disk*1.67, r_bulge)
r_bulge = np.where( flags&2**7>0, tmp_r_disk*1.67, r_bulge)
r_bulge = np.where( flags&2**13>0, tmp_r_disk*1.67, r_bulge)

r_disk = np.where( flags&2**6>0, tmp_r_bulge, r_disk)
r_disk = np.where( flags&2**7>0, tmp_r_bulge, r_disk)
r_disk = np.where( flags&2**13>0, tmp_r_bulge, r_disk)

n_bulge = np.where( flags&2**6>0, tmp_n_disk, n_bulge)
n_bulge = np.where( flags&2**7>0, tmp_n_disk, n_bulge)
n_bulge = np.where( flags&2**13>0, tmp_n_disk, n_bulge)

n_disk = np.where( flags&2**6>0, tmp_n_bulge, n_disk)
n_disk = np.where( flags&2**7>0, tmp_n_bulge, n_disk)
n_disk = np.where( flags&2**13>0, tmp_n_bulge, n_disk)

np.savez('best_model_data.npz', galcount=galcount,mtot=m_tot, 
         r_tot=r_tot, 
         BT=BT, m_bulge=m_bulge,n_bulge=n_bulge, r_bulge=r_bulge,
         m_disk=m_disk, r_disk=r_disk, 
         mcorr=mcorr, kpc_per_arcsec=kpc_per_arcsec,
         ttype=ttype, flags=flags, z=z, grcolor=grcolor, 
         concentration=concentration)
