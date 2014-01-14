import numpy as n
import pyfits
import os.path
from read_list import *
from scipy.special import gamma
from scipy import interpolate
import time
from convolve import convolve2d
import scipy as s
from galmorph_make_image import *
from image_info import *
import time
import sys

class galaxy:
    """Holds all galaxy information used in plotting and calculating objects
    call as a = galaxy(path_main_data, path_root, Name, number,model_type, Ie, re_pix, eb, n, Id, rd_pix, ed, zp,
    kk, airmass, z=0, kcorr = 0)"""

    
    def __init__(self, path_main_data, path_root, Name, number,model_type, Ie, re_pix, eb,bpa, n, Id, rd_pix, ed,dpa,bt, xctr_bulge, yctr_bulge, xctr_disk, yctr_disk,half_light, zp, kk, airmass, Galsky , z=0, kcorr = 0):
        self.log_space = 0
        self.path_main_data = path_main_data
        self.path_root = path_root
        self.Name = Name
        self.model_type = model_type
        self.number = number
        self.Ie = Ie
        self.re_pix = re_pix
        self.eb = eb
        self.n = n
        self.Id = Id
        self.rd_pix = rd_pix
        self.ed = ed
        self.bt = bt
        self.zp = zp
        self.kk = kk
        self.airmass = airmass
        self.z = z
        self.kcorr = kcorr
        self.Galsky = Galsky
        self.dpa = dpa
        self.bpa = bpa
        self.bxc = xctr_bulge # in pixels
        self.byc = yctr_bulge # in pixels
        self.dxc = xctr_disk # in pixels
        self.dyc = yctr_disk # in pixels
        self.half_light = half_light # in pixels
        
        self.weight_image = '%s%08d_r__r_W.fits' %(self.path_root, self.number)
        self.mask = '%sM_%08d_r_stamp.fits' %(self.path_root, self.number)
        self.psf = '%s%08d_r_psf.fits' %(self.path_root, self.number)
        self.out_profile = '%s%06d_r_%s_profile.txt' %(self.path_main_data, self.number,self.model_type)
        self.file_name = 'O_%08d_r_stamp.fits' %(self.number)
        self.out_pymodel = '%s%06d_r_stamp_model_%s.fits' %(self.path_main_data, self.number, self.model_type)
        self.outmask = '%sM_%08d_r_stamp.fits' %(self.path_main_data, self.number)
        self.outstamp = self.path_main_data + self.Name + '_sub_'+self.model_type+ '.fits'
        self.sum_model = self.path_main_data + self.Name + '_sim_sum_model_'+self.model_type+'.fits'
        self.profile = self.path_main_data + self.Name + '_model_profile_'+self.model_type+'.txt'
        self.bulge_prof = self.path_main_data + self.Name + '_model_bulge_'+self.model_type+'.txt'
        self.disk_prof = self.path_main_data + self.Name + '_model_disk_'+self.model_type+'.txt'
        self.model_sim_all = self.path_main_data + self.Name + '_model_all_'+self.model_type+'.txt'
        self.mag_output = self.path_main_data + self.Name + '_mag_arc_profile_'+self.model_type+'.txt'
        self.mag_model =  self.path_main_data + self.Name + '_mag_arc_model_profile_'+self.model_type+'.txt'
        self.mag_model_bulge = self.path_main_data + self.Name + '_model_bulge_mag_'+self.model_type+'.txt'
        self.mag_model_disk = self.path_main_data + self.Name + '_model_disk_mag_'+self.model_type+'.txt'
        self.mag_model_sim_all = self.path_main_data + self.Name + '_model_all_mag_'+self.model_type+'.txt'
        self.bulge_fits = self.path_main_data + self.Name + '_model_bulge_'+self.model_type+'.fits'
        self.disk_fits = self.path_main_data + self.Name + '_model_disk_'+self.model_type+'.fits'
        self.nyu_bulge_fits = self.path_main_data + self.Name + '_nyu_ser.fits'
        self.nyu_prof = self.path_main_data + self.Name + '_nyu_model_ser.txt'
        self.nyu_prof_mag = self.path_main_data + self.Name + '_nyu_mag_arc_profile_ser.txt'
        
        return

    def calc_goodness(self):
        # I use these three things to calculate goodness
        # self.mask_image
        # self.weight_fits
        # self.norm_resid_fits
        # self.mod_x
        # self.mod_y
        # self.half_light

        good_im = image_info(self.model_fits, self.mask_image, self.mod_x, self.mod_y)
        good_im.imstats()
        
        count = 0
        good_pix = 0

        flat_sig = self.norm_resid_fits.flatten()
        flat_weight = (self.weight_fits.flatten())/2.0
        flat_mask = good_im.mask_flat
        flat_x = good_im.x_flat
        flat_y = good_im.y_flat

        cosa = n.cos(good_im.pa)
        sina = n.sin(good_im.pa)
        
        xp   = (flat_x-self.mod_x)*cosa  + (flat_y-self.mod_y)*sina
        yp   = -(flat_x-self.mod_x)*sina  + (flat_y-self.mod_y)*cosa
        rad = n.sqrt( xp**2. + (yp/good_im.ba)**2)

        # we must compare self.half_light*root(b/a) to r_eff which has a root(b/a) in it so i
        # drop this root(b/a) term and just compare semimajor axis

        good_rads = n.extract(flat_mask == 1, rad)
        good_sig = n.extract(flat_mask == 1, flat_sig)
        good_weight = n.extract(flat_mask == 1, flat_weight)

        good_weight = n.extract(good_rads <= 2.0*self.half_light, good_weight)
        
        good_sig = n.extract(good_rads <= 2.0*self.half_light, good_sig)
        
        goodness = float(n.size((n.where(n.abs(good_sig) <= good_weight))))
        
        self.goodness = goodness/float(len(good_sig))
        
        return self.goodness
    
        
        
    def mag_to_counts(self, mag, aa, kk = 0 , airmass = 0):
        exptime = 53.907456 #in seconds, taken from SDSS website www.sdss.org/dr3/algorithms/fluxcal.html
        return exptime * (10**(-.4*mag)) / (10**(0.4*(aa + kk*airmass)))

    def read_images(self, et = 53.907456):
        if os.path.isfile(self.weight_image):
            frame = pyfits.open(self.weight_image)
            self.weight_fits = frame[0].data
            frame.close()
            print 'weight image found'
        fn = self.path_root + self.file_name
        
        if os.path.isfile(fn):
            #print "file exists!!!!!\n\n\n\n\n\n"
            frame = pyfits.open(fn)
            self.data_fits = frame[1].data * et
            self.model_fits = frame[2].data * et
            self.resid_fits = frame[3].data * et
            self.norm_resid_fits  = frame[3].data # unmultiplied image used to calculate 'goodness' parameter. 
            
            if self.model_type in ['DevExp', 'SerExp']:
                self.bulge_im = frame[4].data * et
                self.disk_im = frame[5].data * et
                self.sky_im = frame[6].data * et
                extra = 7

                ext = pyfits.PrimaryHDU(self.disk_im)
                ext.writeto(self.disk_fits, clobber = 1)



            else:
                self.bulge_im = frame[4].data * et
                self.sky_im = frame[5].data * et
                extra = 6
            while extra < len(pyfits.HDUList(frame)):
                self.sky_im += frame[extra].data * et
                print "reading extra ", extra 
                extra += 1

            print 'images read'
            print 'writing subtracted data'
            
            ext = pyfits.PrimaryHDU(self.bulge_im)
            ext.writeto(self.bulge_fits, clobber = 1)

            frame.close()

            self.sub_stamp_data = self.data_fits - self.sky_im
            self.rows_stamp,self.cols_stamp = n.shape(self.data_fits)
            ext = pyfits.PrimaryHDU(self.sub_stamp_data)
            ext.writeto(self.outstamp, clobber = 1)
            
            self.sub_data_pymodel = self.model_fits - self.sky_im
            ext = pyfits.PrimaryHDU(self.sub_data_pymodel)
            ext.writeto(self.out_pymodel, clobber = 1)
            print 'finding image stats'
            # find the image centroid for profile measurements
            norm_model = self.sub_data_pymodel/n.sum(self.sub_data_pymodel)
            x_col_sum = n.sum(norm_model, axis = 1)
            x_weights = range(0,len(x_col_sum))
            self.mod_x = n.average(x_weights, weights = x_col_sum)
            y_col_sum = n.sum(norm_model, axis = 0)
            y_weights = range(0,len(y_col_sum))
            self.mod_y = n.average(y_weights, weights = y_col_sum)
            
            #print self.mod_x, self.bxc, self.mod_y, self.byc
            #print self.mod_x
            #print self.mod_y
            print 'reading mask'
            image =  pyfits.open(self.mask)
            mask_image = image[0].data
            mask_image = n.where(mask_image == 1,2,mask_image)
            mask_image = n.where(mask_image == 0,1,mask_image)
            self.mask_image = n.where(mask_image == 2,0,mask_image)
            ext = pyfits.PrimaryHDU(self.mask_image)
            ext.writeto(self.outmask, clobber = 1)
            image.close()
        else:
            print "THE GALAXY " + fn + " DOESNT EXISIT!!!\n\n\n"
            raise IOError
        

        return

    def make_sim_sum(self):
        if self.model_type in ['DevExp', 'SerExp']:
            ext = pyfits.PrimaryHDU(self.disk_im+self.bulge_im)
        else:
            ext = pyfits.PrimaryHDU(self.bulge_im)
        ext.writeto(self.sum_model, clobber = 1)
        return
        
    def get_main_profiles(self):
        #get profile of background subtracted data
        if self.log_space != 1:
            galmorph_get_profile(self.outstamp, self.outmask, self.mod_x, self.mod_y, self.out_profile, log_profile = 'NULL', ellipticity = 'NULL', position_angle = 'NULL')
        elif self.log_space == 1:
            galmorph_get_profile(self.outstamp, self.outmask, self.mod_x, self.mod_y, 'test.txt', log_profile = self.out_profile, ellipticity = 'NULL', position_angle = 'NULL')
            
        profile_to_arcsec_mag(-1.0 * self.zp, self.kk, self.airmass, self.out_profile, self.mag_output)
        self.profile_data = read_list(self.mag_output, 'F,F,F',column_names = ['rad', 'dat', 'daterr'])
        for key in self.profile_data.keys():
            self.profile_data[key] = n.array(self.profile_data[key])

        #get profile of model that fits the data
        if self.log_space != 1:
            galmorph_get_profile(self.out_pymodel, self.outmask, self.mod_x, self.mod_y, self.profile, log_profile = 'NULL', ellipticity = 'NULL', position_angle = 'NULL')
        elif self.log_space == 1:
            galmorph_get_profile(self.out_pymodel, self.outmask, self.mod_x, self.mod_y, 'test.txt', log_profile = self.profile, ellipticity = 'NULL', position_angle = 'NULL')

        profile_to_arcsec_mag(-1.0 * self.zp, self.kk, self.airmass, self.profile, self.mag_model)
        #print read_list(self.profile, 'F,F,F',column_names = ['rad', 'dat', 'daterr'])
        self.profile_pymodel = read_list(self.mag_model, 'F,F,F',column_names = ['rad', 'dat', 'daterr'])
        for key in self.profile_pymodel.keys():
            self.profile_pymodel[key] = n.array(self.profile_pymodel[key])

        #print self.profile_pymodel
        SplineResult = interpolate.splrep(self.profile_pymodel['rad'],self.profile_pymodel['dat'], s=0, k=3)
        self.fit_resid = interpolate.splev(self.profile_data['rad'], SplineResult, der=0)
        # self.fit_resid = self.profile_pymodel['dat']
        #print self.profile_data['rad']
        #print self.profile_pymodel['rad']
        #print self.fit_resid
        #print self.profile_data['dat']
        #print self.profile_pymodel['dat']
        #print type(self.fit_resid)
        #print type(self.profile_data['dat'])
        
        self.fit_resid = self.fit_resid - self.profile_data['dat']
        #print self.fit_resid
        
        self.fit_res_rad = self.profile_data['rad']

        return

    def get_component_prof(self, shift_counts = 0):
        if self.model_type in ['DevExp', 'SerExp']:
            # get generated bulge component
            if self.log_space != 1:
                galmorph_get_profile(self.bulge_fits, self.outmask, self.mod_x, self.mod_y, self.bulge_prof, log_profile = 'NULL', ellipticity = 'NULL', position_angle = 'NULL')
            if self.log_space == 1:
                galmorph_get_profile(self.bulge_fits, self.outmask, self.mod_x, self.mod_y, 'test.txt', log_profile = self.bulge_prof, ellipticity = 'NULL', position_angle = 'NULL')

            # get generated disk component
            if self.log_space != 1:
                galmorph_get_profile(self.disk_fits, self.outmask, self.mod_x, self.mod_y, self.disk_prof, log_profile = 'NULL', ellipticity = 'NULL', position_angle = 'NULL')
            elif self.log_space ==1:
                galmorph_get_profile(self.disk_fits, self.outmask, self.mod_x, self.mod_y, 'test.txt', log_profile = self.disk_prof, ellipticity = 'NULL', position_angle = 'NULL')
            
            # profile_to_arcsec_mag(-1.0 * self.zp, self.kk, self.airmass, self.bulge_prof, self.mag_model_bulge, shift = shift_counts/2.0)

            pix_sz = 0.396
            profile_bulge = {}
            profile_disk = {}
            
            profile_bulge.update(read_list(self.bulge_prof, 'F,F,F', column_names = ('rad', 'data', 'dataerr')))
            profile_disk.update(read_list(self.disk_prof, 'F,F,F', column_names = ('rad', 'data', 'dataerr')))
            
            for key in profile_bulge.keys():
                profile_bulge[key] = n.array(profile_bulge[key])
                profile_disk[key] = n.array(profile_disk[key])


            pro_bulge_shift = {'data':[], 'rad':[], 'dataerr':[]}
            pro_disk_shift = {'data':[], 'rad':[], 'dataerr':[]}
            
            
            for bulge_flux, disk_flux, bulge_rad, disk_rad, bulge_err, disk_err in zip(profile_bulge['data'],profile_disk['data'],profile_bulge['rad'],profile_disk['rad'],profile_bulge['dataerr'],profile_disk['dataerr']):

                if bulge_flux > 0 and disk_flux > 0:
                    shift_coeff = bulge_flux/(disk_flux + bulge_flux)
                elif bulge_flux > 0 and disk_flux <= 0:
                    shift_coeff = 1
                elif bulge_flux <= 0 and disk_flux > 0:
                    shift_coeff = 0
                else:
                    continue

                if bulge_flux > n.abs(shift_counts*shift_coeff):
                    #print bulge_flux, shift_coeff, bulge_flux + (shift_counts*shift_coeff), bulge_rad
                    pro_bulge_shift['data'].append(bulge_flux + (shift_counts*shift_coeff))
                    pro_bulge_shift['rad'].append(bulge_rad)
                    pro_bulge_shift['dataerr'].append(bulge_err)
                    
                if disk_flux > n.abs(shift_counts*(1.0-shift_coeff)):
                    #print disk_flux, shift_coeff, disk_flux + (shift_counts*(1.0 - shift_coeff)), disk_rad
                    pro_disk_shift['data'].append(disk_flux + (shift_counts*(1.0-shift_coeff)))
                    pro_disk_shift['rad'].append(disk_rad)
                    pro_disk_shift['dataerr'].append(disk_err)

                
            for key in pro_bulge_shift.keys():
                pro_bulge_shift[key] = n.array(pro_bulge_shift[key])
                pro_disk_shift[key] = n.array(pro_disk_shift[key])

            pro_bulge_shift['rad'] = pixels_to_arcsec(pro_bulge_shift['rad'])
            pro_disk_shift['rad'] = pixels_to_arcsec(pro_disk_shift['rad'])
            pro_bulge_shift['dataerr'] = co_pix_to_mag_arc(pro_bulge_shift['data']-pro_bulge_shift['dataerr'], -1.0*self.zp, self.kk, self.airmass) -co_pix_to_mag_arc(pro_bulge_shift['data'], -1.0*self.zp, self.kk, self.airmass) 
            pro_disk_shift['dataerr'] = co_pix_to_mag_arc(pro_disk_shift['data']-pro_disk_shift['dataerr'], -1.0*self.zp, self.kk, self.airmass) -co_pix_to_mag_arc(pro_disk_shift['data'], -1.0*self.zp, self.kk, self.airmass) 
            pro_bulge_shift['data'] = co_pix_to_mag_arc(pro_bulge_shift['data'], -1.0*self.zp, self.kk, self.airmass)
            pro_disk_shift['data'] = co_pix_to_mag_arc(pro_disk_shift['data'], -1.0*self.zp, self.kk, self.airmass)
            
            f = open(self.mag_model_bulge, 'w')
            f.write('# rad data dataerr\n')
            for rad,data,dataerr in zip(pro_bulge_shift['rad'],pro_bulge_shift['data'],pro_bulge_shift['dataerr']):
                f.write('%f %f %f\n' %(rad,data,dataerr))
            f.close()
            
            f = open(self.mag_model_disk, 'w')
            f.write('# rad data dataerr\n')
            for rad,data,dataerr in zip(pro_disk_shift['rad'],pro_disk_shift['data'],pro_disk_shift['dataerr']):
                f.write('%f %f %f\n' %(rad,data,dataerr))
            f.close()

            self.profile_bulge = read_list(self.mag_model_bulge, 'F,F,F',column_names = ['rad', 'dat', 'daterr'])

            self.profile_disk = read_list(self.mag_model_disk, 'F,F,F',column_names = ['rad', 'dat', 'daterr'])
        
        #get shifted image for comparison
        if self.log_space != 1:
            galmorph_get_profile(self.sum_model, self.outmask, self.mod_x, self.mod_y, self.model_sim_all, log_profile = 'NULL',ellipticity = 'NULL', position_angle = 'NULL')
        elif self.log_space == 1:
            galmorph_get_profile(self.sum_model, self.outmask, self.mod_x, self.mod_y, 'test.txt', log_profile = self.model_sim_all, ellipticity = 'NULL', position_angle = 'NULL')
        profile_to_arcsec_mag(-1.0 * self.zp, self.kk, self.airmass, self.model_sim_all, self.mag_model_sim_all, shift = shift_counts)
        self.profile_sim_all = read_list(self.mag_model_sim_all, 'F,F,F',column_names = ['rad', 'dat', 'daterr'])

        SplineResult = interpolate.splrep(self.profile_sim_all['rad'],self.profile_sim_all['dat'], s=0, k=3)
        self.sim_resid = interpolate.splev(self.profile_data['rad'], SplineResult, der=0)
        # self.sim_resid = self.profile_sim_all['dat']

        self.sim_resid = self.sim_resid - self.profile_data['dat']
        self.sim_res_rad = self.profile_data['rad']
        return

    def get_nyu_prof(self):

        #get generated nyu image for comparison
        if self.log_space != 1:
            galmorph_get_profile(self.nyu_bulge_fits, self.outmask, self.mod_x, self.mod_y, self.nyu_prof, log_profile = 'NULL',ellipticity = 'NULL', position_angle = 'NULL')
        elif self.log_space == 1:
            galmorph_get_profile(self.nyu_bulge_fits, self.outmask, self.mod_x, self.mod_y, 'test.txt', log_profile = self.nyu_prof, ellipticity = 'NULL', position_angle = 'NULL')

        profile_to_arcsec_mag(-1.0 * self.zp, self.kk, self.airmass, self.nyu_prof, self.nyu_prof_mag)
        self.profile_nyu_mag = read_list(self.nyu_prof_mag, 'F,F,F',column_names = ['rad', 'dat', 'daterr'])
        
        SplineResult = interpolate.splrep(self.profile_nyu_mag['rad'],self.profile_nyu_mag['dat'], s=0, k=3)
        self.nyu_resid = interpolate.splev(self.profile_data['rad'], SplineResult, der=0)
        # self.nyu_resid = self.profile_nyu_mag['dat']

        self.nyu_resid = self.nyu_resid - self.profile_data['dat']
        self.nyu_res_rad = self.profile_data['rad']
        return
    

    def sersic(self,counts,re,nb, et =53.907456 ):
        self.x = n.reshape(n.arange(self.rows_stamp * self.cols_stamp), (self.rows_stamp, self.cols_stamp)) % self.cols_stamp
        self.x = self.x.astype(n.float32)
        self.x = self.x + 0.5
        self.y = n.reshape(n.arange(self.rows_stamp * self.cols_stamp), (self.rows_stamp, self.cols_stamp)) / self.cols_stamp
        self.y = self.y.astype(n.float32)
        self.y = self.y + 0.5
        xcb = self.mod_x+.5
        ycb = self.mod_y+.5
        eb = self.eb
        mz = self.zp
        i0b = counts
        i0b = (i0b * (self.bfunc(nb))**(2.0 * nb)) / (2.0 * nb * 3.14 * re * re * self.Gamma(2.0 * nb) * n.exp(self.bfunc(nb)) * eb)
        ixcb = int(xcb)
        iycb = int(ycb)
        # r is the radius parameter
        co = n.cos(self.bpa * n.pi / 180.0)
        si = n.sin(self.bpa * n.pi / 180.0)
        xsq = ((self.x - xcb) * co + (self.y-ycb) * si)**2.0
        ysq = ((xcb - self.x) * si + (self.y-ycb) * co)**2.0
        #    one_minus_eb_sq = (1.0 - eb)**2.0
        one_minus_eb_sq = eb * eb #axis ratio
        r = n.sqrt(xsq + ysq / one_minus_eb_sq)
        self.bulge = i0b * n.exp(-self.bfunc(nb) * ((r/re)**(1.0 / nb) - 1.0))
        xmin = int(xcb - 2.0)
        xmax = int(xcb + 3.0)
        ymin = int(ycb - 2.0)
        ymax = int(ycb + 3.0)
        xcb_1 = 2.0 + n.modf(xcb)[0]
        ycb_1 = 2.0 + n.modf(ycb)[0]
        x_1 = n.reshape(n.arange(625), (25, 25)) % 25
        x_1 = x_1.astype(n.float32)
        x_1 = x_1 * 0.20 + 0.1
        y_1 = n.reshape(n.arange(625), (25, 25)) / 25
        y_1 = y_1.astype(n.float32)
        y_1 = y_1 * 0.20 + 0.1
        xsq_1 = ((x_1 - xcb_1) * co + (y_1 - ycb_1) * si)**2.0
        ysq_1 = ((xcb_1 - x_1) * si + (y_1 - ycb_1) * co)**2.0
        r_1 = n.sqrt(xsq_1 + ysq_1 / one_minus_eb_sq)
        self.bulge_1 = i0b * n.exp(-self.bfunc(nb) * ((r_1 / re)**(1.0 / nb) - 1.0))
        self.bulge_1 = self.rebin_sum(self.bulge_1, (5, 5))
        self.bulge[ymin:ymax,xmin:xmax] = self.bulge_1
        xcb_2 = xcb_1 - 1.0
        ycb_2 = ycb_1 - 1.0
        x_2 = n.reshape(n.arange(900), (30, 30)) % 30
        x_2 = x_2.astype(n.float32)
        x_2 = x_2 * 0.1 + 0.05
        y_2 = n.reshape(n.arange(900), (30, 30)) / 30
        y_2 = y_2.astype(n.float32)
        y_2 = y_2 * 0.1 + 0.05
        xsq_2 = ((x_2 - xcb_2) * co + (y_2 - ycb_2) * si)**2.0
        ysq_2 = ((xcb_2 - x_2) * si + (y_2 - ycb_2) * co)**2.0
        r_2 = n.sqrt(xsq_2 + ysq_2 / one_minus_eb_sq)
        self.bulge_2 = i0b * n.exp(-self.bfunc(nb)*((r_2 / re)**(1.0 / nb) - 1.0))
        self.bulge_2 = self.rebin_sum(self.bulge_2, (10, 10))
        self.bulge[ymin+1:ymax-1,xmin+1:xmax-1] = self.bulge_2
        xfin = int(xmin + 2)
        yfin = int(ymin + 2)
        xcb_3 = xcb_2 - 1.0
        ycb_3 = ycb_2 - 1.0
        x_3 = n.reshape(n.arange(400), (20, 20)) % 20 
        x_3 = x_3.astype(n.float32)
        x_3 = x_3 * 0.05 + 0.025
        y_3 = n.reshape(n.arange(400), (20, 20)) / 20 
        y_3 = y_3.astype(n.float32)
        y_3 = y_3 * 0.05 + 0.025
        xsq_3 = ((x_3 - xcb_3) * co + (y_3 - ycb_3) * si)**2.0
        ysq_3 = ((xcb_3 - x_3) * si + (y_3 - ycb_3) * co)**2.0
        r_3 = n.sqrt(xsq_3 + ysq_3 / one_minus_eb_sq)
        self.bulge_3 = i0b * n.exp(-self.bfunc(nb) * ((r_3 / re)**(1.0 / nb) - 1.0))
        self.bulge_3 = self.rebin_sum(self.bulge_3, (20, 20))
        self.bulge[yfin][xfin] = self.bulge_3.sum()
        #self.bulge = n.swapaxes(self.bulge, 0,1) 
        # convolving model with psf
        image =  pyfits.open(self.psf)
        psf_image = image[0].data            
        psf_image = psf_image/psf_image.sum()
        self.nyu_bulge_im  = convolve2d(self.bulge, psf_image, fft=1, mode='wrap')
        image.close()
        
        ext = pyfits.PrimaryHDU(self.nyu_bulge_im)
        ext.writeto(self.nyu_bulge_fits, clobber = 1)

        return
    
    def bfunc(self,x):
        """ This function gives value of b_n given the Sersic index"""
        #    return 0.868242*x -0.142058 # Khosroshahi et al. 2000 approximation
        return 2.0*x -0.331
    def rebin_sum(self, a, (m, nn)):
        M, N = a.shape
        a = n.reshape(a, (M/m,m,N/nn,nn))
        return n.sum(n.sum(a, 3), 1) / float(m*nn)
    def Gamma(self, z):
        """This is the Lanczos approximation for Gamma function"""
        lanczosG = 7
        lanczos_coef = [0.99999999999980993, 676.5203681218851,\
                        -1259.1392167224028, 771.32342877765313,\
                        -176.61502916214059, 12.507343278686905, \
                        -0.13857109526572012, 9.9843695780195716e-6,\
                        1.5056327351493116e-7]
        if z < 0.5:
            return n.pi / (n.sin(n.pi*z)*self.Gamma(1-z))
        else:
            z -= 1
            x = lanczos_coef[0]
            for i in range(1, lanczosG + 2):
                x += lanczos_coef[i]/(z + i)
                t = z + lanczosG + 0.5
            return n.sqrt(2*n.pi) * t**(z + 0.5) * n.exp(-t) * x

