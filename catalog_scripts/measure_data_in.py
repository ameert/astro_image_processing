#!/data2/home/ameert/python/bin/python2.5

import numpy as np
import os
from mysql_class import *
import sys
from petrosian import *
from util_funcs import counts_to_mag, mag_to_counts, mag_sum
import pyfits as pf
import image_info as imin

# lets capture the dfitpack error for error handling
from scipy.interpolate import dfitpack
try:
    dfitpack.sproot(-1, -1, -1)
except Exception, e:
    dfitpack_error = type(e)
try:
    dfitpack.sproot(-1, -1, -1)
except dfitpack_error:
    print "Got it!"
    print "dfitpack error captured...continuing"

clim = int(sys.argv[1])
model = sys.argv[2]

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
cursor = mysql_connect(dba, usr, pwd, 'shredder')

table_name = 'DERT'
tot_stem = '/data2/home/ameert/catalog/r/' 
imstem = '%s/data/%04d/' %(tot_stem, clim)
maskstem = '%s/fits/masks/%04d/' %(tot_stem, clim)
pixsz = 0.396 #arcsec per pix


os.chdir(tot_stem)

cmd = 'Alter ignore table %s add column (petro_psf_rad_%s float default -999);' %(table_name, model)

print cmd
try:
    cursor.execute(cmd)
except:
    pass

cmd = 'Alter ignore table %s add column (petro_psf_hrad_%s float default -999);' %(table_name, model)

print cmd
try:
    cursor.execute(cmd)
except:
    pass

cmd = 'Alter ignore table %s add column (petro_psf_mag_%s float default -999);' %(table_name, model)

print cmd
try:
    cursor.execute(cmd)
except:
    pass


#cmd = "select a.galcount, -a.aa_r - a.kk_r*a.airmass_r, b.bulge_xctr, b.bulge_yctr, -2.5*log10(sky_r) from CAST as a, full_dr7_r_ser as b where a.galcount = b.galcount and a.galcount between %d and %d;" %((clim-1)*250 +1, (clim)*250)
cmd = "select a.galcount, -a.aa_r - a.kk_r*a.airmass_r, b.bulge_xctr, b.bulge_yctr, b.galsky from CAST as a, full_dr7_r_ser as b where a.galcount = b.galcount and a.galcount between %d and %d;" %((clim-1)*250 +1, (clim)*250)
galcount_all, zp_all, yctr_all, xctr_all, sky_all = cursor.get_data(cmd)
# YES these y and x coords are flipped, this is because of the difference
# between c and python coords 


for galcount, zp, xctr, yctr, sky in zip(galcount_all, zp_all, xctr_all, yctr_all, sky_all):


    sky_counts = sky#mag_to_counts(sky, -1.0*zp)*pixsz*pixsz/53.907456

    print sky_counts
    
    infile = pf.open('%s%08d_r_stamp.fits' %(imstem, galcount))
    indat = infile[0].data - sky_counts
    infile.close()

    infile = pf.open('%sEM_r_%08d_r_stamp.fits' %(maskstem, galcount))
    inmask = np.where(infile[0].data <0.5, 1, 0)
    infile.close()

    outfilename = '%s%08d_inpsf_profile_ser.txt' %(imstem,galcount)
    outplot = '%s%08d_profile_spline_ser.pdf' %(imstem,galcount)
    
    print 'shapes: ', indat.shape, inmask.shape

    test_info = imin.image_info(indat, mask=inmask, resample=10, resample_window = 10, x_ctr = xctr, y_ctr = yctr, interpolate_mask = False)
    test_info.profile(outfile=outfilename)

    
    try:
        radii, flux, flux_err, flux_inc = np.loadtxt(outfilename, unpack = True)
    except IOError:
        radii = np.array([-999.0])
        flux = np.array([-999.0])
        flux_err = np.array([-999.0])
        flux_inc = np.array([-999.0])
        
    flux = np.extract(radii>0, flux)
    flux_err = np.extract(radii>0, flux_err)
    flux_inc = np.extract(radii>0, flux_inc)
    radii = np.extract(radii>0, radii)

    # lets truncate after the first negative flux measurement
    low_flux = np.where(flux<0.0)
    if low_flux[0].shape[0]>0:
        trunc_point = np.min(low_flux)
    
        flux = flux[0:trunc_point]
        flux_err = flux_err[0:trunc_point]
        flux_inc = flux_inc[0:trunc_point]
        radii = radii[0:trunc_point]
        
    
    radii = radii*pixsz
    flux = flux/(pixsz**2)

    #for a in zip(radii, flux, flux_inc):
    #    print a[0],a[1], a[2]
#########################################
# measure petrosian values
########################################
    petroRad = -999.0
    petroflux=-999.0
    petromag = -999.0
    petro_halfrad = -999.0
    
    try:
        petroRad = calc_petroRad2(radii.copy(), flux.copy(), flux_inc.copy(), eta=0.2, outfile = '')#outplot)
        try:
            petroflux = get_petroflux(petroRad, radii.copy(), flux_inc.copy(), rad_mult = 2.0)
            try:
                petromag = counts_to_mag(petroflux*53.907456, 1.0*zp)
            except: #dfitpack_error:
                petromag = -999.0

            try:    
                petro_halfrad=get_petrohalfrad(petroflux, radii, flux_inc)     
            except: # dfitpack_error:
                petro_halfrad = -999.0

        except: # dfitpack_error:
            petroflux = -999.0
    
    except: # dfitpack_error:
        petroRad = -999.0

    print "galcount: %d" %galcount
    print "petrorad: %.2f" %petroRad
    print "petroflux: %.2f" %petroflux
    print "petromag: %.2f" %petromag
    print "petrohalfrad: %.2f" %petro_halfrad
    
    cmd = 'update %s set petro_psf_hrad_%s = %f, petro_psf_rad_%s = %f, petro_psf_mag_%s=%f where galcount = %d;' %(table_name, model, petro_halfrad, model, petroRad, model, petromag, galcount)
    print cmd
    cmd = cmd.replace('nan', '-999.0')
    cursor.execute(cmd)
infile.close()

#os.system('rm file_%d.list' %clim)
    
    

