#++++++++++++++++++++++++++
#
# TITLE: 
#
# PURPOSE: This program cleans up the 
#          raw fit data and makes it 
#          usable. 
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

bands = 'r'
models = ['ser']
#models = ['dev', 'ser', 'devexp', 'serexp']

def build_tables(bands, models):
    for band in bands:
        cmd = """create table {band}_newmask_fit (galcount int primary key, 
    SexMag float default -999,  SexMag_err float default -999, 
    SexHrad float default -999,  SexSky  float default -999, 
    num_targets int default -999, 
    C float default -999, C_err float default -999, 
    A float default -999, A_err float default -999,
    S float default -999, S_err float default -999,  
    G float default -999, M20 float default -999);
    """.format(band = band)
        print cmd
        cursor.execute(cmd)

        cmd = 'insert into {band}_newmask_fit (galcount) select galcount from CAST order by galcount;'.format(band=band)
        print cmd
        cursor.execute(cmd)

        for model in models:
            cmd = """create table {band}_newmask_{model} (galcount int primary key, 
    m_tot float default -999, BT float default -999, 
    Hrad_corr float default -999, ba_tot_corr float default -999,
    xctr_bulge float default -999, xctr_bulge_err float default -999,  
    yctr_bulge float default -999, yctr_bulge_err float default -999,  
    m_bulge float default -999, m_bulge_err float default -999,
    r_bulge float default -999, r_bulge_err float default -999,
    n_bulge float default -999, n_bulge_err float default -999,
    ba_bulge float default -999, ba_bulge_err float default -999,
    pa_bulge float default -999, pa_bulge_err float default -999,
    xctr_disk float default -999, xctr_disk_err float default -999,  
    yctr_disk float default -999, yctr_disk_err float default -999,  
    m_disk float default -999, m_disk_err float default -999,
    r_disk float default -999, r_disk_err float default -999,
    ba_disk float default -999, ba_disk_err float default -999,
    pa_disk float default -999, pa_disk_err float default -999,
    chi2nu float default -999, Goodness float default -999,
    Galsky float default -999, Galsky_err float default -999, 
    fit int default -999, FitFlag bigint default -999,
    flag bigint default -999, Manual_flag bigint default -999,
    FinalFlag int default -999,
    Comments varchar(1000));""".format(band = band, model = model)
            print cmd
            cursor.execute(cmd)
            cmd = """insert into {band}_newmask_{model} (galcount) select galcount from CAST order by galcount;""".format(band = band, model = model)
            print cmd
            cursor.execute(cmd)

    return

def load_fit_uncalc(bands, models):
     for band in bands:
         for model in models:
             base_cmd = """update {band}_newmask_fit as a, raw_catalog_fits.newmask_{band}_{model} as b set {argument} where a.galcount = b.galcount {condition};"""
             
             # now do num_targets 
             cmd = base_cmd.format(band = band, model = model,
                                   argument = 'a.num_targets = b.num_targets', 
                                   condition = 'and a.num_targets < b.num_targets')
             print cmd
             #cursor.execute(cmd)

             # now do CASgm
             for val in ['C', 'C_err','A','A_err','S','S_err','G', 'M']:
                 cmd = base_cmd.format(band = band, model = model, 
                                       argument = 'a.%s = b.%s ' %(val,val), 
                        condition = ' and a.%s < 0 and b.%s < 9900' %(val,val))
                 print cmd
             #cursor.execute(cmd)
     return

def load_fit_calc(bands, models):
     models = models[::-1]
     for band in bands:
         for model in models:
             base_cmd = """update {band}_newmask_fit as a, raw_catalog_fits.newmask_{band}_{model} as b set {argument} where a.galcount = b.galcount {condition};"""
             
             # now do SexHRad 
             cmd = base_cmd.format(band = band, model = model,
                                   argument = 'a.SexHrad = b.SexHalfRad*0.396', 
                                   condition = 'and a.SexHrad < 0 and b.SexHalfRad < 9900')
             print cmd
             cursor.execute(cmd)

             # now do SexSky, SexMag, and SexMagErr 
             base_cmd = """update {band}_newmask_fit as a, raw_catalog_fits.newmask_{band}_{model} as b, CAST as c set {argument} where a.galcount = b.galcount and c.galcount = a.galcount {condition};"""

             cmd = base_cmd.format(band = band, model = model,
                                   argument = 'a.SexMag = b.mag_auto-b.magzp-c.aa_{band}-c.kk_{band}*c.airmass_{band}, a.SexSky = -2.5*log10(b.SexSky/pow(0.396,2))-c.aa_{band}-c.kk_{band}*c.airmass_{band}, a.SexMag_err = b.magerr_auto'.format(band = band), 
                                   condition = 'and a.SexMag < 0 and b.mag_auto < 9900')
             print cmd
             cursor.execute(cmd)

     return

