#++++++++++++++++++++++++++
#
# TITLE: profile_to_arcsec_mag
#
# PURPOSE: reads profile in counts and radii 
#          and produces profiles in arcsec and 
#          mag/arcsec^2
#
# INPUTS: input_profile_filename: name of profile in pixels, counts
#         output_profile_filename(optional): name of profile in arcsec,
#                                            in mag/arcsec^2
#
# OUTPUTS: creates output_profile_filename file also returns converted values
#
# PROGRAM CALLS: File contains everything needed
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
#       REVISED: 28 JAN 2013
#-----------------------------------

import numpy as np

plate_scale = 0.396 # arcsec per pixel
exptime = 1.0#53.907456 #in seconds, taken from SDSS website
    #www.sdss.org/dr3/algorithms/fluxcal.html

def profile_to_arcsec_mag(aa, kk, airmass,band,  input_profile_filename, output_profile_filename = 'NULL', kcorr = 0, extinction = 0):

    profile = np.loadtxt(input_profile_filename, unpack=True)
    # profile should have 3 columns of data: radius, counts, and error(counts)

    bad_dat = np.where(profile[1]>-900.0)
    radius = pixels_to_arcsec(profile[0][bad_dat])
    mag, magerr = co_pix_to_mag_arc(profile[1][bad_dat], profile[2][bad_dat], band, 
                                    aa, kk, airmass)
    mag = mag-extinction-kcorr
                                   
    if output_profile_filename != 'NULL':
        f = open(output_profile_filename, 'w')
        f.write('# rad mag magerr\n')
        for rad,data,dataerr in zip(radius,mag,magerr):
            f.write('%.2f %.4e %.4e\n' %(rad,data,dataerr))
        f.close()
    return radius, mag, magerr

def pixels_to_arcsec(pixels):
    return pixels * plate_scale

def co_pix_to_mag_arc(surf_bright, err, band, aa, kk, airmass):
    tmp_sb = surf_bright/(pixels_to_arcsec(1.0))**2.0
    tmp_err = err/(pixels_to_arcsec(1.0))**2.0
    mag, err = counts_to_mag(tmp_sb, tmp_err, band, aa, kk, airmass)

    return mag, err

def counts_to_mag(counts, error, band, aa, kk = 0.0, airmass= 0.0):
    softb = {'u': 1.4e-10,'g': 9.0e-11,'r': 1.2e-10,'i': 1.8e-10,'z': 7.4e-10}
    
    fluxrate =counts/exptime* 10**(0.4*(aa + kk*airmass))
    
    mag = -2.5/np.log(10)*(np.arcsinh(fluxrate/(2.0*softb[band]))+np.log(softb[band]))
    magerr = 2.5/np.log(10) * error/(exptime *0.5*softb[band])*10**(0.4*(aa + kk*airmass))/np.sqrt(1+(fluxrate/(2.0*softb[band]))**2.0)
                          
    return mag, magerr



