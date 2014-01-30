#++++++++++++++++++++++++++
#
# TITLE: simulate_galaxy
#
# PURPOSE: this program will generate
#          the galaxy for the given params
#
# INPUTS:  uses the given params
#
# OUTPUTS: the image, psf, and background
#          
#
# PROGRAM CALLS: ???
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 24 APRIL 2011
#
#-----------------------------------

import sys
import os
import numpy as n
import pyfits as p
import random as r
import scipy as s

seed_val = 34252
s.random.seed(seed_val)

class galaxy:
    """Holds the galaxy information and plotting routines."""

    def __init__(self, main_path, Name, psf_name, flux, bt, rd_arcsec, inc, dang, re_arcsec,
                 ell, bang, ser, point_frac = 0, bar_frac = 0, rbar = 5.0, 
                 barell = 0.0, barser = .5, pix_sz = 0.396, gain = 4.6, dark_variance =  1.0,
                 exptime = 53.907456, bulge_mag = 99, disk_mag = 99, kk = 0, zp = 26, airmass = 0, half_light = 0):
        
        # load the input values 
        self.main_path = main_path
        self.Name = Name
        self.psf_name = psf_name
        self.flux = flux
        self.bt = bt
        self.rd_arcsec = rd_arcsec
        self.inc = inc
        self.dang = dang
        self.re_arcsec = re_arcsec
        self.ell = ell
        self.bang = bang
        self.ser = ser
        self.point_frac = point_frac
        self.bar_frac = bar_frac
        self.rbar = rbar
        self.barell = barell
        self.barser = barser
        self.pix_sz = pix_sz
        self.gain = gain
        self.dark_variance = dark_variance
        self.exptime = exptime
        self.bulge_mag = bulge_mag
        self.disk_mag = disk_mag
        self.kk = kk
        self.zp = zp 
        self.airmass = airmass
        
        
        # Convert the radii to pixels
        self.re = self.re_arcsec/self.pix_sz
        self.rd = self.rd_arcsec/self.pix_sz
        self.rbar = self.rbar/self.pix_sz

        # Establish the bounds of the image and the image center
        if half_light > 0:
            self.x_size = 2.0*8.0*half_light
        else:    
            self.x_size = n.max([self.re,self.rd]) * 20.0
            if self.x_size > 200:
                self.x_size = 200
            
        self.y_size = self.x_size
        self.x_ctr = self.x_size/2.0
        self.y_ctr = self.y_size/2.0
        

        # Create directories to hold all data
        if not os.path.isdir(self.main_path):
            print "supplied path %s is not a valid path!!!\n Please correct this before you can continue with the program!\n\n" %(self.main_path)
            sys.exit()

        if not os.path.isdir(self.main_path+"/sim_image"):
            print "Creating output image dir " + self.main_path+"/sim_image"
            cmd = "mkdir %s/sim_image" %(self.main_path)
            os.system(cmd)
        if not os.path.isdir(self.main_path+"/in_data"):
            print "Creating output input data dir " + self.main_path+"/in_data"
            cmd = "mkdir %s/in_data" %(self.main_path)
            os.system(cmd)
        
        if not os.path.isfile(self.psf_name):
            if not os.path.isfile(self.main_path + '/' + self.psf_name):
                print "PSF file cannot be found. Please put the psf at %s\n" %(self.main_path)
                sys.exit()
            else:
                self.psf_name = self.main_path + '/' + self.psf_name
            
        return


    def make_profile(self, output_profile_filename = "NULL"):
        # Now generate the profile convolved with the psf
        cmd = '/home/ameert/galmorph/bin/GALMORPH_make_image %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %d %d %s %s %s' %(self.flux, self.bt, self.rd, self.inc, self.dang, self.re, self.ell, self.bang, self.ser, self.y_ctr, self.x_ctr, self.point_frac, self.bar_frac, self.rbar, self.barell, self.barser, self.y_size, self.x_size, self.psf_name, self.main_path+"/sim_image/"+self.Name + "_tmp.fits", output_profile_filename)
        os.system(cmd)
        
        # Also copy the psf to a new filename that corresponds to the image
        cmd = 'cp %s %s' %( self.psf_name, self.main_path+"/sim_image/"+self.Name + "_psf.fits")
        os.system(cmd)

        psf = p.open(self.main_path+"/sim_image/"+self.Name + "_psf.fits")
        data = psf[0].data
        header = psf[0].header
        psf.close()

        if n.median(data) > 900:
            data = data - 1000
            ext = p.PrimaryHDU(data, header)
            ext.writeto(self.main_path+"/sim_image/"+self.Name + "_psf.fits", clobber =1)
        
       
        image = p.open(self.main_path+"/sim_image/"+self.Name + "_tmp.fits")
        header = image[0].header
        header.update('EXPOSURE', self.exptime, 'Total Exposure Time (sec)')
        header.update('IE', self.bulge_mag, 'bulge mag')
        header.update('ID', self.disk_mag, 'disk mag')
        header.update('n_ser', self.ser, 'sersic_index')
        header.update('BT', self.bt, 'bulge to total ratio')
        header.update('rd', self.rd_arcsec, 'disk radius in arcsec')
        header.update('re', self.re_arcsec, 'bulge radius in arcsec')
        header.update('pixsz', self.pix_sz, 'pixel size (arcsec/pixel)')
        header.update('ed', 1.0 - n.cos(self.inc), 'ed parameter')
        header.update('eb', self.ell, 'eb parameter')
        header.update('bang', self.bang*180.0/n.pi, 'bulge anlge (deg)')
        header.update('dang', self.dang*180.0/n.pi, 'disk angle (deg)')
        header.update('kk', self.kk, 'kk parameter')
        header.update('zp', self.zp, 'zeropoint parameter')
        header.update('airmass', self.airmass, 'airmass parameter')
        
        ext = p.PrimaryHDU(image[0].data, header)
        ext.writeto(self.main_path+"/sim_image/"+self.Name + "_flat.fits", clobber = 1)
        image.close()

        os.system('rm ' + self.main_path+"/sim_image/"+self.Name + "_tmp.fits")
        
        return

    def add_noise(self):
        a = s.random.standard_normal((self.x_size, self.y_size))
        image = p.open(self.main_path+"/sim_image/"+self.Name + "_flat.fits")
        data = n.abs(image[0].data)

        new_image = data + a * s.sqrt(data/self.gain)

        header = image[0].header
        header.update("GAIN", self.gain, 'Gain used in calculating noise')
        
        ext = p.PrimaryHDU(new_image, header)
        
        ext.writeto(self.main_path+"/sim_image/"+self.Name + "_noise.fits", clobber = 1)

        image.close()
        
        return

    def add_real_back(self, back_im = '/media/BACKUP/sdss_sample/data_dir/fpC-003818-r3-0379.fit.gz'):
        if not os.path.isfile(back_im):
            print "Please provide a valid sdss frame!\n\n"
            #sys.exit()
        else:
            if back_im[-2:] == 'gz':
                os.system('gunzip ' + back_im)
                back_im = back_im[0:-3]
            back_image = p.open(back_im)
            back_head = back_image[0].header
            back_data = back_image[0].data - 1000

            back_image.close()

            os.system('gzip ' + back_im)
            
            data_image = p.open(self.main_path+"/sim_image/"+self.Name + "_noise.fits")

            data = data_image[0].data
            header = data_image[0].header

            data_image.close()
            
            header.update("FILTER", back_head["FILTER"], 'filter used for background')
            header.update("RUN", back_head["RUN"], 'run used for background')
            header.update("FIELD", back_head["FRAME"], 'field used for background')
            header.update("CAMCOL", back_head["CAMCOL"], 'camcol used for background')

            borders = n.shape(data)
            bordersx = borders[0]
            bordersy = borders[1]
            
            center_y = s.random.uniform(n.ceil(bordersx/2.0), n.floor(2048 - bordersx/2.0), 1)
            center_x = s.random.uniform(n.ceil(bordersy/2.0),n.floor(1489 - bordersy/2.0),1)

            center_y = center_y[0]
            center_x = center_x[0]
            
            print bordersx
            print bordersy
            print center_x
            print center_y
            
            new_image = data +back_data[(center_x - borders[0]/2):(center_x + borders[0]/2 + borders[0]%2), (center_y - borders[1]/2):(center_y+borders[1]/2+ borders[1]%2)]

            ext = p.PrimaryHDU(new_image, header)
            ext.writeto(self.main_path+"/sim_image/"+self.Name + "_realback.fits", clobber = 1)
            
        return

    def add_simulated_back(self, band = 'r'):
        vals = {'u':20, 'g':80, 'r':120, 'i':200, 'z':120}
        sky_vals = vals[band]

        image = p.open(self.main_path+"/sim_image/"+self.Name + "_noise.fits")
        data = image[0].data
        header = image[0].header

        header.update("DVAR", self.dark_variance, 'Dark Variance used in background')
        header.update("AVGBACK", sky_vals, 'Average sky background')

        sigma = n.sqrt(sky_vals/self.gain + self.dark_variance)

        header.update("SIGBACK", sigma, 'Sigma of sky background')

        back = n.ones_like(data) * sky_vals
        back += s.random.standard_normal((self.x_size, self.y_size))*sigma

        ext = p.PrimaryHDU(data+back, header)
        ext.writeto(self.main_path+"/sim_image/"+self.Name + "_simsky.fits", clobber = 1)

        image.close()
                    
        return
    
