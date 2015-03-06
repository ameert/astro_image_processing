#!/data2/home/ameert/python/bin/python2.5

from image_info import *
import numpy as np
import os
import os.path
from mysql_class import *
import pyfits as pf
import sys
from util_funcs import *

def move_masks(model):
    thisdir = os.getcwd()
    targetdir = thisdir.split('/')
    targetdir[-2] = 'masks'
    targetdir = '/'.join(targetdir)

    if not os.path.isdir(targetdir):
        os.system('mkdir '+targetdir)

    os.system('mv %s/[EM]*.fits %s/' %(thisdir, targetdir))
    
    return

table_name = sys.argv[1]
model = sys.argv[2]
job_num = int(sys.argv[3])

#os.chdir('./%04d' %job_num)
curr_dir = os.getcwd()

# make sure the catalog is loaded to the the mysql table
os.system('python2.5 /data2/home/ameert/catalog/scripts/load_cat.py %s %s' %(table_name, curr_dir+'/result.csv'))


dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
cursor = mysql_connect(dba, usr, pwd, 'shredder')

#os.chdir('./highN_%04d' %job_num)

cmd = 'Alter ignore table %s add column (hrad_pix_psf float default -999);' %table_name

try:
    cursor.execute(cmd)
except:
    pass

list_fn = 'file.list' 
os.system('ls ./O_*.fits > %s' %(list_fn))
            
infile = open(list_fn)
for line in infile:
    line = line.strip()
    
    Name = line.split('/')[-1].split('O_')[1].split('.fits')[0]
    
    inimage= pf.open(line)
    data = inimage[4].data
    cmd = "select abs(Ie), abs(Id), magzp from %s where Name = '%s';" %(table_name, Name)
    print cmd 
    Ie, Id, zp = cursor.get_data(cmd)
    try:
        tot_mag, bt = mag_sum(Id[0], Ie[0])
        tot_counts = mag_to_counts( float(tot_mag), float(-zp[0]))/ 53.907456
        if model in ['devexp','serexp']:
            data += inimage[5].data
        dat_info = image_info(data, mask = 'threshold')    
        hrad = dat_info.halflight(tot_counts)
        inimage.close()
    except (IndexError, ZeroDivisionError):
        hrad = (-999, -999)
        tot_counts = 1
    print hrad[0], hrad[1]/tot_counts

            
    cmd = "update %s set hrad_pix_psf = %f where Name = '%s';" %(table_name,hrad[0], Name)
    
    cursor.execute(cmd)
infile.close()

os.system('rm %s' %list_fn)
    
# now clean the directory
os.system('/data2/home/ameert/grid_scripts/clean_dir.py')
# and move the masks
move_masks(model)


#import os
#for count in range(1,2684):
#  os.chdir('/data2/home/ameert/catalog/g/fits/dev/%04d' %count)
#  os.system('python2.5 /data2/ameert/home/catalog/scripts/measure_and_clean.py full_dr7_g_dev dev %d' %count)
