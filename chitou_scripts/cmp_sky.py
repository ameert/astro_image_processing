import os
from mysql_class import *
import numpy as np
import sys
import pylab as pl
from MatplotRc import *
from plotting_funcs import *

def mag_to_counts( mag, aa, kk = 0 , airmass = 0):
    exptime = 53.907456 #in seconds, taken from SDSS website 
                        # www.sdss.org/dr3/algorithms/fluxcal.html
    return exptime * (10**(-.4*mag)) / (10**(0.4*(aa + kk*airmass)))

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

cmd = 'select a.galcount, a.galsky*53.907456, d.sky_counts_r, c.sky_counts_r from full_dr7_r_ser as a, CAST as b, simard.simard_bkrd as c, DERT as d where c.objid = b.objid and b.galcount = a.galcount and b.galcount = d.galcount;'

galcount, galsky, cas_sky, simard_sky = cursor.get_data(cmd)

galcount = np.array(galcount, dtype=int)
galsky = np.array(galsky, dtype=float)
cas_sky = np.array(cas_sky, dtype=float)
simard_sky = np.array(simard_sky, dtype=float)

fig_size = get_fig_size(fullwidth = 1, fullheight = 1)
full_ticks = pub_plots(xmaj = 50, xmin = 25, xstr = '%d', ymaj = 0.005, ymin = 0.001, ystr = '%4.3f')
diff_ticks = pub_plots(xmaj = .5, xmin = .25, xstr = '%03.1f', ymaj = 0.5, ymin = 0.1, ystr = '%2.1f')

fig = start_fig(fig_size)

fig.add_subplot(3,2,1)
counts, binedges, patches = pl.hist(cas_sky, range = (50,300), bins = 250, normed = True, histtype='step')
pl.title('SDSS Sky', fontsize = '10')
pl.xlabel('SDSS')
pl.ylabel('n(SDSS)')
pl.xlim((50,250))
pl.ylim((0,0.020))
ax = pl.gca()
full_ticks.set_plot(ax) 

fig.add_subplot(3,2,3)
pl.hist(galsky, range = (50,300), bins = 250, normed = True,histtype='step')
pl.title('PyMorph Sky', fontsize = '10')
pl.xlabel('PyMorph')
pl.ylabel('n(PyMorph)')
pl.ylim((0,0.020))
pl.xlim((50,250))
ax = pl.gca()
full_ticks.set_plot(ax) 

fig.add_subplot(3,2,5)
pl.hist(simard_sky, range = (50,300), bins = 250, normed = True,histtype='step' )
pl.title('Simard Sky', fontsize = '10')
pl.xlabel('Simard')
pl.ylabel('n(Simard)')
pl.ylim((0,0.020))
pl.xlim((50,250))
ax = pl.gca()
full_ticks.set_plot(ax) 


fig.add_subplot(3,2,2)
pl.hist((simard_sky-galsky)*100/galsky, range = (-2,2), bins = 100, normed = True, histtype='step')
pl.title('Simard-PyMorph Sky', fontsize = '10')
pl.xlabel('(Simard-PyMorph)/PyMorph [%]')
pl.ylabel('n($\Delta$)')
#pl.ylim((0,10))
pl.xlim((-2,2))
ax = pl.gca()
diff_ticks.set_plot(ax) 

fig.add_subplot(3,2,4)
pl.hist((simard_sky-cas_sky)*100/cas_sky, range = (-2,2), bins = 100, normed = True, histtype='step')
pl.title('Simard-SDSS Sky', fontsize = '10')
pl.xlabel('(Simard-SDSS)/SDSS [%]')
pl.ylabel('n($\Delta$)')
#pl.ylim((0,10))
pl.xlim((-2,2))
ax = pl.gca()
diff_ticks.set_plot(ax) 

fig.add_subplot(3,2,6)
pl.hist((galsky-cas_sky)*100/cas_sky, range = (-2,2), bins = 100, normed = True,histtype='step')
pl.title('PyMorph-SDSS Sky', fontsize = '10')
pl.xlabel('(PyMorph-SDSS)/SDSS [%]')
pl.ylabel('n($\Delta$)')
#pl.ylim((0,10))
pl.xlim((-2,2))
ax = pl.gca()
diff_ticks.set_plot(ax) 

pl.savefig('/home/ameert/Desktop/sky.eps')


