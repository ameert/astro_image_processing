import sys
import os
import numpy as np
import scipy as sci
import pyfits as pf
from scipy.special import gammainc
from scipy.interpolate import splev, splrep
import scipy.signal as signal
import numpy.random as rand
#rand.seed(130941324)

#import pylab as pl 

class im_obj:
    """This class holds basic image properites like size, convolution, and saving"""
    def __init__(self, image = np.zeros(1)):
        self.image = image
        return

    def set_image_params(self, xcntr = 50, ycntr = 50, xsize = 101, ysize = 101):
        self.xcntr = xcntr
        self.ycntr = ycntr
        self.xsize = xsize
        self.ysize = ysize
        return

    def convolve_image(self, inpsf, boundary= 'NULL'):
        # boundary is [low, high, low, high]
            
        a = pf.open(inpsf)
        inpsf = a[0].data
        inpsf = inpsf/np.sum(inpsf)
        a.close()

        self.convolved_image = self.image.astype(float)

        if boundary == 'NULL':
            self.convolved_image = signal.fftconvolve(self.convolved_image, inpsf.astype(float), mode='same')
        else:
            self.convolved_image[boundary[0]:boundary[1],boundary[2]:boundary[3]]  = signal.fftconvolve(self.convolved_image[boundary[0]:boundary[1],boundary[2]:boundary[3]], inpsf.astype(float), mode='same')

        return

    def save_image(self, outname,  image, header_keys = [], key_vals = [], key_comments = []):
        ext = pf.PrimaryHDU(image)
        for a,b,c in zip(header_keys, key_vals, key_comments):
            ext.header.update(a ,b, c)

        ext. writeto(outname, clobber =1)
        return
 
class sersic(im_obj):
    """This class will generate a sersic profile and populate it with photons 
according to the given distribution. It can then be used to trim the image 
and return an array with the galaxy image in it.""" 
    def __init__(self, I_tot, n_ser, phi, ba, Re):
        """Note that the supplied parameters should be in pixel and counts
for I_tot and Re"""
        self.I_tot = I_tot
        self.n_ser = n_ser
        self.phi = phi
        self.ba = ba
        self.Re = Re 
        self.oversim = np.min([1000.0,10**(9.0-np.log10(self.I_tot))])
        print "Counts: %d oversim:%f" %(self.I_tot, self.oversim)
        self.draw_size = 10.0**6

        if self.I_tot >=1:
            self.tck = self.construct_rad_dist()
        else:
            #Spline not necessary
            pass
        return

    
    def bn(self,n):
        return 1.9992*n -0.3271
    
    def get_integrated_flux(self, n, x):
        return gammainc(2.0*n, x) # we dont need to divide by gamma(2.0*n) 
                                  # because it is already inculded in the gammainc

    def construct_rad_dist(self):
        rad = np.arange(0, self.Re * 50.0, self.Re/100.0)
        x = self.bn(self.n_ser) * (rad/self.Re)**(1.0/self.n_ser)
        flux = self.get_integrated_flux(self.n_ser,x)
        
        rad = np.extract(flux<.9999, rad)        
        x = np.extract(flux<.9999, x)
        flux = np.extract(flux<.9999, flux)
        tck = splrep(flux, rad)

        return tck

    def get_photons(self, num):
        photons = rand.rand(num)

        self.pos_ang = rand.rand(num)*2.0*np.pi
        self.photons = splev(photons, self.tck)

        #pl.hist(self.pos_ang, bins = 200)
        #pl.savefig('/home/ameert/Desktop/posang.eps')
        #pl.hist(self.photons, bins = 200)
        #pl.savefig('/home/ameert/Desktop/photons.eps')

        return


    def rad_to_xy(self):
        xprime =self.photons*np.sqrt(self.ba)*np.cos(self.pos_ang)
        yprime = self.photons/np.sqrt(self.ba)*np.sin(self.pos_ang)
        return xprime, yprime

    def make_image(self):

        imshape = (np.round(self.ysize), np.round(self.xsize))
        self.image = np.zeros(imshape)
        
        counts_to_sim = self.I_tot *self.oversim
        
        im_range = [np.arange(0,imshape[0]+1,1),np.arange(0, imshape[1]+1,1)]
        flat_range = np.arange(0,imshape[0]*imshape[1]+1,1)

        
        while counts_to_sim > 0:
            print "remaining photons: %10.0f" %counts_to_sim
            self.get_photons(np.min((counts_to_sim,self.draw_size)))
        
            xprime, yprime = self.rad_to_xy()

            # this rotates clockwise from the positive x-axis
            #xrot = xprime*np.cos(self.phi) -  yprime*np.sin(self.phi) 
            #yrot = 1.0*xprime*np.sin(self.phi) +  yprime*np.cos(self.phi) 
            # this rotates counter-clockwise from the positive x-axis
            xrot = xprime*np.cos(self.phi) +  yprime*np.sin(self.phi) 
            yrot = -1.0*xprime*np.sin(self.phi) +  yprime*np.cos(self.phi) 

            xcoords = np.floor(xrot+self.xcntr).astype(int)
            ycoords = np.floor(yrot+self.ycntr).astype(int)

            running_image, yedge, xedge = np.histogram2d(ycoords,xcoords, 
                       bins = im_range) 
            self.image = self.image + running_image

            
            counts_to_sim -= self.draw_size
        self.image = self.image /self.oversim
        
        return

