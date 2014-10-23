
#####
# calculates  the distance modulus and angular scale (kpc_per_arcsec)
# and inserts them into the DERT

import os 
import sys
import numpy as np 

from cosmocal import *
from astro_image_processing.mysql import *

H0 = 73.0
WM = 0.25
WV = 0.75
pixelscale = 1.0 #set to 1 in order to return kpc/arcsec instead of kpc/pix

table_name = 'corr_lum_func_CMASS'
dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'

gal = {}

cursor = mysql_connect(dba, usr, pwd, autocommit=False)

cmd = 'select a.thing_id, a.zspec from %s as a where  a.zspec > 0 and a.dismod is NULL;' %table_name
select thing_id, zgal from  group by thing_id;
galcount, z =  cursor.get_data(cmd)

count = 0




for gal, gz in zip(galcount, z):
    flag = 0
    if gz > 0:
        try:
            dismod, kpc_per_arcsec = cal(gz, H0, WM, WV, pixelscale)[2:4]    
        except:
            print 'bad gal %d with z %f ... skipping ' %(gal, gz)
            sys.exit()
    else:
        dismod = 0
        kpc_per_arcsec = 0


    cmd = 'update %s set dismod = %f, kpc_per_arcsec = %f where thing_id = %d;' %(table_name, dismod, kpc_per_arcsec, gal)
    #print cmd
    cursor.execute(cmd)
    count+=1
    if count % 10000 ==0:
        print count
        cursor.Conn.commit()

cursor.Conn.commit()
