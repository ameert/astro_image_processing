#!/data2/home/ameert/python/bin/python2.5

#++++++++++++++++++++++++++
#
# TITLE: measure_new_profs.py
#
# PURPOSE: measure the color gradients
#          using a consistent annulus 
#          and ellipticity across all
#          g,r,i bands
#
# INPUTS: galaxy number
#
# OUTPUTS: color gradient file containing 
#          the magnitude at different radii
#          it is then up to the user to calculate
#          the gradients
#
# PROGRAM CALLS: ????
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 24 JANUARY 2013
#
#-----------------------------------

import numpy as np
from image_info import *
import sys
import pylab as pl
from sersic_classes import im_obj
from measure_profs_functions import *
import os
from mysql_class import *

band = 'r'
m_stem = 'EM'

galcount = int(sys.argv[1])
eb = float(sys.argv[2])
bpa = float(sys.argv[3])
xctr = float(sys.argv[4])
yctr = float(sys.argv[5])

folder_num = (galcount-1)/250 +1

os.system('/data2/home/ameert/color_grads/scripts/regen_galaxy.py %d serexp %d %s ./' %(galcount, folder_num, band))

imstem = './O_{band}_%08d_{band}_stamp.fits' %(galcount)
mask_stem = '/data2/home/ameert/catalog/{band}/fits/masks/%04d/%s_{band}_%08d_{band}_stamp.fits' %(folder_num, m_stem, galcount)

imfiles = [imstem.replace('{band}', band)]
maskfiles = [mask_stem.replace('{band}', band)]

ims, sims,  masks = get_images(imfiles, maskfiles)

mask = np.where(masks[0]==0, 2, 1)-1
im =ims[0]
sim=sims[0]


img = image_info(im, mask=mask, x_ctr = xctr, y_ctr = yctr,ell = eb, pa = bpa)
img.profile()

simg = image_info(sim, mask=mask, x_ctr = xctr, y_ctr = yctr,ell = eb, pa = bpa)
simg.profile()

outfile = '/data2/home/ameert/color_grads/data/%04d/%08d_%s.resid' %(folder_num,galcount,'r_serexp')
out = open(outfile, 'w')
out.write('#rad data data_err prof prof_err\n')

for rad, dat, dat_err, prof, proferr in zip(img.rads, img.prof, img.proferr, simg.prof, simg.proferr):
    out.write('%6.2f %6.3e %6.3e %6.3e %6.3e\n' %(rad, dat, dat_err, prof, proferr))

out.close()

