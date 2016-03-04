#!/data2/home/ameert/python/bin/python2.5

from mysql_class import *
import os

sample_size = 250

cursor = mysql_connect('MANGA', 'pymorph', 'pymorph9455')

print 'Beginning Creating cat'

for subnum in range(1,2):
    cmd = 'select galcount, z from bright34_gal where galcount > %d and galcount <= %d;' %((subnum - 1)*sample_size, subnum * sample_size)

    galcount, z = cursor.get_data(cmd)

    for fil in ['r',]:
        outfile = open('/home/ameert/Desktop/manga/cutouts/%s/%04d/sdss_%s_%04d.cat' %(fil, subnum, fil, subnum), 'w')
        outfile.write("gal_id gimg wimg star z\n")

        for cur_gal, cur_z in zip(galcount,z):
            outfile.write("%08d_%s_stamp %08d_%s_stamp.fits %08d_%s_stamp_W.fits %08d_%s_psf.fits %f\n" %(cur_gal, fil,cur_gal, fil,cur_gal, fil,cur_gal, fil, cur_z))

        outfile.close()


