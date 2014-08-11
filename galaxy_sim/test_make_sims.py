#!/usr/bin/python

#import simulate_galaxy
import pyfits as p
from mysql.mysql_class import *
import numpy as np
import sys
from galaxy_sim.sersic_classes import *
model_list = [sys.argv[1]]
start = int(sys.argv[2])
stop = int(sys.argv[3])

cursor = mysql_connect('catalog','ameert','al130568')

for model in model_list:
    cmd = "select a.galcount, b.run, b.camcol, b.field,  a.n, a.re, a.re_kpc, a.Ie, a.eb,a.rd, a.Id, a.ed, a.BT, a.zeropoint_sdss_r,a.bpa, a.dpa, a.z, b.petroR50_r from  simulations.sim_input as a, CAST as b where  a.galcount = b.galcount and a.model = '%s' and a.simcount between %d and %d order by a.galcount;" %(model, start, stop)

    #LOOK HERE!!!!!!!!!!!!!
    # the bpa and dpa ARE given and MUST BE given to the galaxy class in degrees 
    galcount, run, camcol, field, n, re, re_kpc, Ie, eb, rd, Id, ed, BT, zeropoint_sdss_r,bpa, dpa, z, petroR50_r= cursor.get_data(cmd)
    print galcount
    half_rad = np.array(petroR50_r)#/0.396
 
    bpa = np.array([45 for a in bpa])
    eb = np.array([.4 for a in eb])
 
    for g1, run1, camcol1, field1, n1, re1, re_kpc1, Ie1, eb1, rd1, Id1, ed1, BT1, zeropoint_sdss_r1,bpa1, dpa1, z1, petroR50_r1, half_rad1 in zip(galcount, run, camcol, field, n, re, re_kpc, Ie, eb, rd, Id, ed, BT, zeropoint_sdss_r,bpa, dpa, z, petroR50_r, half_rad):

        #if n1 > 8:
        #    continue
        #if re_kpc1 > 40:
        #    continue
        #if re1/rd1 > 1:
        #    if BT1 < .5:
        #        continue

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
           
        name = '%08d_%s' %(g1, model)
        psf_image = '/media/ACTIVE/short_sample/data/r/psf/%08d_r_psf.fits' %(g1)
        #psf_image = '/home/ameert/Desktop/final_sim/20/perfect_psf.fits' 
        background = '/media/BACKUP/sdss_sample/data/r/fpC-%06d-r%d-%04d.fit.gz' %(run1, camcol1, field1)
        if 1:
        #try:

        
            #gal = simulate_galaxy.galaxy('/scratch/final_sim/20/',name,Ie_count+Id_count, BT1, rd1, inc, dpa1, re1, eb1, bpa1, n1, bulge_mag = Ie1, disk_mag = Id1, zp = zeropoint_sdss_r1, half_light_arcsec = half_rad1, psf_name= psf_image )
            
            gal = galaxy('/home/ameert/Desktop/',name,Ie_count,Id_count, rd1, inc, dpa1, re1, eb1, bpa1, n1, bulge_mag = Ie1, disk_mag = Id1, zp = zeropoint_sdss_r1, half_light_arcsec = half_rad1)#, psf_name= psf_image )
            #gal = galaxy('/home/ameert/Desktop/',name,Ie_count,Id_count, rd1, inc, dpa1, re1, eb1, bpa1, n1, bulge_mag = Ie1, disk_mag = Id1, zp = zeropoint_sdss_r1, half_light_arcsec = half_rad1*1.5, psf_name= psf_image )
            #print "inc ", inc
            #print '/home/ameert/Desktop/',name,0.0,1000.0, 10.0, inc*0, dpa1*0, re1, 1.0, bpa1*0, 4.0,  900,  zeropoint_sdss_r1, zeropoint_sdss_r1, 10,  psf_image
            #print '/home/ameert/Desktop/',name,0.0,1000.0, 10.0, 0, 0, re1, 1.0, 0, 4.0,  900,  3, zeropoint_sdss_r1,  1, psf_image
            #gal = galaxy('/home/ameert/Desktop/',name+'_1',0,1000.0, 10.0, inc*0, dpa1*0, re1, 1.0, bpa1*0, 4.0, bulge_mag = 900, disk_mag = 3, zp = zeropoint_sdss_r1, half_light_arcsec = 10.0, psf_name= psf_image )
            #gal.make_profile()

            #gal = galaxy('/home/ameert/Desktop/',name+'_2',0,1000.0, 10.0, 0.0, 0, re1, 1.0, 0.0, 4.0, bulge_mag = 900, disk_mag = 3, zp = zeropoint_sdss_r1, half_light_arcsec = 10.0, psf_name= psf_image )
           
            gal.make_profile()

            #gal.add_noise()
            #gal.add_simulated_back()
            #gal.add_real_back(back_im = background)
#        except:
#            pass

#infile.close()

