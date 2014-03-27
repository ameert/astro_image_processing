import sys
import os
import numpy as np
import statistics.bin_stats as bs
import pylab as pl
from MatplotRc import *

data = np.load('ba_data_serexp.npz')
fig = pl.figure(figsize = (6,4))
fig.subplots_adjust(left = 0.14, right = 0.9, top = 0.9, bottom = 0.1, 
                    wspace = 0.75, hspace = 0.75)
for count, gal_opt in enumerate(['Ell','S0','Sab','Scd']):
    print count
    if gal_opt == 'All':
        tlow = -8.0
        thigh = 10.0
    elif gal_opt == 'Ell':
        tlow = -8.0
        thigh = -3.0
    elif gal_opt == 'S0':
        tlow = -3.0
        thigh = 0.5
    elif gal_opt == 'Sab':
        tlow = 0.5
        thigh = 4.0
    elif gal_opt == 'Scd':
        tlow = 4.0
        thigh = 10.0

    ttype =  np.where(data['ttype']<=thigh,1,0)*np.where(data['ttype']>tlow,1,0)
    ba_bulge = np.where( ttype==1, data['ba_bulge'], np.nan)
    BT = np.where( ttype==1, data['BT'], np.nan)
    flag = data['flags']

    bad_gal =  np.where(flag&2**4,1,0)|np.where(flag&2**13,1,0)|np.where(flag&2**14,1,0)|np.where(flag&2**19,1,0)
#    bad_gal =  np.where(flag&2**4,1,0)|np.where(flag&2**19,1,0)
    #bad_gal = bad_gal | np.where(data['r_bulge']<=0.1,1,0)|np.where(data['n_bulge']>=7.95,1,0)|
    ba_bulge = np.where( bad_gal==0, ba_bulge, np.nan)
    BT = np.where( bad_gal==0, BT, np.nan)

    print 'Type ', gal_opt
    print np.extract(ba_bulge<0.1, data['galcount'])
    pl.subplot(2,2,count+1)
    pl.hist(ba_bulge, range=(0,1), bins = 50, log = True)
    pl.ylabel('counts')
    pl.xlabel('b/a bulge')
    pl.title( gal_opt)
    pl.ylim(1,10000)
pl.savefig('ba_bulge_serexp.eps')


