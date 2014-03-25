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

cmd = 'select a.galcount, d.sky_counts_r, c.db_r, c.sky_counts_r from full_dr7_r_ser as a, CAST as b, simard.simard_bkrd as c, DERT as d where c.objid = b.objid and b.galcount = a.galcount and b.galcount = d.galcount;'

galcount, cas_sky, simard_db, simard_sky = cursor.get_data(cmd)

galcount = np.array(galcount, dtype=int)
cas_sky = np.array(cas_sky, dtype=float)
simard_db = np.array(simard_db, dtype=float)
simard_sky = np.array(simard_sky, dtype=float)

fig_size = get_fig_size(fullwidth = 1, fullheight = 1)
full_ticks = pub_plots(xmaj = 1, xmin = .25, xstr = '%d', ymaj = 1, ymin = .1, ystr = '%d')
diff_ticks = pub_plots(xmaj = 1, xmin = .25, xstr = '%2.1f', ymaj = 1, ymin = 1, ystr = '%d')
#diff_ticks = pub_plots(xmaj = 50, xmin = 25, xstr = '%03.1f', ymaj = 1, ymin = 1, ystr = '%d')

fig = start_fig(fig_size)

fig.add_subplot(2,2,1)
pl.hist(simard_db, range = (-3,3), bins = 60, normed = True)
pl.title('db Sky', fontsize = '10')
pl.xlabel('db')
pl.ylabel('n(db)')
#pl.ylim((0,10))
#pl.xlim((-3,3))
ax = pl.gca()
full_ticks.set_plot(ax) 

fig.add_subplot(2,2,2)
#pl.hist(cas_sky, range = (75,300), bins = 225, normed = True)
pl.hist(simard_db*100/cas_sky, range = (-2,2), bins = 80, normed = True)
pl.title('Simard-CasJobs Sky', fontsize = '10')
pl.xlabel('(Simard-CasJobs)/CasJobs [%]')
pl.ylabel('n($\Delta$)')
#pl.ylim((0,10))
#pl.xlim((-2,2))
ax = pl.gca()
diff_ticks.set_plot(ax) 

fig.add_subplot(2,2,3)
pl.hist((simard_sky-cas_sky)*100/cas_sky, range = (-2,2), bins = 80, normed = True)
pl.title('Simard-CasJobs Sky', fontsize = '10')
pl.xlabel('(Simard-CasJobs)/CasJobs [%]')
pl.ylabel('n($\Delta$)')
#pl.ylim((0,10))
#pl.xlim((-2,2))
ax = pl.gca()
diff_ticks.set_plot(ax) 

pl.savefig('/home/ameert/Desktop/simard_db.eps')
