import sys
import os
import numpy as np
import bin_stats as bs
import pylab as pl
from MatplotRc import *
from bm_plot_funcs import *


gal_opt = sys.argv[1]

log_Mstar_bulge, r_bulge, n_bulge, BT, ttype, sel_ser, galcount = extract_data()

if gal_opt == 'Ell':
    tlow = -8.0
    thigh = -4.0
    binnames = ['0.5<BT<=0.65','0.65<BT<=1.0', 'Single Ser'] 
    bt_bins = [0.5, 0.65,0.95,1.05]
elif gal_opt == 'S0':
    tlow = -4.0
    thigh = 0.5
    binnames = ['0.35<BT<=0.5','0.5<BT<=0.65','0.65<BT<=1.0', 'Single Ser'] 
    bt_bins = [0.35, 0.5, 0.65,0.95,1.05]
elif gal_opt == 'Sab':
    tlow = 0.5
    thigh = 4.0
    binnames = ['0.2<BT<=0.35','0.35<BT<=0.5','0.5<BT<=0.65','0.65<BT<=1.0'] 
    bt_bins = [0.2,0.35, 0.5, 0.65,0.8]
elif gal_opt == 'Scd':
    tlow = 4.0
    thigh = 10.0
    binnames = ['Pure Disk','0.0<BT<=0.35','0.35<BT<=0.5'] 
    bt_bins = [0.0,0.05, 0.35,0.5]

ttype =  np.where(ttype<=thigh,1,0)*np.where(ttype>tlow,1,0)
if gal_opt == 'Scd':
    ttype = ttype*(np.where(BT<0.05, 1,0)|np.where(log_Mstar_bulge<11.0, 1,0))
n_bulge = np.where( ttype==1, n_bulge, np.nan)
BT = np.where( ttype==1, BT, np.nan)
r_bulge = np.where( ttype==1, r_bulge, np.nan)

bad_gal =  np.where(n_bulge>=7.95,1,0) #np.where(r_bulge<=0.1,1,0)|
n_bulge = np.where( bad_gal==0, n_bulge, np.nan)
BT = np.where( bad_gal==0, BT, np.nan)
r_bulge = np.where( bad_gal==0, r_bulge, np.nan)


nrow_plots = 7
ncol_plots = 3
fig = pl.figure(figsize = (3*ncol_plots,3*nrow_plots))
pl.subplots_adjust(hspace=0.5, wspace = 0.5)

array_list = [log_Mstar_bulge,n_bulge, BT,  r_bulge]

selection = np.where(BT>bt_bins[0], 1,0)*np.where(BT<=bt_bins[-1], 1,0)
bt_selection =np.where(BT>bt_bins[0], 1,0)*np.where(BT<=bt_bins[-1], 1,0)
new_arr_list = get_data(selection, array_list)
BT_arr_list = get_data(bt_selection, array_list)
plot_figs(log_Mstar_bulge,new_arr_list[1], BT_arr_list[2],  new_arr_list[3], 1, fig, nrow_plots, ncol_plots, gal_opt)

for rowct, tmp_bt in enumerate(bt_bins):
    if rowct == len(bt_bins)-1:
        continue
    selection = np.where(BT<=bt_bins[rowct+1], 1,0)*np.where(BT>tmp_bt, 1,0)
    bt_selection =np.where(BT<=bt_bins[rowct+1], 1,0)*np.where(BT>tmp_bt, 1,0)
    new_arr_list = get_data(selection, array_list)
    BT_arr_list = get_data(bt_selection, array_list)
    plot_figs(log_Mstar_bulge,new_arr_list[1], BT_arr_list[2],  new_arr_list[3], 3*(rowct+1)+1, fig, nrow_plots, ncol_plots, binnames[rowct])

pl.savefig('bulgem_%s.eps' %gal_opt, bbox_inches='tight')
