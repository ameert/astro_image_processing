from astro_image_processing import mysql
from astro_image_processing.user_settings import *
import pyfits as pf
import numpy as np
from scipy import integrate
import sys
from cosmocal import *

dir = '/home/clampitt/filaments/spatial_cats/'
patches = np.arange(0, 34, 1)
tablename="LRG_pairs"
H0 = 100.0
WM = 0.3
WV = 0.7
pixelscale = 1.0 #set to 1 in order to return kpc/arcsec instead of kpc/pix


#connect to the database
cursor = mysql.mysql_connect('LRGPairs',mysql_params['user'],
                             mysql_params['pwd'], mysql_params['host'],
                             autocommit=False)

#prepare a new table
cursor.execute("DROP TABLE IF EXISTS %s;" %tablename)
cursor.execute("CREATE TABLE %s (id int primary key auto_increment, ra_mid float default -999, dec_mid float default -999, z float default -999, id1 int default -999, ra1 float default -999, dec1 float default -999, id2 int default -999, ra2 float default -999, dec2 float default -999, R_pair float default -999, drlos float default -999, dz float default -999, patch int default -999, dismod float default -999, kpc_per_arcsec float default -999);" %tablename)

#commit the changes
cursor.Conn.commit()

#now load the data one patch at a time
for patch in patches:
    print('Patch number %d' % (patch))
    lensfile = 'pair-cat-nov4_LRG_Rmax24.0_rlos6.0_p%d.fit' % (patch)
    hdu = pf.open(dir + lensfile)
    data = hdu[1].data
    cmd = "insert into %s (ra_mid, dec_mid, z, id1, ra1, dec1, id2, ra2, dec2, R_pair, drlos, dz, patch, dismod, kpc_per_arcsec) values " %tablename
    count=0
    for i in data:
        try:
            dismod, kpc_per_arcsec = cal(i[2], H0, WM, WV, pixelscale)[2:4]    
        except:
            dismod, kpc_per_arcsec = [-999,-999]
        cmd+=' (%f, %f, %f, %d, %f, %f, %d, %f, %f, %f, %f, %f, %d, %f, %f) ' %(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],patch, dismod, kpc_per_arcsec)
        count+=1
        if count % 1000==0:
            print count
            cursor.execute(cmd+';')
            cmd = "insert into %s (ra_mid, dec_mid, z, id1, ra1, dec1, id2, ra2, dec2, R_pair, drlos, dz, patch, dismod, kpc_per_arcsec) values " %tablename
        else:
            cmd+=','
    hdu.close()
    cursor.Conn.commit()

