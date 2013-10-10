from mysql_class import *
import numpy as np
import healpy as hp
from create_healpy_map import *

dba = 'catalog'
pwd = 'visitor'
usr = 'visitor'
    
cursor = mysql_connect(dba, usr, pwd)

tablename = 'CAST'
NSIDE = 256

cmd = "create table %s_healpy (galcount int primary key, ra_gal float default -999, dec_gal float default -999, healpix int default -999);" %(tablename)
#cursor.execute(cmd)

cmd = "create table %s_healpy_info (healpix int primary key, start_count int default -999,  end_count int default -999);" %(tablename)
#cursor.execute(cmd)

cmd = 'insert into %s_healpy (galcount, ra_gal, dec_gal) select galcount, ra_gal, dec_gal from %s;' %(tablename, tablename) 
#cursor.execute(cmd)

cmd = 'select galcount, ra_gal, dec_gal from %s_healpy;' %(tablename)
galcount, ra, dec = cursor.get_data(cmd)

cat1 = catalog(galcount, ra, dec, NSIDE=256)
cat1.map_sample()

for a, b in zip(cat1.galcount, cat1.pix):
    cmd = 'update %s_healpy set healpix = %d where galcount = %d;' %(tablename, b,a)
    cursor.execute(cmd)

for b in cat1.pix_info.items():
    cmd = 'insert ignore into %s_healpy_info (healpix,start_count, end_count) values (%d, %d, %d);' %(tablename, b[0], b[1][0],b[1][1])
    cursor.execute(cmd)
    
