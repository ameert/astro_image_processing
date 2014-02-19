#!/usr/bin/python

# We are going to clean our sample similar to Simard ...

from mysql_class import *
import numpy as np
from sdss_flags import *

in_table = 'CAST_raw'
out_table = 'CAST'
outfile = 'results.txt'

cursor = mysql_connect('catalog', 'pymorph', 'pymorph')

# first remove any galaxies not in the Legacy survey
infile = open('allrunsdr7db.par')

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
                cmd_stem = 'delete from %s where run = %s and rerun = %s and field= ' %(in_table, run, rerun)

                for curf in range(field0, field0+nfield):
                    cursor.execute(cmd_stem + str(curf) + ';')
                    
        except:
            pass

conditions = []
# construct our conditions ...

# we want z to exist and for it to not be contaminated by the 
# peculiar velocity of the galaxy
# we also want the redshift to make sense...
conditions.append('redshift between 0.005 and 1')

# we want to only retain galaxies above the 23 mag / arcsec^2 surface 
# brightness cutoff so that the sample is complete
conditions.append('-2.5*log10(pow(10, -0.4*petromag_r)/(pow(petroR50_r, 2.0)*3.14159)) < 23.0')

# We also would like to remove galaxies that are possibly stars and those that have saturated pixels
conditions.append('(badflag & %d) = 0 ' %sdss_flag['DEBLENDED_AS_PSF'])
conditions.append('(badflag & %d) = 0 ' %sdss_flag['SATURATED'])

fop = open(outfile, 'w')

fop.write('# This file contains the number of galaxies with each bad condition\n')
fop.write('# conditon     number\n')

cmd_stem = 'select count(*) from %s where ' %in_table

for con in conditions:
    a, = cursor.get_data(cmd_stem + con + ';')
    fop.write(con + '\t' +str(a[0])+'\n')

a, = cursor.get_data(cmd_stem + ' and '.join(conditions) + ';')
fop.write('all conditions' + '\t' +str(a[0])+'\n')

a, = cursor.get_data('select count(*) from %s;' %in_table)
fop.write('raw number' + '\t' +str(a[0])+'\n')

fop.close()

cmd = 'create table %s like %s;' %(out_table, in_table)
cursor.execute(cmd)

# now trim the table
cmd = 'insert into %s select * from %s where %s;' %(out_table, in_table, ' and '.join(conditions))
cursor.execute(cmd)

# now change the pirmary key (objid) to a unique key
cmd = 'alter table %s drop primary key;' %out_table
cursor.execute(cmd)
cmd = 'alter table %s add unique key (objid);' %out_table
cursor.execute(cmd)

# now add in a 'galcount' column and rename redshift to z
cmd = 'alter table %s change column redshift z float default -888;' %out_table
cursor.execute(cmd)

cmd = 'alter table  %s add column galcount int not null primary key auto_increment first;' %out_table
cursor.execute(cmd)

#converts maggies/arcsec^2 to mags/arcsec^2 and converts error
for band in 'ugriz':
    cmd = 'Update CAST set skyErr_%s = 2.5/log(10) *skyErr_%s/sky_%s;' %(band,band, band)
    cursor.execute(cmd)
    
    cmd = 'Alter table CAST drop column skySig_%s;' %band
    cursor.execute(cmd)
    
    cmd = 'Update CAST set sky_%s = 22.5 - 2.5*log10(sky_%s);' %(band, band)
    cursor.execute(cmd)





 
