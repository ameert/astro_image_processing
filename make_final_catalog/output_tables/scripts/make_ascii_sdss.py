from mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys

dba = 'catalog'
pwd = 'al130568'
usr = 'ameert'

stem = 'newt9'

cursor = mysql_connect(dba, usr, pwd)

for model, count in zip(['ser'], [1,2,3]):
    cmd = """select a.galcount, f.ra_gal, f.dec_gal, a.z, 
a.hrad_pix_corr *a.re_kpc/a.re_pix , a.re_kpc,  a.rd_kpc,
a.hrad_pix_corr *0.396, a.re_pix *0.396,  a.rd_pix *0.396, 
a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.kcorr_r-f.extinction_r ,
a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-d.kcorr_r-f.extinction_r , 
a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r,
a.Id-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r , 
a.BT, a.n, a.eb, 
f.devmag_r - f.extinction_r, f.devmag_r - f.extinction_r-a.dis_modu-d.kcorr_r, f.devrad_r, f.devrad_r * sqrt(f.devab_r), f.devrad_r * sqrt(f.devab_r) * a.re_kpc/(a.re_pix*0.396) 
from full_dr7_r_%s as a, CAST as f, DERT as d where  a.galcount = f.galcount and a.galcount = d.galcount order by a.galcount into outfile "/tmp/%s_%d.txt";""" %(model, stem,count) 

    cursor.execute(cmd)


