from astro_image_processing.mysql.mysql_class import *
import numpy as np
import pylab as pl
from astro_image_processing.MatplotRc import *
from astro_image_processing.statistics.bin_stats import *
import sys
import os
import os.path
import pyfits as pf
import astro_image_processing.astro_utils.image_analysis.image_info as info
import scipy.stats as stats

real = 1
def start_fig(sizech = (13,13)):
    matrc4X6()

    fig = pl.figure(figsize =sizech, frameon = True)

    fig.subplots_adjust(left = 0.3,  # the left side of the subplots of the figure
                        right = 0.97,    # the right side of the subplots of the figure
                        bottom = 0.3,   # the bottom of the subplots of the figure
                        top = 0.95,      # the top of the subplots of the figure
                        wspace = 0.48,   # the amount of width reserved for blank space between subplots
                        hspace = 0.48)   # the amount of height reserved for white space between subplots

    return fig

def mag_sum(mag1, mag2):
    mag1 = 10.0**( -.4*mag1)
    mag2 = 10.0**(-.4*mag2)

    mag_tot = mag1 + mag2
    bt = mag1/(mag1+mag2)
    mag_tot = -2.5 * np.log10(mag_tot)

    return mag_tot, bt

def measure_sn(r_pix, source_count, bkrd, gain, darkvar):
    #calculate the s/n inside the halflight raduis
    num_pix = np.pi*(r_pix**2)
    half_flux = source_count/(2.0*num_pix)
    back_flux = bkrd
    sn = half_flux/np.sqrt((half_flux+back_flux)/gain + darkvar)

    print "galsky ", bkrd[0:2]
    print "counts ", half_flux[0:2]
    print "gain ", gain[0:2]
    print 'darkvar ', darkvar[:2]
    print 'sn ', sn[:2]

    return sn

def mag_to_counts( mag, aa, kk = 0 , airmass = 0):
    exptime = 53.907456 #in seconds, taken from SDSS website 
                        # www.sdss.org/dr3/algorithms/fluxcal.html
    return exptime * (10**(-.4*mag)) / (10**(0.4*(aa + kk*airmass)))

def nanomaggies_to_mags(nanomaggies):
    return 22.5 -2.5*np.log10(nanomaggies)

def find_dir(galcount):
    count = (galcount-1)/250 + 1
    if not os.path.isfile('/media/SDSS2/fit_catalog/data/r/%04d/%08d_r_stamp.fits' %(count, galcount)):
        print "ERROR not found /media/SDSS2/fit_catalog/data/r/%04d/%08d_r_stamp.fits" %(count, galcount)
        sys.exit()
        
    return count
          
dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

# first get the distribution of sn from our original measurements
# we will use the fitted position angle and ellipticity from the 
# single sersic fit

fig_size = get_fig_size()
fig = start_fig(fig_size)            
plot_set = pub_plots(xmaj = 15, xmin = 5, xstr = '%d', 
                     ymaj = 0.05, ymin = 0.01, ystr =  '% 03.2f')

plotrange = (0,75)
binnum = 40
lsl = [1,1,1]

def make_plot(data, color, binnum, plotrange, cls):
    galcount, Ie, Id, magzp, hrad, sky, gain, dark_var  = data

    galcount = np.array(galcount)
    Ie = np.array(Ie)
    Id = np.array(Id)
    magzp = np.array(magzp)
    hrad = np.array(hrad) 
    galsky = np.array(sky, dtype = float )
    gain = np.array(gain)
    dark_var = np.array(dark_var)

    tot_mag = mag_sum(Ie, np.abs(Id))[0]
    counts =  mag_to_counts( tot_mag, -1.0*magzp, kk = 0 , airmass = 0)

    #galsky = nanomaggies_to_mags(galsky)
    galsky = mag_to_counts(galsky, -1.0*magzp, kk = 0 , airmass = 0)
    galsky *=0.396*0.396 #convert to counts per pixel

    sn = measure_sn(hrad, counts, galsky, gain, dark_var)

    weight = np.ones_like(sn)/len(sn)

    pl.hist(sn, range = plotrange,bins = binnum, weights = weight, histtype = 'step', color = color, lw = cls)

    return sn

cmd = "select b.galcount, b.petromag_g, 999, -b.aa_g-b.kk_g*b.airmass_g, b.petroR50_g/0.396, b.sky_g, b.gain_g, b.darkvariance_g from  catalog.CAST as b;"      
data = cursor.get_data(cmd)
make_plot(data, 'g', binnum, plotrange, 2)
#print stats.ks_2samp(sn_real, sn_tmp)

cmd = "select b.galcount, b.petromag_r, 999, -b.aa_r-b.kk_r*b.airmass_r, b.petroR50_r/0.396, b.sky_r, b.gain_r, b.darkvariance_r from  catalog.CAST as b;"      
data = cursor.get_data(cmd)
make_plot(data, 'r', binnum, plotrange, 2)


cmd = "select b.galcount, b.petromag_i, 999, -b.aa_i-b.kk_i*b.airmass_i, b.petroR50_i/0.396, b.sky_i, b.gain_i, b.darkvariance_i from  catalog.CAST as b;"      
data = cursor.get_data(cmd)
make_plot(data, 'k', binnum, plotrange, 2)

pl.xlim((0,55))
pl.ylim((0,.16))
pl.xlabel('S/N')
pl.ylabel('n(S/N)')
    
ax = pl.gca()
plot_set.set_plot(ax)
pl.savefig("data_cmp_sn_all.eps" , format = 'eps')


#vals_real, bins_real, patches =  pl.hist(sn_real, range = plotrange,bins = binnum, normed = True, cumulative = True)
#vals_tmp, bins_tmp, patches =  pl.hist(sn_tmp, range = plotrange,bins = binnum, normed = True, cumulative = True)
#pl.close('all')
#bp = (bins_real[1:]+bins_real[:-1])/2
#pl.plot(bp, vals_real - vals_tmp)
#pl.show()
