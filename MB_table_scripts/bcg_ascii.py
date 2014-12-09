from mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys

dba = 'MB'
pwd = 'al130568'
usr = 'ameert'

stem = 'bcg5'

cursor = mysql_connect(dba, usr, pwd)

if 1:
    for model, count in zip(['ser','devexp','serexp'], [1,2,3]):
        cmd = """select a.galcount, f.ra_gal, f.dec_gal, a.z, 
        a.hrad_pix_corr *a.re_kpc/a.re_pix, a.re_kpc,  a.rd_kpc,
        a.hrad_pix_corr *0.396, a.re_pix *0.396,  a.rd_pix *0.396, 
        a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.blanton_kr-f.extinction_r ,
        a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.blanton_kr-f.extinction_r , 
        a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r,
        a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r , 
        a.BT, a.n, a.eb, a.flag, a.fitflag, a.manual_flag, d.kcorr_r, 
        d.blanton_kr
        from maxBCG.bcg_r_%s as a, maxBCG.bcg_CAST as f, maxBCG.bcg_DERT as d, old_bcg_%s as b, maxBCG.bcg_topcat as z where b.galcount = z.galcount and z.objid = a.galcount and a.galcount = f.galcount and a.galcount = d.galcount order by z.objid into outfile "/tmp/%s_%d.txt";""" %(model,model, stem, count)
        cursor.execute(cmd)
        os.system('cp /tmp/%s_%d.txt ./tbcg_%d.txt' %(stem,count,count))
if 1:
    for model, count in zip(['ser', 'serexp'], [1,3]):
        cmd = """select a.galcount, f.ra_gal, f.dec_gal, a.z, 
        a.hrad_pix_corr *a.re_kpc/a.re_pix, a.re_kpc,  a.rd_kpc,
        a.hrad_pix_corr *0.396, a.re_pix *0.396,  a.rd_pix *0.396, 
        a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.blanton_kr-f.extinction_r ,
        a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.blanton_kr-f.extinction_r , 
        a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r,
        a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r , 
        a.BT, a.n, a.eb, a.flag, a.fitflag, a.manual_flag, d.kcorr_r, 
        d.blanton_kr
        from maxBCG.bcg_r_highN_%s as a, maxBCG.bcg_CAST as f, maxBCG.bcg_DERT as d, old_bcg_%s as b, maxBCG.bcg_topcat as z where b.galcount = z.galcount and z.objid = a.galcount and a.galcount = f.galcount and a.galcount = d.galcount order by z.objid into outfile "/tmp/%s_highN_%d.txt";""" %(model,model, stem, count)
        cursor.execute(cmd)
        os.system('cp /tmp/%s_highN_%d.txt ./tbcg_highN_%d.txt' %(stem,count,count))

if 0:
    for model, count in zip(['ser','devexp','serexp'], [4,5,6]):
        cmd = """select a.galcount, a.ra_gal, a.dec_gal, a.z, 
    a.hrad_kpc, a.re_kpc,  a.rd_kpc,
    a.hrad_arcsec, a.re_arcsec,  a.rd_arcsec, 
    a.AbsIe, a.AbsId, a.Ie, a.Id, 
    a.BT, a.n, a.eb, a.f_test_ser, a.f_test_devexp 
    from old_simard_%s as a, catalog.DERT as d where a.galcount = d.galcount  order by a.galcount into outfile "/tmp/%s_%d.txt";""" %(model, stem,count) 

        cursor.execute(cmd)
        os.system('cp /tmp/%s_%d.txt ./tf_%d.txt' %(stem,count,count))

