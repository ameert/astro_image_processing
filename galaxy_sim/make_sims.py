#!/usr/bin/python

import pyfits as p
import numpy as np
import sys
import pickle
import traceback
import logging

from astro_image_processing.mysql.mysql_class import *
from astro_image_processing.galaxy_sim import *
from astro_image_processing import user_settings
from astro_image_processing.astro_utils.magnitudes import mag_to_counts 

if __name__=="__main__":
	logging.basicConfig(filename='make_sims.log',level=logging.DEBUG)
	

	try:
		incat = sys.argv[1]
		print "Reading pickled catalog %s" %incat
		logging.info("Reading pickled catalog %s" %incat)
		infile = open(incat)
		sim_settings = pickle.load(infile)
		infile.close()
	except:
		print "Catalog cannot be read!"
		traceback.print_exc()
		logging.error('Catalog cannot be read!\n', exc_info=True)
	for galnum in sim_settings['catalog'].keys():
		curr_gal = sim_settings['catalog'][galnum]
		logging.info("Beginning galaxy %d" %galnum)

		try:
			Ie_count = mag_to_counts(curr_gal['Ie'],0.0, 
						 curr_gal['zeropoint'], 
						 band = sim_settings['band'],
						 magtype = sim_settings['magtype'], 
						 exptime = sim_settings['exptime'])[0]
			Id_count = mag_to_counts(curr_gal['Id'],0.0, 
						 curr_gal['zeropoint'], 
						 band = sim_settings['band'],
						 magtype = sim_settings['magtype'], 
						 exptime = sim_settings['exptime'])[0]

			gal = galaxy(sim_settings['outpath'],curr_gal['name'],
			     Ie_count,Id_count, 
			     curr_gal['rd'], curr_gal['inc'], curr_gal['dpa'],
			     curr_gal['re'], curr_gal['eb'], curr_gal['bpa'], 
			     curr_gal['n'], bulge_mag = curr_gal['Ie'], 
			     disk_mag = curr_gal['Id'], 
			     zp = curr_gal['zeropoint'], 
			     half_light_arcsec = curr_gal['half_rad'], 
			     psf_name= curr_gal['psf_image'], 
			     pix_sz = sim_settings['pixelscale'])
			gal.make_profile()
			if sim_settings['noise'] or sim_settings['realback']:
				gal.add_noise()
			if sim_settings['simback']:
				gal.add_simulated_back()
			if sim_settings['realback']:
				gal.add_real_back(back_im=curr_gal['background'])
			
		except:
			logging.warning("Galaxy %d Skipped or inproperly simulated" %galnum, exc_info=True)