class point(im_obj):
    """This class will generate a point source. It can then be used to 
trim the image and return an array with the galaxy image in it.""" 
    def __init__(self, I_tot, xcntr, ycntr):
        """Note that the supplied parameters should be in pixel and counts
for I_tot and Re"""
        self.I_tot = I_tot
        self.set_image_params(xcntr = xcntr, ycntr = ycntr, xsize = 2048, ysize = 1489)
     
        return

    def make_image(self, inpsf):
        
        self.image = np.zeros((self.ysize,self.xsize))
        self.image[self.ycntr,self.xcntr] = self.I_tot
        self.convolve_image(inpsf, [np.max((self.ycntr-50, 0)),np.min((self.ycntr+50, self.ysize - 1)),np.max((self.xcntr-50, 0)),np.min((self.xcntr+50, self.xsize - 1))] )
        
        return


class disk(sersic):
    def __init__(self, I_tot, phi, ba, R_scale):
        """Note that the supplied parameters should be in pixel and counts
for I_tot and Re"""
        self.I_tot = I_tot
        self.n_ser = 1
        self.phi = phi
        self.ba = ba
        self.Re = R_scale*np.sqrt(self.ba) #this factor is here to adjust for the shearing in the rotation since we are using the ellipticity rotation for bulges rather than the inclination rotation used for disks
        self.oversim = np.min([1000.0,10**(9.0-np.log10(self.I_tot))])
        self.draw_size = 10.0**6

        if self.I_tot >=1:
            self.tck = self.construct_rad_dist()
        else:
            #Spline not necessary
            pass

        return

    def construct_rad_dist(self):
        rad = np.arange(0, self.Re * 50.0, self.Re/100.0)
        x = (rad/self.Re)
        flux = self.get_integrated_flux(self.n_ser,x)
        
        rad = np.extract(flux<.9999, rad)        
        x = np.extract(flux<.9999, x)
        flux = np.extract(flux<.9999, flux)
        tck = splrep(flux, rad)

        return tck

    def rad_to_xy(self):
        xprime = self.photons*np.cos(self.pos_ang)
        yprime = self.photons*self.ba*np.sin(self.pos_ang)
        return xprime, yprime


