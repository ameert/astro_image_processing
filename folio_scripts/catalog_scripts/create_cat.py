#!/data2/home/ameert/python/bin/python2.5

from astro_image_processing.mysql.mysql_class import *
import os

cursor = mysql_connect('pymorph', 'pymorph', 'pymorph9455', 'shredder')

print 'Beginning Creating cat'

for subnum in range(260,351): #2684
    print "cat %d" %subnum
    cmd = 'select a.galcount, a.zspec from claudia_CAST as a where a.galcount between %d and %d and a.zspec between 0.5 and 0.7 order by a.galcount ;' %((subnum-1)*500+1, subnum*500)
    #cmd = 'select a.galcount, a.z from CAST as a, full_dr7_r_serexp as b where a.galcount = b.galcount and (b.fitflag & pow(2, 7)) and a.galcount > %d and a.galcount <= %d order by a.galcount;' %((subnum-1)*250, subnum*250)
    #cmd = 'select a.galcount,a.z from CAST as a left join full_dr7_g_ser_rerun as b on a.galcount = b.galcount where b.galcount is null;'
    galcount, z = cursor.get_data(cmd)
    
    for fil in ['i']:
        #outfile = open('/data2/home/ameert/catalog/%s/data/%04d/sdss_HNserexp_%s_%d.cat' %(fil,subnum, fil, subnum), 'w')
        #outfile = open('/data2/home/ameert/catalog/%s/data/%04d/sdss_%s_%d.cat' %(fil,subnum,fil,subnum), 'w')
        outfile = open('/data2/scratch/ameert/CMASS/%s/data/%04d/sdss_%s_%d.cat' %(fil,subnum,fil,subnum), 'w')
        outfile.write("gal_id gimg wimg star z\n")

        for cur_gal, cur_z in zip(galcount,z):
            outfile.write("%08d_%s_stamp %08d_%s_stamp.fits %08d_%s_stamp_W.fits %08d_%s_psf.fits %f\n" %(cur_gal, fil,cur_gal, fil,cur_gal, fil,cur_gal, fil, cur_z))

        outfile.close()

        os.system('touch /data2/scratch/ameert/CMASS/%s/data/%04d/psflist.list' %(fil,subnum))
        #outfile = open('/data2/home/ameert/catalog/r/data/psflist.list' , 'w')
        #outfile.write("")
        #outfile.close()

            


