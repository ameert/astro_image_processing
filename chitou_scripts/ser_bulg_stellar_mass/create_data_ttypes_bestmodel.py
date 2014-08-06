import os
import numpy as np

os.system("""mysql -u pymorph -ppymorph catalog -e "select b.galcount, b.m_tot - c.extinction_r, b.hrad_corr,  b.BT, b.m_bulge - c.extinction_r,  b.n_bulge, IFNULL(b.r_bulge*sqrt(b.ba_bulge),-999),  b.m_disk - c.extinction_r,  IFNULL(b.r_disk*sqrt(b.ba_disk),-999),d.kcorr_r + d.dismod, d.kpc_per_arcsec, -4.5775*m.probaEll -2.35723*m.probaS0+2.48028*m.probaSab+6.0815*m.probaScd, u.flag from M2010 as m, Flags_optimize as u, CAST as c, DERT as d, r_band_serexp as b where c.galcount = m.galcount and c.galcount = b.galcount and c.galcount = d.galcount and c.galcount = u.galcount and u.ftype = 'u' and u.band = 'r' and u.model = 'serexp' and u.flag>=0;" > test.txt """)  

galcount, m_tot, r_tot, BT, m_bulge, n_bulge, r_bulge,  m_disk, r_disk, mcorr, kpc_per_arcsec, ttype, flags = np.loadtxt('./test.txt', skiprows=1, unpack=True)

os.system('/bin/rm test.txt')

flags = flags.astype(int)

np.savez('best_model_data.npz', galcount=galcount,mtot=m_tot, r_tot=r_tot, 
         BT=BT, m_bulge=m_bulge,n_bulge=n_bulge, r_bulge=r_bulge,
         m_disk=m_disk, r_disk=r_disk, 
         mcorr=mcorr, kpc_per_arcsec=kpc_per_arcsec,
         ttype=ttype, flags=flags)
