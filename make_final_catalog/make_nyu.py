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

bands = 'gi'
models = ['ser']

def build_tables(bands, models, new_tablestem = 'nyu'):
    for band in bands:
        cmd = """create table {band}_{new_tablestem}_fit (
    galcount int primary key, 
    dis_arcsec float default -999,  ID_nyu int default -999, 
    ra_nyu float default -999,  dec_nyu float default -999);
    """.format(band = band, new_tablestem = new_tablestem)
        print cmd
        cursor.execute(cmd)

        cmd = 'insert into {band}_{new_tablestem}_fit (galcount) select galcount from CAST order by galcount;'.format(band=band, new_tablestem = new_tablestem)
        print cmd
        cursor.execute(cmd)

        for model in models:
            cmd = """create table {band}_{new_tablestem}_{model} (
    galcount int primary key, 
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

def load_fit_uncalc(bands, models, new_tablestem='nyu'):
     for band in bands:
         cmd = 'UPDATE {band}_{new_tablestem}_fit as a,intermediate_tables.NYUT as b set  a.dis_arcsec=b.dis_arcsec, a.Id_nyu=b.Id_nyu, a.ra_nyu=b.ra_nyu, a.dec_nyu=b.dec_nyu where a.galcount=b.galcount;'.format(band = band, 
                                                new_tablestem = new_tablestem)
         print cmd
         cursor.execute(cmd)

     return

def load_model_calc(bands, models, new_tablestem='nyu'):
    mags_to_copy = ['m_tot','A']
    index_to_copy = ['n_bulge','n_ser']
    rads_to_copy = ['Hrad_corr', 'r_0']
    
    base_cmd = """update {band}_{new_tablestem}_{model} as a, intermediate_tables.NYUT as b set {argument} where a.galcount = b.galcount;"""
    for model in models:
    # do unconverted vals
        for band in bands:
            arg = 'a.n_bulge= b.n_ser_{band}, a.Hrad_corr = b.r0_{band}*pow(b.bn_{band}, b.n_ser_{band}) '.format(band = band)
            cmd = base_cmd.format(band=band, new_tablestem=new_tablestem,
                                  model=model, argument=arg)
            print cmd
            cursor.execute(cmd)

        # now do mags
        for band in bands:
            arg = 'a.m_tot = 22.5-2.5*log10(b.A_{band}*exp(-1.0*b.bn_{band}+b.bn_{band})*pow(a.hrad_corr,2)*2*PI()* b.n_ser_{band}*b.gamma_{band}/pow(b.bn_{band}, 2.0*b.n_ser_{band}))'.format(band = band)
            cmd = base_cmd.format(band=band, new_tablestem=new_tablestem,
                                  model = model, argument=arg)
            print cmd
            cursor.execute(cmd)

        # copy to other entries for completness
        for band in bands:
            arg = 'a.m_bulge = a.m_tot, a.r_bulge = a.Hrad_corr '.format(band = band)
            cmd = base_cmd.format(band=band, new_tablestem=new_tablestem,
                                  model = model, argument=arg)
            print cmd
            cursor.execute(cmd)


    return

build_tables(bands, models, new_tablestem='nyu')
load_fit_uncalc(bands, models, new_tablestem='nyu')
load_model_calc(bands, models[:],new_tablestem='nyu')


