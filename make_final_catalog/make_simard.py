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
models = ['ser','devexp','serexp']

def build_tables(bands, models, new_tablestem = 'simard'):
    for band in bands:
        cmd = """create table {band}_{new_tablestem}_fit (galcount int primary key, 
    Vmax float default -999, kpc_per_arcsec float default -999, 
    Smoothness float default -999, Prob_pS float default -999,
    Prob_n4 float default -999);
    """.format(band = band, new_tablestem = new_tablestem)
        print cmd
        cursor.execute(cmd)

        cmd = 'insert into {band}_{new_tablestem}_fit (galcount) select galcount from CAST order by galcount;'.format(band=band, new_tablestem = new_tablestem)
        print cmd
        cursor.execute(cmd)

        for model in models:
            cmd = """create table {band}_{new_tablestem}_{model} (galcount int primary key, 
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
    Comments varchar(1000));""".format(band = band, model = model, new_tablestem=new_tablestem)
            print cmd
            cursor.execute(cmd)
            cmd = """insert into {band}_{new_tablestem}_{model} (galcount) select galcount from CAST order by galcount;""".format(band = band, model = model, new_tablestem=new_tablestem)
            print cmd
            cursor.execute(cmd)

    return

def load_fit_uncalc(bands, models, old_tablestem='simard', new_tablestem='simard'):
     for band in bands:
         for model in models:
             base_cmd = """update {band}_{new_tablestem}_fit as a, simard.{old_tablestem}_{model} as b set {argument} where a.galcount = b.galcount {condition};"""
             # now do everything
             for val in [('Vmax','V_max'), ('kpc_per_arcsec','kpc_per_arcsec'),
                         ('Smoothness','s2_%s' %band)]:
                 cmd = base_cmd.format(band = band, model = model, old_tablestem = old_tablestem, 
                                       new_tablestem = new_tablestem, 
                                       argument = 'a.%s = b.%s ' %(val[0],val[1]), 
                        condition = ' and a.%s < 0 and b.%s < 9900' %(val[0],val[1]))
                 print cmd
                 cursor.execute(cmd)
             # now do the f_test probability
             if model =='serexp':
                 for val in [('Prob_pS','f_test_ser'), 
                             ('Prob_n4','f_test_devexp')]:
                     cmd = base_cmd.format(band = band, model = model, 
                                           old_tablestem = old_tablestem, 
                                           new_tablestem = new_tablestem, 
                                   argument = 'a.%s = b.%s ' %(val[0],val[1]), 
                                           condition = '' )
                 print cmd
                 cursor.execute(cmd) 
     return


def load_model_uncalc(bands, models, old_tablestem='full_dr7', new_tablestem='band'):
    for band in bands:
        for model in models:
            params_to_copy = [['m_tot', 'mag_%s_tot' %band],
                              ['BT', 'BT_%s' %band],
                              ['n_bulge','n'],
                              ['pa_bulge', 'bpa']]
            if model in ['devexp', 'serexp']:
                params_to_copy += [['pa_disk', 'dpa']]
                       
            base_cmd = """update {band}_{new_tablestem}_{model} as a, simard.{old_tablestem}_{model} as b set {argument} where a.galcount = b.galcount {condition};"""

             # now do params
            for val in params_to_copy:
                cmd = base_cmd.format(band = band, model = model, old_tablestem = old_tablestem, 
                                      new_tablestem = new_tablestem,
                                      argument = 'a.%s = b.%s ' %(val[0],val[1]), 
                                      condition = ' and a.%s <= 0 and b.%s < 9900' %(val[0],val[1]))
                print cmd
                cursor.execute(cmd)
    return

def load_model_calc(bands, models, old_tablestem='simard', new_tablestem='simard'):
    
    for band in bands:
        rads_to_copy = [['Hrad_corr','re_cir_hl_%s' %band], 
                        ['r_bulge','re_kpc'],
                        ['r_disk','rd_kpc']]

        for model in models:
            base_cmd = """update {band}_{new_tablestem}_{model} as a, simard.{old_tablestem}_{model} as b, CAST as c, simard.simard_bkrd as d set {argument} where a.galcount = b.galcount and c.galcount = a.galcount and d.objid = b.objid {condition};"""
            # now do rads
            for val in rads_to_copy:
                cmd = base_cmd.format(band = band, model = model, old_tablestem = old_tablestem, 
                                       new_tablestem = new_tablestem,
                                    argument = 'a.%s = b.%s/b.kpc_per_arcsec ' %(val[0],val[1]),
                   condition = ' and a.%s < 0 and b.%s < 9900' %(val[0],val[1]))
                print cmd
                cursor.execute(cmd)

            # now do mags
            if model == 'ser':
                cmd = base_cmd.format(band = band, model = model, 
                                      old_tablestem = old_tablestem, 
                                      new_tablestem = new_tablestem,
                         argument = 'a.m_bulge = a.m_tot, a.m_disk = 9999.0 ',
                                      condition = '')
                
            else:
                cmd = base_cmd.format(band = band, model = model, 
                                      old_tablestem = old_tablestem, 
                                      new_tablestem = new_tablestem,
                         argument = 'a.m_bulge = ifnull(a.m_tot-2.5*log10(a.BT), 9999), a.m_disk = ifnull(a.m_tot-2.5*log10(1.0-a.BT), 9999.0)',
                                      condition = '')
            print cmd
            cursor.execute(cmd)

            # ellipticty    
            cmd = base_cmd.format(band = band, model = model, 
                                  old_tablestem = old_tablestem, 
                                  new_tablestem = new_tablestem,
                                  argument = 'a.ba_tot_corr = pow(b.re_cir_hl_%s/re_hl_%s, 2.0) ' %(band,band),condition = '')
            print cmd
            cursor.execute(cmd)
            
            if model in ['ser', 'dev']:
                params_to_copy = [ ['ba_bulge', 'b.eb']]    
            elif model in ['serexp','devexp', 'cmodel']: 
                params_to_copy = [ ['ba_bulge', 'b.eb'],['ba_disk', '1.0+cos(radians(b.id))']]

            for val in params_to_copy:
                print val
                cmd = base_cmd.format(band = band, model = model, 
                                      old_tablestem = old_tablestem, 
                                      new_tablestem = new_tablestem,
                                      argument = 'a.%s = 1.0-%s ' %(val[0],val[1]),
                                      condition = '')
                print cmd
                cursor.execute(cmd)
            
            # now do sky
            cmd = base_cmd.format(band = band, model = model, 
                                  old_tablestem = old_tablestem, 
                                  new_tablestem = new_tablestem,
                         argument = 'a.Galsky = -2.5*log10(d.sky_counts_{band}/(53.907456*pow(0.396,2)))-c.aa_{band}-c.kk_{band}*c.airmass_{band} '.format(band=band),
                                  condition = '')
            print cmd
            cursor.execute(cmd)

    return

#build_tables(bands, models, new_tablestem='simard')
#load_fit_uncalc(bands, models,old_tablestem='simard', new_tablestem='simard')
#load_model_uncalc(bands, models,old_tablestem='simard', new_tablestem='simard')
load_model_calc(bands, models,old_tablestem='simard', new_tablestem='simard')
