#!/usr/bin/python

import pyfits as pf
import numpy as np
import scipy as s
import os
import sys
from numpy.random import shuffle
import random as ran
from mysql.mysql_class import *
import time
import pylab as pl
import scipy.signal as signal

seed_val = int(time.time())
s.random.seed(seed_val)
main_path = '/home/ameert/RESEARCH/clusters/data/sims/'
exptime =53.907456

def add_real_back(main_path, nm_stm, gal_num, ICL_num, useICL,back_im,
                  rowc, colc):
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
    
    print (center_x - borders[0]/2),(center_x + borders[0]/2 + borders[0]%2), (center_y - borders[1]/2),(center_y+borders[1]/2+ borders[1]%2)
    back_cut = back_data[(center_x - borders[0]/2):(center_x + borders[0]/2 + borders[0]%2), (center_y - borders[1]/2):(center_y+borders[1]/2+ borders[1]%2)]
    print np.shape(data)
    print np.shape(back_cut)

    new_image = data + back_cut

    ext = pf.PrimaryHDU(new_image, header)
    ext.writeto(nm_stm+"_chipflat.fits", clobber = 1)
            
    return new_image, header

def add_noise(image,header, Name,gain, dark_var):
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


def mkwgt(Name, gain, dark_var):
    image = pf.open(Name + "_chip.fits")
    head = image[0].header 
    data = image[0].data*exptime
    image.close()

    wz =  np.sqrt(data / gain+dark_var) / exptime

    hdu = pf.PrimaryHDU(wz.astype(np.float32))
    hdu.writeto(Name + "_chip_r_W.fits", clobber = 1)

    return

if __name__=="__main__":

    gal_cat = {'galcount':(138529,142447,149162,558387,561842), 
               'run':(2583,2662,2738,3325,3325),
               'rerun':(40,40,40,41,41),
               'camcol':(4,3,4,1,4), 
               'field':(130,210,201,212,133),
               'rowc':{'g':(501.419,505.145,662.795,748.299,544.346),
                       'r':(490.855,494.561,652.493,735.198,534.715)},
               'colc':{'g':(881.964,1717.7,1070.83,1255.06,1789.28),
                       'r':(879.202,1716.55,1071.73,1256.36,1791.83)},
               'gain':{'g':(3.995,3.845,3.995,3.32,3.995),
                       'r':(4.76,4.72,4.76,4.71,4.76)},
               'darkvar':{'g':(1.96,1.3225,1.96,15.6025,1.96),
                          'r':(1.3225,1.3225,1.3225,1.8225,1.3225)},}

    gal_num = int(sys.argv[1])
    band = sys.argv[2]
    try:
        useICL = sys.argv[3]
        if useICL=='icl':
            useICL = True
        else:
            useICL = False
    except:
        useICL = False

    ICL_num = gal_num +63

    nm_stm = '%08d_%s_' %(gal_num, band)
    if useICL:
        nm_stm +="ICL_"
    else:
        nm_stm +="noICL_"

    print 'galaxy ',gal_num
    if useICL:
        print "adding ICL"
    else:
        print "NOT adding ICL"
    print 'ICL ',ICL_num

    image, header = add_real_back(main_path, nm_stm, gal_num, ICL_num, useICL,
                                  back_im,rowc, colc)
    add_noise(image, header, nm_stm,gain, dark_var)
    mkwgt(nm_stm, gain, dark_var)
    infile.close()
