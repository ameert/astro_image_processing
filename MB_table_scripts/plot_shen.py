import pylab as pl
import numpy as np
from MatplotRc import *

absmag, hrad = np.loadtxt('topcat_bcg_short.txt', usecols=(6,8), unpack=True)

print absmag, hrad


a = 0.65
b =  -5.22

shenmags = np.arange(-26, -17)
shenrads = -0.4*a*shenmags + b

ticks= pub_plots(xmaj = 1.0, xmin = 0.1, xstr = '%d', ymaj = 0.5, ymin = 0.1, ystr = '%2.1f')
pl.plot(shenmags, shenrads, 'k--')
pl.scatter(absmag, hrad)
pl.xlim(-19.5, -26)
pl.ylim(-0.1, 2.5)
ticks.set_plot(pl.gca())
pl.xlabel('M_ser')
pl.ylabel('logR_kpc')
pl.show()
