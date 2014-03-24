import os
import sys
import pylab as pl
import numpy as np
from utilities import *
from  scipy import stats 
from numpy import random

def kormendy(Rkpc, Rkpc_err, Lum, Lum_err, nser):
    Rpc = Rkpc*1000.0 # now in pc
    Rpc_err = Rkpc_err*1000.0 # now in pc

    Ibar = 0.5 * Lum/(np.pi*Rpc**2) # surface brightness in Lsun/pc^2

    y = np.log10(Ibar/(1.2*10.0**3.0)) # now unitless
    x = np.log10(Rpc/(1000.0 * h7**(-1))) # now unitless

    pl.scatter(x,y, s = 3.0, c= nser, edgecolor = 'none', vmax = 8.0, vmin =0.0)
    pl.xlim(-1.0 ,3.0)
    pl.ylim(-5.0, 2.0)

    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

    linex = np.arange(-2.0, 4.01, 0.25)
    liney = slope*linex + intercept

    rms = np.sqrt(np.mean((y-( slope*x + intercept))**2.0))

    ax = pl.gca()
    #pl.plot(linex, liney)
    pl.title('Kormendy colored by n')
    pl.ylabel('$log_{10}(\\bar{I_{e, R}}/(1.2*10^3\ L_{sun}\ pc^{-2}))$')
    pl.xlabel('$log_{10}(R_e/(1000\ h_7^{-1}\ pc))$')
    #pl.text(0.12, 0.32, 'm = %5.4f' %slope,transform = ax.transAxes)
    #pl.text(0.12, 0.27, 'b = %5.4f' %intercept,transform = ax.transAxes)
    #pl.text(0.12, 0.22, 'r = %5.4f' %r_value,transform = ax.transAxes)
    #pl.text(0.12, 0.17, 'p = %5.4f' %p_value,transform = ax.transAxes)
    #pl.text(0.12, 0.12, 'RMS = %5.4f' %rms,transform = ax.transAxes)

    return ax
    
