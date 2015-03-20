#!/data2/home/ameert/python/bin/python2.5

from image_info import *
import numpy as np
import os
import os.path
from mysql_class import *
import pyfits as pf
import sys
from util_funcs import *

table_name = sys.argv[1]
model = sys.argv[2]
job_num = int(sys.argv[3])

curr_dir = os.getcwd()

# make sure the catalog is loaded to the the mysql table

    
# now clean the directory
os.system('/data2/home/ameert/grid_scripts/clean_dir.py')
# and move the masks


#import os
#for count in range(1,2684):
#  os.chdir('/data2/home/ameert/catalog/g/fits/dev/%04d' %count)
#  os.system('python2.5 /data2/ameert/home/catalog/scripts/measure_and_clean.py full_dr7_g_dev dev %d' %count)
