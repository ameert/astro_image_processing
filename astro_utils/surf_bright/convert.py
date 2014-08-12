from astro_image_processing.astro_utils.user_params import *
from astro_image_processing.astro_utils.sizes import *
from astro_image_processing.astro_utils.magnitudes import *


def co_pix_to_mag_arc(surf_bright, sberr, zeropoint, kk = defaults['kk'] , 
                   airmass = defaults['airmass'], band = defaults['band'], 
                   magtype = defaults['magtype'], exptime=defaults['exptime'],
                      pixsz = defaults['pixsz']):

    holder = surf_bright/(pixels_to_size(1.0,pixsz = pixsz)**2.0)
    err = sberr/(pixels_to_size(1.0,pixsz = pixsz)**2.0)
    holder, err = counts_to_mag(holder, err, zeropoint, kk = kk, 
                                airmass = airmass, band = band, 
                                magtype = magtype, exptime=exptime)

    return holder, err

def mag_arc_to_co_pix(surf_bright, sberr, zeropoint, kk = defaults['kk'] , 
                   airmass = defaults['airmass'], band = defaults['band'], 
                   magtype = defaults['magtype'], exptime=defaults['exptime'],
                      pixsz = defaults['pixsz']):


    holder, err = mag_to_counts(surf_bright, sberr, zeropoint, 
                                kk = kk , airmass = airmass, band = band, 
                                magtype = magtype, exptime=exptime)

    holder = holder*(pixels_to_size(1.0,pixsz = pixsz)**2.0)
    err = err*(pixels_to_size(1.0,pixsz = pixsz)**2.0)
    
    return holder, err



