from mysql_class import *
import numpy as np
import pylab as pl
from MatplotRc import *
import ndimage
from bin_stats import *
import pylab as pl
import sys
import os
import os.path
import pyfits as pf
import image_info as info
import scipy.stats as stats

real = 1
zint = 20

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
    half_flux = source_count/2
    num_pix = np.pi*(r_pix**2)
    back_flux = num_pix*bkrd
    sn = half_flux/np.sqrt((half_flux+back_flux)/gain + num_pix*darkvar)

    return sn

def mag_to_counts( mag, aa, kk = 0 , airmass = 0):
    exptime = 2286.0
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
plot_set = pub_plots(xmaj = 100, xmin = 25, xstr = '%d', 
                     ymaj = 0.02, ymin = 0.01, ystr =  '% 03.2f')

plotrange = (0,400)
binnum = 50
lsl = [1,1,1]

def make_plot(data, color, binnum, plotrange, cls):
    galcount, Ie, Id, magzp, hrad, sky, gain, dark_var  = data

    galcount = np.array(galcount, dtype = int)
    Ie = np.array(Ie, dtype = float)
    Id = np.array(Id, dtype = float)
    magzp = np.array(magzp, dtype = float)
    hrad = np.array(hrad, dtype = float) 
    galsky = np.array(sky, dtype = float)
    gain = np.array(gain, dtype = float)
    dark_var = np.array(dark_var, dtype = float)

    tot_mag = mag_sum(Ie, np.abs(Id))[0]
    counts =  mag_to_counts( tot_mag, -1.0*magzp, kk = 0 , airmass = 0)

    sn = measure_sn(hrad, counts, galsky, gain, dark_var)

    weight = np.ones_like(sn)/len(sn)

    pl.hist(sn, range = plotrange,bins = binnum, weights = weight, histtype = 'step', color = color, lw = cls)

    return sn

cmd = "select a.galcount, a.Ie, a.Id, a.magzp, a.hrad_pix_psf, a.galsky, b.gain_r, b.darkvariance_r from  full_dr7_r_%s as a, CAST as b where a.galcount = b.galcount;" %('serexp') 

#data = cursor.get_data(cmd)
#sn_real = make_plot(data, 'k',binnum, plotrange, 2)

for model, color1 in zip(['ser','devexp','serexp'],['r','g','b']):

#    cmd = "select a.galcount, a.Ie-%f+a.z-a.dismod+dismod_%d, a.Id-%f+a.z-a.dismod+dismod_%d, 24.84068, a.hrad_pix_psf*0.396*a.kpc_per_arcsec/(kpc_per_arcsec_%d * 0.03), 17.1824096325044 , %f, 0.0 from  simulations.sim_input as a where  a.model = '%s' ;" %(zint/10.0+1,zint,zint/10.0+1, zint, zint,zint/10.0, model) 
    cmd = """select a.galcount, a.Ie+a.z-a.dismod, a.Id+a.z-a.dismod,
dismod_10-1.0,dismod_15-1.5,dismod_17-1.7,dismod_20-2.0, 24.84068, 
a.hrad_pix_psf*0.396*a.kpc_per_arcsec,
(kpc_per_arcsec_10 * 0.03),(kpc_per_arcsec_15 * 0.03),
(kpc_per_arcsec_17 * 0.03),(kpc_per_arcsec_20 * 0.03), 17.1824096325044 , 1.0,
 0.0 from  simulations.sim_input as a where  a.model = '%s' ;""" %( model) 

    data = cursor.get_data(cmd)
    
    data_new = []
    data_new.append(data[0] * 4)

    Ie_un = np.array(data[1]*4, dtype = float)
    Ie_new = Ie_un + np.array(data[3]+data[4]+data[5]+data[6], dtype = float)
    data_new.append(Ie_new)
    
    Id_un = np.array(data[2]*4, dtype = float)
    Id_new = Id_un + np.array(data[3]+data[4]+data[5]+data[6], dtype = float)
    data_new.append(Id_new)
    
    data_new.append(data[7] * 4)

    r_un = np.array(data[8]*4, dtype = float)
    r_new = r_un/np.array(data[8]+data[9]+data[10]+data[11], dtype = float)
    data_new.append(r_new)

    data_new.append(data[12] * 4)
    data_new.append(data[13] * 4)
    data_new.append(data[14] * 4)
    data = data_new

    sn_tmp = make_plot(data, color1, binnum, plotrange, 1)
    print 'mean ',  np.mean(sn_tmp)
    print 'median ', np.median(sn_tmp)
    # print stats.ks_2samp(sn_real, sn_tmp)


pl.xlim((0,400))
pl.ylim((0,0.10001))
pl.xlabel('S/N$_{r}$')
pl.ylabel('n(S/N$_{r}$)')
    
ax = pl.gca()
plot_set.set_plot(ax)
pl.savefig("sn_hst.eps" , format = 'eps', bbox_inches="tight")
