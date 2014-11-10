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

table_name = 'sim_input'
mode = 'corr'

model = sys.argv[1]
start = int(sys.argv[2])


tot_stem = '/data2/home/ameert/make_sims/data/pix2/sim_image'

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

os.system('ls %s/*%s_flat.fits > file.list' %(tot_stem, model))
            
infile = open('file.list' )
for line in infile:
    line = line.strip()
    galcount = int(line.split('/')[-1].split('_')[0])
    if galcount not in range((start-1)*250+1, start*250 +1):
        continue
    #if galcount not in [20129]:
    #    continue
    
    tot_counts = get_gal_info(cursor, table_name, galcount, count_name = 'simcount', zp_name = 'zeropoint_sdss_r')
    print "tot counts ", tot_counts
    try:
        hrad = get_hrad(line, tot_counts, to_sum = [0])
        
        cmd = 'update %s set hrad_pix_%s = %f, hrad_ba_%s =%f where simcount = %d;' %(table_name,mode,hrad[0], mode, hrad[2], galcount)
        print cmd
        cursor.execute(cmd)
    except:
        pass
infile.close()

#os.system('rm file.list')
    
    

