from astro_image_processing.mysql import *
import os
import itertools
import pyfits
import datetime
import sys

dba = 'catalog'
pwd = 'pymorph'
usr = 'pymorph'

stem = 'newt538'

cursor = mysql_connect(dba, usr, pwd)

cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
ifnull(log10(f.veldisp),-999), s.Vmax,  
m.probaE,m.probaEll,m.probaS0,m.probaSab,m.probaScd,
f.ModelMag_g-d.dismod-d.kcorr_g-f.extinction_g,
f.ModelMag_r-d.dismod-d.kcorr_r-f.extinction_r,
ifnull(j.Mstar_avg, -999),
ifnull(j.M_star_P16, -999),
ifnull(j.Mstar_P84, -999),
if(u.flag&pow(2,14)>0,1,0)+if(u.flag&pow(2,19)>0,2,0)+if(u.flag is NULL,-1,0),
if(x.flag&pow(2,14)>0,1,0)+if(x.flag&pow(2,19)>0,2,0)+if(x.flag is NULL,-1,0),
f.petroR50_r*d.kpc_per_arcsec, 
f.petroMag_r-d.dismod-d.kcorr_r-f.extinction_r,
f.petroR50_g*d.kpc_per_arcsec, 
f.petroMag_g-d.dismod-d.kcorr_g-f.extinction_g
from 
catalog.r_band_ser as a, catalog.r_band_serexp as b, 
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_optimize as u,
catalog.Flags_optimize as x, COLOR_GRAD_ser as z
where  
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
f.galcount = z.galcount and u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and x.band='r' and x.model = 'ser' 
order by f.galcount 
into outfile "/tmp/%s_1.txt";""" %(stem)
#print cmd
#cursor.execute(cmd)
#os.system('cp /tmp/%s_1.txt /scratch/MB/galtable_1.txt' %(stem))

cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
a.m_tot-d.dismod-d.kcorr_r-f.extinction_r,
ifnull(log10(a.hrad_corr*d.kpc_per_arcsec),-999), 
a.n_bulge, a.ba_tot_corr, 
ifnull(b.m_tot-d.dismod-d.kcorr_r-f.extinction_r,-999),
ifnull(log10(b.hrad_corr/sqrt(a.ba_tot_corr)*d.kpc_per_arcsec),-999), 
b.ba_tot_corr, b.BT,
ifnull(log10(b.r_bulge*sqrt(b.ba_bulge)*d.kpc_per_arcsec),-999), b.n_bulge, 
b.ba_bulge,
ifnull(log10(b.r_disk*sqrt(b.ba_disk)*d.kpc_per_arcsec),-999), b.ba_disk,   
if(u.flag&pow(2,14)>0,1,0)+if(u.flag&pow(2,19)>0,2,0)+if(u.flag is NULL,-1,0),
if(x.flag&pow(2,14)>0,1,0)+if(x.flag&pow(2,19)>0,2,0)+if(x.flag is NULL,-1,0)
from 
catalog.r_band_ser as a, catalog.r_band_serexp as b, 
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_optimize as u,catalog.Flags_optimize as x,
COLOR_GRAD_ser as z
where  
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
f.galcount = z.galcount and u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and x.band='r' and x.model = 'ser'order by f.galcount 
into outfile "/tmp/%s_2.txt";""" %(stem)

#cursor.execute(cmd)
#os.system('cp /tmp/%s_2.txt /scratch/MB/galtable_2.txt' %(stem))

cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
z.grCenter_hl, z.giCenter_hl, z.riCenter_hl, 
z.grOuter_hl, z.giOuter_hl, z.riOuter_hl,
z.grtwo_hl, z.gitwo_hl, z.ritwo_hl,
z.grhalf_hl, z.gihalf_hl, z.rihalf_hl,
z.gr15_hl, z.gi15_hl, z.ri15_hl,
z.gr25_hl, z.gi25_hl, z.ri25_hl,
z.gr3_hl, z.gi3_hl, z.ri3_hl,
z.gr90_hl, z.gi90_hl, z.ri90_hl,
if(u.flag&pow(2,14)>0,1,0)+if(u.flag&pow(2,19)>0,2,0)+if(u.flag is NULL,-1,0),
if(x.flag&pow(2,14)>0,1,0)+if(x.flag&pow(2,19)>0,2,0)+if(x.flag is NULL,-1,0)
from 
catalog.r_band_ser as a, catalog.r_band_serexp as b, 
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_optimize as u, catalog.Flags_optimize as x,
COLOR_GRAD_ser as z
where  
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
f.galcount = z.galcount and u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and x.band='r' and x.model = 'ser'order by f.galcount 
into outfile "/tmp/%s_3.txt";""" %(stem)

#cursor.execute(cmd)
#os.system('cp /tmp/%s_3.txt /scratch/MB/galtable_3.txt' %(stem))

cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
a.Galsky, b.Galsky, s.Galsky, gser.Galsky, gse.Galsky, gsim.Galsky,
if(u.flag&pow(2,14)>0,1,0)+if(u.flag&pow(2,19)>0,2,0)+if(u.flag is NULL,-1,0),
if(x.flag&pow(2,14)>0,1,0)+if(x.flag&pow(2,19)>0,2,0)+if(x.flag is NULL,-1,0)
from 
catalog.r_band_ser as a, catalog.r_band_serexp as b, 
catalog.g_band_ser as gser, catalog.g_band_serexp as gse, 
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, catalog.r_simard_ser as s, catalog.g_simard_ser as gsim,
catalog.M2010 as m, catalog.Flags_optimize as u, catalog.Flags_optimize as x
where  
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = gser.galcount and f.galcount = gse.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and 
f.galcount = gsim.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and 
x.band='r' and x.model = 'ser' order by f.galcount 
into outfile "/tmp/%s_4.txt";""" %(stem)

#cursor.execute(cmd)
#os.system('cp /tmp/%s_4.txt /scratch/MB/galtable_4.txt' %(stem))

cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
ain.g_mag + f.extinction_g + d.kcorr_g, b.g_mag + f.extinction_g + d.kcorr_g, 
s.g_mag + f.extinction_g + d.kcorr_g, gser.g_mag + f.extinction_g + d.kcorr_g, 
gse.g_mag + f.extinction_g + d.kcorr_g, gsim.g_mag + f.extinction_g + d.kcorr_g,
ain.r_mag + f.extinction_r + d.kcorr_r, b.r_mag + f.extinction_r + d.kcorr_r, 
s.r_mag + f.extinction_r + d.kcorr_r, gser.r_mag + f.extinction_r + d.kcorr_r,
gse.r_mag + f.extinction_r + d.kcorr_r, gsim.r_mag + f.extinction_r + d.kcorr_r,
if(u.flag&pow(2,14)>0,1,0)+if(u.flag&pow(2,19)>0,2,0)+if(u.flag is NULL,-1,0),
if(x.flag&pow(2,14)>0,1,0)+if(x.flag&pow(2,19)>0,2,0)+if(x.flag is NULL,-1,0),
-2.5/log(10)*log(pow(10.0, -0.4*r.Galsky-2)/2 + sqrt(pow(9.0e-11,2.0)+0.25*pow(10,-0.8*r.Galsky-4))),
-2.5/log(10)*log(pow(10.0, -0.4*rs.Galsky-2)/2 + sqrt(pow(1.2e-10,2.0)+0.25*pow(10,-0.8*rs.Galsky-4))),
f.extinction_g, f.extinction_r, 
d.kcorr_g, d.kcorr_r, f.petroR50_r, rs.Hrad_corr, rserexp.Hrad_corr
from 
catalog.ser_color_HL as ain, catalog.ser_color_HL as b, 
catalog.ser_color_HL as gser, catalog.ser_color_HL as gse, 
catalog.ser_color_HL as s, catalog.ser_color_HL as gsim,
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, 
catalog.M2010 as m, catalog.Flags_optimize as u, catalog.Flags_optimize as x,
catalog.g_band_ser as r, catalog.r_band_ser as rs, 
catalog.r_band_serexp as rserexp
where  
f.galcount = r.galcount and f.galcount = rs.galcount and
f.galcount = rserexp.galcount and 
f.galcount = ain.galcount and f.galcount = b.galcount and 
f.galcount = gser.galcount and f.galcount = gse.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and 
f.galcount = gsim.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and
ain.HL_rad_10= 10 and  b.HL_rad_10= 15 and  s.HL_rad_10= 25 and  
gser.HL_rad_10= 30 and  gse.HL_rad_10= 40 and  gsim.HL_rad_10= 90 and 
u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and 
x.band='r' and x.model = 'ser' order by f.galcount 
into outfile "/tmp/%s_5.txt";""" %(stem)
#print cmd
#cursor.execute(cmd)
#os.system('cp /tmp/%s_5.txt /scratch/MB/galtable_5.txt' %(stem))

cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
z.grCenter, z.giCenter, z.riCenter, 
z.gr05_hl, z.gi05_hl, z.ri05_hl,
z.gr10_hl, z.gi10_hl, z.ri10_hl,
z.gr15_hl, z.gi15_hl, z.ri15_hl,
z.gr20_hl, z.gi20_hl, z.ri20_hl,
z.gr25_hl, z.gi25_hl, z.ri25_hl,
z.gr30_hl, z.gi30_hl, z.ri30_hl,
z.gr90_hl, z.gi90_hl, z.ri90_hl,
if(u.flag&pow(2,14)>0,1,0)+if(u.flag&pow(2,19)>0,2,0)+if(u.flag is NULL,-1,0),
if(x.flag&pow(2,14)>0,1,0)+if(x.flag&pow(2,19)>0,2,0)+if(x.flag is NULL,-1,0), 
z.centerrad_arcsec
from 
catalog.r_band_ser as a, catalog.r_band_serexp as b, 
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_optimize as u, catalog.Flags_optimize as x,
ser_colorgrad_serrad as z
where  
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
f.galcount = z.galcount and u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and x.band='r' and x.model = 'ser'order by f.galcount 
into outfile "/tmp/%s_6.txt";""" %(stem)

