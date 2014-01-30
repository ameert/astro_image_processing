#!/data2/home/ameert/python/bin/python2.5

from image_info import *
import os
import os.path
from mysql_class import *
import sys
from hrad_funcs import *

def move_masks(model):
    thisdir = os.getcwd()
    targetdir = thisdir.replace(model, 'masks')

    if not os.path.isdir(targetdir):
        os.system('mkdir '+targetdir)

    os.system('mv %s/*.fits %s/' %(thisdir, targetdir))
    
    return


dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
cursor = mysql_connect(dba, usr, pwd, 'shredder')

table_name = sys.argv[1]
model = table_name.split('_')[-1]

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
    
    galcount = int(line.split('/')[-1].split('_')[2])
    
    tot_counts = get_tot_counts(cursor, table_name, galcount, count_name = 'galcount', zp_name = 'magzp')
    try:
        if model == 'ser':
            hrad = get_hrad(line, tot_counts, to_sum = [4])
        else:
            hrad = get_hrad(line, tot_counts, to_sum = [4,5])
    
        cmd = 'update %s set hrad_pix_psf = %f where galcount = %d;' %(table_name,hrad[0], galcount)
        print cmd
        cursor.execute(cmd)
    except:
        pass
infile.close()

os.system('rm %s' %list_fn)
    
# now clean the directory
#os.system('/data2/home/ameert/grid_scripts/clean_dir.py')
# and move the masks
#move_masks(model)


