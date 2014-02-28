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


def build_tables(bands, models, new_tablestem = 'band'):
    for band in bands:
        cmd = """create table {band}_{new_tablestem}_fit (galcount int primary key, 
    rowcount int default -999,  objid_dr8 bigint default -999, 
    model varchar(10));
    """.format(band = band, new_tablestem = new_tablestem)
        print cmd
        cursor.execute(cmd)

        cmd = 'insert into {band}_{new_tablestem}_fit (galcount) select galcount from Lackner.Lackner_DR8 where galcount >0 order by galcount;'.format(band=band, new_tablestem = new_tablestem)
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
            cmd = """insert into {band}_{new_tablestem}_{model} (galcount) select galcount from Lackner.Lackner_DR8 where galcount > 0 order by galcount;""".format(band = band, model = model, new_tablestem=new_tablestem)
            print cmd
            cursor.execute(cmd)

    return

def load_fit_uncalc(bands, models, old_tablestem='full_dr7', new_tablestem='band'):
     for band in bands:
         base_cmd = """update {band}_{new_tablestem}_fit as a, Lackner.Lackner_DR8 as b set {argument} where a.galcount = b.galcount;"""
             
         cmd = base_cmd.format(band = band, new_tablestem = new_tablestem,
                               argument = 'a.rowcount = b.rowcount, a.objid_dr8=b.objid_dr8, a.model=b.model ')
         print cmd
         cursor.execute(cmd)
     return


def load_model_uncalc(bands, models, old_tablestem='', new_tablestem='lackner'):
    
    for band in bands:
        for model in models:
            if model in ['nb1','nb4']:
                params_to_copy = [['BT', 'BULGE_TO_TOT_%s' %band],
                                  ['m_bulge_err', 'BULGE_MAG_%s_ERR' %band],
                                  ['r_bulge','BULGE_RE'],
                                  ['r_bulge_err','BULGE_RE_ERR'],
                                  ['ba_bulge', 'BULGE_Q'],
                                  ['ba_bulge_err','BULGE_Q_ERR'],
                                  ['pa_bulge', 'BULGE_PHI'],
                                  ['pa_bulge_err','BULGE_PHI_ERR'],
                                  ['m_disk_err', 'DISK_MAG_%s_ERR' %band],
                                  ['r_disk','DISK_R0'],
                                  ['r_disk_err','DISK_R0_ERR'],
                                  ['ba_disk', 'DISK_Q'], 
                                  ['ba_disk_err','DISK_Q_ERR'],
                                  ['pa_disk', 'DISK_PHI'],
                                  ['pa_disk_err','DISK_PHI_ERR'],
                                  ['chi2nu', 'CHI_SQ_R'] ]
                if model == 'nb1':
                    params_to_copy.append(['a.n_bulge', '1.0'])
                elif model == 'nb4':
                    params_to_copy.append(['a.n_bulge', '4.0'])


            elif model == 'exp':
                params_to_copy = [['a.BT', '0.0' ],
                                  ['a.m_disk_err', 'b.TOTAL_MAG_%s_ERR' %band],
                                  ['a.r_disk','b.RE'],
                                  ['a.r_disk_err','b.RE_ERR'],
                                  ['a.ba_disk', 'b.AXIS_Q'], 
                                  ['a.ba_disk_err','b.AXIS_Q_ERR'],
                                  ['a.pa_disk', 'b.PHI'],
                                  ['a.pa_disk_err','b.PHI_ERR'],
                                  ['a.chi2nu', 'b.CHI_SQ_R'],
                                  ['a.n_bulge', '1.0']]

            else:
                params_to_copy = [ ['a.BT', '1.0'],
                                  ['a.m_bulge_err', 'b.TOTAL_MAG_%s_ERR' %band],
                                  ['a.r_bulge','b.RE'],
                                  ['a.r_bulge_err','b.RE_ERR'],
                                  ['a.ba_bulge', 'b.AXIS_Q'],
                                  ['a.ba_bulge_err','b.AXIS_Q_ERR'],
                                  ['a.pa_bulge', 'b.PHI'],
                                  ['a.pa_bulge_err','b.PHI_ERR'],
                                  ['a.chi2nu', 'b.CHI_SQ_R'],
                                  ['a.Hrad_corr','b.RE*sqrt(b.AXIS_Q)'] ]

                if model == 'dvc':
                    params_to_copy.append(['a.n_bulge', '4.0'])
                elif model == 'ser':
                    params_to_copy.append(['a.n_bulge', 'b.SERSIC_INDEX'])
                    params_to_copy.append(['a.n_bulge_err', 'b.SERSIC_INDEX_ERR'])

            base_cmd = """update {band}_{new_tablestem}_{model} as a, Lackner.{model} as b, Lackner.Lackner_DR8 as c set {argument} where a.galcount = c.galcount and c.rowcount = b.rowcount;"""
             
             # now do params
            for val in params_to_copy:
                cmd = base_cmd.format(band = band, model = model,  
                                      new_tablestem = new_tablestem,
                                      argument='%s = %s ' %(val[0],val[1]))
                print cmd
                cursor.execute(cmd)
    
            #if model=='exp':
            #    base_cmd = """update {band}_{new_tablestem}_{model} set r_disk=1.678*r_disk,r_disk_err=1.678*r_disk_err;"""
            #    cmd = base_cmd.format(band = band, model = model,  
            #                          new_tablestem = new_tablestem)
            #    print cmd
            #    cursor.execute(cmd)
    return