def load_model_uncalc(bands, models):
    params_to_copy = [['ba_tot_corr','hrad_ba_corr'],
                      ['BT', 'BT'],
                      ['xctr_bulge','bulge_xctr'],
                      ['xctr_bulge_err','bulge_xctr_err'],
                      ['yctr_bulge','bulge_yctr'],
                      ['yctr_bulge_err','bulge_yctr_err'],
                      ['m_bulge_err', 'Ie_err'],['n_bulge','n'],
                      ['n_bulge_err', 'n_err'],['ba_bulge', 'eb'],
                      ['ba_bulge_err','eb_err'],['pa_bulge', 'bpa'],
                      ['pa_bulge_err','bpa_err'],
                      ['xctr_disk','disk_xctr'],
                      ['xctr_disk_err','disk_xctr_err'],
                      ['yctr_disk','disk_yctr'],
                      ['yctr_disk_err','disk_yctr_err'],
                      ['m_disk_err', 'Id_err'],
                      ['ba_disk', 'ed'], ['ba_disk_err','ed_err'],
                      ['pa_disk', 'dpa'],['pa_disk_err','dpa_err'],
                      ['chi2nu', 'chi2nu'],['Goodness','Goodness'],
                      ['fit','fit'],['FitFlag','FitFlag'],['flag','flag'],
                      ['Manual_flag','Manual_flag']
                      ] 

    for band in bands:
        for model in models:
            base_cmd = """update {band}_newmask_{model} as a, raw_catalog_fits.newmask_{band}_{model} as b set {argument} where a.galcount = b.galcount {condition};"""
             
             # now do params
            for val in params_to_copy:
                cmd = base_cmd.format(band = band, model = model, 
                                      argument = 'a.%s = b.%s ' %(val[0],val[1]), 
                                      condition = ' and a.%s <= 0 and b.%s < 9900' %(val[0],val[1]))
                print cmd
                cursor.execute(cmd)
            cmd = base_cmd.format(band = band, model = model, 
                                  argument = 'a.Comments = b.Comments ', 
                                  condition = ' and a.Comments is NULL and b.Comments is not NULL' )
            print cmd
            cursor.execute(cmd)
    return

def load_model_calc(bands, models):
    rads_to_copy = [#['Hrad_corr','hrad_pix_corr'],
                    ['r_bulge','re_pix'],['r_bulge_err', 're_pix_err'],
                    ['r_disk','rd_pix'],['r_disk_err', 'rd_pix_err']
                    ]
    mags_to_copy = [['m_bulge', 'Ie'],['m_disk', 'Id']]


    for band in bands:
        for model in models:
            base_cmd = """update {band}_newmask_{model} as a, raw_catalog_fits.newmask_{band}_{model} as b, CAST as c set {argument} where a.galcount = b.galcount and c.galcount = a.galcount {condition};"""
            # now do rads
            for val in rads_to_copy:
                cmd = base_cmd.format(band = band, model = model, 
                                    argument = 'a.%s = b.%s*0.396 ' %(val[0],val[1]),
                   condition = ' and a.%s < 0 and b.%s < 9900' %(val[0],val[1]))
                print cmd
                cursor.execute(cmd)

            # now do mags
            for val in mags_to_copy:
                cmd = base_cmd.format(band = band, model = model, 
                         argument = 'a.{val1} = b.{val2}-b.magzp-c.aa_{band}-c.kk_{band}*c.airmass_{band} '.format(val1=val[0],val2=val[1], band = band), condition = ' and a.%s < 0 and b.%s < 9900' %(val[0],val[1]))
                print cmd
                cursor.execute(cmd)

            # now do total Mags
            if model in ['ser','dev']:
                cmd = base_cmd.format(band = band, model = model, 
                                      argument = 'a.m_tot = a.m_bulge ', 
                                      condition = '')
                print cmd
                cursor.execute(cmd)
            elif model in ['serexp','devexp']:
                cmd = base_cmd.format(band = band, model = model, 
                                      argument = 'a.m_tot = -2.5*log10(pow(10,-0.4*a.m_bulge)+pow(10,-0.4*a.m_disk))', condition = '')
                print cmd
                cursor.execute(cmd)
            
            # now do Galsky
            cmd = base_cmd.format(band = band, model = model, 
                         argument = 'a.Galsky = -2.5*log10(b.Galsky/pow(0.396,2))-c.aa_{band}-c.kk_{band}*c.airmass_{band} '.format(band=band) , condition = ' and a.%s < 0 and b.%s < 9900' %(val[0],val[1]))
            print cmd
            cursor.execute(cmd)

            cmd = base_cmd.format(band = band, model = model, 
                       argument = 'a.Galsky_err = 2.5/log(10)*b.Galsky_err/b.Galsky'.format(band=band) , condition = ' and a.%s < 0 and b.%s < 9900' %(val[0],val[1]))
            print cmd
            cursor.execute(cmd)
            
        return

build_tables(bands, models)
load_fit_uncalc(bands, models)
load_fit_calc(bands, models[:])
load_model_uncalc(bands, models)
load_model_calc(bands, models)
