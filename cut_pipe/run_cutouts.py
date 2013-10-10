#!/usr/bin/python

### First the imports ####
from download_files import *
from prepare_psf import *
from cut_images import *
import os 
import sys
import numpy as np

sys.path.append('/home/ameert/python/alan_code/')
from mysql_class import *

### Now set the essential variables ###
### mysql info ###
table_name = 'CAST'
dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'
### Paths ###
data_dir = '/media/SDSS1/sdss_sample/data/'
cut_dir =  '/scratch/rerun/'
### Settings for cutouts ###
bands = 'gri' # list all desired bands in a single string
pix_scale = 0.396 # arcsec per pixel
cut_size = 20.0 # the radius of the cutout image in multiples of PetroRad50
min_size = 80.0 # minimum size in pixels
folder_size = 250 # num of galaxies/folder
folder_fmt = "%04d"

### And fetch the starting and ending points, if not supplied, it will
### try to do EVERYTHING ###
try:
    start_num = int(sys.argv[1])
except:
    start_num = -999
try:
    end_num = int(sys.argv[2])
except:
    end_num = 1000000000

if (end_num-start_num > 1000000) or start_num < 0 or end_num >999999999:
    print """-----------------------------------------------
!!!!WARNING!!!!
-----------------------------------------------
The start_num %d and/or end_num %d may be wrong. 
Hit enter to continue, otherwise type "exit" to 
quit the program.
"""
    choice = raw_input("Please enter your choice: ")

    if choice.strip() == 'exit':
        sys.exit()


gal = {}

cursor = mysql_connect(dba, usr, pwd)

### construct the query
### the first entry is the name in mysql, the second in the name for my program
table_prefix = 'a'
band_params = ['rowc','colc','petroR50','gain','darkvariance']
params = ['galcount','run','rerun','camCol','field']

cmd = 'select '+table_prefix+'.'+ (', '+table_prefix + '.').join(params)
for bp in band_params:
    for band in bands:
        cmd += ", %s.%s_%s" %(table_prefix, bp, band)

cmd += ' from %s as %s where %s.galcount >= %d and %s.galcount <= %d order by %s.galcount;' %(table_name, table_prefix, table_prefix, start_num, table_prefix, end_num, table_prefix)


### fetch data
data  =  cursor.get_data(cmd)

for tmp_data, name in zip(data, params+['%s_%s' %(tmp_param, band) for tmp_param in band_params for band in bands]):
    gal[name] = tmp_data

### group the output into directories for easier handling
gal['dir_end'] = [ folder_fmt %a for a in ((np.array(gal['galcount'])-1)/folder_size +1)]
 
### now cut the data
for band in bands:
    download_files(gal, data_dir, band)
    prepare_psf(gal, band, data_dir, cut_dir)
    cut_images(gal, band, data_dir, cut_dir, cut_size = cut_size, 
               pix_scale = pix_scale, min_size = min_size))
