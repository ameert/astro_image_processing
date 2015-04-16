#!/usr/bin/python

### First the imports ####
import os 
import sys
import numpy as np
from argparse import ArgumentParser, ArgumentError
from download_files import *
from prepare_psf import *
from cut_sdss3 import *
import astro_image_processing.user_settings as user_settings
import astro_image_processing.cut_pipe.get_data as get_data
from astro_image_processing.mysql import *
from make_dirs import build_dirs

<<<<<<< HEAD
### Now set the essential variables ###
### mysql info ###
table_name = 'manga_earlytypes'
### Paths ###
data_dir = '/data3/MANGA/SDSS3/data/'
cut_dir =  '/data3/MANGA/SDSS3/cutouts/'
### Settings for cutouts ###
bands = 'gri' # list all desired bands in a single string
pix_scale = 0.396 # arcsec per pixel, check for MANGA!!!!
cut_size = 20.0 # the radius of the cutout image in multiples of PetroRad50
min_size = 80.0 # minimum size in pixels
folder_size = 250 # num of galaxies/folder
folder_fmt = "%04d"

### And fetch the starting and ending points, if not supplied, it will
### try to do EVERYTHING ###
try:
    start_num = int(sys.argv[1])
except:
    start_num = -999
try:
    end_num = int(sys.argv[2])
except:
    end_num = 1000000000

if (end_num-start_num > 1000000) or start_num < 0 or end_num >999999999:
    print """-----------------------------------------------
!!!!WARNING!!!!
-----------------------------------------------
The start_num %d and/or end_num %d may be wrong. 
Hit enter to continue, otherwise type "exit" to 
quit the program.
"""
    choice = raw_input("Please enter your choice: ")

    if choice.strip() == 'exit':
        sys.exit()
=======
### Now import configuration variables ###
from cutout_config import *

def get_options_main():
    desc = """Downloads the data and makes cutouts for galaxies with ID numbers 
between start_num and end_num given by the user"""

    parser = ArgumentParser(description = desc)
    parser.add_argument("start_num", action="store", type=int,
                         help="Starting Galaxy for cutouts")
    parser.add_argument("end_num", action="store", type=int,
                        help="Ending Galaxy for cutouts")
    parser.add_argument("-t","--test", action="store_false", 
                        dest="full_run", default = True,
                        help="run a test set")
>>>>>>> 6c397462e67a35862fba0efc2387c4d3553bae4d

    # parses command line aguments for pymorph
    args = parser.parse_args()

    return args

def main():
    """run_cutouts downloads the images and runs the cutouts, weight, and PSF images for a set of galaxies"""

    options = get_options_main()

    # Test for the folders and fix if possible, otherwise exit
    if not build_dirs(data_dir, cut_dir, bands):
        print "Dir structure is wrong and can't be fixed!!!\nExiting now..."
        sys.exit()

    if options.full_run:
        #runs on user-submitted data
        """get the data needed for fitting
    This script requires galcount, run, rerun, camCol, field, 
    rowc(for each band), colc(for each band), petroR50(for each band) 
    """
        gal = get_data.get_cut_data(options.start_num, options.end_num)

    else:
        #uses a small test set provided for the user
        testfile = 'cut_example_data.pickle'
        print "Running test set contained in %s" %testfile
        import pickle
        a = open(testfile)
        gal = pickle.load(a)
        a.close()

    ### now cut the data
    for band in bands:
        download_files(gal, data_dir, band)
        prepare_psf(gal, band, data_dir, cut_dir)
        cut_images(gal, band, data_dir, cut_dir, cut_size = cut_size, 
                   pix_scale = pix_scale, min_size = min_size)

    return 0


<<<<<<< HEAD
gal = get_cut_data(table_prefix, params, bands, band_params, start_num, end_num,
                   cursor)
### group the output into directories for easier handling
gal['dir_end'] = [ folder_fmt %a for a in ((np.array(gal['galcount'])-1)/folder_size +1)]
 
### now cut the data
for band in bands:
    download_files(gal, data_dir, band)
    prepare_psf(gal, band, data_dir, cut_dir)
    cut_images(gal, band, data_dir, cut_dir, cut_size = cut_size, 
               pix_scale = pix_scale, min_size = min_size)
=======
>>>>>>> 6c397462e67a35862fba0efc2387c4d3553bae4d

if __name__ == "__main__":
    main()
