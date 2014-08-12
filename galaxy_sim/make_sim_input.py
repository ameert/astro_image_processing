#!/usr/bin/python

import pyfits as p
import numpy as np
import sys
import pickle

from astro_image_processing.mysql.mysql_class import *
from astro_image_processing import user_settings

def get_catalog(sim_settings):
    """Returns a catalog dictionary for the make_sim code"""
    cursor = mysql_connect(user_settings.mysql_params['dba'],
			       user_settings.mysql_params['user'],
			       user_settings.mysql_params['pwd'],
			       user_settings.mysql_params['host'])

    start = get_val("Enter the starting simcount value:", int)
    stop = get_val("Enter the starting simcount value:", int)

    cmd = "select a.simcount, b.run, b.camcol, b.field,  a.n, a.re, a.Ie, a.eb,a.rd, a.Id, a.ed, a.BT, a.zeropoint_sdss_r,a.bpa+90.0, a.dpa+90.0, a.z, b.petroR50_r, a.galcount from  sim_input as a, CAST as b where  a.galcount = b.galcount and a.simcount between %d and %d order by a.simcount;" %(start, stop)
    print cmd
    cursor.cursor.execute(cmd)
    catalog = {}
	
    for row in cursor.cursor.fetchall():		
        print row
        simcount, run, camcol, field, n, re, Ie, eb, rd, Id, ed, BT, zeropoint_sdss_r,bpa, dpa, z, petroR50_r, galcount= row
        
        re = re * np.sqrt(eb) # now circularized 

        # ensure that undefined magnitudes are treated as dim objects
        if Id < -60:
            Id = -1.0* Id
        if Ie < -60:
            Ie = -1.0* Ie

        #make sure disk radii don't cause integration issues
        if rd < 0:
            rd = 1000

        if ed < 0:
            ed = 0
        elif ed > 1:
            ed = 1

        catalog[simcount] = {
                    'simcount':simcount, 
                    'run':run, 
                    'comcol':camcol, 
                    'field':field, 
                    'n':n, 
                    're':re, 
                    'Ie':Ie, 
                    'eb':eb, 
                    'rd':rd, 
                    'Id':Id, 
                    'inc':np.arccos(ed), 
                    'BT':BT, 
                    'zeropoint':zeropoint_sdss_r,
                    'bpa':bpa, 
                    'dpa':dpa, 
                    'z':z, 
                    'half_rad':petroR50_r, #in arcsec 
                    'name':'%08d' %(simcount),
                    'psf_image':'/media/SDSS2/fit_catalog/data/{band}/{folder:04d}/{galcount:08d}_{band}_psf.fits'.format(galcount=galcount, folder = (galcount-1)/250 +1, band=sim_settings['band']),
                    'background':'/media/BACKUP/sdss_sample/data/{band}/fpC-{run:06d}-{band}{camcol}-{field:04d}.fit.gz'.format(band = sim_settings['band'],run=run, camcol=camcol, field=field),
}
    return catalog

def get_val(text, rettype):
    """gets value and tests that it is correct type"""
    while True:
        outval=raw_input(text)
        try:
            outval = rettype(outval)
            break
        except:
            print "Improper value entered! Try again!"
    return outval

# get the file to dump catalog to 
outfile = get_val("Enter the output catalog file name (full path please):", str)

sim_settings = {}

sim_settings['pixelscale'] = get_val("Enter the pixelscale in arcsec/pixel:", float)
sim_settings['exptime']    = get_val("Enter exposure time in seconds:", float)
sim_settings['magtype']    = get_val("Enter the magnitude type (pogson or asinh):", str)
sim_settings['band']    = get_val("Enter the band (g,r,i):", str)
sim_settings['outpath'] = get_val("Enter the path to the simulation output directory:", str)
sim_settings['noise'] = get_val("Add noise?(yes or no)", str).lower()=='yes'
sim_settings['simback'] = get_val("Add simulated background?(yes or no)", str).lower()=='yes'
sim_settings['realback'] = get_val("Add Real background?(yes or no)", str).lower()=='yes'

print """
---------------------------------
  BEGIN CATALOG GENERATION 
---------------------------------
NOTE: Catalogs should have circularized bulge radii,
non-circularized disk radii,
all magnitudes greater than 0,
all ellipticities greater than 0,
all disk ellipticities given in inclination (radians)
"""

sim_settings['catalog'] = get_catalog(sim_settings)
print sim_settings['catalog']

print "Writing pickle catalog"
dumpfile = open(outfile,'w')
pickle.dump(sim_settings,dumpfile)
dumpfile.close()
print "Catalog written to %s. You may now run make_sims" %outfile
