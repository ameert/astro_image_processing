#!/usr/bin/python

import pyfits as p
import numpy as np
import sys
from astro_image_processing.mysql.mysql_class import *
from astro_image_processing.galaxy_sim import *
from astro_image_processing import user_settings
from astro_image_processing.astro_utils.magnitudes import mag_to_counts 

if __name__=="__main__":
	try:
		pixscale = float(sys.argv[1])
	except IndexError:
		pixscale = float(raw_input("Enter the pixel scale (arcsec/pixel):"))
	try:
		start = int(sys.argv[2])
	except IndexError:
		start = int(raw_input("Enter the starting index:"))	
	try:
		stop = int(sys.argv[3])
	except IndexError:
		stop = int(raw_input("Enter the stopping index:"))	



	cursor = mysql_connect(user_settings.mysql_params['dba'],
			       user_settings.mysql_params['user'],
			       user_settings.mysql_params['pwd'],
			       user_settings.mysql_params['host'])

	cmd = "select a.simcount, b.run, b.camcol, b.field,  a.n, a.re, a.re_kpc, a.Ie, a.eb,a.rd, a.Id, a.ed, a.BT, a.zeropoint_sdss_r,a.bpa+90.0, a.dpa+90.0, a.z, b.petroR50_r from  sim_input as a, CAST as b where  a.galcount = b.galcount and a.simcount between %d and %d order by a.simcount;" %(start, stop)

	cursor.cursor.execute(cmd)
	row = cursor.cursor.fetchone()
	
	while row is not None:		
		galcount, run, camcol, field, n, re, re_kpc, Ie, eb, rd, Id, ed, BT, zeropoint_sdss_r,bpa, dpa, z, petroR50_r= row

		print galcount
		simcount = galcount
		half_rad = petroR50_r #in arcsec

		re = re * np.sqrt(eb) # now circularized 

		# ensure that undefined magnitudes are treated as dim objects
		if Id < -60:
		    Id = -1.0* Id
		if Ie < -60:
		    Ie = -1.0* Ie

		#make sure disk radii don't cause integration issues
		if rd < 0:
		    rd = 1000

		Ie_count = mag_to_counts(Ie,0.0, zeropoint_sdss_r, kk=0.0, 
					 airmass = 0.0, band = 'r',
					 magtype = 'pogson', exptime = 1.0)
		Id_count = mag_to_counts(Id,0.0, zeropoint_sdss_r, kk=0.0, 
					 airmass = 0.0, band = 'r',
					 magtype = 'pogson', exptime = 1.0)
		Ie_count = 1
		Id_count = 1

		if ed < 0:
		    ed = 0
		elif ed > 1:
		    ed = 1

		inc = np.arccos(ed)

		name = '%08d' %(simcount)
		psf_image = '/media/SDSS2/fit_catalog/data/r/%04d/%08d_r_psf.fits' %((galcount-1)/250 +1, galcount)
		background = '/media/BACKUP/sdss_sample/data/r/fpC-%06d-r%d-%04d.fit.gz' %(run, camcol, field)
		#try:

		gal = galaxy('/home/ameert/test_sims/',name,Ie_count,Id_count, 
			     rd, inc, dpa, re, eb, bpa, n, bulge_mag = Ie, 
			     disk_mag = Id, zp = zeropoint_sdss_r, 
			     half_light_arcsec = half_rad, 
			     psf_name= psf_image, pix_sz = pixscale)
		gal.make_profile()
		gal.add_noise()
		gal.add_simulated_back()
		    #gal.add_real_back(back_im = background)
	#        except:
	#            pass

		row = cursor.cursor.fetchone()
