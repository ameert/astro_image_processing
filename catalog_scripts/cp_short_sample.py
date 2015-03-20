from mysql_class import *
import os 
import sys
import os.path
import numpy as np

#start = int(sys.argv[1])
#stop = int(sys.argv[2])

band = 'r'
dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
path = '/data2/home/ameert/catalog/r/data/'
path1 = '/data2/home/ameert/catalog/gama/r/data/'

cursor = mysql_connect(dba, usr, pwd, 'shredder')
#galcount, gal_dirs = cursor.get_data('select a.galcount, (a.galcount -1)/250 +1 from CAST_incomplete as a;' )
#galcount, gal_dirs = cursor.get_data('select a.galcount, (a.galcount -1)/250 +1 from full_dr7_r_serexp as a where a.fitflag & pow(2, 8);' )
galcount, gal_dirs = cursor.get_data('select a.galcount, (a.galcount -1)/250 +1 from CAST a , GAMA as b where a.galcount = b.galcount;' )

for count, in_dir in zip(galcount, gal_dirs):
    # now sort files
    for curf in ['r_psf.fits', 'r_stamp.fits', 'r_stamp_W.fits']:
        os.system('cp %s/%04d/%08d_%s %s/' %(path, in_dir, count, curf, path1))





                
