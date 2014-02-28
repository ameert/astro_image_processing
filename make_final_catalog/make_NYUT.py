#++++++++++++++++++++++++++
#
# TITLE: 
#
# PURPOSE: This program cleans up the 
#          NYU data and makes it 
#          have the same format as us. 
#
# INPUTS: 
#
# OUTPUTS: 
#
# PROGRAM CALLS:
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# WITH: Mariangela Bernardi
#       Department of Physics and Astronomy
#       University of Pennsylvania
#
# DATE:
#
#-----------------------------------

import numpy as np
import pylab as pl
import scipy as sc
from mysql_class import *
import os
import sys

this_dir = os.getcwd()

dba = 'catalog'
pwd = 'pymorph'
usr = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

bands = 'gri'

def build_tables(bands):
    cmd = """create table NYUT (galcount int primary key, 
    dis_arcsec float default -999,  ID_nyu int default -999, 
    ra_nyu float default -999,  dec_nyu float default -999, 
    """
    add_params = ["""m_tot_{band} float default -999,hrad_tot_{band} float default -999, n_{band} float default -999""".format(band=band) for band in bands] 
    add_params = ','.join(add_params)
    cmd = cmd + add_params +');'
    print cmd
    cursor.execute(cmd)

    cmd = 'insert into NYUT (galcount, dis_arcsec, Id_nyu, ra_nyu, dec_nyu) select galcount, dis_arcsec, Id_nyu, ra_nyu, dec_nyu from intermediate_tables.NYUT order by galcount;'
    print cmd
    cursor.execute(cmd)
    return

def load_fit_calc(bands, models):
     models = models[::-1]
     for band in bands:
         for model in models:
             base_cmd = """update {band}_band_fit as a, raw_catalog_fits.full_dr7_{band}_{model} as b set {argument} where a.galcount = b.galcount {condition};"""
             
             # now do SexHRad 
             cmd = base_cmd.format(band = band, model = model,
                                   argument = 'a.SexHrad = b.SexHalfRad*0.396', 
                                   condition = 'and a.SexHrad < 0 and b.SexHalfRad < 9900')
             print cmd
             cursor.execute(cmd)

             # now do SexSky, SexMag, and SexMagErr 
             base_cmd = """update {band}_band_fit as a, raw_catalog_fits.full_dr7_{band}_{model} as b, CAST as c set {argument} where a.galcount = b.galcount and c.galcount = a.galcount {condition};"""

             cmd = base_cmd.format(band = band, model = model,
                                   argument = 'a.SexMag = b.mag_auto-b.magzp-c.aa_{band}-c.kk_{band}*c.airmass_{band}, a.SexSky = -2.5*log10(b.SexSky/pow(0.396,2))-c.aa_{band}-c.kk_{band}*c.airmass_{band}, a.SexMag_err = b.magerr_auto'.format(band = band), 
                                   condition = 'and a.SexMag < 0 and b.mag_auto < 9900')
             print cmd
             cursor.execute(cmd)

     return

def load_fit_calc(bands):
    mags_to_copy = ['m_tot','A']
    index_to_copy = ['n','n_ser']
    rads_to_copy = ['hrad_tot', 'r_0']
    
    base_cmd = """update NYUT as a, intermediate_tables.NYUT as b set {argument} where a.galcount = b.galcount {cond};"""
    for band in bands:
        arg = 'a.n_{band}= b.n_ser_{band}, a.hrad_tot_{band} = b.r0_{band}*pow(b.bn_{band}, b.n_ser_{band}) '.format(band = band)
        cmd = base_cmd.format(argument = arg, cond='')
        print cmd
        cursor.execute(cmd)

    # now do mags
    for band in bands:
        arg = 'a.m_tot_{band} = 22.5-2.5*log10(b.A_{band}*exp(-1.0*b.bn_{band}+b.bn_{band})*pow(a.hrad_tot_{band},2)*2*PI()* b.n_ser_{band}*b.gamma_{band}/pow(b.bn_{band}, 2.0*b.n_ser_{band}))'.format(band = band)
        cmd = base_cmd.format(argument = arg, cond='')
        print cmd
        cursor.execute(cmd)


    return







#build_tables(bands)
load_fit_calc(bands)
