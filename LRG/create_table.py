from astro_image_processing import mysql
import pyfits as pf
import numpy as np
from scipy import integrate
import sys

dir = '/home/clampitt/filaments/spatial_cats/'
patches = np.arange(1, 2, 1)
tablename="LRG_pairs";

#connect to the database
cursor = mysql.mysql_connect('LRGPairs',mysql_params['user'],
                             mysql_params['pwd'], mysql_params['host'],
                             autocommit=False)

#prepare a new table
cursor.execute("DROP TABLE IF EXISTS %s;" %tablename)
cursor.execute("CREATE TABLE %s (id int primary key auto_increment, ra_mid float default -999, dec_mid float default -999, z float default -999, id1 int default -999, ra1 float default -999, dec1 float default -999, id2 int default -999, ra2 float default -999, dec2 float default -999, R_pair float default -999, drlos float default -999, dz float default -999, patch int defualt -999, dismod float -999, kpc_per_arcsec float -999);" %tablename)

#commit the changes
cursor.Conn.commit()

#now load the data one patch at a time
for patch in patches:
    print('Patch number %d' % (patch))
    cmd = "insert into %s (ra_mid, dec_mid, z, id1, ra1, dec1, id2, ra2, dec2, R_pair, drlos, dz, patch) values " %tablename
    lensfile = 'pair-cat-nov4_LRG_Rmax24.0_rlos6.0_p%d.fit' % (patch)
    hdu = pf.open(dir + lensfile)
    data = hdu[1].data
    print hdu[1].header
    for i in data:
        cmd+= '(%f, %f, %f, %d, %f, %f, %d, %f, %f, %f, %f, %f, %d),'  %(*i, patch)
    hdu.close()
    cmd[-1]=';'
    cursor.execute(cmd)
    cursor.Conn.commit()

