from astro_image_processing.astro_utils.user_params import *

def pixels_to_size(pixels, pixsz = defaults['pixsz']):
    """#++++++++++++++++++++++++++
#
# TITLE: pixels_to_size
#
# PURPOSE: converts pixel scale to angular/physical scale
#
# INPUTS: pixels-the size in pixels
#         pixsz-the size in [units]/pixel
#
# OUTPUTS: returns size in [units] of the numerator of the pixelsz parameter
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
    return pixels * pixsz


def size_to_pixels(size, pixsz = defaults['pixsz']):
    """#++++++++++++++++++++++++++
#
# TITLE: size_to_pixels
#
# PURPOSE: converts angular/physical scale to pixel scale 
#
# INPUTS: size-the size in [units] of the numerator of the pixelsz parameter
#         pixsz-the size in [units]/pixel
#
# OUTPUTS: returns size in pixels
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
    return pixels / pixsz

