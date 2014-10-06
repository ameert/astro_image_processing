import sys
import os
import numpy as np
import astro_image_processing.statistics.bin_stats as bs
import pylab as pl
from astro_image_processing.MatplotRc import *
from btn_plot_funcs import *

data = np.load('best_model_data.npz')

n_bulge=data['n_bulge']
BT = data['BT']
r_bulge = data['r_bulge']
flags = data['flags']
ttype = data['ttype']

#BT = np.where(flags&(2**1)>0, 1.0, BT)
BT = np.where(flags&(2**4)>0, 0.01, BT)

r_bulge = np.where(flags&(2**4)>0, 0.001, r_bulge)
n_bulge = np.where(flags&(2**4)>0, 0.01, n_bulge)

nrow_plots = 1
ncol_plots = 3
fig = pl.figure(figsize = (3*ncol_plots,2.5*nrow_plots))
pl.subplots_adjust(hspace=0.5, wspace = 0.5)

array_list = [BT, n_bulge, r_bulge]

bt_selection =np.where(flags&(2**10+2**1+2**4)>0, 1,0)*np.where(n_bulge>=7.95,0,1)
n_selection = np.where(flags&(2**11+2**12+2**1+2**4)>0, 1,0)*np.where(n_bulge>=7.95,0,1)
n_arr_list = get_data(n_selection, array_list)
BT_arr_list = get_data(bt_selection, array_list)
plot_figs(ttype,n_arr_list[1], BT_arr_list[0],  n_arr_list[2], 1, fig, nrow_plots, ncol_plots, "")




bad_gal =  np.where(r_bulge<=0.1,1,0)|np.where(n_bulge>=7.95,1,0)
n_bulge_t = np.where( bad_gal==0, n_bulge, np.nan)
BT_t = np.where( bad_gal==0, BT, np.nan)
r_bulge_t = np.where( bad_gal==0, r_bulge, np.nan)

array_list = [BT_t, n_bulge_t, r_bulge_t]

bt_selection =np.where(flags&(2**10+2**1+2**4)>0, 1,0)
n_selection = np.where(flags&(2**11+2**12+2**1)>0, 1,0)
n_arr_list = get_data(n_selection, array_list)
BT_arr_list = get_data(bt_selection, array_list)
#plot_figs(ttype,n_arr_list[1], BT_arr_list[0],  n_arr_list[2], 4, fig, nrow_plots, ncol_plots, "n<7.95, r_kpc>0.1")



pl.savefig('ttype_n_bt.eps', bbox_inches='tight')
