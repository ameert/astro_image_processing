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

seed_val = int(time.time())
s.random.seed(seed_val)
main_path = '/home/ameert/andre_bcg/sims/sim_image/'
gain = 4.7
dark_var = 1.1732
make_chips = 0
num_backs = 200
exptime =53.907456

params = {'rowc_r':135, 'colc_r':140, 'darkvariance_r':110, 'gain_r':105, 
          'airmass_r':100, 'kk_r':95, 'aa_r':90, 'fracdev_r':75, 'expmag_r':70,
          'expPhi_r':65, 'expab_r':60, 'expRad_r':55, 'devmag_r':50, 
          'devPhi_r':45, 'devab_r':40, 'devRad_r':35, 'PSFmag_r':30, 
          'probPSF':12, 'petroMag_r':25, 'run':3, 'rerun':4, 'camCol':5,
          'field':6}

if __name__=="__main__":
    model = sys.argv[1]
    start_num = int(sys.argv[2])
    end_num = int(sys.argv[3])

    curlist = 'list_%s_%d.txt' %(model, start_num)
    os.system('ls %s/0*_%s_flat.fits > %s' %(main_path, model, curlist))
    infile = open(curlist)


    for line in infile.readlines()[start_num:end_num]:
        line = line.strip()
        print line
        split_line = line.split('/')
        galcount_tmp = int(split_line[-1].split('_')[0])
        #if galcount_tmp < 224727:
        #    continue
        nm_stm = main_path+'/final_im/'+split_line[-1].split('_flat.fits')[0]
        chip_choice = s.random.randint(1,num_backs+1)
        print galcount_tmp
        print nm_stm
        print line
        print chip_choice
        print '/home/ameert/bkrd_2/flat_back_%d.fits' %(chip_choice)
        print '/home/ameert/bkrd_2/get_field_data/background_%d.fit' %(chip_choice)
        image, header = add_real_back(line, nm_stm, back_im = '/home/ameert/bkrd_2/flat_back_%d.fits' %(chip_choice), frame =  '/home/ameert/bkrd_2/get_field_data/background_%d.fit' %(chip_choice))
        add_noise(image, header, nm_stm)
        mkwgt(nm_stm)
    infile.close()