#print cmd
#cursor.execute(cmd)
#os.system('cp /tmp/%s_6.txt /scratch/MB/galtable_6.txt' %(stem))

cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
ain.g_mag , b.g_mag ,
g20.g_mag , s.g_mag , gser.g_mag, 
gse.g_mag , gsim.g_mag ,
ain.r_mag , b.r_mag , 
g20.r_mag , 
s.r_mag , gser.r_mag ,
gse.r_mag , gsim.r_mag ,
if(u.flag&pow(2,14)>0,1,0)+if(u.flag&pow(2,19)>0,2,0)+if(u.flag is NULL,-1,0),
if(x.flag&pow(2,14)>0,1,0)+if(x.flag&pow(2,19)>0,2,0)+if(x.flag is NULL,-1,0),
IFNULL(-2.5/log(10)*log(pow(10.0, -0.4*r.Galsky-2)/2 + sqrt(pow(9.0e-11,2.0)+0.25*pow(10,-0.8*r.Galsky-4))),-999),
IFNULL(-2.5/log(10)*log(pow(10.0, -0.4*rs.Galsky-2)/2 + sqrt(pow(1.2e-10,2.0)+0.25*pow(10,-0.8*rs.Galsky-4))),-999),
f.extinction_g, f.extinction_r, 
d.kcorr_g, d.kcorr_r, f.petroR50_r, rs.Hrad_corr, rserexp.Hrad_corr
from 
catalog.ser_magHL_serrad2 as ain, catalog.ser_magHL_serrad2 as b
, catalog.ser_magHL_serrad2 as g20 ,
catalog.ser_magHL_serrad2 as gser, catalog.ser_magHL_serrad2 as gse, 
catalog.ser_magHL_serrad2 as s, catalog.ser_magHL_serrad2 as gsim,
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, 
catalog.M2010 as m, catalog.Flags_optimize as u, catalog.Flags_optimize as x,
catalog.g_band_ser as r, catalog.r_band_ser as rs, 
catalog.r_band_serexp as rserexp
where  
f.galcount = r.galcount and f.galcount = rs.galcount and
f.galcount = rserexp.galcount and 
f.galcount = ain.galcount and f.galcount = b.galcount and 
f.galcount = gser.galcount and f.galcount = gse.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and 
f.galcount = gsim.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and
f.galcount = g20.galcount and
ain.HL_rad_10= 10 and  b.HL_rad_10= 15 and  g20.HL_rad_10= 20 and
 s.HL_rad_10= 25 and  
