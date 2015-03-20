import os
import sys
import pylab as pl
import numpy as np

import pylab as pl
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


a = open('mass_file_r.npz')
gal = np.load(a)
print gal.keys()

flag = gal['flag']
good_gals = np.where(flag&2**1>0,1,0)+np.where(flag&2**4>0,1,0)+np.where(flag&2**10>0,1,0)

print np.sum(good_gals)
outflag = np.extract(good_gals>0, gal['flag'])
BT = np.extract(good_gals>0, gal['BT'])
mass = np.extract(good_gals>0, gal['mstar'])
vweight = np.extract(good_gals>0, gal['vweight'])
vweight = vweight/np.sum(vweight)

BT = np.where(outflag&2**1, 1.0, BT)
BT = np.where(outflag&2**4, 0.0, BT)


hist,xedge,yedge=np.histogram2d(mass, BT, bins=[np.arange(9.0,12.01, 0.1), np.arange(-0.1,1.101,0.05)], weights = vweight)

hist =hist.T
hist = np.where(np.isinf(hist), 0, hist)
hist = hist/np.max(hist)
#hist = np.log10(hist)

print hist

plt.figure()
#CS = plt.imshow(hist, extent=[9.0,12.0,0.0,1.0], origin='lower',interpolation='none', aspect=5.0/2.0)

CS = plt.contour(hist,np.array([0.0001,0.0005,0.001,0.005,0.01,0.05,0.1,0.5]) , extent=[9.0,12.0,-0.1,1.1], origin='lower', aspect=5.0/2.0, vmax=-1.0, vmin=-9.0)
plt.clabel(CS, inline=1, fontsize=10)
plt.title('BT vs Mstar, vmax weighted')
CB = plt.colorbar(CS, shrink=0.8, extend='both')
plt.xlabel('log(M$_{star}$)')
plt.ylabel('B/T')
plt.show()
