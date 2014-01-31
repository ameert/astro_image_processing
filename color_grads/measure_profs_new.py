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


bands = 'gri'
m_stem = 'EM'

galcount = int(sys.argv[1])

folder_num = (galcount-1)/250 +1

save_dir = '/scratch/%08d' %galcount
try:
    os.system('mkdir %s' %save_dir)
except:
    pass

for band in bands:
    os.system('/home/ameert/color_grads/scripts/regen_galaxy.py %d ser %d %s %s' %(galcount, folder_num, band, save_dir))

imstem = '%s/O_{band}_%08d_{band}_stamp.fits' %(save_dir, galcount)
mask_stem = '/home/ameert/catalog/{band}/fits/masks/%04d/%s_{band}_%08d_{band}_stamp.fits' %(folder_num, m_stem, galcount)

imfiles = [ imstem.replace('{band}', band) for band in bands]
maskfiles = [mask_stem.replace('{band}', band) for band in bands]

try:
    im, sim,  masks = get_images(imfiles, maskfiles)
 
    try:
        mask = np.where(masks[0]+masks[1]+masks[2] == 0, 1, 0)
        im.append(im[0]+im[1]+im[2])
        sim.append(sim[0]+sim[1]+sim[2])
    except:
        im = resize_images(galcount, im)
        sim = resize_images(galcount, sim)
        masks = resize_images(galcount, masks)

        mask = np.where(masks[0]+masks[1]+masks[2] == 0, 1, 0)
        im.append(im[0]+im[1]+im[2])
        sim.append(sim[0]+sim[1]+sim[2])

    imdat = image_info(sim[3], mask = mask[:,:])

    for im_d in [0,1,2]:
        img = image_info(sim[im_d], mask = mask[:,:], 
                         x_ctr = imdat.x_ctr, y_ctr = imdat.y_ctr,
                         ell = imdat.ba, pa = imdat.pa)
        img.profile(outfile = '/home/ameert/color_grads/data/%04d/%08d_%s_ser.npz' %(folder_num,galcount,bands[im_d]))

        for im_f in [0,1,2]:
            if im_d == im_f:
                continue
            im_con = im_obj(image = sim[im_d])
            im_con.convolve_image('/home/ameert/catalog/%s/data/%04d/%08d_%s_psf.fits' %(bands[im_f],folder_num, galcount, bands[im_f]))
            img = image_info(im_con.convolved_image, mask = mask[:,:], 
                             x_ctr = imdat.x_ctr, y_ctr = imdat.y_ctr,
                             ell = imdat.ba, pa = imdat.pa)
            img.profile(outfile = '/home/ameert/color_grads/data/%04d/%08d_%s_%s_ser.npz' %(folder_num,galcount,bands[im_d], bands[im_f]))

except:
    pass

os.system('rm -rf %s' %save_dir)
 
"""will measure the color gradients for a single galaxy given lists of bands, image_names, psfs, masks, centers (as a list of (x_ctr, y_ctr) tuples), backgrounds, k corrections, extinctions and magnitude zeropoints...NOTE:this assumes that the images have the same exposure time so you must normalize properly."""



