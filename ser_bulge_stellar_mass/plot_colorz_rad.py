import sys
import os
import numpy as np
import astro_image_processing.statistics.bin_stats as bs
import pylab as pl
from astro_image_processing.MatplotRc import *
from btn_plot_funcs import *

data = np.load('best_model_data.npz')

mtot = data['mtot']-data['mcorr']
gr_color = data['grcolor']
z=data['z']
n_bulge =data['n_bulge']
r_tot =data['r_tot']
flags = data['flags']
ttype = data['ttype']
resolution = 0.396*data['kpc_per_arcsec']
concentration = data['concentration']

nrow_plots = 6
ncol_plots = 4
fig = pl.figure(figsize = (3*ncol_plots,2.5*nrow_plots))
pl.subplots_adjust(hspace=0.5, wspace = 0.5)

array_list = [mtot, gr_color, z, r_tot, concentration]

bulges = np.where(flags&(2**1)>0, 1,0)
disks = np.where(flags&(2**4)>0, 1,0)
good_2com = np.where(flags&(2**10)>0, 1,0)*np.where(n_bulge<7.95,1,0)
n8 = np.where(flags&(2**10)>0, 1,0)*np.where(n_bulge>=7.95,1,0)
prob_2com = np.where(flags&(2**14)>0, 1,0)
bad = np.where(flags&(2**20)>0, 1,0)

new_arr_list = get_data(bulges, array_list)
plot_figs2(new_arr_list[3],new_arr_list[1], new_arr_list[0],  new_arr_list[2], new_arr_list[4], 1, fig, nrow_plots, ncol_plots, title="bulges", xlim=(0.0, 10.0), xlabel='r$_{tot, hl}$ [arcsec]', xbin=np.arange(0,10.01, 0.5))

new_arr_list = get_data(good_2com, array_list)
plot_figs2(new_arr_list[3],new_arr_list[1], new_arr_list[0],  new_arr_list[2], new_arr_list[4], 5, fig, nrow_plots, ncol_plots, title="2com", xlim=(0.0, 10.0), xlabel='r$_{tot, hl}$ [arcsec]', xbin=np.arange(0,10.01, 0.5))

new_arr_list = get_data(n8, array_list)
plot_figs2(new_arr_list[3],new_arr_list[1], new_arr_list[0],  new_arr_list[2], new_arr_list[4], 9, fig, nrow_plots, ncol_plots, title="n8", xlim=(0.0, 10.0), xlabel='r$_{tot, hl}$ [arcsec]', xbin=np.arange(0,10.01, 0.5))

new_arr_list = get_data(prob_2com, array_list)
plot_figs2(new_arr_list[3],new_arr_list[1], new_arr_list[0],  new_arr_list[2], new_arr_list[4], 13, fig, nrow_plots, ncol_plots, title="prob 2com", xlim=(0.0, 10.0), xlabel='r$_{tot, hl}$ [arcsec]', xbin=np.arange(0,10.01, 0.5))

new_arr_list = get_data(bad, array_list)
plot_figs2(new_arr_list[3],new_arr_list[1], new_arr_list[0],  new_arr_list[2], new_arr_list[4], 17, fig, nrow_plots, ncol_plots, title="bad", xlim=(0.0, 10.0), xlabel='r$_{tot, hl}$ [arcsec]', xbin=np.arange(0,10.01, 0.5))

new_arr_list = get_data(disks, array_list)
plot_figs2(new_arr_list[3],new_arr_list[1], new_arr_list[0],  new_arr_list[2], new_arr_list[4], 21, fig, nrow_plots, ncol_plots, title="disks", xlim=(0.0, 10.0), xlabel='r$_{tot, hl}$ [arcsec]', xbin=np.arange(0,10.01, 0.5))

pl.savefig('rtot_colorz.eps', bbox_inches='tight')
