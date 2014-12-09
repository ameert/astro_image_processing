import os
import numpy as np

os.system("""mysql -u pymorph -ppymorph catalog -e "select a.galcount, a.SDSSLOGMSTAR, a.ABSMAGTOT, b.bt, b.m_tot - c.extinction_r - d.kcorr_r - d.dismod, b.hrad_corr,  b.m_bulge - c.extinction_r - d.kcorr_r - d.dismod,  b.n_bulge, IFNULL(b.r_bulge*d.kpc_per_arcsec*sqrt(b.ba_bulge),-999),  b.m_disk - c.extinction_r - d.kcorr_r - d.dismod,  1.0, IFNULL(b.r_disk*d.kpc_per_arcsec*sqrt(b.ba_disk),-999), -6.0*m.probaEll -3.0*m.probaS0+4.0*m.probaSab+8.0*m.probaScd, u.flag, x.m_tot - c.extinction_r - d.kcorr_r - d.dismod,  x.n_bulge, IFNULL(x.r_bulge*d.kpc_per_arcsec*sqrt(x.ba_bulge),-999) from M2010 as m, Flags_optimize as u, SSDR6 as a, CAST as c, DERT as d, r_band_serexp as b, r_band_ser as x where c.galcount = m.galcount and  c.galcount = x.galcount and a.galcount = c.galcount and c.galcount = b.galcount and c.galcount = d.galcount and c.galcount = u.galcount and u.ftype = 'u' and u.band = 'r' and u.model = 'serexp' and u.flag>=0;" > test.txt """)  

galcount, SDSSLOGMSTAR, ABSMAGTOT, BT, m_tot, r_tot, m_bulge, n_bulge, r_bulge,  m_disk, n_disk, r_disk, ttype, flags, nser, rser, mser = np.loadtxt('./test.txt', skiprows=1, unpack=True)

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


Mstar = 10**SDSSLOGMSTAR
log_Mstar_bulge = np.log10(Mstar * 10**(-0.4*(m_bulge- ABSMAGTOT)))
log_Mstar_tot = np.log10(Mstar * 10**(-0.4*(m_tot- ABSMAGTOT)))

np.savez('SSDR6_data.npz', BT=BT, mtot=m_tot, r_tot=r_tot, n_bulge=n_bulge, 
         r_bulge=r_bulge,  ttype=ttype, flags=flags,log_Mstar_tot=log_Mstar_tot,
         log_Mstar_bulge=log_Mstar_bulge, galcount = galcount)
