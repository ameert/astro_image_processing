import os
import sys
import pylab as pl
import numpy as np
from utilities import *
from  scipy import stats 
from numpy import random

def faber_jackson(vel_disp, vel_disp_err, Lum, Lum_err, nser):
    y = np.log10(vel_disp/150.0) # now unitless, was km/s for vel_disp and 150
    x = np.log10(Lum/(10.0**10 * h7**(-2))) # now unitless, Lum was in L_sun

    pl.scatter(x,y, s = 3.0, c= nser, edgecolor = 'none', vmax = 8.0, vmin =0.0)
    pl.xlim(-2.0,3.0)
    pl.ylim(-1.0, 1.0)
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

    linex = np.arange(-2.0, 3.01, 0.25)
    liney = slope*linex + intercept

    rms = np.sqrt(np.mean((y-( slope*x + intercept))**2.0))
    ax = pl.gca()
    #pl.plot(linex, liney)
    pl.title('Faber Jackson colored by n')
    pl.ylabel('$log_{10}(\sigma/(150\ km/s))$')
    pl.xlabel('$log_{10}(L/(10^{10} h_7^{-2} L_{sun}))$')
    #pl.text(0.12, 0.92, 'm = %5.4f' %slope,transform = ax.transAxes)
    #pl.text(0.12, 0.87, 'b = %5.4f' %intercept,transform = ax.transAxes)
    #pl.text(0.12, 0.82, 'r = %5.4f' %r_value,transform = ax.transAxes)
    #pl.text(0.12, 0.77, 'p = %5.4f' %p_value,transform = ax.transAxes)
    #pl.text(0.12, 0.72, 'RMS = %5.4f' %rms, transform = ax.transAxes)

    return ax
