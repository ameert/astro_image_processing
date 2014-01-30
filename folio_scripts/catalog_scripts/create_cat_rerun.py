#!/data2/home/ameert/python/bin/python2.5

from mysql_class import *
import os

cursor = mysql_connect('pymorph', 'pymorph', 'pymorph9455', 'shredder')

print 'Beginning Creating cat'

for subnum in range(1,2684): #2684
    cmd = 'select a.galcount, a.z from CAST as a, full_dr7_neighborcount as b, new_neighborcount as c where a.galcount = b.galcount and a.galcount = c.galcount and a.galcount between %d and %d and b.num_neigh_i!=c.num_neigh_i  order by a.galcount;' %((subnum-1)*250, subnum*250)
    galcount, z = cursor.get_data(cmd)

    #if len(galcount) < 30:
    #    print "folder %d, len %d" %(subnum, len(galcount))
    #continue
    for fil in ['i']:
        outfile = open('/data2/home/ameert/catalog/%s/data/%04d/sdss_rerun_%s_%d.cat' %(fil,subnum,fil,subnum), 'w')
        outfile.write("gal_id gimg wimg star z\n")

        for cur_gal, cur_z in zip(galcount,z):
            outfile.write("%08d_%s_stamp %08d_%s_stamp.fits %08d_%s_stamp_W.fits %08d_%s_psf.fits %f\n" %(cur_gal, fil,cur_gal, fil,cur_gal, fil,cur_gal, fil, cur_z))

        outfile.close()

        #outfile = open('/data2/home/ameert/catalog/r/data/psflist.list' , 'w')
        #outfile.write("")
        #outfile.close()

            


