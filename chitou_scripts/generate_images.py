import pyfits as pf
import numpy as np
import scipy as sci

import os
import sys

from sersic_classes import *

def decide_obj(probPSF):
    if probPSF > .9:
        return 1
    else:
        return 0

class galaxy(im_obj):
    def __init__(self, Ie_counts, bang, ab, re, Id_counts, dang, ed, rd, 
                 fracdev, xcntr, ycntr, psf_name):
        self.Ie_counts = Ie_counts
        self.bang = bang*np.pi/180.0
        self.ba = 1.0/ab
        self.re = re/0.396
        self.Id_counts = Id_counts
        self.dang = dang*np.pi/180.0
        self.ed = 1/ed
        self.rd = rd/0.396
        self.fracdev = fracdev

        # set convolution box size for 20 times the largest halflight radii
        self.convolution_box_size = np.max((int(self.re*20), int(self.rd*20*1.678), 50))
        print 'box size ', self.convolution_box_size
        self.set_image_params(xcntr = xcntr, ycntr = ycntr, xsize = 2048, ysize = 1489)
        
        sersic_com = sersic(self.Ie_counts, 4.0, self.bang, self.ba, self.re)
        sersic_com.set_image_params(xcntr = self.xcntr, ycntr = self.ycntr, xsize = self.xsize, ysize = self.ysize)
        sersic_com.make_image()
                        
        disk_com = disk(self.Id_counts, self.dang, self.ed, self.rd)
        disk_com.set_image_params(xcntr = self.xcntr, ycntr = self.ycntr, xsize = self.xsize, ysize = self.ysize)
        disk_com.make_image()

        self.new_gal =  im_obj(self.fracdev*sersic_com.image+(1.0-self.fracdev)*disk_com.image)
        
        
        self.new_gal.convolve_image(psf_name, [int(np.max((self.ycntr-self.convolution_box_size, 0))),int(np.min((self.ycntr+self.convolution_box_size, self.ysize - 1))),int(np.max((self.xcntr-self.convolution_box_size, 0))),int(np.min((self.xcntr+self.convolution_box_size, self.xsize - 1)))])


