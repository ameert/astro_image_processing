import os
import sys
import pylab as pl
import numpy as np
from utilities import *
from  scipy import stats 
from numpy import random
from fund_plane import linreg_3D

def photo_fund_plane(Rkpc, Rkpc_err, n_b, n_b_err, Lum, Lum_err, BT):
    Ibar = 0.5 * Lum/(np.pi*Rkpc**2) # surface brightness in Lsun/kpc^2
    x = n_b # now unitless
    y = np.log10(Ibar/(1.2*10.0**3.0)) # now unitless
    z = np.log10(Rkpc/h7**(-1)) # now unitless
    
    ans = linreg_3D(x,y,z)
    a = ans[0,0]
    b = ans[1,0]
    c = ans[2,0]
    print a,b,c
    
    pl.scatter(a*x +b*y, z, c= BT, s = 3, edgecolor = 'none', vmax = 1.0, vmin =0.0)
    pl.xlim(-8.0 ,-1)
    pl.ylim(-3.0, 3)
    
    projection = a*x+b*y
    to_fit = np.where(projection>-5, 1,0)*np.where(projection<-1, 1,0)
    goodxy = np.extract(to_fit > 0.5, projection)
    goodz = np.extract(to_fit > 0.5, z)
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(goodxy,goodz)

    linex = np.arange(-8.0, -1.01, 0.25)
    liney = slope*linex + intercept
    
    rms = np.sqrt(np.mean((z-( projection + c))**2.0))
    ax = pl.gca()
    pl.plot(linex, liney)
    pl.title('Fundamental Plane')
    pl.xlabel('$%3.2f \ n\ + \ (%3.2f)log_{10}(\\bar{I_{e, R}}/(1.2*10^3\ L_{sun}\ pc^{-2}))$' %(a,b))
    pl.ylabel('$log_{10}(R_e/(1000\ h_7^{-1}\ pc))$')
    #pl.text(0.12, 0.32, 'm = %5.4f' %slope,transform = ax.transAxes)
    #pl.text(0.12, 0.27, 'b = %5.4f' %intercept,transform = ax.transAxes)
    pl.text(0.12, 0.92, 'r = %5.4f' %r_value,transform = ax.transAxes)
    #pl.text(0.12, 0.87, 'p = %5.4f' %p_value,transform = ax.transAxes)
    pl.text(0.12, 0.87, 'RMS = %5.4f' %rms,transform = ax.transAxes)
    
    
    return ax
