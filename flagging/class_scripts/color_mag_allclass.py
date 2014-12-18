import numpy as np
import os
import sys
import pylab as pl
import matplotlib.cm as cm
from utilities import *
from scipy import ndimage
from test_hull import *

def dense_plot(rmag,mcolor, contours = False, color = 'r'):
    extent = [(-26.0, -16.0),(-0.20, 1.2)]
    H, xedges, yedges = np.histogram2d(rmag, mcolor, range = extent, 
                                   bins = (50,50))

    xval, yval = np.meshgrid(xedges, yedges)
    Hpic = ndimage.rotate(H, 90.0)
    Hpic = np.log10(Hpic)
    if contours:
        pl.contour(xval, yval,Hpic, [4,3,2], color = [color,color,color], linestyles=['-','--',':'],
                   extent = [extent[0][0],extent[0][1],extent[1][0],extent[1][1]],
                   aspect='auto',origin='lower')
    else:
        img = pl.imshow(Hpic,  interpolation='nearest', 
                        extent = [extent[0][0],extent[0][1],extent[1][0],extent[1][1]],
                        aspect='auto', cmap = cm.Greys,vmax = 4, vmin = -1)

    return

gal = {}

for band in 'gri':
    a = open('color_file_{band}.npz'.format(band=band))
    gal[band]  = np.load(a)
    print gal.keys()

rmag = gal['r']['cmodelr']-gal['r']['dismod']-gal['r']['kr']
mcolor = gal['r']['modelg']-gal['r']['kg'] - (gal['r']['modelr']-gal['r']['kr'])
flaglist = [ (1,1,1), (4,4,4),  (10,10,10), (4, 10, 1), (4,10,10), (10, 10, 1)]
colorlist = [ 'Red', 'Blue',  'Green',  'Cyan', 'Magenta']
labellist = [ "BBB", "DDD", "222", "D22", "22B"]
pl.subplot(1,1,1)
dense_plot(rmag,mcolor)

for ftmp, ctmp, ltmp in zip(flaglist, colorlist, labellist):
    
    rmag_tmp = np.extract((gal['g']['flag']&2**ftmp[0])*(gal['r']['flag']&2**ftmp[1])*(gal['i']['flag']&2**ftmp[2]) >0, rmag)
    color_tmp = np.extract((gal['g']['flag']&2**ftmp[0])*(gal['r']['flag']&2**ftmp[1])*(gal['i']['flag']&2**ftmp[2]) >0, mcolor)
    print rmag_tmp.size
    plot_data(rmag_tmp, color_tmp, 1000, 5, -26, -16, 50,-0.20, 1.2, 50, color = ctmp)
    
#handles, labels = pl.gca().get_legend_handles_labels()
#pl.legend(handles, labellist)
mags = np.arange(-26.0, -15.0,0.1)
pl.plot(mags, -0.025*(mags+20)+0.611, 'm-')
pl.plot(mags, -0.05-0.025*(mags+20)+0.611, 'm:')
pl.plot(mags, 0.05-0.025*(mags+20)+0.611, 'm:')

pl.xlim(-25, -16)
pl.ylim(0.2, 1.0)
pl.xlabel('M$_r$')
pl.ylabel('M$_g$-M$_r$')
pl.title('mag color diagram')

pl.savefig('colormag_allclass.eps'.format(band=band))
pl.close('all')


if 0:
    pl.subplot(1,1,1)
    dense_plot(rmag,mcolor)
    sel = (np.where(flag&2**11>0, 1,0)|np.where(flag&2**12>0, 1,0))*np.where(gal['n_bulge']>2, 1,0)*np.where(gal['n_bulge']<7.95, 1,0)
    rmag_tmp = np.extract(sel==1, rmag)
    color_tmp = np.extract(sel==1, mcolor)
    plot_data(rmag_tmp, color_tmp, 1000, 5, -26, -16, 50,-0.20, 1.2, 50, color = 'g')

    sel = (np.where(flag&2**11>0, 1,0)|np.where(flag&2**12>0, 1,0))*np.where(gal['n_bulge']<=2, 1,0)
    rmag_tmp = np.extract(sel==1, rmag)
    color_tmp = np.extract(sel==1, mcolor)
    plot_data(rmag_tmp, color_tmp, 1000, 5, -26, -16, 50,-0.20, 1.2, 50, color = 'c')

    sel = (np.where(flag&2**11>0, 1,0)|np.where(flag&2**12>0, 1,0))*np.where(gal['n_bulge']>=7.95, 1,0)
    rmag_tmp = np.extract(sel==1, rmag)
    color_tmp = np.extract(sel==1, mcolor)
    plot_data(rmag_tmp, color_tmp, 1000, 5, -26, -16, 50,-0.20, 1.2, 50, color = 'm')

    mags = np.arange(-26.0, -15.0,0.1)
    pl.plot(mags, -0.025*(mags+20)+0.611, 'm-')
    pl.plot(mags, -0.05-0.025*(mags+20)+0.611, 'm:')
    pl.plot(mags, 0.05-0.025*(mags+20)+0.611, 'm:')

    pl.xlim(-26, -16)
    pl.ylim(0.20, 1.0)
    pl.xlabel('M$_r$')
    pl.ylabel('M$_g$-M$_r$')
    pl.title('mag color diagram')
    #pl.colorbar()

    pl.savefig('colormag_twocom_{band}.eps'.format(band=band))
    pl.close('all')
    a.close()


