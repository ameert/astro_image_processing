from mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys

dba = 'catalog'
pwd = 'al130568'
usr = 'ameert'

stem = 'newt503'

cursor = mysql_connect(dba, usr, pwd)

cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
ifnull(log10(f.veldisp),-999), s.Vmax,  
a.m_tot-d.dismod-d.kcorr_r-f.extinction_r,
ifnull(log10(a.hrad_corr*d.kpc_per_arcsec),-999), 
a.n_bulge, a.ba_tot_corr, 
ifnull(b.m_tot-d.dismod-d.kcorr_r-f.extinction_r,-999),
ifnull(log10(b.hrad_corr/sqrt(a.ba_tot_corr)*d.kpc_per_arcsec),-999), 
b.ba_tot_corr, b.BT,
ifnull(log10(b.r_bulge*sqrt(b.ba_bulge)*d.kpc_per_arcsec),-999), b.n_bulge, 
b.ba_bulge,
ifnull(log10(b.r_disk*sqrt(b.ba_disk)*d.kpc_per_arcsec),-999), b.ba_disk,   
m.probaE,m.probaEll,m.probaS0,m.probaSab,m.probaScd,
f.ModelMag_g-d.dismod-d.kcorr_g-f.extinction_g,
f.ModelMag_r-d.dismod-d.kcorr_r-f.extinction_r,
ifnull(j.Mstar_avg, -999),
ifnull(j.M_star_P16, -999),
ifnull(j.Mstar_P84, -999),
z.grCenter_hl, z.giCenter_hl, z.riCenter_hl, 
z.grOuter_hl, z.giOuter_hl, z.riOuter_hl,
z.grtwo_hl, z.gitwo_hl, z.ritwo_hl,
z.grhalf_hl, z.gihalf_hl, z.rihalf_hl,
if(u.flag&pow(2,14)>0,1,0)+if(u.flag&pow(2,19)>0,2,0)+if(u.flag is NULL,-1,0)
from 
catalog.r_band_ser as a, catalog.r_band_serexp as b, 
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_optimize as u,
COLOR_GRAD_ser as z
where  
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
f.galcount = z.galcount and u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
order by f.galcount 
into outfile "/tmp/%s_1.txt";""" %(stem)

cursor.execute(cmd)


os.system('cp /tmp/%s_1.txt /scratch/MB/galtable.txt' %(stem))

os.system('cat topcat_head.txt /scratch/MB/galtable.txt > final_cat.txt')
