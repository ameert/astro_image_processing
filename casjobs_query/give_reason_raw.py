#!/usr/bin/python

# We are going to clean our sample similar to Simard ...

import numpy as np
import astro_image_processing.mysql as mysql
from astro_image_processing.sdss_flags import *
from astro_image_processing.user_settings import mysql_params

in_table = 'CAST_raw'

cursor = mysql.mysql_connect(mysql_params['dba'],mysql_params['user'],
                       mysql_params['pwd'],mysql_params['host'])

# first remove any galaxies not in the Legacy survey
infile = open('../allrunsdr7db.par')

for line in infile.readlines():
    if line[0] not in '#':
        try:
            line = line.split()
            run = line[1]
            rerun = line[2]
            field0 = int(line[7])
            nfield = int(line[8])
            use = line[12]

            if use != 'Legacy':
                cmd_stem = 'Update %s set disqual_flag = 1 where run = %s and rerun = %s and field= ' %(in_table, run, rerun)

                for curf in range(field0, field0+nfield):
                    cmd = cmd_stem + str(curf) + ';'
                    print cmd
                    cursor.execute(cmd)
                    
        except:
            pass

conditions = ['redshift < 0.005 or redshift > 1', '-2.5*log10(pow(10, -0.4*petromag_r)/(pow(petroR50_r, 2.0)*3.14159)) >= 23.0', '(badflag & %d) != 0 ' %sdss_flag['DEBLENDED_AS_PSF'], '(badflag & %d) != 0 ' %sdss_flag['SATURATED']]
flags = [2,4,8,16]

cmd_stem = 'Update %s set disqual_flag = disqual_flag + {flagval} where ' %in_table

for con, flag in zip(conditions, flags):
    cmd = cmd_stem + con + ';'
    cmd = cmd.format(flagval=flag)
    print cmd
    cursor.execute(cmd)
    





 
