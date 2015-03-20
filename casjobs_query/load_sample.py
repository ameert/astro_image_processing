#!/usr/bin/python

import numpy as np
astro_image_processing.mysql import load_table
import astro_image_processing.mysql as mysql
from astro_image_processing.sdss_flags import *
from astro_image_processing.user_settings import mysql_params

infile = '../spectro_sample.cat'
table_name = 'CAST_raw'

cursor = mysql.mysql_connect(mysql_params['dba'],mysql_params['user'],
                       mysql_params['pwd'],mysql_params['host'])

columns = ['objid','badflag','nchild',
'run','rerun','camCol','field','obj','stripe','startmu',
'specobjid','plate','mjd','fiberid','ra_gal','dec_gal',
'redshift','veldisp','veldispErr','eclass',
'p_el_debiased','p_cs_debiased','spiral','elliptical','uncertain',
'petroR90_u','petroR90_g','petroR90_r','petroR90_i','petroR90_z',
'petroR50_u','petroR50_g','petroR50_r','petroR50_i','petroR50_z',
'petroMag_u','petroMag_g','petroMag_r','petroMag_i','petroMag_z',
'devRad_u','devRad_g','devRad_r','devRad_i','devRad_z',
'devab_u','devab_g','devab_r','devab_i','devab_z',
'devmag_u','devmag_g','devmag_r','devmag_i','devmag_z',
'fracdev_u','fracdev_g','fracdev_r','fracdev_i','fracdev_z',
'dered_u','dered_g','dered_r','dered_i','dered_z',
'extinction_u','extinction_g','extinction_r','extinction_i','extinction_z',
'aa_u','aa_g','aa_r','aa_i','aa_z',
'kk_u','kk_g','kk_r','kk_i','kk_z',
'airmass_u','airmass_g','airmass_r','airmass_i','airmass_z',
'gain_u','gain_g','gain_r','gain_i','gain_z',
'darkvariance_u','darkvariance_g','darkvariance_r','darkvariance_i','darkvariance_z',
'sky_u','sky_g','sky_r','sky_i','sky_z',
'skySig_u','skySig_g','skySig_r','skySig_i','skySig_z',
           'skyErr_u','skyErr_g','skyErr_r','skyErr_i','skyErr_z',
'psfWidth_u','psfWidth_g','psfWidth_r','psfWidth_i','psfWidth_z',
'rowc_u','rowc_g','rowc_r','rowc_i','rowc_z',
'colc_u','colc_g','colc_r','colc_i','colc_z']

column_types = ['bigint primary key', 'bigint','smallint',
'smallint','smallint','smallint','smallint','smallint','int','int',
'bigint','smallint','int','smallint','float','float',
'float','float','float','float',
'float ','float','int','int','int',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
'float','float','float','float','float',
]

load_table(cursor, table_name, infile, columns, column_types)


for band in 'ugriz':
    #cmd = 'Update CAST_raw set skyErr_%s = 2.5/log(10) *skyErr_%s/sky_%s;' %(band,band, band)
    #cursor.execute(cmd)
    
    #cmd = 'Alter table CAST_raw drop column skySig_%s;' %band
    #cursor.execute(cmd)
    
    #cmd = 'Update CAST_raw set sky_%s = 22.5 - 2.5*log10(sky_%s*pow(10,9));' %(band, band)
   # cursor.execute(cmd)
    pass
