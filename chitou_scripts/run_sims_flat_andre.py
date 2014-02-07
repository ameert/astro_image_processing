#!/usr/bin/python

import pyfits as p
from mysql_class import *
import numpy as np
import sys
from sersic_classes import *
import random

import profile

def main():
    model_list = [sys.argv[1]]
    start = int(sys.argv[2])
    stop = int(sys.argv[3])

    def mag_sum(mag1, mag2):
        print mag1, mag2
        mag1 = 10.0**( -.4*mag1)
        mag2 = 10.0**(-.4*mag2)

        mag_tot = mag1 + mag2
        bt = mag1/(mag1+mag2)
        mag_tot = -2.5 * np.log10(mag_tot)

        return mag_tot, bt

    def mag_to_counts( mag, aa, kk = 0 , airmass = 0):
        exptime = 53.907456 #in seconds, taken from SDSS website www.sdss.org/dr3/algorithms/fluxcal.html
        return exptime * (10**(-.4*mag)) / (10**(0.4*(aa + kk*airmass)))

    def counts_to_mag( counts, aa, kk = 0 , airmass = 0):
        exptime = 53.907456 #in seconds, taken from SDSS website www.sdss.org/dr3/algorithms/fluxcal.html
        return -2.5 * np.log10(counts/exptime) + aa

    cursor = mysql_connect('andre_BCG','ameert','al130568')

    for model in model_list:
        cmd = "select a.simcount, a.n_bulge, a.r_bulge, a.m_bulge+7, a.ba_bulge, a.r_disk, a.m_disk+7, a.ba_disk, a.BT, a.zeropoint, a.pa_bulge, a.pa_disk, a.z, If(b.petroR50_r*d.kpc_per_arcsec/a.kpc_per_arcsec<1.5, 1.5,b.petroR50_r*d.kpc_per_arcsec/a.kpc_per_arcsec) from  sim_input as a, CAST as b, DERT as d where  a.galcount = b.galcount and a.galcount = d.galcount and a.galcount between %d and %d and model = '%s' order by a.simcount limit 1;" %(start, stop, model)

        galcount, n, re, Ie, eb, rd, Id, ed, BT, zeropoint_sdss_r,bpa, dpa, z, petroR50_r= cursor.get_data(cmd)
        print galcount
        half_rad = np.array(petroR50_r)

        for g1, n1, re1, Ie1, eb1, rd1, Id1, ed1, BT1, zeropoint_sdss_r1,bpa1, dpa1, z1, petroR50_r1, half_rad1 in zip(galcount, n, re, Ie, eb, rd, Id, ed, BT, zeropoint_sdss_r,bpa, dpa, z, petroR50_r, half_rad):

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
            psf_val = random.randint(1, 11)
            psf_image = '/home/ameert/andre_bcg/cutouts/r/0001/%08d_r_psf.fits' %(psf_val) 
            #background = '/media/BACKUP/sdss_sample/data/r/fpC-%06d-r%d-%04d.fit.gz' %(run1, camcol1, field1)
            if 1:
            #try:

                gal = galaxy('/home/ameert/test/sims/',name,Ie_count,Id_count, rd1, inc, dpa1, re1, eb1, bpa1, n1, bulge_mag = Ie1, disk_mag = Id1, zp = zeropoint_sdss_r1, half_light_arcsec = half_rad1)#, psf_name= psf_image )
                gal.make_profile()

                #gal.add_noise()
                #gal.add_simulated_back()
                #gal.add_real_back(back_im = background)
    #        except:
    #            pass

    #infile.close()

prof_name = '/home/ameert/test/prof_out.dat'
profile.run('main()', prof_name)
