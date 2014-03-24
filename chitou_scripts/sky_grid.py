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

fig_size = (10,10)#get_fig_size(fullwidth = 1, fullheight = 1)
full_ticks = pub_plots(xmaj = 100, xmin = 25, xstr = '%d', ymaj = 0.01, ymin = 0.001, ystr = '%3.2f')
diff_ticks = pub_plots(xmaj = 1, xmin = .25, xstr = '%03.1f', ymaj = 2.0, ymin = 0.5, ystr = '%2.1f')

fig = start_fig(fig_size)
fig.subplots_adjust(left = 0.07,  # the left side of the subplots of the figure
                    right = 0.97,    # the right side of the subplots of the figure
                    bottom = 0.08,   # the bottom of the subplots of the figure
                    top = 0.95,      # the top of the subplots of the figure
                    wspace = 0.7,   # the amount of width reserved for blank space between subplots
                    hspace = 0.8)   # the amount of height reserved for white space between subplots

cursor = mysql_connect(dba, usr, pwd)

cmd = 'select a.galcount, a.galsky*53.907456,b.galsky*53.907456,c.galsky*53.907456,d.galsky*53.907456, e.sky_counts_r, f.sky_counts_r from full_dr7_r_dev as a, full_dr7_r_ser as b, full_dr7_r_devexp as c, full_dr7_r_serexp as d, CAST as g, simard.simard_bkrd as e, DERT as f where e.objid = g.objid and f.galcount = g.galcount and a.galcount = g.galcount and a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount;'

galcount, galsky_dev, galsky_ser, galsky_devexp, galsky_serexp, cas_sky, simard_sky = cursor.get_data(cmd)

galcount = np.array(galcount, dtype=int)
left = ['SDSS', 'Simard', 'Dev', 'Ser', 'DevExp', 'SerExp']
data  = {'SDSS':np.array(cas_sky, dtype=float), 
         'Simard':np.array(simard_sky, dtype=float), 
         'Dev':np.array(galsky_dev, dtype=float), 
         'Ser':np.array(galsky_ser, dtype=float), 
         'DevExp':np.array(galsky_devexp, dtype=float),
         'SerExp':np.array(galsky_serexp, dtype=float)}

count = 0
for lpos, cleft in enumerate(left):
    for tpos, ctop in enumerate(left):
        count +=1
        
        if lpos == tpos:
            fig.add_subplot(6,6,count)
            pl.hist(data[cleft], range = (50,300), bins = 250, normed = True, histtype='step')
            pl.title('%s Sky' %cleft, fontsize = '10')
            pl.xlabel(cleft)
            pl.ylabel('n(%s)' %cleft)
            pl.xlim((50,250))
            pl.ylim((0,0.020))
            ax = pl.gca()
            full_ticks.set_plot(ax) 
        else:
            fig.add_subplot(6,6,count)
            pl.hist((data[cleft]-data[ctop])*100/data[ctop], range = (-2,2), bins = 100, normed = True, histtype='step')
            pl.title('%s - %s' %(cleft,ctop), fontsize = '10')
            #pl.xlabel('(%s - %s)/%s [%s]' %(cleft,ctop,ctop, '%'))
            pl.xlabel('% diff' )
            pl.ylabel('n($\Delta$)')
            ylim = pl.ylim()
            pl.ylim(0,np.max((2,ylim[1])))
            pl.xlim((-1.5,1.5))
            ax = pl.gca()
            diff_ticks.set_plot(ax) 

pl.savefig('/home/ameert/Desktop/sky.eps')


