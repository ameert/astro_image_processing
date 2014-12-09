from mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys

dba = 'catalog'
pwd = 'al130568'
usr = 'ameert'

stem = 'DR6_gamma11'

cursor = mysql_connect(dba, usr, pwd)

cmd = """select ifnull(f.z, z.REDSHIFT),
ifnull(x.fiber2Mag_g, -999),
ifnull(x.fiber2Mag_r, -999),
ifnull(x.fiber2Mag_i, -999),
ifnull(f.PetroMag_g, -999),
ifnull(f.PetroMag_r, -999),
ifnull(f.PetroMag_i, -999),
ifnull(f.ModelMag_g, -999),
ifnull(f.ModelMag_r, -999),
ifnull(f.ModelMag_i, -999),
ifnull(-2.5*log10(f.fracdev_g*pow(10,-0.4*(f.devmag_g))+(1.0-f.fracdev_g)*pow(10, -0.4*(f.expmag_g))), -999),
ifnull(-2.5*log10(f.fracdev_r*pow(10,-0.4*(f.devmag_r))+(1.0-f.fracdev_r)*pow(10, -0.4*(f.expmag_r))), -999),
ifnull(-2.5*log10(f.fracdev_i*pow(10,-0.4*(f.devmag_i))+(1.0-f.fracdev_i)*pow(10, -0.4*(f.expmag_i))), -999),
ifnull(f.extinction_g, -999), 
ifnull(f.extinction_r, -999), 
ifnull(f.extinction_i, -999), 
ifnull(d.kcorr_g, -999), 
ifnull(d.kcorr_r, -999), 
ifnull(d.kcorr_i, -999), 
ifnull(c.m_tot, -999),
ifnull(b.m_tot, -999),
ifnull(a.m_tot, -999),
If(c.r_bulge*sqrt(c.ba_bulge)< 10*f.petroR50_g, IF(c.n_bulge between 0.5 and 7.5, 0,1),2),
If(b.r_bulge*sqrt(b.ba_bulge)< 10*f.petroR50_r, IF(b.n_bulge between 0.5 and 7.5, 0,1),2),
If(a.r_bulge*sqrt(a.ba_bulge)< 10*f.petroR50_i, IF(a.n_bulge between 0.5 and 7.5, 0,1),2)
from 
catalog.SSDR6 as z left join (catalog.CAST as f left join catalog.i_band_ser as a on a.galcount = f.galcount left join catalog.r_band_ser as b on b.galcount = f.galcount left join catalog.g_band_ser as c on c.galcount = f.galcount left join catalog.DERT as d on f.galcount = d.galcount left join catalog.M2010 as m on f.galcount = m.galcount) on f.galcount = z.galcount left join catalog.CAST_dr10 as x on f.galcount=x.galcount
order by z.rowcount
into outfile "/tmp/%s_10.txt";""" %(stem)

cursor.execute(cmd)


os.system('cp /tmp/%s_10.txt /scratch/MB/July2011_ri_CMASS.txt' %(stem))

outfile = open('tmp_head.txt', 'w')
outfile.write('#z fiber2mag_g fiber2mag_r fiber2mag_i PetroMag_g PetroMag_r PetroMag_i ModelMag_g ModelMag_r ModelMag_i cmodel_g cmodel_r cmodel_i extinction_g extinction_r extinction_i kcorr_g kcorr_r kcorr_i Sersicmag_g Sersicmag_r Sersicmag_i flag_g flag_r flag_i\n')
outfile.close()

os.system('cat tmp_head.txt /scratch/MB/July2011_ri_CMASS.txt > /scratch/MB/July2011_ri_CMASS_new.txt')

os.system('rm tmp_head.txt')
os.system('mv /scratch/MB/July2011_ri_CMASS_new.txt /scratch/MB/July2011_ri_CMASS.txt')

