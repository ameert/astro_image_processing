from mysql_class import *
import numpy as np
import pylab as pl
from MatplotRc import *
import time
from bin_stats import *

pix_sz = 0.396
exptime = 53.907456 

dba = 'simard'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)

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


def mag_to_counts( mag, aa, kk = 0 , airmass = 0, exptime = 53.907456):
# the 53 seconds 
#in seconds, taken from SDSS website www.sdss.org/dr3/algorithms/fluxcal.html
    return exptime * (10**(-.4*mag)) / (10**(0.4*(aa + kk*airmass)))

cmd = 'select a.galcount, a.sky_r, a.aa_r, a.kk_r, a.airmass_r from catalog.CAST as a;'

galcount, sky, aa, kk, airmass = cursor.get_data(cmd)

mag = 22.5 - 2.5*np.log10(np.array(sky)*10**9.0)

counts = mag_to_counts(mag, np.array(aa), np.array(kk), np.array(airmass), exptime = exptime) *pix_sz**2.0

fig_size = get_fig_size()
fig = start_fig(fig_size)            
plot_set = pub_plots(xmaj = 50, xmin = 10, xstr = '%d', 
                     ymaj = 0.01, ymin = 0.005, ystr =  '%03.2f')

print counts

pl.hist(counts, bins= 125, range=(50,300), 
        histtype = 'step', color = 'k', lw = 1, normed = True)
pl.xlabel('DN$_{\mathrm{r}}$/pix/exposure')
pl.ylabel('n(DN)')
pl.xlim((50, 275))
pl.ylim((0,0.02))
ax = pl.gca()
plot_set.set_plot(ax)
pl.savefig('sky_hist.eps')
pl.close(fig)

cmd = 'select a.galcount, a.galsky*%f, d.sky_counts_r from catalog.full_dr7_r_ser as a, catalog.DERT as d where d.galcount = a.galcount;' %exptime

galcount, galsky, cassky = cursor.get_data(cmd)

galcount = np.array(galcount, dtype=int)
galsky = np.array(galsky, dtype=float)
cassky = np.array(cassky, dtype=float)

sky_diff = (galsky-cassky)*100/cassky

sky_bins = np.array([-100,100])
a = bin_stats(sky_diff, sky_diff, sky_bins, -100,100)

fig_size = get_fig_size()
fig = start_fig(fig_size)            
plot_set = pub_plots(xmaj = 1, xmin = .25, xstr = '%d', 
                     ymaj = 0.25, ymin = 0.05, ystr =  '%03.2f')

pl.hist(sky_diff, bins= 40, range=(-2,2), 
        histtype = 'step', color = 'k', lw = 1, normed = True)
pl.xlabel('$\Delta$sky$_{r}$ [%]')
pl.ylabel('n($\Delta$sky$_{r}$)')

ylims = pl.ylim()
pl.plot([a.bin_median[0],a.bin_median[0]], ylims, 'r-')
pl.plot([a.bin_68[2][0],a.bin_68[2][0]], ylims, 'r--')
pl.plot([a.bin_95[2][0],a.bin_95[2][0]], ylims, 'r-.')
pl.plot([a.bin_99[2][0],a.bin_99[2][0]], ylims, 'r:')
pl.plot([a.bin_68[3][0],a.bin_68[3][0]], ylims, 'r--')
pl.plot([a.bin_95[3][0],a.bin_95[3][0]], ylims, 'r-.')
pl.plot([a.bin_99[3][0],a.bin_99[3][0]], ylims, 'r:')

ax = pl.gca()
pl.xlim((-2,2))
plot_set.set_plot(ax)
pl.savefig('sky_diff.eps')
pl.close(fig)
