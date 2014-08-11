#!/usr/bin/python

import pyfits as p
from mysql.mysql_class import *
import numpy as np
import sys
from galaxy_sim.sersic_classes import *
pixscale = float(sys.argv[1])
start = int(sys.argv[2])
stop = int(sys.argv[3])

cursor = mysql_connect('catalog','ameert','al130568')

cmd = "select a.simcount, b.run, b.camcol, b.field,  a.n, a.re, a.re_kpc, a.Ie, a.eb,a.rd, a.Id, a.ed, a.BT, a.zeropoint_sdss_r,a.bpa+90.0, a.dpa+90.0, a.z, b.petroR50_r from  sim_input as a, CAST as b where  a.galcount = b.galcount and a.simcount between %d and %d order by a.simcount;" %(start, stop)

    #LOOK HERE!!!!!!!!!!!!!
    # the bpa and dpa ARE given and MUST BE given to the galaxy class in degrees 
galcount, run, camcol, field, n, re, re_kpc, Ie, eb, rd, Id, ed, BT, zeropoint_sdss_r,bpa, dpa, z, petroR50_r= cursor.get_data(cmd)
print galcount
simcount=galcount
half_rad = np.array(petroR50_r)#/0.396
    
for g1, run1, camcol1, field1, n1, re1, re_kpc1, Ie1, eb1, rd1, Id1, ed1, BT1, zeropoint_sdss_r1,bpa1, dpa1, z1, petroR50_r1, half_rad1, simcount1 in zip(galcount, run, camcol, field, n, re, re_kpc, Ie, eb, rd, Id, ed, BT, zeropoint_sdss_r,bpa, dpa, z, petroR50_r, half_rad,simcount):

        re1 = re1 * np.sqrt(eb1) # now circularized 

        if Id1 < -60:
            Id1 = -1.0* Id1
        if Ie1 < -60:
            Ie1 = -1.0* Ie1

        if rd1 < 0:
            rd1 = 1000


        Ie_count = mag_to_counts(Ie1, -1.0*zeropoint_sdss_r1)
        Id_count = mag_to_counts(Id1, -1.0*zeropoint_sdss_r1)

        if ed1 < 0:
            ed1 = 0
        elif ed1 > 1:
            ed1 = 1

        inc = np.arccos(ed1)
           
        name = '%08d' %(simcount1)
        psf_image = '/media/SDSS2/fit_catalog/data/r/%04d/%08d_r_psf.fits' %((g1-1)/250 +1, g1)
        #psf_image = '/home/ameert/Desktop/final_sim/20/perfect_psf.fits' 
        background = '/media/BACKUP/sdss_sample/data/r/fpC-%06d-r%d-%04d.fit.gz' %(run1, camcol1, field1)
        if 1:
        #try:
            
            gal = galaxy('/home/ameert/des_sims/',name,Ie_count,Id_count, rd1, inc, dpa1, re1, eb1, bpa1, n1, bulge_mag = Ie1, disk_mag = Id1, zp = zeropoint_sdss_r1, half_light_arcsec = half_rad1, psf_name= psf_image, pix_sz = pixscale)
            gal.make_profile()

            #gal.add_noise()
            #gal.add_simulated_back()
            #gal.add_real_back(back_im = background)
#        except:
#            pass

#infile.close()