def load_model_calc(bands, models, old_tablestem='lackner', new_tablestem='lackner'):
    for band in bands:
        for model in models:
            if model in ['nb1','nb4']:
                mags_to_copy = [['a.m_tot','b.TOTAL_MAG_{band} +c.extinction_{band} + d.kcorr_{band}+d.dismod'.format(band=band)],
                                ['a.m_bulge','b.BULGE_MAG_{band} +c.extinction_{band} + d.kcorr_{band}+d.dismod'.format(band=band)],
                                ['a.m_disk', 'b.DISK_MAG_{band} +c.extinction_{band} + d.kcorr_{band}+d.dismod'.format(band=band)]
                                ]
            
            elif model =='exp': 
                mags_to_copy = [['a.m_tot','b.TOTAL_MAG_{band} +c.extinction_{band} + d.kcorr_{band}+d.dismod'.format(band=band)],
                                ['a.m_disk', 'a.m_tot']
                                ]

            else: 
                mags_to_copy = [['a.m_tot','b.TOTAL_MAG_{band} +c.extinction_{band} + d.kcorr_{band}+d.dismod'.format(band=band)],
                                ['a.m_bulge', 'a.m_tot']
                                ]


            base_cmd = """update {band}_{new_tablestem}_{model} as a, Lackner.{model} as b, CAST as c, DERT as d, Lackner.Lackner_DR8 as f set {argument} where a.galcount = f.galcount and c.galcount = a.galcount and c.galcount = d.galcount and f.rowcount = b.rowcount {condition};"""
            # now do mags
            for val in mags_to_copy:
                cmd = base_cmd.format(band = band, model = model, old_tablestem = old_tablestem, 
                                       new_tablestem = new_tablestem,
                         argument = '{val1} = {val2} '.format(val1=val[0],val2=val[1]), condition = ' and %s < 0 and %s between 0 and 990' %(val[0],val[1]))
                print cmd
                cursor.execute(cmd)

            
    return

bands = 'gri'
models = ['dvc', 'exp', 'ser', 'nb4', 'nb1']

#build_tables(bands, models, new_tablestem='lackner')
#load_fit_uncalc(bands, models,old_tablestem='', new_tablestem='lackner')
load_model_uncalc(bands, models,old_tablestem='', new_tablestem='lackner')
#load_model_calc(bands, models,old_tablestem='', new_tablestem='lackner')
