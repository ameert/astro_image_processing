import sys
import os
import numpy as np
import bin_stats as bs
import pylab as pl
from MatplotRc import *
from bm_plot_funcs import *

log_Mstar_bulge, r_bulge, n_bulge, BT, ttype, sel_ser, galcount = extract_data()

#bad_gal =  np.where(r_bulge<=0.1,1,0)|np.where(n_bulge>=7.95,1,0)
#n_bulge = np.where( bad_gal==0, n_bulge, np.nan)
#BT = np.where( bad_gal==0, BT, np.nan)
#r_bulge = np.where( bad_gal==0, r_bulge, np.nan)

nrow_plots = 4
ncol_plots = 3
fig = pl.figure(figsize = (3*ncol_plots,3*nrow_plots))
pl.subplots_adjust(hspace=0.5, wspace = 0.5)

array_list = [log_Mstar_bulge,n_bulge, BT,  r_bulge, ttype, galcount]

tbins = [-8.0, -4.0, 0.5, 4.0, 10.0]
binnames = ["Ell", "S0", "Sab", "Scd"]
bt_lims = [(0.5,1.05),(0.35,1.05),(0.2,0.8),(0.0,0.5) ]
for rowct in range(len(tbins[:-1])):
    selection = np.where(ttype<=tbins[rowct+1], 1,0)*np.where(ttype>tbins[rowct], 1,0)*np.where(n_bulge<=7.95, 1,0)*np.where(BT<=bt_lims[rowct][1], 1,0)*np.where(BT>bt_lims[rowct][0], 1,0)
    bt_selection = np.where(ttype<=tbins[rowct+1], 1,0)*np.where(ttype>tbins[rowct], 1,0)*np.where(n_bulge<=7.95, 1,0)
    new_arr_list = get_data(selection, array_list)
    BT_arr_list = get_data(bt_selection, array_list)
    
    if binnames[rowct] == 'Scd':
        count =  0
        for a in zip(new_arr_list[-1], new_arr_list[0], new_arr_list[-2],new_arr_list[2] ):
            if a[1]>11:
                if a[3]>0.0:
                    print a
                    count +=1
        print "total gals>11 ", count
    plot_figs(log_Mstar_bulge,new_arr_list[1], BT_arr_list[2],  new_arr_list[3], 3*rowct+1, fig, nrow_plots,ncol_plots, binnames[rowct])


pl.savefig('bulgem_ttype.eps', bbox_inches='tight')
