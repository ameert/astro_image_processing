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
#        download_files(gal, data_dir, band)
#        prepare_psf(gal, band, data_dir, cut_dir)
        cut_images(gal, band, data_dir, cut_dir, cut_size = cut_size, 
                   pix_scale = pix_scale, min_size = min_size)

    return 0



if __name__ == "__main__":
    main()
