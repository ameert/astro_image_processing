import sys
import os
import numpy as np
import bin_stats as bs
import pylab as pl
from MatplotRc import *
from bm_plot_funcs import *


gal_opt = 'Scd'

data = np.load('SSDR6_data2.npz')

log_Mstar_bulge = data['log_Mstar_bulge']
n_bulge=data['n_bulge']
BT = data['BT']
r_bulge = data['r_bulge']
flags = data['flags']
ttype = data['ttype']
galcount = data['galcount']


BT = np.where(flags&(2**1)>0, 1.0, BT)
BT = np.where(flags&(2**4)>0, 0.01, BT)

if gal_opt == 'Ell':
    tlow = -8.0
    thigh = -4.0
elif gal_opt == 'S0':
    tlow = -4.0
    thigh = 0.5
elif gal_opt == 'Sab':
    tlow = 0.5
    thigh = 4.0
elif gal_opt == 'Scd':
    tlow = 4.0
    thigh = 10.0


ttype =  np.where(ttype<=thigh,1,0)*np.where(ttype>tlow,1,0)
n_bulge = np.where( ttype==1, n_bulge, np.nan)
BT = np.where( ttype==1, BT, np.nan)
r_bulge = np.where( ttype==1, r_bulge, np.nan)

bad_gal =  np.where(r_bulge<=0.1,1,0)|np.where(n_bulge>=7.95,1,0)
n_bulge = np.where( bad_gal==0, n_bulge, np.nan)
BT = np.where( bad_gal==0, BT, np.nan)
r_bulge = np.where( bad_gal==0, r_bulge, np.nan)

for a in zip(galcount, BT, n_bulge, r_bulge):
    if a[1]<=0.7 and a[1]>0.5:
        print a
