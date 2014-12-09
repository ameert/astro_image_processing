from mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys

dba = 'MB'
pwd = 'al130568'
usr = 'ameert'

stem = 'members3'

cursor = mysql_connect(dba, usr, pwd)

#if 1:
for cat in ['members','bcgs']:
    for model, count in zip(['ser','serexp'], [1,3]):
        cmd = """select a.galcount, f.ra_gal, f.dec_gal, a.z, 
        a.hrad_pix_corr *a.re_kpc/a.re_pix, a.re_kpc,  a.rd_kpc,
        a.hrad_pix_corr *0.396, a.re_pix *0.396,  a.rd_pix *0.396, 
        a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.kcorr_r-f.extinction_r ,
        a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.kcorr_r-f.extinction_r , 
        a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r,
        a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r , 
        a.BT, a.n, a.eb, a.flag, a.fitflag, a.manual_flag, z.bcgID, 
        f.devmag_r-a.dis_modu-d.kcorr_r-f.extinction_r ,
        log10(f.devrad_r*sqrt(f.devab_r)*a.re_kpc/(a.re_pix*0.396)),
        x.ModelMag_g-a.dis_modu-d.kcorr_g-f.extinction_g , 
        x.ModelMag_r-a.dis_modu-d.kcorr_r-f.extinction_r, 
        z.Ngals, m.ProbaE
        from catalog.full_dr7_r_%s as a, catalog.CAST as f, catalog.DERT as d, maxBCG_members.%s as z, catalog.magerr as x, catalog.M2010 as m where z.galcount = a.galcount and a.galcount = f.galcount and a.galcount = d.galcount and a.galcount = m.galcount and a.galcount = x.galcount order by z.bcgID into outfile "/tmp/%s%s_%d.txt";""" %(model,cat, stem,cat, count)
        cursor.execute(cmd)
        os.system('cp /tmp/%s%s_%d.txt ./%s_%d.txt' %(stem,cat,count,cat,count))
if 0:
    for model, count in zip(['ser', 'serexp'], [1,3]):
        cmd = """select a.galcount, f.ra_gal, f.dec_gal, a.z, 
        a.hrad_pix_corr *a.re_kpc/a.re_pix, a.re_kpc,  a.rd_kpc,
        a.hrad_pix_corr *0.396, a.re_pix *0.396,  a.rd_pix *0.396, 
        a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.kcorr_r-f.extinction_r ,
        a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.kcorr_r-f.extinction_r , 
        a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r,
        a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r , 
        a.BT, a.n, a.eb, a.flag, a.fitflag, a.manual_flag, z.bcgID 
        f.devmag_r-a.dis_modu-d.kcorr_r-f.extinction_r ,
        log10(f.devrad*sqrt(f.devab)*a.re_kpc/(a.re_pix*0.396)),
        x.ModelMag_g-a.dis_modu-d.kcorr_g-f.extinction_g , 
        x.ModelMag_r-a.dis_modu-d.kcorr_r-f.extinction_r, 
        z.Ngals, m.ProbaE
        from catalog.full_dr7_r_%s as a, catalog.CAST as f, catalog.DERT as d, maxBCG_members.%s as z, catalog.magerr as x, catalog.M2010 as m where z.galcount = a.galcount and a.galcount = f.galcount and a.galcount = d.galcount and a.galcount = m.galcount and a.galcount = x.galcount order by z.bcgID into outfile "/tmp/%s%s_%d.txt";""" %(model,cat, stem,cat, count)
        cursor.execute(cmd)
        os.system('cp /tmp/%s_highN_%d.txt ./tbcg_highN_%d.txt' %(stem,count,count))
