#!/data2/home/ameert/python/bin/python2.5

import numpy as np
import os
from mysql_class import *
import sys
from hrad_funcs import *


print "hello!!!!!!!!!"
dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
cursor = mysql_connect(dba, usr, pwd, 'shredder')

table_name = 'sim_input_hst'
mode = 'corr'

start_num = int(sys.argv[1])-1


tot_stem = '/data2/home/ameert/hst_sims/sim_image'

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

#os.system('ls %s/*_hst_nopsf.fits > file.list' %(tot_stem))
            
infile = open('file.list' )
for line in infile.readlines()[start_num:start_num+1]:
    line = line.strip()
    galcount = int(line.split('/')[-1].split('_')[0])
    
    tot_counts = get_gal_info(cursor, table_name, galcount, count_name = 'simcount', zp_name = 'zeropoint_sdss_r')
    print "tot counts ", tot_counts
    if 1:
        #try:
        hrad = get_hrad(line, tot_counts, to_sum = [0])
        
        outfile = open('hst_rads_%d.txt' %galcount, 'w',0)
        outfile.write( '%d %f %f\n' %(galcount, hrad[0], hrad[2]))
        outfile.close()
        print '%d %f %f\n' %(galcount, hrad[0], hrad[2])
        #cmd = 'update %s set hrad_pix_%s = %f, hrad_ba_%s =%f where simcount = %d;' %(table_name,mode,hrad[0], mode, hrad[2], galcount)
        #print cmd
#        cursor.execute(cmd)
#        print "ello govnor"
    #except:
    #    pass
infile.close()

#os.system('rm file.list')
    
    

