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