gser.HL_rad_10= 30 and  gse.HL_rad_10= 40 and  gsim.HL_rad_10= 90 and 
u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and 
x.band='r' and x.model = 'ser' order by f.galcount 
into outfile "/tmp/%s_7.txt";""" %(stem)
#print cmd
#cursor.execute(cmd)
#os.system('cp /tmp/%s_7.txt /scratch/MB/galtable_7.txt' %(stem))


ifpogson = '_pogson'
 
for a in [('',''),('aperture','_ap')]:
    cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
z.grCenter, z.giCenter, z.riCenter, 
z.gr05_hl, z.gi05_hl, z.ri05_hl,
z.gr10_hl, z.gi10_hl, z.ri10_hl,
z.gr15_hl, z.gi15_hl, z.ri15_hl,
z.gr20_hl, z.gi20_hl, z.ri20_hl,
z.gr25_hl, z.gi25_hl, z.ri25_hl,
z.gr30_hl, z.gi30_hl, z.ri30_hl,
z.gr90_hl, z.gi90_hl, z.ri90_hl,
if(u.flag&pow(2,14)>0,1,0)+if(u.flag&pow(2,19)>0,2,0)+if(u.flag is NULL,-1,0),
if(x.flag&pow(2,14)>0,1,0)+if(x.flag&pow(2,19)>0,2,0)+if(x.flag is NULL,-1,0), 
z.centerrad_arcsec
from 
catalog.r_band_ser as a, catalog.r_band_serexp as b, 
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_optimize as u, catalog.Flags_optimize as x,
ser_color{apsql}_serrad{ifpogson} as z
where  
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
f.galcount = z.galcount and u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and x.band='r' and x.model = 'ser'order by f.galcount 
into outfile "/tmp/{stem}_6_gmr{isap}{ifpogson}.txt";""".format(apsql = a[0], isap=a[1], stem=stem, ifpogson=ifpogson)

    #print cmd
    #cursor.execute(cmd)
    #os.system('cp /tmp/{stem}_6_gmr{isap}{ifpogson}.txt /scratch/MB/galtable_6_gmr{isap}{ifpogson}.txt'.format(stem=stem, isap=a[1], ifpogson=ifpogson))

    cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
ain.g_mag , b.g_mag ,
g20.g_mag , s.g_mag , gser.g_mag, 
gse.g_mag , gsim.g_mag ,
ain.r_mag , b.r_mag , 
g20.r_mag , 
s.r_mag , gser.r_mag ,
gse.r_mag , gsim.r_mag ,
if(u.flag&pow(2,14)>0,1,0)+if(u.flag&pow(2,19)>0,2,0)+if(u.flag is NULL,-1,0),
if(x.flag&pow(2,14)>0,1,0)+if(x.flag&pow(2,19)>0,2,0)+if(x.flag is NULL,-1,0),
IFNULL(-2.5/log(10)*log(pow(10.0, -0.4*r.Galsky-2)/2 + sqrt(pow(9.0e-11,2.0)+0.25*pow(10,-0.8*r.Galsky-4))), -999),
IFNULL(-2.5/log(10)*log(pow(10.0, -0.4*rs.Galsky-2)/2 + sqrt(pow(1.2e-10,2.0)+0.25*pow(10,-0.8*rs.Galsky-4))),-999),
f.extinction_g, f.extinction_r, 
d.kcorr_g, d.kcorr_r, f.petroR50_r, rs.Hrad_corr, rserexp.Hrad_corr
from 
catalog.ser_magHL{apsql}_serrad{ifpogson} as ain, catalog.ser_magHL{apsql}_serrad{ifpogson} as b
, catalog.ser_magHL{apsql}_serrad{ifpogson} as g20 ,
catalog.ser_magHL{apsql}_serrad{ifpogson} as gser, catalog.ser_magHL{apsql}_serrad{ifpogson} as gse, 
catalog.ser_magHL{apsql}_serrad{ifpogson} as s, catalog.ser_magHL{apsql}_serrad{ifpogson} as gsim,
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, 
catalog.M2010 as m, catalog.Flags_optimize as u, catalog.Flags_optimize as x,
catalog.g_band_ser as r, catalog.r_band_ser as rs, 
catalog.r_band_serexp as rserexp
where  
f.galcount = r.galcount and f.galcount = rs.galcount and
f.galcount = rserexp.galcount and 
f.galcount = ain.galcount and f.galcount = b.galcount and 
f.galcount = gser.galcount and f.galcount = gse.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and 
f.galcount = gsim.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and
f.galcount = g20.galcount and
ain.HL_rad_10= 10 and  b.HL_rad_10= 15 and  g20.HL_rad_10= 20 and
 s.HL_rad_10= 25 and  
