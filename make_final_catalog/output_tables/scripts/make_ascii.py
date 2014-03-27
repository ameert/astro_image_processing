from mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys

dba = 'catalog'
pwd = 'al130568'
usr = 'ameert'

stem = 'newta6'

cursor = mysql_connect(dba, usr, pwd)

if 1:
    for model, count in zip(['ser','devexp','serexp'], [1,2,3]):
        cmd = """select a.galcount, f.ra_gal, f.dec_gal, a.z, 
a.hrad_pix_corr/sqrt(a.hrad_ba_corr)*a.re_kpc/a.re_pix, a.re_kpc,  a.rd_kpc,
a.hrad_pix_corr/sqrt(a.hrad_ba_corr)*0.396, a.re_pix *0.396,  a.rd_pix *0.396, 
a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.kcorr_r-f.extinction_r ,
a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.kcorr_r-f.extinction_r , 
a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r,
a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r , 
a.BT, a.n, a.eb, a.flag, a.fitflag, a.manual_flag, d.kcorr_r, a.hrad_ba_corr, 
a.ed
from full_dr7_r_%s as a, CAST as f, DERT as d where  a.galcount = f.galcount and a.galcount = d.galcount order by a.galcount into outfile "/tmp/%s_%d.txt";""" %(model, stem,count) 

        cursor.execute(cmd)
        os.system('cp /tmp/%s_%d.txt table_%d.txt' %(stem,count,count))

if 0:
    for model, count in zip(['ser', 'serexp'], [1,3]):
        cmd = """select a.galcount, f.ra_gal, f.dec_gal, a.z, 
a.hrad_pix_corr *a.re_kpc/a.re_pix, a.re_kpc,  a.rd_kpc,
a.hrad_pix_corr *0.396, a.re_pix *0.396,  a.rd_pix *0.396, 
a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.kcorr_r-f.extinction_r ,
a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.kcorr_r-f.extinction_r , 
a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r,
a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r , 
a.BT, a.n, a.eb, a.flag, a.fitflag, a.manual_flag,  d.kcorr_r, d.blanton_kr
from full_dr7_r_highN_%s as a, CAST as f, DERT as d where  a.galcount = f.galcount and a.galcount = d.galcount order by a.galcount into outfile "/tmp/%s_highN_%d.txt";""" %(model, stem,count) 

        cursor.execute(cmd)
        os.system('cp /tmp/%s_highN_%d.txt table_highN_%d.txt' %(stem,count,count))

if 0:
    for model, count in zip(['ser','devexp','serexp'], [4,5,6]):
        cmd = """select a.galcount, f.ra_gal, f.dec_gal, a.z,
c.re_cir_hl_r, a.re_kpc_%s, a.rd_kpc_%s, 
c.re_cir_hl_r/a.kpc_per_arcsec, a.re_kpc_%s/a.kpc_per_arcsec, a.rd_kpc_%s/a.kpc_per_arcsec, 
a.Ie_%s - d.dismod- d.kcorr_r-f.extinction_r, 
a.Id_%s - d.dismod- d.kcorr_r-f.extinction_r, 
a.Ie_%s -f.extinction_r, a.Id_%s -f.extinction_r, 
a.BT_%s, a.n_%s, 1.0-a.eb_ser, a.f_test_ser, a.f_test_devexp   
from simard_sample as a, CAST as f, DERT as d, simard.simard_%s as c where  a.galcount = f.galcount and a.galcount = d.galcount and a.galcount = c.galcount order by a.galcount into outfile "/tmp/%s_%d.txt";""" %(model,model,model,model,model,model,model,model,model,model,model,stem,count)

        cursor.execute(cmd)
        os.system('cp /tmp/%s_%d.txt table_%d.txt' %(stem,count,count))


