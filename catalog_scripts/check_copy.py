from mysql_class import *
import os 
import sys
import os.path
import numpy as np

band = 'r'
dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
path = '/data2/home/ameert/catalog/r/data/'
path1 = '/data2/home/ameert/catalog/short_sample/r/data/'
bad_count = 0

cursor = mysql_connect(dba, usr, pwd, 'shredder')
galcount, cat_count, gal_dirs = cursor.get_data('select a.galcount, a.cat_count, (a.galcount -1)/250 +1 from CAST_incomplete as a left join full_dr7_r_serexp as b on a.galcount = b.galcount  where b.galcount is NULL;' )

outfile = open('to_source', 'w')

for count, in_dir, out_dir in zip(galcount, gal_dirs, cat_count):
    # now sort files
    for curf in ['r_psf.fits', 'r_stamp.fits', 'r_stamp_W.fits']:
        if not os.path.isfile('%s/%04d/%08d_%s' %(path1, out_dir,count, curf)):
            outfile.write('cp %s/%04d/%08d_%s %s/%04d/ \n' %(path, in_dir, count, curf, path1, out_dir))
                          
            bad_count +=1

outfile.close()
print len(galcount)
print bad_count/3
