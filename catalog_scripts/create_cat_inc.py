#!/data2/home/ameert/python/bin/python2.5

from mysql_class import *
import os

cursor = mysql_connect('pymorph', 'pymorph', 'pymorph9455', 'shredder')

print 'Beginning Creating cat'

for subnum in range(1,45):
    cmd = 'select a.galcount,a.z from CAST as a, GAMA as b where a.galcount = b.galcount order by a.galcount limit %d,250;' %((subnum-1)*250)

    galcount, z = cursor.get_data(cmd)

    for fil in ['r']:
        outfile = open('/data2/home/ameert/catalog/gama/%s/data/sdss_%s_%d.cat' %(fil, fil, subnum), 'w')
        outfile.write("gal_id gimg wimg star z\n")

        for cur_gal, cur_z in zip(galcount,z):
            outfile.write("%08d_%s_stamp %08d_%s_stamp.fits %08d_%s_stamp_W.fits %08d_%s_psf.fits %f\n" %(cur_gal, fil,cur_gal, fil,cur_gal, fil,cur_gal, fil, cur_z))

        outfile.close()

        outfile = open('/data2/home/ameert/catalog/r/data/psflist.list' , 'w')
        outfile.write("")
        outfile.close()

            