cmd = """select ifnull(f.z, z.REDSHIFT),
ifnull(x.fiber2Mag_g, -999),
ifnull(x.fiber2Mag_r, -999),
ifnull(x.fiber2Mag_i, -999),
ifnull(x.PetroMag_g, -999),
ifnull(x.PetroMag_r, -999),
ifnull(x.PetroMag_i, -999),
ifnull(x.ModelMag_g, -999),
ifnull(x.ModelMag_r, -999),
ifnull(x.ModelMag_i, -999),
ifnull(-2.5*log10(x.fracdev_g*pow(10,-0.4*(x.devmag_g))+(1.0-x.fracdev_g)*pow(10, -0.4*(x.expmag_g))), -999),
ifnull(-2.5*log10(x.fracdev_r*pow(10,-0.4*(x.devmag_r))+(1.0-x.fracdev_r)*pow(10, -0.4*(x.expmag_r))), -999),
ifnull(-2.5*log10(x.fracdev_i*pow(10,-0.4*(x.devmag_i))+(1.0-x.fracdev_i)*pow(10, -0.4*(x.expmag_i))), -999),
ifnull(x.extinction_g, -999), 
ifnull(x.extinction_r, -999), 
ifnull(x.extinction_i, -999), 
ifnull(d.kcorr_g, -999), 
ifnull(d.kcorr_r, -999), 
ifnull(d.kcorr_i, -999), 
ifnull(c.m_tot, -999),
ifnull(b.m_tot, -999),
ifnull(a.m_tot, -999),
If(c.r_bulge*sqrt(c.ba_bulge)< 10*x.petroR50_g, IF(c.n_bulge between 0.5 and 7.5, 0,1),2),
If(b.r_bulge*sqrt(b.ba_bulge)< 10*x.petroR50_r, IF(b.n_bulge between 0.5 and 7.5, 0,1),2),
If(a.r_bulge*sqrt(a.ba_bulge)< 10*x.petroR50_i, IF(a.n_bulge between 0.5 and 7.5, 0,1),2)
from 
catalog.SSDR6 as z left join (catalog.CAST as f left join catalog.i_band_ser as a on a.galcount = f.galcount left join catalog.r_band_ser as b on b.galcount = f.galcount left join catalog.g_band_ser as c on c.galcount = f.galcount left join catalog.DERT as d on f.galcount = d.galcount left join catalog.M2010 as m on f.galcount = m.galcount) on f.galcount = z.galcount left join catalog.CAST_dr10 as x on f.galcount=x.galcount
order by z.rowcount
into outfile "/tmp/%s_11.txt";""" %(stem)

cursor.execute(cmd)


os.system('cp /tmp/%s_11.txt /scratch/MB/July2011_ri_CMASS_10_tmp.txt' %(stem))

outfile = open('tmp_head.txt', 'w')
outfile.write('#z fiber2mag_g fiber2mag_r fiber2mag_i PetroMag_g PetroMag_r PetroMag_i ModelMag_g ModelMag_r ModelMag_i cmodel_g cmodel_r cmodel_i extinction_g extinction_r extinction_i kcorr_g kcorr_r kcorr_i Sersicmag_g Sersicmag_r Sersicmag_i flag_g flag_r flag_i\n')
outfile.close()

os.system('cat tmp_head.txt /scratch/MB/July2011_ri_CMASS_10_tmp.txt > /scratch/MB/July2011_ri_CMASS_DR10.txt')

os.system('rm tmp_head.txt')
os.system('rm /scratch/MB/July2011_ri_CMASS_10_tmp.txt')


