import sys
import os
import numpy as np
import bin_stats as bs
import pylab as pl
from MatplotRc import *
from bm_plot_funcs import *


log_Mstar_bulge, r_bulge, n_bulge, BT, ttype, sel_ser = extract_data()

#bad_gal =  np.where(r_bulge<=0.1,1,0)|np.where(n_bulge>=7.95,1,0)
#n_bulge = np.where( bad_gal==0, n_bulge, np.nan)
#BT = np.where( bad_gal==0, BT, np.nan)
#r_bulge = np.where( bad_gal==0, r_bulge, np.nan)

array_list = [log_Mstar_bulge,n_bulge,BT,r_bulge]

nrow_plots = 5
ncol_plots = 3
fig = pl.figure(figsize = (3*ncol_plots,3*nrow_plots))
pl.subplots_adjust(hspace=0.5, wspace = 0.5)

plot_figs(log_Mstar_bulge,n_bulge, BT,  r_bulge, 1, fig, nrow_plots, ncol_plots, "All Galaxies")

binnames = ['0.0<BT<=0.3','0.3<BT<=0.5','0.5<BT<=0.7','0.7<BT<=1.0'] 

bt_bins = [0.0,0.3, 0.5, 0.7,1.0]
for rowct, tmp_bt in enumerate(bt_bins):
    if rowct == len(bt_bins)-1:
        continue
    selection = np.where(BT<=bt_bins[rowct+1], 1,0)*np.where(BT>tmp_bt, 1,0)
    bt_selection =np.where(BT<=bt_bins[rowct+1], 1,0)*np.where(BT>tmp_bt, 1,0)
    new_arr_list = get_data(selection, array_list)
    BT_arr_list = get_data(bt_selection, array_list)
    plot_figs(log_Mstar_bulge,new_arr_list[1], BT_arr_list[2],  new_arr_list[3], 3*(rowct+1)+1, fig, nrow_plots, ncol_plots, binnames[rowct])

pl.savefig('bulgem.eps', bbox_inches='tight')

