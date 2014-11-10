#!/data2/home/ameert/python/bin/python2.5

import numpy as np
import os
from mysql_class import *
import sys
from hrad_funcs import *

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
cursor = mysql_connect(dba, usr, pwd, 'shredder')

table_name = sys.argv[1]
model = table_name.split('_')[-1]
try:
    mode = sys.argv[2]
except:
    mode = 'corr'

tot_stem = os.getcwd()#'/data2/home/ameert/regen_galfit/'

cmd = 'Alter ignore table %s add column (hrad_pix_%s float default -999);' %(table_name, mode)
try:
    cursor.execute(cmd)
except:
    pass
cmd = 'Alter ignore table %s add column (hrad_ba_%s float default -999);' %(table_name, mode)
print cmd
try:
    cursor.execute(cmd)
except:
    pass

#os.system('ls %s/O_*no_psf.fits > file.list' %(tot_stem))
os.system('ls %s/O_*.fits > file.list' %(tot_stem))
            
infile = open('file.list' )
for line in infile:
    print line
    line = line.strip()
    galcount = int(line.split('/')[-1].split('_')[2])

    tot_counts = get_gal_info(cursor, table_name, galcount, count_name = 'galcount', zp_name = 'magzp')#/ 53.907456
    print "tot_counts ", tot_counts
    if 1:
        if model in ['ser', 'dev', 'exp']:
            hrad = get_hrad(line, tot_counts, to_sum = [4])
        else:
            hrad = get_hrad(line, tot_counts, to_sum = [4,5])

        hrad = [a if not np.isnan(a) else -999.0 for a in hrad]
    
        cmd = 'update %s set hrad_pix_%s = %f, hrad_ba_%s =%f where galcount = %d;' %(table_name,mode,hrad[0], mode, hrad[2], galcount)
        print cmd
        cursor.execute(cmd)
    #except:
    #    pass
infile.close()

#os.system('rm file.list')
    
    