gser.HL_rad_10= 30 and  gse.HL_rad_10= 40 and  gsim.HL_rad_10= 90 and 
u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and 
x.band='r' and x.model = 'ser' order by f.galcount 
into outfile "/tmp/{stem}_7{isap}{ifpogson}.txt";""".format(apsql = a[0], isap=a[1], stem=stem, ifpogson=ifpogson)
    #print cmd
    #cursor.execute(cmd)
    #os.system('cp /tmp/{stem}_7{isap}{ifpogson}.txt /scratch/MB/galtable_7{isap}{ifpogson}.txt'.format(stem=stem, isap=a[1], ifpogson=ifpogson))

cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
z.grCenter, z.giCenter, z.riCenter, 
z.gr05_hl, z.gi05_hl, z.ri05_hl,
z.gr10_hl, z.gi10_hl, z.ri10_hl,
z.gr15_hl, z.gi15_hl, z.ri15_hl,
z.gr20_hl, z.gi20_hl, z.ri20_hl,
z.gr25_hl, z.gi25_hl, z.ri25_hl,
z.gr30_hl, z.gi30_hl, z.ri30_hl,
z.gr90_hl, z.gi90_hl, z.ri90_hl,
if(u.flag&pow(2,14)>0,1,0)+if(u.flag&pow(2,19)>0,2,0)+if(u.flag is NULL,-1,0),
if(x.flag&pow(2,14)>0,1,0)+if(x.flag&pow(2,19)>0,2,0)+if(x.flag is NULL,-1,0), 
z.centerrad_arcsec
from 
catalog.r_band_ser as a, catalog.r_band_serexp as b, 
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_optimize as u, catalog.Flags_optimize as x,
serexp_colorgrad_serexprad as z
where  
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
f.galcount = z.galcount and u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and x.band='r' and x.model = 'ser'order by f.galcount 
into outfile "/tmp/%s_8.txt";""" %(stem)

#print cmd
#cursor.execute(cmd)
#os.system('cp /tmp/%s_8.txt /scratch/MB/galtable_8.txt' %(stem))

cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
ain.g_mag + f.extinction_g + d.kcorr_g, b.g_mag + f.extinction_g + d.kcorr_g, 
s.g_mag + f.extinction_g + d.kcorr_g, gser.g_mag + f.extinction_g + d.kcorr_g, 
gse.g_mag + f.extinction_g + d.kcorr_g, gsim.g_mag + f.extinction_g + d.kcorr_g,
ain.r_mag + f.extinction_r + d.kcorr_r, b.r_mag + f.extinction_r + d.kcorr_r, 
s.r_mag + f.extinction_r + d.kcorr_r, gser.r_mag + f.extinction_r + d.kcorr_r,
gse.r_mag + f.extinction_r + d.kcorr_r, gsim.r_mag + f.extinction_r + d.kcorr_r,
if(u.flag&pow(2,14)>0,1,0)+if(u.flag&pow(2,19)>0,2,0)+if(u.flag is NULL,-1,0),
if(x.flag&pow(2,14)>0,1,0)+if(x.flag&pow(2,19)>0,2,0)+if(x.flag is NULL,-1,0),
-2.5/log(10)*log(pow(10.0, -0.4*r.Galsky-2)/2 + sqrt(pow(9.0e-11,2.0)+0.25*pow(10,-0.8*r.Galsky-4))),
-2.5/log(10)*log(pow(10.0, -0.4*rs.Galsky-2)/2 + sqrt(pow(1.2e-10,2.0)+0.25*pow(10,-0.8*rs.Galsky-4))),
f.extinction_g, f.extinction_r, 
d.kcorr_g, d.kcorr_r, f.petroR50_r, rs.Hrad_corr, rserexp.Hrad_corr
from 
catalog.serexp_magHL_serexprad as ain, catalog.serexp_magHL_serexprad as b, 
catalog.serexp_magHL_serexprad as gser, catalog.serexp_magHL_serexprad as gse, 
catalog.serexp_magHL_serexprad as s, catalog.serexp_magHL_serexprad as gsim,
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, 
catalog.M2010 as m, catalog.Flags_optimize as u, catalog.Flags_optimize as x,
catalog.g_band_serexp as r, catalog.r_band_serexp as rs, 
catalog.r_band_serexp as rserexp
where  
f.galcount = r.galcount and f.galcount = rs.galcount and
f.galcount = rserexp.galcount and 
f.galcount = ain.galcount and f.galcount = b.galcount and 
f.galcount = gser.galcount and f.galcount = gse.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and 
f.galcount = gsim.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and
ain.HL_rad_10= 10 and  b.HL_rad_10= 15 and  s.HL_rad_10= 25 and  
gser.HL_rad_10= 30 and  gse.HL_rad_10= 40 and  gsim.HL_rad_10= 90 and 
u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and 
x.band='r' and x.model = 'ser' order by f.galcount 
into outfile "/tmp/%s_9.txt";""" %(stem)
#print cmd
#cursor.execute(cmd)
#os.system('cp /tmp/%s_9.txt /scratch/MB/galtable_9.txt' %(stem))

cmd = """select f.galcount, 
if(u.flag<=0,-1,if(u.flag&pow(2,19)>0,5,if(u.flag&pow(2,4)>0,2,if(u.flag&pow(2,1)>0,1,if(u.flag&pow(2,14)>0,4,if(u.flag&pow(2,13)>0,3,0)))))),
if(x.flag<=0,-1,if(x.flag&pow(2,19)>0,5,if(x.flag&pow(2,4)>0,2,if(x.flag&pow(2,1)>0,1,if(x.flag&pow(2,14)>0,4,if(x.flag&pow(2,13)>0,3,0)))))),
if(u.flag&pow(2,19)>0,-999,if(u.flag&pow(2,4)>0,0.0,if(u.flag&pow(2,1)>0,1.0,if(u.flag&pow(2,13)>0,1.0-rse.BT,rse.BT)))),
-4.5775*m.probaEll -2.35723*m.probaS0+2.48028*m.probaSab+6.0815*m.probaScd
from 
catalog.CAST as f, M2010 as m,
catalog.Flags_optimize as u, catalog.Flags_optimize as x,
catalog.r_band_ser as rs, catalog.r_band_serexp as rse
where  
f.galcount = rs.galcount and f.galcount = rse.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and
u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and 
x.band='r' and x.model = 'ser' order by f.galcount 
into outfile "/tmp/%s_10.txt";""" %(stem)
#print cmd
#cursor.execute(cmd)
#os.system('cp /tmp/%s_10.txt /scratch/MB/galflags.txt' %(stem))



cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
ifnull(k.V_DISP, -999),ifnull(k.V_DISP_ERR, -999),
ifnull(j.sigma_balmer, -999),ifnull(j.sigma_balmer_err, -999),
ifnull(j.sigma_forbid, -999),ifnull(j.sigma_forbid_err, -999),
ifnull(l.median, -999),ifnull(l.P16, -999),ifnull(l.P84, -999),
ifnull(l.flag, -999),
ifnull(n.median, -999),ifnull(n.P16, -999),ifnull(n.P84, -999),
ifnull(n.flag, -999),
ifnull(o.med, -999),ifnull(o.P16, -999),ifnull(o.P84, -999)
from 
catalog.r_band_ser as a, catalog.r_band_serexp as b, 
catalog.CAST as f left join JHU.JHU_Balmer as j on f.galcount = j.galcount 
left join JHU.JHU_veldisp as k on f.galcount = k.galcount
left join JHU.JHU_sfr as l on f.galcount = l.galcount
left join JHU.JHU_specsfr as n on f.galcount = n.galcount
left join JHU.JHU_fiboh as o on f.galcount = o.galcount,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_optimize as u,
catalog.Flags_optimize as x, COLOR_GRAD_ser as z
where  
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
f.galcount = z.galcount and u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and x.band='r' and x.model = 'ser' 
order by f.galcount 
into outfile "/tmp/%s_11.txt";""" %(stem)
#print cmd
#cursor.execute(cmd)
#os.system('cp /tmp/%s_11.txt /scratch/MB/veldisp.txt' %(stem))


cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
a.m_tot-d.dismod-d.kcorr_r-f.extinction_r,
ifnull(log10(a.hrad_corr*d.kpc_per_arcsec),-999), 
a.n_bulge, a.ba_tot_corr, 
ifnull(b.m_tot-d.dismod-d.kcorr_r-f.extinction_r,-999),
ifnull(log10(b.hrad_corr/sqrt(a.ba_tot_corr)*d.kpc_per_arcsec),-999), 
b.ba_tot_corr, b.BT,
ifnull(log10(b.r_bulge*sqrt(b.ba_bulge)*d.kpc_per_arcsec),-999), b.n_bulge, 
b.ba_bulge,
ifnull(log10(b.r_disk*sqrt(b.ba_disk)*d.kpc_per_arcsec),-999), b.ba_disk,   
if(s.Prob_pS>0.32,0,1),
0
from 
catalog.r_simard_ser as a, catalog.r_simard_serexp as b, 
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_optimize as u,catalog.Flags_optimize as x,
COLOR_GRAD_ser as z
where  
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
f.galcount = z.galcount and u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and x.band='r' and x.model = 'ser'order by f.galcount 
into outfile "/tmp/%s_simard.txt";""" %(stem)

#print cmd
#cursor.execute(cmd)
#os.system('cp /tmp/%s_simard.txt /scratch/MB/galtable_simard.txt' %(stem))

cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
IF(u.flag&pow(2,1)>0,'bulge',IF(u.flag&pow(2,4)>0,'disk',IF(u.flag&pow(2,10)>0 and c.n_bulge<7.95,'2com',IF(u.flag&pow(2,14)>0,'bad_2com',IF(u.flag&pow(2,10)>0 and c.n_bulge>=7.95,'n8',IF(u.flag&pow(2,19)>0,'bad','')))))),
-4.5775*m.probaEll -2.35723*m.probaS0+2.48028*m.probaSab+6.0815*m.probaScd 
from 
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, catalog.Flags_optimize as u,catalog.Flags_optimize as x,
catalog.M2010 as m,catalog.r_band_serexp as c
where  
f.galcount = m.galcount and f.galcount = c.galcount and
f.galcount = d.galcount and f.galcount = u.galcount and 
u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and x.band='r' and x.model = 'ser'order by f.galcount 
into outfile "/tmp/%s_types.txt";""" %(stem)