class galaxy:
        """Holds the galaxy information and plotting routines."""
        def __init__(self, main_path, Name, Ie_counts, Id_counts, rd_arcsec, 
                     inc, dang, re_arcsec, ba, bang, ser,  
                     pix_sz =0.396, gain = 4.6, dark_variance =  1.0,
                     exptime = 53.907456, bulge_mag = 99, disk_mag = 99, 
                     kk = 0, zp = 26, airmass = 0, half_light_arcsec = 0, 
                     outdir = "sim_image", psf_name = 'NULL'):

            
            # load the input values 
            self.main_path = main_path
            self.Name = Name
            self.psf_name = psf_name
            self.Ie_counts = Ie_counts
            self.Id_counts = Id_counts
            self.flux = Ie_counts + Id_counts
            self.bt = Ie_counts/self.flux
            self.rd_arcsec = rd_arcsec
            self.inc = inc
            self.ed = np.cos(self.inc)
            self.dang = dang*np.pi/180.0 # now in radians
            self.re_arcsec = re_arcsec
            self.ba = ba
            self.bang = bang*np.pi/180.0 # now in radians
            self.ser = ser
            self.pix_sz = pix_sz
            self.gain = gain
            self.dark_variance = dark_variance
            self.exptime = exptime
            self.bulge_mag = bulge_mag
            self.disk_mag = disk_mag
            self.kk = kk
            self.zp = zp 
            self.airmass = airmass
            self.outdir = outdir
            self.perfect_psf = self.main_path + "perfect_psf.fits"

            if psf_name == 'NULL':
                self.psf_name = self.perfect_psf

            # Convert the radii to pixels
            self.re = self.re_arcsec/self.pix_sz
            self.rd = self.rd_arcsec/self.pix_sz
            half_light = half_light_arcsec/self.pix_sz

            # Establish the bounds of the image and the image center
            if half_light > 0:
                self.x_size = 2.0*25.0*half_light
            else: 
                if self.rd > 300:
                    self.x_size = np.max([self.re,-1.0*self.rd]) *2* 25.0
                else:
                    self.x_size = np.max([self.re,self.rd]) * 2*25.0

            if self.x_size < 200:
                self.x_size = 200

            self.y_size = self.x_size
            self.x_ctr = self.x_size/2.0
            self.y_ctr = self.y_size/2.0

            print self.x_size
            print self.y_size
            print self.x_ctr
            print self.y_ctr
            # Create directories to hold all data
            if not os.path.isdir(self.main_path):
                print "supplied path %s is not a valid path!!!\n Please correct this before you can continue with the program!\n\n" %(self.main_path)
                sys.exit()

            if not os.path.isdir(self.main_path+self.outdir):
                print "Creating output image dir " + self.main_path+self.outdir
                cmd = "mkdir %s/%s" %(self.main_path, self.outdir)
                os.system(cmd)

            # Create "perfect psf" for use in generating unconvolved galaxy images
            if self.psf_name == self.perfect_psf:
                make_psf(self.perfect_psf, 0.0)


            #cmd = '/home/ameert/galmorph/bin/GALMORPH_make_image %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %d %d %s %s NULL' %(self.flux, self.bt, self.rd, self.inc, self.dang- np.pi/2.0, self.re, 1.0-self.ba, self.bang- np.pi/2.0, self.ser, self.y_ctr, self.x_ctr, 0.0, 0.0, 1.0, 0.5, 2.0, self.y_size, self.x_size, self.psf_name, self.main_path+"/"+self.outdir+"/"+self.Name + "_galfit.fits")
            #print cmd
            #print os.system(cmd)

            return


        def make_profile(self, output_profile_filename = "NULL"):
            # Now generate the profile convolved with the psf
            print self.flux, self.bt, self.rd, self.inc, self.dang, self.re, self.ba, self.bang, self.ser, self.y_ctr, self.x_ctr, self.y_size, self.x_size, self.psf_name, self.main_path+"/"+self.outdir+"/"+self.Name + "_tmp.fits", output_profile_filename

            
            sersic_com = sersic(self.Ie_counts*self.gain, self.ser, self.bang, self.ba, self.re)
            sersic_com.set_image_params(xcntr = self.x_ctr, ycntr = self.y_ctr, xsize = self.x_size, ysize = self.y_size)
            sersic_com.make_image()
            
            
            disk_com = disk(self.Id_counts*self.gain, self.dang, self.ed, self.rd)
            disk_com.set_image_params(xcntr = self.x_ctr, ycntr = self.y_ctr, xsize = self.x_size, ysize = self.y_size)
            disk_com.make_image()
            
            new_gal =  im_obj((sersic_com.image+disk_com.image)/self.gain)
            print new_gal.image.shape
            new_gal.convolve_image(self.psf_name)

            header_keys = ['EXPTIME', 'IE','ID','n_ser','BT','rd','re','pixsz','ed','eb','bang',
                           'dang','kk','zp', 'airmass']
            key_vals = [self.exptime, self.bulge_mag, self.disk_mag, self.ser, self.bt, 
                        self.rd_arcsec, self.re_arcsec, self.pix_sz, self.ed, self.ba,
                        self.bang*180.0/np.pi, self.dang*180.0/np.pi, self.kk, self.zp, 
                        self.airmass] 
            key_comments = ['Total Exposure Time (sec)','bulge mag','disk mag', 'sersic_index',
                            'bulge to total ratio','disk radius in arcsec','bulge radius in arcsec',
                            'pixel size (arcsec/pixel)','ed parameter','eb parameter',
                            'bulge anlge (deg)','disk angle (deg)','kk parameter',
                            'zeropoint parameter','airmass parameter']

            new_gal.save_image(self.main_path+"/"+self.outdir+"/"+self.Name + "_flat.fits", image = new_gal.convolved_image,  header_keys = header_keys, key_vals = key_vals, key_comments = key_comments)        

            # Also copy the psf to a new filename that corresponds to the image
            cmd = 'cp %s %s' %( self.psf_name, self.main_path+"/"+self.outdir+"/"+self.Name + "_psf.fits")
            os.system(cmd)

            return

        def add_noise(self):
            a = sci.random.standard_normal((self.x_size, self.y_size))
            image = pf.open(self.main_path+"/"+self.outdir+"/"+self.Name + "_flat.fits")
            data = np.abs(image[0].data)

            new_image = data + a * sci.sqrt(data/self.gain)

            header = image[0].header
            header.update("GAIN", self.gain, 'Gain used in calculating noise')

            ext = pf.PrimaryHDU(new_image, header)

            ext.writeto(self.main_path+"/"+self.outdir+"/"+self.Name + "_noise.fits", clobber = 1)

            image.close()

            return

        def add_real_back(self, back_im = '/media/BACKUP/sdss_sample/data/r/fpC-003818-r3-0379.fit.gz'):
            print back_im
            if not os.path.isfile(back_im):
                print "Please provide a valid sdss frame!\n\n"
                #sys.exit()
            else:
                if back_im[-2:] == 'gz':
                    os.system('gunzip ' + back_im)
                    back_im = back_im[0:-3]
                back_image = pf.open(back_im)
                back_head = back_image[0].header
                back_data = back_image[0].data - 1000

                back_image.close()

                os.system('gzip ' + back_im)

                data_image = pf.open(self.main_path+"/"+self.outdir+"/"+self.Name + "_noise.fits")

                data = data_image[0].data
                header = data_image[0].header

                data_image.close()

                header.update("FILTER", back_head["FILTER"], 'filter used for background')
                header.update("RUN", back_head["RUN"], 'run used for background')
                header.update("FIELD", back_head["FRAME"], 'field used for background')
                header.update("CAMCOL", back_head["CAMCOL"], 'camcol used for background')

                borders = np.shape(data)
                bordersx = borders[0]
                bordersy = borders[1]

                center_y = sci.random.uniform(np.ceil(bordersx/2.0), np.floor(2048 - bordersx/2.0), 1)
                center_x = sci.random.uniform(np.ceil(bordersy/2.0),np.floor(1489 - bordersy/2.0),1)

                center_y = center_y[0]
                center_x = center_x[0]

                print bordersx
                print bordersy
                print center_x
                print center_y

                new_image = data +back_data[(center_x - borders[0]/2):(center_x + borders[0]/2 + borders[0]%2), (center_y - borders[1]/2):(center_y+borders[1]/2+ borders[1]%2)]

                ext = pf.PrimaryHDU(new_image, header)
                ext.writeto(self.main_path+"/"+self.outdir+"/"+self.Name + "_realback.fits", clobber = 1)

            return

        def add_simulated_back(self, band = 'r'):
            vals = {'u':20, 'g':80, 'r':120, 'i':200, 'z':120}
            sky_vals = vals[band]

            image = pf.open(self.main_path+"/"+self.outdir+"/"+self.Name + "_flat.fits")
            data = image[0].data
            header = image[0].header

            header.update("DVAR", self.dark_variance, 'Dark Variance used in background')
            header.update("AVGBACK", sky_vals, 'Average sky background')

            sigma = np.sqrt(sky_vals/self.gain + self.dark_variance)

            header.update("SIGBACK", sigma, 'Sigma of sky background')


            back = np.ones_like(data) * sky_vals
            total = back + data
            sig_im = np.sqrt(total/self.gain + self.dark_variance)
            total += sci.random.standard_normal((self.x_size, self.y_size))*sig_im

            ext = pf.PrimaryHDU(total, header)
            ext.writeto(self.main_path+"/"+self.outdir+"/"+self.Name + "_simsky.fits", clobber = 1)

            image.close()

            return


