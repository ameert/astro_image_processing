#!/data2/home/ameert/python/bin/python2.5

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

model = 'ser'
main_path = '/data2/home/ameert/make_sims/data/ICL/sim_image/g_noise/'
gain = 4.7
dark_var = 1.17
exptime =53.907456

def add_noise(image,header, Name):
    x_size, y_size  = np.shape(image)
    a = s.random.standard_normal((x_size, y_size))
    data = np.abs(image)

    new_image = data + a * s.sqrt(data*exptime/gain + dark_var)/exptime
    header.update("GAIN", gain, "Gain used in chip sim")
    header.update('RDNOISE', dark_var, "Dark Var in chip")
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


curlist = 'list_%s.txt' %(model)
os.system('ls /data2/home/ameert/make_sims/data/ICL/sim_image/0*_chipflat.fits > %s' %(curlist))
infile = open(curlist)
for line in infile.readlines():
    line = line.strip()
    split_line = line.split('/')
    galcount_tmp = int(split_line[-1].split('_')[0])
    nm_stm = main_path+'/'+split_line[-1].split('_chipflat.fits')[0]

    print galcount_tmp
    print nm_stm

    image = pf.open(line)
    head = image[0].header 
    data = image[0].data
    image.close()
    
    add_noise(data, head, nm_stm)

    mkwgt(nm_stm)

infile.close()
