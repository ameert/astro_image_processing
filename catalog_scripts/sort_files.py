from mysql_class import *
import os 
import sys
import os.path
import numpy as np

start = int(sys.argv[1])
stop = int(sys.argv[2])

band = 'r'
dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
path = '/data2/home/ameert/catalog/r/data/'
path1 = '/data2/home/ameert/catalog/r/cats/ims/'

cursor = mysql_connect(dba, usr, pwd, 'shredder')
galcount, z = cursor.get_data('select galcount, z from CAST_incomplete where galcount >= %d and galcount <= %d order by galcount;' %(start, stop))

gal_dirs = (np.array(galcount)-1)/250 + 1
# make any missing dirs
dirs_needed = list(set(gal_dirs))

for a in dirs_needed:
    if not os.path.isdir('%s/%04d' %(path, a)):
        os.system('mkdir %s/%04d' %(path, a))

prev_count = 0
for count, count_dir, cur_z in zip(galcount, gal_dirs, z):
    if count_dir != prev_count:
        try:
            a.close()
        except:
            pass
        a = open('%s/%04d/psflist.list' %(path, count_dir), 'w')
        a.write('')
        a.close()
        a = open('%s/%04d/sdss_%s_%d.cat' %(path, count_dir, band,count_dir), 'w')
        a.write('gal_id gimg wimg star z\n')
        prev_count = count_dir
    a.write('%08d_%s_stamp %08d_%s_stamp.fits %08d_%s_stamp_W.fits %08d_%s_psf.fits %f\n' %(count, band,count,  band,count,  band,count,  band,cur_z))

a.close()

# now sort files
for count, count_dir in zip(galcount, gal_dirs):
    for curf in ['r_psf.fits', 'r_stamp.fits', 'r_stamp_W.fits']:
        if os.path.isfile('%s/%08d_%s' %(path1, count, curf)):
            os.system('mv %s/%08d_%s %s/%04d/' %(path1, count, curf, path, count_dir))
    if count % 250 == 0:
        print count




                
