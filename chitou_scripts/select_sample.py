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

sample_size = 10000
model_list = ['serexp']#,'devexp','serexp']
cursor = mysql_connect('catalog','ameert','al130568')
simcount = 0

if 0:
    for model in model_list:
        cmd = 'DROP table simulations.sample_%s;' %(model)
        try:
            cursor.execute(cmd)
        except:
            pass
    
        # for model in model_list:
        cmd = 'create table simulations.sample_%s like catalog.full_dr7_r_%s;' %(model, model)
        cursor.execute(cmd)

        cmd = """insert into simulations.sample_%s select b.* from 
                 catalog.full_dr7_r_%s as b, simulations.CAST_short as c 
                 where b.galcount = c.galcount and  b.re_kpc < 40  and
                 b.Ie < 40.0 and b.Ie > 0.0 and  b.n < 8   and 
                 (b.re_kpc/b.rd_kpc) < 1 or b.BT > .5) and b.alan_hrad_pix > 0
                 ;""" %(model, model)
        cursor.execute(cmd)

if 0:
    cmd = 'DROP table simulations.sim_input;'
    try:
        cursor.execute(cmd)
    except:
        pass
        
    cmd = "create table if not exists simulations.sim_input (simcount int primary key, model varchar(8), galcount int, name varchar(30), n float default -888,re float default -888, re_kpc float default -888, Ie float default -888, eb float default -888,rd float default -888,Id float default -888,ed float default -888,BT float default -888, zeropoint_sdss_r float default -888,bpa float default -888,dpa float default -888,z float default -888);"
    try:
        cursor.execute(cmd)
    except:
        pass
if 1:
    #cmd = "delete from simulations.sim_input where model='devexp';"
    #cursor.execute(cmd)

    for model in model_list:
        # for model in model_list:
        #cmd = "select galcount from simulations.sample_%s;" %model
        cmd = "select simcount from simulations.sim_input where model = '%s';" %model
        galcount, = cursor.get_data(cmd)
        
        galcount = np.array(galcount)
        #ran.shuffle(galcount)
        cmd = "update simulations.sim_input as a, simulations.sample_%s as b, simulations.CAST_short as c set a.n = b.n, a.re= b.re_pix*0.396, a.re_kpc =b.re_kpc, a.Ie=b.Ie-25.256-c.aa_r, a.eb =b.eb,a.rd = b.rd_pix*0.396, a.Id=b.Id-25.256-c.aa_r, a.ed=b.ed, a.BT=b.BT, a.zeropoint_sdss_r=-1.0*c.aa_r, a.bpa = b.bpa+90.0, a.dpa= b.dpa+90.0, a.z=b.z where a.galcount = b.galcount and b.galcount = c.galcount and a.model = '%s';" %(model,model)
        #cursor.execute(cmd)

        for tmp_g in galcount[0:sample_size]: 
            #simcount += 1
            name = '%08d_%s' %(tmp_g, model)

            #cmd = """insert into simulations.sim_input select %d, '%s', a.galcount, '%s', a.n, 
            #         a.re_pix*0.396, a.re_kpc, a.Ie-25.256-b.aa_r, a.eb,
            #         a.rd_pix*0.396, a.Id-25.256-b.aa_r, a.ed, a.BT, -1.0*b.aa_r, a.bpa+90.0, 
            #         a.dpa+90.0, a.z from simulations.sample_%s as a, CAST as b where  
            #         a.galcount = b.galcount and a.galcount = %d;""" %(simcount, model, name, model, tmp_g) 
            cmd = "update simulations.sim_input as a set name = '%s' where simcount= %d;" %(name, tmp_g)
            cursor.execute(cmd)
