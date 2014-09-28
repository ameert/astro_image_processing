import os
import sys
import pylab as pl
import numpy as np
from utilities import *

from numpy import random
from test_hull import *
import pylab as pl
import matplotlib.cm as cm
from sklearn import linear_model
from sklearn.cross_validation import train_test_split


def kormendy(Rkpc, Lum, color='r'):
    Rpc = Rkpc*1000.0 # now in pc

    Ibar = 0.5 * Lum/(np.pi*Rpc**2) # surface brightness in Lsun/pc^2

    y = np.log10(Ibar/(1.2*10.0**3.0)) # now unitless
    x = np.log10(Rpc/(1000.0 * h7**(-1))) # now unitless

    selection = np.where(np.isinf(y),0,1)
    x = np.extract(selection==1,x)
    y = np.extract(selection==1,y)
    
    plot_data(x, y, 1000, 5, -1.0, 2.0, 50.0,-2.0, 2.0, 50.0, color = color)
    pl.xlim(-1.0 ,3.0)
    pl.ylim(-5.0, 2.0)

    
    # Split the data into training/testing sets
    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.33,
                                                        random_state=76)

   
    x_train = x_train.reshape(x_train.size,1)
    x_test = x_test.reshape(x_test.size,1)
    y_train = y_train.reshape(y_train.size,1)
    y_test = y_test.reshape(y_test.size,1)
    
    # Create linear regression object
    regr = linear_model.LinearRegression(fit_intercept=True)

    # Train the model using the training sets
    regr.fit(x_train, y_train)

    # The coefficients
    print('Coefficients: ', regr.coef_)
    print('intercept: ', regr.intercept_)
    # The mean square error
    rms = np.sqrt(np.mean((regr.predict(y_test) - y_test) ** 2))
    print("Residual sum of squares: %.2f" %rms)
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % regr.score(x_test, y_test))
    
    linex = np.arange(-2.0, 4.01, 0.25)
    linex = linex.reshape(linex.size,1)
    liney = regr.predict(linex)

    ax = pl.gca()
    pl.plot(linex, liney, c = color, ls = '-')
    pl.title('Kormendy')
    pl.ylabel(r'$log_{10}(\bar{I_{e, R}}/(1.2*10^3\ L_{sun}\ pc^{-2}))$')
    pl.xlabel(r'$log_{10}(R_e/(1000\ h_7^{-1}\ pc))$')
    
    if color == 'r':
        pl.text(0.1, 0.15, 'm$_{early}$ = %3.2f' %regr.coef_[0],transform = ax.transAxes)
        pl.text(0.1, 0.1, 'RMS$_{early}$ = %3.2f' %rms,transform = ax.transAxes)
    elif color == 'g':
        pl.text(0.7, 0.95, 'm$_{bulge}$ = %3.2f' %regr.coef_[0],transform = ax.transAxes)
        pl.text(0.7, 0.9, 'RMS$_{bulge}$ = %3.2f' %rms,transform = ax.transAxes)

    return ax
    
a = open('color_file.npz')
gal = np.load(a)
print gal.keys()

pl.subplot(1,1,1)

#bulges
rmag = gal['mag']-gal['dismod']-gal['kr']
rmag, rmag_err = absmag_to_LSun(rmag, 0.0*rmag, band = 'r')
rad = np.array(gal['hrad_corr'], dtype=float)*gal['kpc_per_arcsec']
flag = gal['flag']

rad_good = np.logical_and(gal['hrad_corr']>2.0,gal['hrad_corr']<=100.0)

rmag_tmp = np.extract(np.logical_and(flag&2**1>0, rad_good), rmag)
rad_tmp = np.extract(np.logical_and(flag&2**1>0, rad_good), rad)

kormendy(rad_tmp, rmag_tmp, color = 'r')

#twocom disks
rmag = gal['m_bulge']-gal['dismod']-gal['kr']
rmag, rmag_err = absmag_to_LSun(rmag, 0.0*rmag, band = 'r')
rad = np.array(gal['r_bulge'], dtype=float)*gal['kpc_per_arcsec']
flag = gal['flag']

sel = (np.where(flag&2**11>0, 1,0)|np.where(flag&2**12>0, 1,0))*rad_good.astype(int)
#*np.where(gal['n_bulge']>2, 1,0)*np.where(gal['n_bulge']<7.95, 1,0)
rmag_tmp = np.extract(sel==1, rmag)
rad_tmp = np.extract(sel==1, rad)
kormendy(rad_tmp, rmag_tmp, color = 'g')

pl.title('Kormendy')
pl.ylabel('$log_{10}(\\bar{I_{e, R}}/(1.2*10^3\ L_{sun}\ pc^{-2}))$')
pl.xlabel('$log_{10}(R_e/(1000\ h_7^{-1}\ pc))$')
pl.xlim(-1.0,1.5)
pl.ylim(-1.5,1.2)
pl.savefig('kormendy_4.eps')
