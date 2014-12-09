from mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys

dba = 'MB'
pwd = 'al130568'
usr = 'ameert'

stem = 'fuk8'

cursor = mysql_connect(dba, usr, pwd)

if 1:
    for model, count in zip(['ser','serexp'], [1,3]):
        cmd = """select a.galcount, f.ra_gal, f.dec_gal, a.z, 
ifnull(a.hrad_pix_corr/sqrt(a.hrad_ba_corr)*a.re_kpc/a.re_pix, -999), 
a.re_kpc,  a.rd_kpc,
ifnull(a.hrad_pix_corr/sqrt(a.hrad_ba_corr)*0.396, -999),
 a.re_pix *0.396,  a.rd_pix *0.396, 
ifnull(a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.blanton_kr-f.extinction_r,-999) ,
ifnull(a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.blanton_kr-f.extinction_r,-999) , 
ifnull(a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r,-999),
ifnull(a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r,-999) , 
a.BT, a.n, a.eb, a.flag, a.fitflag, a.manual_flag, d.kcorr_r, a.hrad_ba_corr, 
a.ed, a.hrad_pix_ana*a.re_kpc/a.re_pix, a.hrad_pix_baavg*a.re_kpc/a.re_pix     
from fukugita.fukugita_r_%s as a, fukugita.fukugita_CAST as f, fukugita.fukugita_DERT as d, old_fukugita_%s as b where a.galcount = b.galcount and a.galcount = f.f07id and a.galcount = d.galcount order by a.galcount into outfile "/tmp/%s_%d.txt";""" %(model,model, stem, count)
        cursor.execute(cmd)
        os.system('cp /tmp/%s_%d.txt /scratch/MB/tf_%d.txt' %(stem,count,count))
if 0:
    #for model, count in zip(['ser','devexp','serexp'], [1,2,3]):
    for model, count in zip(['ser', 'serexp'], [1,3]):
        cmd = """select a.galcount, f.ra_gal, f.dec_gal, a.z, 
        a.hrad_pix_corr *a.re_kpc/a.re_pix, a.re_kpc,  a.rd_kpc,
        a.hrad_pix_corr *0.396, a.re_pix *0.396,  a.rd_pix *0.396, 
        a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.kcorr_r-f.extinction_r ,
        a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.kcorr_r-f.extinction_r , 
        a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r,
        a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r , 
        a.BT, a.n, a.eb, a.flag, a.fitflag, a.manual_flag, d.kcorr_r, 
        d.blanton_kr
        from fukugita.fukugita_r_%s as a, fukugita.fukugita_CAST as f, fukugita.fukugita_DERT as d, old_fukugita_%s as b where a.galcount = b.galcount and a.galcount = f.f07id and a.galcount = d.galcount order by a.galcount into outfile "/tmp/%s_highN_%d.txt";""" %(model,model, stem, count)
        cursor.execute(cmd)
        os.system('cp /tmp/%s_highN_%d.txt ./tf_highN_%d.txt' %(stem,count,count))

if 0:
    for model, count in zip(['ser','devexp','serexp'], [4,5,6]):
        cmd = """select a.galcount, a.ra_gal, a.dec_gal, a.z, 
    a.hrad_kpc, a.re_kpc,  a.rd_kpc,
    a.hrad_arcsec, a.re_arcsec,  a.rd_arcsec, 
    a.AbsIe, a.AbsId, a.Ie, a.Id, 
    a.BT, a.n, a.eb, a.f_test_ser, a.f_test_devexp 
    from old_simard_%s as a, catalog.DERT as d where a.galcount = d.galcount  order by a.galcount into outfile "/tmp/%s_%d.txt";""" %(model, stem,count) 

        cursor.execute(cmd)
        os.system('cp /tmp/%s_%d.txt /scratch/MB/tf_%d.txt' %(stem,count,count))

