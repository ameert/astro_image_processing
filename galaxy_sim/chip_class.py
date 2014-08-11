#!/usr/bin/python

import pyfits as pf
import numpy as np
import scipy as s
import os
import sys
from numpy.random import shuffle
import random as ran
from mysql_class import *
import time
import pylab as pl
import scipy.signal as signal


def test_choice(data, back_cut):
    back_sigma = np.sqrt(130/gain)#/exptime
    backlevel = 130.#/exptime
    mask_data = np.where(np.abs(data) > 3.0 * back_sigma, 1, 0)
    mask_back = np.where(np.abs(back_cut-backlevel) > 3.0 * back_sigma, 1, 0)

    total = np.sum(mask_back*mask_data)
    
    if total >0:
        good = 0
    else:
        good = 1
    return good
                         
          
def add_real_back(infile, nm_stm, back_im = 'test_flat.fits', frame = 'None'):
    back_image = pf.open(back_im)
    back_head = back_image[0].header 
    back_data = back_image[0].data
    back_image.close()
            
    data_image = pf.open(infile)
    data = data_image[0].data
    header = data_image[0].header
    data_image.close()

    back_frame_psf = pf.open(frame)
    obj = back_frame_psf[1].data[0]
    run=obj[params['run']]
    camcol=obj[params['camCol']]
    field=obj[params['field']]
    back_frame_psf.close()

    # added temporarily
    back_data = np.tile(back_data, (2, 2))
    print "back data", np.shape(back_data)

    back_borders = np.shape(back_data)
    print back_borders
    
    borders = np.shape(data)
    print borders
    
    if back_borders[0]<borders[0]:
        diff = borders[0] - back_borders[0]
        data = data[np.ceil(diff/2.0):np.floor(borders[0] - diff/2.0),np.ceil(diff/2.0):np.floor(borders[0] - diff/2.0)]
        borders = np.shape(data)
    if back_borders[1]<borders[1]:
        diff = borders[1] - back_borders[1]
        data = data[np.ceil(diff/2.0):np.floor(borders[1] - diff/2.0),np.ceil(diff/2.0):np.floor(borders[1] - diff/2.0)]
        borders = np.shape(data)
    
    bordersx = borders[0]
    bordersy = borders[1]

    good_choice = 0
    tot_trys = 0
    while good_choice == 0:
        tot_trys += 1
        
        center_y = s.random.uniform(np.ceil(bordersx/2.0), np.floor(back_borders[1] - bordersx/2.0), 1)
        center_x = s.random.uniform(np.ceil(bordersy/2.0),np.floor(back_borders[0] - bordersy/2.0),1)

        center_y = center_y[0]
        center_x = center_x[0]
            
        print bordersx
        print bordersy
        print center_x
        print center_y

        print (center_x - borders[0]/2),(center_x + borders[0]/2 + borders[0]%2), (center_y - borders[1]/2),(center_y+borders[1]/2+ borders[1]%2)
        back_cut = back_data[(center_x - borders[0]/2):(center_x + borders[0]/2 + borders[0]%2), (center_y - borders[1]/2):(center_y+borders[1]/2+ borders[1]%2)]

        print np.shape(data)
        print np.shape(back_cut)
        good_choice = test_choice(data, back_cut)
        if tot_trys > 15:
            good_choice = 1
            print "BAD:infile ", infile, ' doesnt fit!!!!'
        if  good_choice:
            psf_name = do_psf(nm_stm,center_x%2978,center_y%4096,band_char='r',
                              run=run,camcol=camcol,field=field)
            #do a modified psf for fitting
            psf_y = s.random.uniform(np.max([np.ceil(center_y%4096-50), 1]), np.min([np.floor(center_y%4096+50), 4096]))
            psf_x = s.random.uniform(np.max([np.ceil(center_x%2978-50), 1]), np.min([np.floor(center_x%2978+50), 2978]))
            psf_name = do_psf(nm_stm+'_fit',psf_x,psf_y,band_char='r',
                              run=run,camcol=camcol,field=field)
            print "convolving"
            data = make_new_flat('/home/ameert/andre_bcg/sims/sim_image/final_im/', infile, psf_name, fwhm = 0.0)
            print "convolve complete!"
            new_image = data + back_cut

            ext = pf.PrimaryHDU(new_image, header)
            ext.writeto(nm_stm+"_chipflat.fits", clobber = 1)

            ext2 = pf.PrimaryHDU(back_cut)
            ext2.writeto(nm_stm+"_chipback.fits", clobber = 1)
            
    return new_image, header

def do_psf(nm_stm,rowc,colc,band_char='r',run=745,camcol=2,field=518):  
    if band_char == 'u':
        band = 1
    elif band_char == 'g':
        band = 2
    elif band_char == 'r':
        band = 3
    elif band_char == 'i':
        band = 4
    elif band_char == 'z':
        band = 5
        
    nm  = '/home/ameert/bkrd_2/get_field_data/psField-%06d-%d-%04d.fit' %(run, camcol, field)
                
    cmd = '/home/ameert/software/readAtlasImages-v5_4_11/read_PSF  %s %d %f %f %s_psf_con.fits' %(nm, band, rowc, colc, nm_stm)
    os.system(cmd)

    a = pf.open('%s_psf_con.fits' %(nm_stm),'update' )
    # remove 1000 count soft-bias from images
    a[0].data = a[0].data - 1000
    a[0].data = np.abs(a[0].data)
    a[0].data = a[0].data/np.sum(a[0].data)
    a.close()
    return '%s_psf_con.fits' %(nm_stm)

def make_new_flat(outdir, inflat, inpsf, fwhm = 0.0):
    outfile_name = inflat.split('/')[-1]
    outfile_name = outdir+'/'+outfile_name.replace('.fits','_con.fits')
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

    ext. writeto(outfile_name, clobber = 1)
    return new_flat

def add_noise(image,header, Name):
    x_size, y_size  = np.shape(image)
    a = s.random.standard_normal((x_size, y_size))
    data = np.abs(image)

    new_image = data/exptime + a * s.sqrt(data/gain + dark_var)/exptime
    header.update("GAIN", gain, "Gain used in chip sim")
    header.update('RDNOISE', dark_var, "Dark Var in chip")
    header.update('EXPTIME', 1.0, "Exposure time (Sec)")

    ext = pf.PrimaryHDU(new_image, header)
    
    ext.writeto(Name + "_chip.fits", clobber = 1)
        
    return


def mkwgt(Name):
    image = pf.open(Name + "_chip.fits")
    head = image[0].header 
    data = image[0].data*exptime
    image.close()

    wz =  np.sqrt(data / gain+dark_var) / exptime

    hdu = pf.PrimaryHDU(wz.astype(np.float32))
    hdu.writeto(Name + "_chip_r_W.fits", clobber = 1)

    return
