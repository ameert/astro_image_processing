from astro_utils.user_params import *
import numpy as np

def mag_to_counts( mag, magerr, zeropoint, kk = defaults['kk'] , 
                   airmass = defaults['airmass'], band = defaults['band'], 
                   magtype = defaults['magtype'], exptime=defaults['exptime']):
    """#++++++++++++++++++++++++++
#
# TITLE: mag_to_counts
#
# PURPOSE: converts magnitudes to counts
#
# INPUTS: mag-magnitude
#         magerr-error on magnitudes
#         zeropoint-zeropoint
#         kk-extinction coefficeint
#         airmass-the airmass value
#         band-str representing the band if using asinh  
#         magtype-pogson or asinh 
#         exptime-the exposure time in seconds
#
# OUTPUTS: returns counts
#
# PROGRAM CALLS: astro_utils.user_params
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# DATE: 1 Feb 2011
# 
# NOTE: This uses the default params 
#       given in the user_params file
#       
#-----------------------------------
"""
    if magtype == 'pogson':
        fluxrate = 10.0**(-0.4*mag) 
        fluxrate_err = (np.log(10)/2.5)*fluxrate*magerr     
    elif magtype == 'asinh':
        fluxrate = 2.0 * softb[band]*np.sinh((np.log(10)-mag)/2.5 -np.log(softb[band]))
        fluxrate_err = (np.log(10)/2.5)*(2.0 *magerr*np.sqrt(1.0 + (fluxrate/(2.0*softb[band]))**2.0))/softb[band] 

    counts = fluxrate*exptime / 10.0**(-0.4*(zeropoint - kk*airmass)) 
    count_err = fluxrate_err*exptime / 10.0**(-0.4*(zeropoint - kk*airmass))
    
    return counts, count_err

def counts_to_mag(counts, count_err, zeropoint, kk = defaults['kk'] , 
                  airmass = defaults['airmass'], band = defaults['band'], 
                  magtype = defaults['magtype'], exptime=defaults['exptime']):
    """#++++++++++++++++++++++++++
#
# TITLE: counts_to_mag
#
# PURPOSE: converts counts to magnitudes
#
# INPUTS: counts-counts for the given exptime
#         count_err-error on counts
#         zeropoint-zeropoint
#         kk-extinction coefficeint
#         airmass-the airmass value
#         band-str representing the band if using asinh  
#         magtype-pogson or asinh 
#         exptime-the exposure time in seconds
#         
# OUTPUTS: returns counts
#
# PROGRAM CALLS: astro_utils.user_params
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# DATE: 1 Feb 2011
# 
# NOTE: This uses the default params 
#       given in the user_params file
#       
#-----------------------------------
"""
    
    fluxrate =(counts/exptime)* 10**(-0.4*(zeropoint - kk*airmass))
    fluxrate_err =(count_err/exptime)* 10**(-0.4*(zeropoint - kk*airmass))

    if magtype == 'pogson':
        mag = -2.5 * np.log10(fluxrate)
        magerr = 2.5/np.log(10) * count_err/counts
    elif magtype == 'asinh':
        mag = -2.5/np.log(10)*(np.arcsinh(fluxrate/(2.0*softb[band]))+np.log(softb[band]))
        magerr = 2.5/np.log(10) * fluxrate_err*(0.5*softb[band])/np.sqrt(1+(fluxrate/(2.0*softb[band]))**2.0)
                          
    return mag, magerr

def magsum(mag1, mag2):
    """#++++++++++++++++++++++++++
#
# TITLE: magsum
#
# PURPOSE: adds two magnitudes
#
# INPUTS: mag1 - a magnitude
#         mag2 - a magnitude
#         
# OUTPUTS: returns magsum
#
# PROGRAM CALLS: numpy
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# DATE: 1 Feb 2011
# 
# NOTE: This uses the default params 
#       given in the user_params file
#       
#-----------------------------------
"""
    return -2.5*np.log10(10**(-0.4*mag1)+10**(-0.4*mag2))
