#++++++++++++++++++++++++++
#
# TITLE: galmorph_make_image.py
#
# PURPOSE: runs galmorph_make_image
#
# INPUTS: all galmorph parameters
#      (a) flx:    total bulge + disk galaxy flux in counts.
#      (b) bt:     bulge-to-total flux ratio.
#      (c) rd:     disk radius in pixels.
#      (d) inc:    disk inclination in radians (0<inc<pi/2). 
#      (e) dang:   disk position angle in radians (0<dang<pi).
#      (f) re:     bulge radius in pixel.
#      (g) ell:    ellipticity of bulge (1-b/a).
#      (h) bang:   bulge position angle in radians (0<bang<pi).
#      (i) ser:    bulge sersic index (0<ser<10).
#      (j) rowctr: center coordinates of galaxy in row dimension.
#      (k) colctr: center coordinates of galaxy in column dimension.
#      (l) point:  fraction of flux in point source
#      (m) bar:    fraction of flux in bar
#      (n) rbar:   half-light radius of bar in pixels
#      (o) barell: bar ellipticity (1-b/a).
#      (p) barser: bar sersic index.
#      (q) nrows:  number of rows in output image.
#      (r) ncols:  number of columns in output image.
#      (s) psf_filename:  filename of psf file (.fits or .txt).
#      (t*) output_filename:  filename of output image file (.fits).
#      (u*) output_profile_filename:  filename of output profile file (.txt).
#
# OUTPUTS: normal galmorph outputs, also returns str of command
#
# PROGRAM CALLS: galmorph_make_image c program
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

import os

def galmorph_make_image( flx,bt,rd,inc, dang, re,ell, bang, ser,rowctr, colctr,point, bar,rbar, barell, barser, nrows, ncols,psf_filename, output_filename = 'NULL', output_profile_filename = 'NULL'):
    cmd = '/home/ameert/galmorph/bin/GALMORPH_make_image %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %d %d %s %s %s' %(flx,bt,rd,inc, dang, re,ell, bang, ser,rowctr, colctr,point, bar,rbar, barell, barser, nrows, ncols,psf_filename, output_filename, output_profile_filename)

    os.system(cmd)

    return cmd

#++++++++++++++++++++++++++
#
# TITLE: galmorph_get_profile
#
# PURPOSE: runs galmorph_get_profile
#
# INPUTS: all galmorph parameters
#      (a) input_image_filename:  filename of image file (.fits or .txt).
#      (b) input_mask_filename:  filename of image file (.fits or .txt).
#      (c) rowctr: center coordinates of galaxy in row dimension.
#      (d) colctr: center coordinates of galaxy in column dimension.
#      (e) output_profile_filename:  filename of output profile file (.txt).
#      (f) ellipticity (optional):  filename of output profile file (.txt).
#      (g) position_angle (optional):  filename of output profile file (.txt).
#
# OUTPUTS: normal galmorph outputs, also returns str of command
#
# PROGRAM CALLS: galmorph_get_profile c program
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

def galmorph_get_profile(input_image_filename, input_mask_filename, rowctr, colctr, output_profile_filename, log_profile = 'NULL', ellipticity = 'NULL', position_angle = 'NULL'):
    cmd = '/home/ameert/galmorph/bin/GALMORPH_get_profile %s %s %d %d %s %s %s %s' %(input_image_filename, input_mask_filename, rowctr, colctr, output_profile_filename, log_profile, ellipticity, position_angle)

    os.system(cmd)

    return cmd


#++++++++++++++++++++++++++
#
# TITLE: profile_to_arcsec_mag
#
# PURPOSE: runs galmorph_get_profile
#
# INPUTS: input_profile_filename: name of profile in pixels, counts
#         output_profile_filename(optional): name of profile in arcsec,
#                                            in mag/arcsec^2
#
# OUTPUTS: creates output_profile_filename file also returns converted values
#
# PROGRAM CALLS: galmorph_get_profile c program
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
import numpy as np

def profile_to_arcsec_mag(aa, kk, airmass,band,  input_profile_filename, output_profile_filename = 'NULL', kcorr = 0, extinction = 0, shift = 0):
    print "hello"
    print input_profile_filename
    print output_profile_filename
    profile = np.loadtxt(input_profile_filename, unpack=True)
    # profile should have 3 columns of data: radius, counts, and error(counts)

    #now shift sky 
    profile[1] += shift

    radius = pixels_to_arcsec(profile[0])
    mag, magerr = co_pix_to_mag_arc(profile[1], profile[2], 
                                    aa, kk, airmass, band)
    mag = mag-extinction-kcorr

    if output_profile_filename != 'NULL':
        f = open(output_profile_filename, 'w')
        f.write('# rad mag magerr\n')
        for rad,data,dataerr in zip(radius,mag,magerr):
            f.write('%.2f %.4e %.4e\n' %(rad,data,dataerr))
        f.close()
    return radius, mag, magerr


def profile_to_arcsec_mag2(aa, kk, airmass, input_profile_filename, output_profile_filename = 'NULL', shift = 0, band = 'r'):

    pix_sz = 0.396
    rad, data, dataerr, aperture_flux = np.loadtxt(input_profile_filename, unpack = True)
    
    #now shift sky 
    data += shift

    rad = pixels_to_arcsec(rad)
    data, dataerr= co_pix_to_mag_arc(data, dataerr, aa, kk, airmass, band)
                                   
    if output_profile_filename != 'NULL':
        f = open(output_profile_filename, 'w')
        f.write('# rad data dataerr\n')
        for rad1,data1,dataerr1 in zip(rad,data,dataerr):
            f.write('%f %f %f\n' %(rad1,data1,dataerr1))
        f.close()
    return rad, data, dataerr

def pixels_to_arcsec(pixels):
    pixel_arcsec = 0.396 #arcseconds per pixel for SDSS

    return pixels * pixel_arcsec

def co_pix_to_mag_arc(surf_bright, sberr, aa, kk, airmass, band):
    holder = surf_bright/((pixels_to_arcsec(1.0))**2.0)
    err = sberr/(pixels_to_arcsec(1.0))**2.0
    holder, err = counts_to_mag(holder, err, band, aa, kk, airmass)

    return holder, err

def mag_to_counts( mag, aa, kk = 0 , airmass = 0):
    exptime = 53.907456 #in seconds, taken from SDSS website www.sdss.org/dr3/algorithms/fluxcal.html
    return exptime * (10**(-.4*mag)) / (10**(0.4*(aa + kk*airmass)))


def counts_to_mag(counts, error, band, aa, kk = 0.0, airmass= 0.0, pogson = True):
    exptime = 53.907456 #in seconds, taken from SDSS website www.sdss.org/dr3/algorithms/fluxcal.html
    softb = {'u': 1.4e-10,'g': 9.0e-11,'r': 1.2e-10,'i': 1.8e-10,'z': 7.4e-10}
    
    fluxrate =(counts/exptime)* 10**(0.4*(aa + kk*airmass))

    if pogson:
        mag = -2.5 * np.log10(fluxrate)
        magerr = 2.5/np.log(10) * error/counts
    else:
        mag = -2.5/np.log(10)*(np.arcsinh(fluxrate/(2.0*softb[band]))+np.log(softb[band]))
        magerr = 2.5/np.log(10) * error/(exptime *0.5*softb[band])*10**(0.4*(aa + kk*airmass))/np.sqrt(1+(fluxrate/(2.0*softb[band]))**2.0)
                          
    return mag, magerr
