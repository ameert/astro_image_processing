from astro_utils.user_params import *
from astro_utils.sizes import *
from astro_utils.surf_bright import *

import numpy as np

def profile_to_arcsec_mag(input_profile_filename, zeropoint, 
                   output_profile_filename = 'NULL', kk = defaults['kk'] , 
                   airmass = defaults['airmass'], band = defaults['band'], 
                   magtype = defaults['magtype'], exptime=defaults['exptime'],
                   pixsz = defaults['pixsz'], shift = 0):
    """#++++++++++++++++++++++++++
#
# TITLE: profile_to_arcsec_mag
#
# PURPOSE: converts a profile in pixels and counts
#          to a profile in mags and arcsec
#
# INPUTS: input_profile_filename: name of profile in pixels, counts with format 
#                                 commented lines begin with '#'
#                                 first 3 columns must be (rad, data, err)
#                                 additional columns ignored
#         zeropoint-zeropoint
#         output_profile_filename(optional): name of profile in arcsec,
#                                            in mag/arcsec^2
#         kk-extinction coefficeint
#         airmass-the airmass value
#         band-str representing the band if using asinh  
#         magtype-pogson or asinh 
#         exptime-the exposure time in seconds
#         pixsz- the pixel size in [units]/pixel
#         shift- the number of counts/pixel to shift the image 
#                (for adjusting sky levels)
#
# OUTPUTS: creates output_profile_filename file also returns converted values
#
# PROGRAM CALLS: numpy, additional code from this package
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# DATE: 1 Feb 2011
#
#-----------------------------------
"""
    input_type = input_profile_filename.split('.')[1]
    if input_type == 'npz':
        print 'loading npz file'
        profile = np.load(input_profile_filename)
    else:
        print 'loading txt file'
        profile = {}
        profile['rads'], profile['prof'],profile['proferr'],profile['aperflux'],profile['included_pix'] = np.loadtxt(input_profile_filename, unpack=True)

    #now shift sky 
    profile['prof'] += shift

    radius = pixels_to_size(profile['rads'],pixsz = pixsz)
    mag, magerr = co_pix_to_mag_arc(profile['prof'], profile['proferr'], 
                                    zeropoint, kk = kk, 
                                    airmass = airmass, band = band, 
                                    magtype = magtype, exptime=exptime)

    if output_profile_filename != 'NULL':
        f = open(output_profile_filename, 'w')
        f.write('# rad mag magerr\n')
        for rad,data,dataerr in zip(radius,mag,magerr):
            f.write('%.2f %.4e %.4e\n' %(rad,data,dataerr))
        f.close()
    return radius, mag, magerr
