from mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys

dba = 'andre_BCG'
pwd = 'al130568'
usr = 'ameert'

stem = 'newt55'

cursor = mysql_connect(dba, usr, pwd)

cmd = """select f.galcount, f.objid , f.ra_gal, f.dec_gal, f.andre_spec_z,
ifnull(log10(f.veldisp),-999),  
a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-d.dismod-d.kcorr_r-f.extinction_r,
a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r,
ifnull(log10(a.hrad_pix_corr*d.kpc_per_arcsec*0.396),-999), 
a.n, a.hrad_ba_corr, 
ifnull(-2.5*log10(pow(10,-0.4*b.Ie) + pow(10,-0.4*b.Id))-b.magzp-f.aa_r-
f.kk_r*f.airmass_r-d.dismod-d.kcorr_r-f.extinction_r,-999),
ifnull(-2.5*log10(pow(10,-0.4*b.Ie) + pow(10,-0.4*b.Id))-b.magzp-f.aa_r-
f.kk_r*f.airmass_r-f.extinction_r,-999),
ifnull(log(b.hrad_pix_corr*d.kpc_per_arcsec*0.396),-999), 
b.hrad_ba_corr, b.BT,
ifnull(log10(b.re_pix*sqrt(b.eb)*d.kpc_per_arcsec*0.396),-999), b.n, b.eb,   
ifnull(log10(b.rd_pix*sqrt(b.ed)*d.kpc_per_arcsec*0.396),-999), b.ed,   
f.ModelMag_g-d.dismod-d.kcorr_g-f.extinction_g,
f.ModelMag_r-d.dismod-d.kcorr_r-f.extinction_r
from 
andre_BCG.andre_r_ser as a, andre_BCG.andre_r_serexp as b, 
andre_BCG.CAST as f ,
andre_BCG.DERT as d
where  
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount  
order by f.galcount
into outfile "/tmp/%s_1.txt";""" %(stem)

cursor.execute(cmd)


os.system('cp /tmp/%s_1.txt /scratch/MB/BCG_short.txt' %(stem))

os.system('cat BCG_topcat_head.txt /scratch/MB/BCG_short.txt > topcat_bcg_short.txt')
