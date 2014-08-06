import numpy as np
import pylab as pl
import matplotlib.cm as cm
from scipy import ndimage

galcount, logmstar, ttype, BT = np.loadtxt('scd_out.txt', unpack = True, delimiter = ',')

pl.subplot(3,2,1)
pl.hist(logmstar, normed = True, log = True)
pl.xlabel('Log10(Mstar)')
pl.subplot(3,2,2)
pl.hist(ttype, normed = True, log = True)
pl.xlabel('Ttype')
pl.subplot(3,2,3)
pl.hist(BT, normed = True, log = True)
pl.xlabel('BT')
pl.subplot(3,2,6)
extent = [(0.0, 0.5),(11.0, 12.5)]
H, xedges, yedges = np.histogram2d(BT, logmstar, range = extent, bins = (50,50))

xval, yval = np.meshgrid(xedges, yedges)
Hpic = ndimage.rotate(H, 90.0)
Hpic = np.log10(Hpic)
img = pl.imshow(Hpic,  interpolation='nearest', 
                extent = [extent[0][0],extent[0][1],extent[1][0],extent[1][1]],
                aspect='auto', cmap = cm.Greys,vmax = 3, vmin = -1)
pl.xlabel('BT')
pl.ylabel('Log10(Mstar)')

pl.subplot(3,2,5)
extent = [(4.0, 7.5),(11.0, 12.5)]
H, xedges, yedges = np.histogram2d(ttype, logmstar, range = extent, bins = (50,50))

xval, yval = np.meshgrid(xedges, yedges)
Hpic = ndimage.rotate(H, 90.0)
Hpic = np.log10(Hpic)
img = pl.imshow(Hpic,  interpolation='nearest', 
                extent = [extent[0][0],extent[0][1],extent[1][0],extent[1][1]],
                aspect='auto', cmap = cm.Greys,vmax = 3, vmin = -1)
pl.xlabel('Ttype')
pl.ylabel('Log10(Mstar)')

pl.subplot(3,2,4)
extent = [(4.0, 7.5),(0.0, 0.5)]
H, xedges, yedges = np.histogram2d(ttype, BT, range = extent, bins = (50,50))

xval, yval = np.meshgrid(xedges, yedges)
Hpic = ndimage.rotate(H, 90.0)
Hpic = np.log10(Hpic)
img = pl.imshow(Hpic,  interpolation='nearest', 
                extent = [extent[0][0],extent[0][1],extent[1][0],extent[1][1]],
                aspect='auto', cmap = cm.Greys,vmax = 3, vmin = -1)
pl.xlabel('Ttype')
pl.ylabel('BT')




pl.subplots_adjust(hspace =0.3, wspace=0.4)
pl.show()

for a in np.extract(BT>0.05, galcount):
    print int(a)
