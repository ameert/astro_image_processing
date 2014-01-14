#++++++++++++++++++++++++++
#
# TITLE: prep_images
#
# PURPOSE: program reads in the list of galaxies, gets the
#          necessary data from casjobs, and performs cutouts
#          and generates psf images
#
# INPUTS: list_name: name of the file listing objects
#         bands:     the bands that we wish to fit
#         data_dir:  the directory where all the data
#                    will be created
#         sdss_filename: the name that all casjobs data queried
#                        from sdss casjobs. If this file already
#                        exists, it should be in the data_dir. The
#                        program looks here for the file before
#                        submitting the query. Default is 'casjobs_sdss.txt'
#
# OUTPUTS: NONE, but does create many files. These
#          include psfield, fpc files. Image cutouts
#          and psf images
#
# PROGRAM CALLS: download_files (these are all imported)
#                read_list
#                prepare_psf
#                cut_images
#                casjobs
#                os
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 4 JAN 2011
#
#-----------------------------------

# Here are all necessary imports needed to run the program 
import os 

def prep_images(list_name='data.txt', bands='r', data_dir='./data_dir/',cut_dir='./cut_dir/', sdss_filename = 'casjobs_sdss.txt'):
    """ PURPOSE: program reads in the list of galaxies, gets the necessary
    data from casjobs, and performs cutouts and generates psf images
    
    INPUTS: list_name: name of the file listing objects
            bands:     the bands that we wish to fit
            data_dir:  the directory where all the data
                       will be created
            sdss_filename: the name that all casjobs data queried
                           from sdss casjobs. If this file already
                           exists, it should be in the data_dir. The
                           program looks here for the file before
                           submitting the query. Default is 'casjobs_sdss.txt'

    OUTPUTS: NONE, but does create many files. These
             include psfield, fpc files. Image cutouts
             and psf images

    PROGRAM CALLS: download_files (these are all imported)
                   read_list
                   prepare_psf
                   cut_images
                   casjobs
                   os

    CALLING METHOD: prep_images(list_name='data.txt', bands='r', data_dir='./data_dir/',cut_dir='./cut_dir/', sdss_filename = 'casjobs_sdss.txt')"""


    # check for existence of data directory and cutout directory
    # these directories are used to store downloads and output
    if not os.path.isdir(data_dir):
        print data_dir + ' must exist!!'
        print 'Please choose an existing directory!'
        print 'Terminating program'
        return
    if not os.path.isdir(cut_dir):
        print cut_dir + ' must exist!!'
        print 'Please choose an existing directory!'
        print 'Terminating program'
        return

    # check to see if the data has already been downloaded from casjobs
    # if not, then load the catalog
    gal = {}
    if not os.path.isfile(data_dir + sdss_filename):
        gal_cat = {}
        gal_cat['filename'] = sdss_filename

        # try loading the catalog as ra/dec locations
        gal_cat.update(utilities.read_list(data_dir+list_name, 'F,F'))
        if not gal_cat.has_key('ra'):
            print '\nCatalog NOT in ra/dec format, trying sdssobjid format\n\n'
            # try loading the catalog as sdss objid objects
            gal_cat.update(utilities.read_list(data_dir+list_name, 'A'))
        no_sucess = casjobs(gal_cat, data_dir, username, wsid, password)
    else:
        no_sucess = 0

    # This causes the program to exit if there was no sucessful
    # query and no data was found
    if  no_sucess:
        print 'NO CASJOBS DATA FOUND!!!'
        print 'Casjobs query was incorrect or casjobs file is corrupt,'
        print 'please correct the settings and try again'
        return

    # Otherwise, we continue with the program
    gal['filename'] = sdss_filename

    # Right now, All I care about is the data needed to do the cutouts and
    # data downloads, so I ignore all other data and jsut load this.
    gal.update(utilities.read_list(data_dir + sdss_filename, 'I,X,X,I,I,I,I,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,F,F,X,X,X,X,X,F,F,F,F,F,F,F,F,F,F', delimiter = ','))
    #download_files(gal, data_dir, bands)
    make_images.prepare_psf(gal, bands, data_dir, cut_dir)
    make_images.cut_images(gal, bands, data_dir, cut_dir)

    print 'Files downloaded in '+data_dir
    print 'cutouts and psf created in '+cut_dir

    return


