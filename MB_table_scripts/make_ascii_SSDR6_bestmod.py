from astro_image_processing.mysql import *
import os
import itertools
import pyfits
import datetime
import sys

# r_band_flagmodel constructed by 
#mysql> create table r_band_flagmodel like r_band_serexp;
#mysql> insert into r_band_flagmodel select a.* from r_band_serexp as a, bestmod as b where a.galcount = b.galcount and b.band = 'r' and b.best_model ='serexp';
#mysql> insert into r_band_flagmodel select a.* from r_band_devexp as a, bestmod as b where a.galcount = b.galcount and b.band = 'r' and b.best_model ='devexp';
#mysql> insert into r_band_flagmodel select a.* from r_band_ser as a, bestmod as b where a.galcount = b.galcount and b.band = 'r' and b.best_model ='ser';
#mysql> insert ignore into r_band_flagmodel (galcount) select galcount from CAST;

dba = 'catalog'
pwd = 'pymorph'
usr = 'pymorph'

stem = 'DR6_newt2'

cursor = mysql_connect(dba, usr, pwd)

cmd = """select ifnull(f.ra_gal, z.ra_gal), ifnull(f.dec_gal, z.dec_gal), 
ifnull(f.z, z.REDSHIFT),
ifnull(a.m_tot-f.extinction_r-d.dismod-d.kcorr_r, -999),
ifnull(a.n_bulge, -999),
ifnull(log10(a.Hrad_corr/sqrt(a.ba_tot_corr)*d.kpc_per_arcsec),-999), 
ifnull(a.ba_tot_corr, -999), 
ifnull(b.m_tot-f.extinction_r-d.dismod-d.kcorr_r,-999),
ifnull(b.n_bulge, -999),
ifnull(log10(b.Hrad_corr/sqrt(b.ba_tot_corr)*d.kpc_per_arcsec),-999), 
ifnull(b.ba_tot_corr, -999), ifnull(b.BT, -999),
ifnull(m.probaE, -999), ifnull(m.probaEll, -999), ifnull(m.probaS0, -999),
ifnull(m.probaSab, -999), ifnull(m.probaScd, -999), ifnull(d.Vmax, -999),  
ifnull(d.dismod+d.kcorr_r, -999), ifnull(x.SexMag-f.extinction_r, -999)
from 
catalog.SSDR6 as z left join (catalog.CAST as f left join catalog.r_band_ser as a on a.galcount = f.galcount left join catalog.r_band_fit as x on x.galcount = f.galcount left join catalog.r_band_flagmodel as b on f.galcount = b.galcount left join catalog.DERT as d on f.galcount = d.galcount left join catalog.M2010 as m on f.galcount = m.galcount ) on f.galcount = z.galcount
order by z.rowcount
into outfile "/tmp/%s_1.txt";""" %(stem)

#cursor.execute(cmd)

#os.system('cp /tmp/%s_1.txt /scratch/MB/Sample_match_July2011_newmask.txt' %(stem))

#outfile = open('tmp_head.txt', 'w')
#outfile.write('#ra_gal dec_gal z absmag_ser n_ser hrad_semimajor_ser ba_ser absmag_best n_best hrad_semimajor_best ba_best BT_best P(E) P(Ell) P(S0) P(Sab) P(Scd) V_max absmagcorr mag_auto_r\n')
#outfile.close()

#os.system('cat tmp_head.txt /scratch/MB/Sample_match_July2011_newmask.txt > /scratch/MB/Sample_match_July2011_withhead_newmask.txt')

#os.system('rm tmp_head.txt')
#os.system('mv /scratch/MB/Sample_match_July2011_withhead_newmask.txt /scratch/MB/Sample_match_July2011_best.txt')



cmd = """select f.galcount, IFNULL(k.ra_gal,-999), IFNULL(k.dec_gal,-999), 
IFNULL(k.zspec,-999),  IFNULL(k.M09_redchi2,-999), 
IFNULL(k.M09_age,-999), IFNULL(k.M09_ebv,-999), IFNULL(k.M09_templ,-999), 
IFNULL(k.M09_mstar_l,-999), IFNULL(k.M09_mstar,-999),
IFNULL(k.M09_sfr,-999), IFNULL(k.Mabs_M09_u,-999), IFNULL(k.Mabs_M09_g,-999), 
IFNULL(k.Mabs_M09_r,-999), IFNULL(k.Mabs_M09_i,-999), 
IFNULL(k.Mabs_M09_z,-999),IFNULL(k.umag,-999), 
IFNULL(k.gmag,-999), IFNULL(k.rmag,-999), IFNULL(k.imag,-999), 
IFNULL(k.zmag,-999) 
from 
catalog.SSDR6 as z left join (catalog.CAST as f left join catalog.DR7_Portsmouth_krouall as k on f.objid=k.objid) on f.galcount = z.galcount
order by z.rowcount
into outfile "/tmp/%s_DR7_Portsmouth_krouall_July2011.txt";""" %(stem)
print cmd
cursor.execute(cmd)
os.system('cp /tmp/%s_DR7_Portsmouth_krouall_July2011.txt /home/alan/Desktop/galtable_DR7_Portsmouth_krouall_July2011.txt' %(stem))





