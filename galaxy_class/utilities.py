#++++++++++++++++++++++++++
#
# TITLE: Utilities.py
#
# PURPOSE: various conversion routines for flux conversion
#          of 1d and 2d profiles
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 1 Feb 2011
#
#-----------------------------------

from read_list import *
import numpy as n



#++++++++++++++++++++++++++
#
# TITLE: profile_to_arcsec_mag
#
# PURPOSE: convert a 1d profile from counts/pixel
#          to mag/arcsec^2
#
# INPUTS: aa: zeropoint, should be negative by this convention
#         kk: extinction coefficient
#         airmass: the airmass of the observation
#         input_profile_filename: the name of the file with the
#                                 profile in counts/pixel
#         output_profile_filename: the name of the file that will contain
#                                  the profile in mag/arcsec^2
#         shift: default=0, shift in counts, used for shifting background
#                or subtracting the background
#
# OUTPUTS: returns the galaxy profile in mag/arcsec^2  as a dict. In addition
#          if output_profile_filename is defined, writes the profile to a file
#
# PROGRAM CALLS: uses numpy package, also uses read_list.py written
#                by Alan Meert 
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE:Modified 8 APRIL 2011
#
#-----------------------------------

def profile_to_arcsec_mag(aa, kk, airmass, input_profile_filename, output_profile_filename = 'NULL', shift = 0 ):

    pix_sz = 0.396
    profile = {}
    profile.update(read_list(input_profile_filename, 'F,F,F', column_names = ('rad', 'data', 'dataerr')))
    
    for key in profile.keys():
        profile[key] = n.array(profile[key])

    # remove the fluxes comparable or less than the shift
    profile['rad'] = n.extract(profile['data'] > n.abs(shift), profile['rad'])
    profile['dataerr']= n.extract(profile['data'] > n.abs(shift), profile['dataerr'])
    profile['data'] = n.extract(profile['data'] > n.abs(shift), profile['data'])

    #now shift
    profile['data'] += shift
    # remove negative fluxes to prevent strange interpolation
    profile['rad'] = n.extract(profile['data'] > 0, profile['rad'])
    profile['dataerr']= n.extract(profile['data'] > 0, profile['dataerr'])
    profile['data'] = n.extract(profile['data'] > 0, profile['data'])

    profile['rad'] = pixels_to_arcsec(profile['rad'])
    profile['dataerr'] = co_pix_to_mag_arc(profile['data']-profile['dataerr'], aa, kk, airmass) -co_pix_to_mag_arc(profile['data'], aa, kk, airmass) 
    profile['data'] = co_pix_to_mag_arc(profile['data'], aa, kk, airmass)
                                   
    if output_profile_filename != 'NULL':
        f = open(output_profile_filename, 'w')
        f.write('# rad data dataerr\n')
        for rad,data,dataerr in zip(profile['rad'],profile['data'],profile['dataerr']):
            f.write('%f %f %f\n' %(rad,data,dataerr))
        f.close()
    return profile['rad'], profile['data'], profile['dataerr']
#++++++++++++++++++++++++++
#
# TITLE: 
#
# PURPOSE: 
#
# INPUTS: 
#
# OUTPUTS: 
#
# PROGRAM CALLS:
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE:
#
#-----------------------------------

def pixels_to_arcsec(pixels):
    pixel_arcsec = 0.396 #arcseconds per pixel for SDSS

    return pixels * pixel_arcsec
#++++++++++++++++++++++++++
#
# TITLE: 
#
# PURPOSE: 
#
# INPUTS: 
#
# OUTPUTS: 
#
# PROGRAM CALLS:
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE:
#
#-----------------------------------

def co_pix_to_mag_arc(surf_bright, aa, kk, airmass):
    holder = surf_bright/(pixels_to_arcsec(1.0))**2.0
    holder = counts_to_mag(holder, aa, kk, airmass)

    return holder
#++++++++++++++++++++++++++
#
# TITLE: 
#
# PURPOSE: 
#
# INPUTS: 
#
# OUTPUTS: 
#
# PROGRAM CALLS:
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE:
#
#-----------------------------------

def counts_to_mag(counts, aa, kk = 0.0, airmass= 0.0):
    exptime = 53.907456 #in seconds, taken from SDSS website
    #www.sdss.org/dr3/algorithms/fluxcal.html

    return -2.5 * n.log10(counts/exptime) -( aa + (kk * airmass))
#++++++++++++++++++++++++++
#
# TITLE: 
#
# PURPOSE: 
#
# INPUTS: 
#
# OUTPUTS: 
#
# PROGRAM CALLS:
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE:
#
#-----------------------------------

def mag_to_counts( mag, aa, kk = 0 , airmass = 0):
    exptime = 53.907456 #in seconds,
    # taken from SDSS website www.sdss.org/dr3/algorithms/fluxcal.html
    return exptime * (10**(-.4*mag)) / (10**(0.4*(aa + kk*airmass)))