#print cmd
#cursor.execute(cmd)
#os.system('cp /tmp/%s_types.txt /scratch/MB/galtable_types.txt' %(stem))

cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
a.m_tot-d.dismod-d.kcorr_r-f.extinction_r,
ifnull(log10(a.hrad_corr*d.kpc_per_arcsec),-999), 
a.n_bulge, a.ba_tot_corr, 
ifnull(b.m_tot-d.dismod-d.kcorr_r-f.extinction_r,-999),
ifnull(log10(b.hrad_corr/sqrt(a.ba_tot_corr)*d.kpc_per_arcsec),-999), 
b.ba_tot_corr, b.BT,
ifnull(log10(b.r_bulge*sqrt(b.ba_bulge)*d.kpc_per_arcsec),-999), b.n_bulge, 
b.ba_bulge,
ifnull(log10(b.r_disk*sqrt(b.ba_disk)*d.kpc_per_arcsec),-999), b.ba_disk,   
if(u.flag&pow(2,14)>0,1,0)+if(u.flag&pow(2,20)>0,2,0)+if(u.flag is NULL,-1,0),
if(x.flag&pow(2,14)>0,1,0)+if(x.flag&pow(2,20)>0,2,0)+if(x.flag is NULL,-1,0)
from 
catalog.r_highn_ser as a, catalog.r_highn_serexp as b, 
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_highn as u,catalog.Flags_highn as x,
COLOR_GRAD_ser as z
where  
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
f.galcount = z.galcount and u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and x.band='r' and x.model = 'ser'order by f.galcount 
into outfile "/tmp/%s_highn.txt";""" %(stem)

#print cmd
#cursor.execute(cmd)
#os.system('cp /tmp/%s_highn.txt /scratch/MB/galtable_highn.txt' %(stem))


cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,  
d.kcorr_r, f.petroMag_r-f.extinction_r,
IFNULL(-2.5*log10(f.fracdev_r*pow(10.0, -0.4*(f.devmag_r-f.extinction_r)) +
(1.0-f.fracdev_r)*pow(10.0, -0.4*(f.expmag_r-f.extinction_r))), -999)
from 
catalog.r_band_ser as a, catalog.r_band_serexp as b, 
catalog.CAST as f,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_catalog as u,
catalog.Flags_catalog as x, COLOR_GRAD_ser as z
where  
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
f.galcount = z.galcount and u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
and f.galcount = x.galcount and x.ftype = 'u' and x.band='r' and x.model = 'ser' 
order by f.galcount 
into outfile "/tmp/%s_for_vmax.txt";""" %(stem)
#print cmd
#cursor.execute(cmd)
#os.system('cp /tmp/%s_for_vmax.txt /home/alan/Desktop/galtable_for_vmax.txt' %(stem))


cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,  
f10.fiber2mag_g,f10.fiber2mag_r,f10.fiber2mag_i,
f10.petromag_g,f10.petromag_r,f10.petromag_i,
f10.modelmag_g,f10.modelmag_r,f10.modelmag_i,
f10.cmodelmag_g,f10.cmodelmag_r,f10.cmodelmag_i,
f10.extinction_g,f10.extinction_r,f10.extinction_i,
f10.kcorrg,f10.kcorrr,f10.kcorri,
a.m_tot, ai.m_tot, sr.m_tot,
IF(u.flag&pow(2,0)>0, IF(a.n_bulge between 0.5 and 7.5, 0, 1),2),
IF(x.flag&pow(2,0)>0, IF(ai.n_bulge between 0.5 and 7.5, 0, 1),2)
from 
catalog.r_band_ser as a,
catalog.r_simard_ser as sr,
catalog.i_band_ser as ai,
catalog.r_band_serexp as b, 
catalog.dr10_CAST as f10,
catalog.CAST as f,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_catalog as u,
catalog.Flags_catalog as x
where  
f.galcount = ai.galcount and f.galcount = f10.galcount and 
f.galcount = sr.galcount and 
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
 u.ftype = 'u' and u.band='r' and u.model = 'ser' 
and f.galcount = x.galcount and x.ftype = 'u' and x.band='i' and x.model = 'ser'
order by f.galcount 
into outfile "/tmp/%s_fiber2mag_all.txt";""" %(stem)
#print cmd
#cursor.execute(cmd)
#os.system('cp /tmp/%s_fiber2mag_all.txt /home/alan/Desktop/galtable_fiber2mag_all.txt' %(stem))

cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,  
f10.fiber2mag_g,f10.fiber2mag_r,f10.fiber2mag_i,
f.petromag_g,f.petromag_r,f.petromag_i,
f.modelmag_g,f.modelmag_r,f.modelmag_i,
IFNULL(-2.5*log10(f.fracdev_g*pow(10.0, -0.4*(f.devmag_g)) +
(1.0-f.fracdev_g)*pow(10.0, -0.4*(f.expmag_g))), -999),
IFNULL(-2.5*log10(f.fracdev_r*pow(10.0, -0.4*(f.devmag_r)) +
(1.0-f.fracdev_r)*pow(10.0, -0.4*(f.expmag_r))), -999),
IFNULL(-2.5*log10(f.fracdev_i*pow(10.0, -0.4*(f.devmag_i)) +
(1.0-f.fracdev_i)*pow(10.0, -0.4*(f.expmag_i))), -999),
f.extinction_g,f.extinction_r,f.extinction_i,
d.kcorr_g,d.kcorr_r,d.kcorr_i,
a.m_tot, ai.m_tot, sr.m_tot,
IF(u.flag&pow(2,0)>0, IF(a.n_bulge between 0.5 and 7.5, 0, 1),2),
IF(x.flag&pow(2,0)>0, IF(ai.n_bulge between 0.5 and 7.5, 0, 1),2),
a.r_bulge, a.ba_bulge, a.n_bulge,
ai.r_bulge, ai.ba_bulge, ai.n_bulge
from 
catalog.r_highn_ser as a,
catalog.r_simard_ser as sr,
catalog.i_highn_ser as ai,
catalog.r_band_serexp as b, 
catalog.dr10_CAST as f10,
catalog.CAST as f,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_catalog as u,
catalog.Flags_catalog as x
where  
f.galcount = ai.galcount and f.galcount = f10.galcount and 
f.galcount = sr.galcount and 
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
 u.ftype = 'u' and u.band='r' and u.model = 'ser' 
and f.galcount = x.galcount and x.ftype = 'u' and x.band='i' and x.model = 'ser'
order by f.galcount 
into outfile "/tmp/%s_fiber2mag_all_dr7_highn.txt";""" %(stem)
#print cmd
#cursor.execute(cmd)
#os.system('cp /tmp/%s_fiber2mag_all_dr7_highn.txt /home/alan/Desktop/galtable_fiber2mag_all_dr7_highn.txt' %(stem))

cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,  
polyid_boss.polyid
from 
catalog.polyid_boss as polyid_boss,
catalog.r_highn_ser as a,
catalog.r_simard_ser as sr,
catalog.i_highn_ser as ai,
catalog.r_band_serexp as b, 
catalog.dr10_CAST as f10,
catalog.CAST as f,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_catalog as u,
catalog.Flags_catalog as x
where  
f.galcount = ai.galcount and f.galcount = f10.galcount and 
f.galcount = sr.galcount and f.galcount = polyid_boss.galcount and 
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
 u.ftype = 'u' and u.band='r' and u.model = 'ser' 
and f.galcount = x.galcount and x.ftype = 'u' and x.band='i' and x.model = 'ser'
order by f.galcount 
into outfile "/tmp/%s_polyid_all.txt";""" %(stem)
print cmd
cursor.execute(cmd)
os.system('cp /tmp/%s_polyid_all.txt /home/alan/Desktop/galtable_polyid_all.txt' %(stem))
