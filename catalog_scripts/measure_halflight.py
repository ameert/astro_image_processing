#!/data2/home/ameert/python/bin/python2.5

from image_info import *
import numpy as np
import os
from mysql_class import *
import pyfits as pf
import sys
from util_funcs import *
#from measure_bkrd import *

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
cursor = mysql_connect(dba, usr, pwd, 'shredder')

table_name = sys.argv[1]
model = sys.argv[2]

cmd = 'Alter ignore table %s add column (alan_hrad_pix float default -999);' %table_name

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
    galcount = int(Name.split('_')[1])
    inimage= pf.open(line)
    data = inimage[4].data
    cmd = "select abs(Ie), abs(Id), magzp from %s where galcount = %d;" %(table_name, galcount)

    Ie, Id, zp = cursor.get_data(cmd)

    if len(Ie)==0:
        continue
    try:
        tot_mag, bt = mag_sum(Id[0], Ie[0])
        tot_counts = mag_to_counts( float(tot_mag), float(-zp[0]))/ 53.907456
        if model in ['devexp','serexp']:
            data += inimage[5].data
        dat_info = image_info(data, mask = 'threshold')    
        hrad = dat_info.halflight(tot_counts)
        inimage.close()
    except IndexError:
        hrad = (-999, -999)
    print hrad[0], hrad[1]/tot_counts

            
    cmd = "update %s set alan_hrad_pix = %f where galcount = %d;" %(table_name,hrad[0], galcount)
    
    cursor.execute(cmd)
infile.close()

os.system('rm %s' %list_fn)
    
    