def make_psf(outname, FWHM, pix_sz = 0.396):
    """ Returns a normalized 2D gauss kernel array for convolutions """
    if not os.path.isfile(outname):
        if FWHM == 0.0:
            a = np.zeros((51,51))
            a[25,25] = 1.0
            ext = pf.PrimaryHDU(a)
            ext.header.add_comment('this is a perfect psf for simulation')
        else:
            size = int(FWHM/pix_sz)
            sigma  = size/2.3548
            # ensure that psf is at least 50 px across
            size = np.max([size*3, 50.0])
            sizey = size
            x, y = np.mgrid[-size:size+1, -sizey:sizey+1]
            g = np.exp(-(x**2/float(sigma)+y**2/float(sigma)))
            ext = pf.PrimaryHDU( g / g.sum())
        ext.header.update('FWHM', FWHM, 'pixels')
        ext.writeto(outname)
    else:
        print "PSF %s cannot be made. File already exists" %(outname)
        
    return


def make_new_flat(outdir, inflat, inpsf, fwhm = 0.0):
    outfile_name = inflat.split('/')[-1]
    outfile_name = outdir+'/'+outfile_name
    print "outfile name ", outfile_name
    a = pf.open(inflat)
    inflat = a[0].data
    header = a[0].header
    a.close()
     
    a = pf.open(inpsf)
    inpsf = a[0].data
    a.close()

    new_flat = signal.convolve2d(inflat, inpsf, mode='same')

    ext = pf.PrimaryHDU(new_flat, header)
    ext.header.update('FWHM' , fwhm, 'arcsec')

    ext. writeto(outfile_name)
    return new_flat

def stack_ims(small_im, big_im, xctr, yctr):
    shape = np.shape(small_im)

    print shape
    corner_x = xctr - shape[0]/2
    corner_y = yctr - shape[1]/2

    if corner_x < 0:
        min_x = int(np.abs(corner_x))
        corner_x = 0 
    else:
        min_x = 0
    if corner_y < 0:
        min_y = int(np.abs(corner_y))
        corner_y = 0 
    else:
        min_y = 0

    for x in range(min_x , shape[0]):
        if x + corner_x - min_x >= 1489:
            continue
        for y in range(min_y,shape[1]):
            if y + corner_y -min_y>= 2048:
                continue
            try:
                big_im[ x + corner_x-min_x][y + corner_y-min_y] += small_im[x][y]
            except:
                pass

        return big_im