sys.exit()


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
ifnull(d.dismod+d.kcorr_r, -999), ifnull(x.SexMag-f.extinction_r, -999),
if(y.flag&pow(2,14)>0,1,0)+if(y.flag&pow(2,19)>0,2,0)+if(y.flag is NULL,-1,0)
from 
catalog.SSDR6 as z left join (catalog.CAST as f left join catalog.r_band_ser as a on a.galcount = f.galcount left join catalog.r_band_fit as x on x.galcount = f.galcount left join catalog.r_band_serexp as b on f.galcount = b.galcount left join catalog.DERT as d on f.galcount = d.galcount left join catalog.M2010 as m on f.galcount = m.galcount left join catalog.Flags_optimize as y on y.galcount = f.galcount ) on f.galcount = z.galcount where (y.band = 'r' or y.band is NULL) and (y.ftype = 'u' or y.ftype is NULL) and (y.model = 'serexp' or y.model is NULL)
order by z.rowcount
into outfile "/tmp/%s_1.txt";""" %(stem)

cursor.execute(cmd)


os.system('cp /tmp/%s_1.txt /scratch/MB/Sample_match_July2011_newmask.txt' %(stem))

outfile = open('tmp_head.txt', 'w')
outfile.write('#ra_gal dec_gal z absmag_ser n_ser hrad_semimajor_ser ba_ser absmag_serexp n_serexp hrad_semimajor_serexp ba_serexp BT_serexp P(E) P(Ell) P(S0) P(Sab) P(Scd) V_max absmagcorr mag_auto_r good_bad\n')
outfile.close()

os.system('cat tmp_head.txt /scratch/MB/Sample_match_July2011_newmask.txt > /scratch/MB/Sample_match_July2011_withhead_old.txt')

os.system('rm tmp_head.txt')
os.system('mv /scratch/MB/Sample_match_July2011_withhead_old.txt /scratch/MB/Sample_match_July2011_final_cat.txt')


# now do Simard's data

cmd = """select ifnull(f.ra_gal, z.ra_gal), ifnull(f.dec_gal, z.dec_gal), 
ifnull(f.z, z.REDSHIFT),
ifnull(a.mag_r_tot-f.extinction_r-d.dismod-d.kcorr_r, -999),
ifnull(a.n, -999),
ifnull(log10(a.re_hl_r),-999), 
ifnull(pow(a.re_cir_hl_r/a.re_hl_r,2), -999), 
ifnull(b.mag_r_tot-f.extinction_r-d.dismod-d.kcorr_r, -999),
ifnull(b.n, -999),
ifnull(log10(b.re_hl_r),-999), 
ifnull(pow(b.re_cir_hl_r/b.re_hl_r,2), -999), 
ifnull(b.BT_r, -999),
ifnull(d.Vmax, -999),
ifnull(d.dismod+d.kcorr_r, -999)
from 
catalog.SSDR6 as z left join (catalog.CAST as f left join simard.simard_ser as a on a.galcount = f.galcount left join simard.simard_serexp as b on f.galcount = b.galcount left join catalog.DERT as d on f.galcount = d.galcount left join catalog.M2010 as m on f.galcount = m.galcount) on f.galcount = z.galcount
order by z.rowcount
into outfile "/tmp/%s_3.txt";""" %(stem)

cursor.execute(cmd)


os.system('cp /tmp/%s_3.txt /scratch/MB/Sample_simard_July2011.txt' %(stem))

outfile = open('tmp_head.txt', 'w')
outfile.write('#ra_gal dec_gal z absmag_ser n_ser hrad_semimajor_ser ba_ser absmag_serexp n_serexp hrad_semimajor_serexp ba_serexp BT_serexp Vmax absmagcorr \n')
outfile.close()

os.system('cat tmp_head.txt /scratch/MB/Sample_simard_July2011.txt > /scratch/MB/Sample_simard_July2011_withhead.txt')

os.system('rm tmp_head.txt')
os.system('mv /scratch/MB/Sample_simard_July2011_withhead.txt /scratch/MB/Sample_simard_July2011.txt')

# GAMMA matches
cmd = """select  ifnull(c.galcount, -999),  ifnull(b.m_tot-c.extinction_r, -999), ifnull(a.mag_r_tot-c.extinction_r, -999), ifnull(g.r_mag_10Re_ser_rerun-c.extinction_r, -999),
ifnull(g.r_mag_10Re_ser_simard-c.extinction_r, -999),
ifnull(g.r_mag_10Re_ser-c.extinction_r, -999),
ifnull(d.dismod+d.kcorr_r, -999), ifnull(g.Kron_r_ext, -999)
from 
catalog.SSDR6 as z left join (CAST as c left join simard.simard_ser as a on a.galcount = c.galcount left join r_rerun_ser as b on c.galcount = b.galcount left join GAMA as g on g.galcount=c.galcount left join DERT as d on c.galcount = d.galcount) on c.galcount = z.galcount
order by z.rowcount
into outfile "/tmp/%s_7.txt";""" %(stem)
cursor.execute(cmd)

os.system('cp /tmp/%s_7.txt /scratch/MB/Sample_July2011_gamma_newmask.txt' %(stem))

outfile = open('tmp_head.txt', 'w')
outfile.write('# galcount  appmag_inf_us appmag_inf_simard appmag_10Re_us appmag_10Re_simard appmag_10Re_gama absmagcorr mag_auto_r\n')
outfile.close()

os.system('cat tmp_head.txt /scratch/MB/Sample_July2011_gamma_newmask.txt > /scratch/MB/Sample_July2011_withhead_gamma_newmask.txt')

os.system('rm tmp_head.txt')
os.system('mv /scratch/MB/Sample_July2011_withhead_gamma_newmask.txt /scratch/MB/Sample_July2011_gamma_rerun.txt')
