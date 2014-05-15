#!/usr/bin/python

import pyfits as p
from mysql_class import *
import numpy as np
import sys
import pylab as pl
import numpy.random as ran

def mag_sum(mag1, mag2):
    print mag1, mag2
    mag1 = 10.0**( -.4*mag1)
    mag2 = 10.0**(-.4*mag2)

    mag_tot = mag1 + mag2
    bt = mag1/(mag1+mag2)
    mag_tot = -2.5 * np.log10(mag_tot)

    return mag_tot, bt

def mag_to_counts( mag, aa, kk = 0 , airmass = 0):
    exptime = 53.907456 #in seconds, taken from SDSS website www.sdss.org/dr3/algorithms/fluxcal.html
    return exptime * (10**(-.4*mag)) / (10**(0.4*(aa + kk*airmass)))

def counts_to_mag( counts, aa, kk = 0 , airmass = 0):
    exptime = 53.907456 #in seconds, taken from SDSS website www.sdss.org/dr3/algorithms/fluxcal.html
    return -2.5 * np.log10(counts/exptime) + aa

sample_size = 1000
pser = 0.3

cursor = mysql_connect('catalog','pymorph','pymorph')
simcount = 0

if 0:
    
    cmd = 'DROP table simsample_des_hst;' 
    try:
        cursor.execute(cmd)
    except:
        pass
    
    cmd = 'create table simsample_des_hst like r_band_serexp;' 
    cursor.execute(cmd)
    cmd = 'alter table simsample_des_hst drop primary key;' 
    cursor.execute(cmd)

    cmd = """insert into simsample_des_hst select b.* from 
                 r_band_serexp as b, CAST as c, Flags_optimize as f, 
                 DERT as d, M2010 as m
                 where b.galcount = c.galcount and f.galcount = c.galcount and
                 d.galcount = c.galcount and m.galcount = c.galcount and   
                 ((-4.5775*m.probaEll -2.35723*m.probaS0+2.48028*m.probaSab+6.0815*m.probaScd) between -6 and 0) and f.band='r' and f.model = 'serexp' and 
f.ftype = 'u' and f.flag>0 and f.flag&(pow(2,11)+pow(2,12)+pow(2,1)+pow(2,5)+pow(2,6)+pow(2,7)+pow(2,8))>0 order by RAND() limit {limnum};""".format(limnum = int(sample_size*(1.0-pser)))
    print cmd
    cursor.execute(cmd)

    cmd = """insert into simsample_des_hst select b.* from 
                 r_band_ser as b, CAST as c, Flags_optimize as f, 
                 DERT as d, M2010 as m
                 where b.galcount = c.galcount and f.galcount = c.galcount and
                 d.galcount = c.galcount and m.galcount = c.galcount and   
                 ((-4.5775*m.probaEll -2.35723*m.probaS0+2.48028*m.probaSab+6.0815*m.probaScd) between -6 and 0) and f.band='r' and f.model = 'serexp' and 
f.ftype = 'u' and f.flag>0 and f.flag&(pow(2,11)+pow(2,12)+pow(2,1)+pow(2,5)+pow(2,6)+pow(2,7)+pow(2,8))>0 order by RAND() limit {limnum};""".format(limnum = int(sample_size*(pser)))
    print cmd
    cursor.execute(cmd)

if 0:
    cmd = 'DROP table sim_input;'
    try:
        cursor.execute(cmd)
    except:
        pass
        
    cmd = """create table if not exists sim_input (simcount int primary key, model varchar(8), n float default -888,re float default -888, re_kpc float default -888, Ie float default -888, eb float default -888,rd float default -888,Id float default -888,ed float default -888,BT float default -888, zeropoint_sdss_r float default -888,bpa float default -888,dpa float default -888,z float default -888);"""
    try:
        cursor.execute(cmd)
    except:
        pass
if 0:
    #cmd = "delete * from sim_input;"
    #cursor.execute(cmd)
    
    #cmd = "insert into sim_input ( simcount)  select galcount from simsample_des_hst;" 
    #cursor.execute(cmd)
        
    cmd = "update sim_input as a, simsample_des_hst as b, CAST as c, DERT as d set a.n = b.n_bulge, a.re= b.r_bulge*d.kpc_per_arcsec, a.re_kpc =b.r_bulge*d.kpc_per_arcsec, a.Ie=b.m_bulge, a.eb =b.ba_bulge,a.rd = b.r_disk*d.kpc_per_arcsec, a.Id=b.m_disk, a.ed=b.ba_disk, a.BT=b.BT, a.zeropoint_sdss_r=-1.0*c.aa_r, a.bpa = b.pa_bulge+90.0, a.dpa= b.pa_disk+90.0, a.z=c.z where a.simcount = b.galcount and b.galcount = c.galcount and d.galcount = c.galcount;" 
    cursor.execute(cmd)

if 0:
    cmd = """update sim_input set galcount = simcount;"""
    cursor.execute(cmd)



if 1:
    cmd = """update sim_input set re = re/{kpcscale}, rd = rd/{kpcscale};""".format(kpcscale=6.104)
    print cmd
    cursor.execute(cmd)
    
    
