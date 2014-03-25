from mysql_class import *
import numpy as np
import pylab as pl
from MatplotRc import *
from bin_stats import *
import sys
import os
import os.path
import pyfits as pf
import image_info as info
import scipy.stats as stats

real = 1
def start_fig(sizech = (13,13)):
    matrc4X6()

    fig = pl.figure(figsize =sizech, frameon = True)

    fig.subplots_adjust(left = 0.25,  # the left side of the subplots of the figure
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

    return sn

def mag_to_counts( mag, aa, kk = 0 , airmass = 0):
    exptime = 53.907456 #in seconds, taken from SDSS website 
                        # www.sdss.org/dr3/algorithms/fluxcal.html
    return exptime * (10**(-.4*mag)) / (10**(0.4*(aa + kk*airmass)))

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
                     ymaj = 0.5, ymin = 0.1, ystr =  '% 02.1f')

plotrange = (0,50)
binnum = 20
lsl = [1,1,1]

def make_plot(data, color, binnum, plotrange, cls):
    galcount, Ie, Id, magzp, hrad, sky, gain, dark_var  = data

    galcount = np.array(galcount)
    Ie = np.array(Ie)
    Id = np.array(Id)
    magzp = np.array(magzp)
    hrad = np.array(hrad) 
    galsky = np.array(sky, dtype = float )*53.907456
    gain = np.array(gain)
    dark_var = np.array(dark_var)

    tot_mag = mag_sum(Ie, np.abs(Id))[0]
    counts =  mag_to_counts( tot_mag, -1.0*magzp, kk = 0 , airmass = 0)

    sn = measure_sn(hrad, counts, galsky, gain, dark_var)

    weight = np.ones_like(sn)*10/len(sn)

    pl.hist(sn, range = plotrange,bins = binnum, weights = weight, histtype = 'step', color = color, lw = cls)

    return sn

#cmd = "select a.galcount, a.Ie, a.Id, a.magzp, a.hrad_pix_psf, a.galsky, b.gain_r, b.darkvariance_r from  full_dr7_r_%s as a, CAST as b where a.galcount = b.galcount;" %('serexp') 
cmd = "select a.galcount, b.petromag_r, 999, -b.aa_r-b.kk_r*b.airmass_r, b.petroR50_r/0.396, a.galsky, b.gain_r, b.darkvariance_r from  full_dr7_r_%s as a, CAST as b where a.galcount = b.galcount;" %('serexp') 

data = cursor.get_data(cmd)
sn_real = make_plot(data, 'k',binnum, plotrange, 2)
print 'mean med ', np.mean(sn_real), np.median(sn_real)

for model, color1 in zip(['ser','devexp','serexp'],['r','g','b']):

#    cmd = "select a.galcount, a.Ie, a.Id, a.magzp, a.hrad_pix_psf, a.galsky, b.gain_r, b.darkvariance_r from  simulations.chip20_serexp as a, CAST as b, simulations.sim_input as d where a.galcount = b.galcount and d.model = '%s' and a.galcount = d.galcount;" %(model) 
    cmd = "select b.galcount, b.petromag_r, 999, -b.aa_r-b.kk_r*b.airmass_r, b.petroR50_r/0.396,  130.0/53.907456, b.gain_r, b.darkvariance_r from  simulations.sim_input as a, CAST as b where a.galcount = b.galcount and a.model = '%s';" %(model) 

    
    data = cursor.get_data(cmd)
    sn_tmp = make_plot(data, color1, binnum, plotrange, 1)
    print stats.ks_2samp(sn_real, sn_tmp)


pl.xlim((0,50))
pl.ylim((0,1.5001))
pl.xlabel('S/N$_{r}$')
pl.ylabel('n(S/N$_{r}$)')
    
ax = pl.gca()
plot_set.set_plot(ax)
pl.savefig("sn_all.eps" , format = 'eps')
