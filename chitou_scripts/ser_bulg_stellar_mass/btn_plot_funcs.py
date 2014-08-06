import sys
import os
import numpy as np
import statistics.bin_stats as bs
import pylab as pl
from MatplotRc import *

def plot_figs(log_Mstar_bulge,n_bulge, BT,  r_bulge_cir, plotstart, 
              fig, nrow_plots, ncol_plots, title=''):
    xmaj = 3.0
    xstr = "%d"
    xmin = 0.25
   
    ax = fig.add_subplot(nrow_plots,ncol_plots,plotstart)
    data_holder = pub_plots(xmaj, xmin, xstr, 2.0, 0.5, '%d')
    ndata = bs.bin_stats(log_Mstar_bulge, n_bulge, np.arange(-8,10.0,.5), 0.0, 8.0)
    ndata.plot_ebar('median', 'med95ci', ecolor='r', linestyle = 'none', ms=3, marker='o')
    ndata.lay_bounds(sigma_choice = [68,95])
    pl.ylim(0.0, 8.0)
    pl.xlim(-8, 10.0)
    pl.xlabel('ttype')
    pl.ylabel('n$_{bulge}$')
    pl.title(title)
    #pl.text(0.1, 0.1,str(np.sum(ndata.bin_number)), horizontalalignment='left',
    #     verticalalignment='center',transform=ax.transAxes)
    data_holder.set_plot(ax)

    ax = fig.add_subplot(nrow_plots,ncol_plots,plotstart+1)
    data_holder2 = pub_plots(xmaj, xmin, xstr, 0.2, 0.05, '%0.1f')
    ndata = bs.bin_stats(log_Mstar_bulge, BT, np.arange(-8.0,10,.5), 0.0, 8.0)
    ndata.plot_ebar('median', 'med95ci', ecolor='r', linestyle = 'none', ms=3, marker='o')
    ndata.lay_bounds(sigma_choice = [68,95])
    pl.ylim(0.0, 1.0)
    pl.xlim(-8.0, 10.0)
    pl.xlabel('ttype')
    pl.ylabel('BT')
    pl.title(title)
    #pl.text(0.1, 0.1,str(np.sum(ndata.bin_number)), horizontalalignment='left',
    #     verticalalignment='center',transform=ax.transAxes)
    data_holder2.set_plot(ax)

    ax = fig.add_subplot(nrow_plots,ncol_plots,plotstart+2)
    data_holder3 = pub_plots(xmaj, xmin, xstr, 0.5, 0.1, '%0.1f')
    
    ndata = bs.bin_stats(log_Mstar_bulge, r_bulge_cir, np.arange(-8,10,.5), 0.0, 100.0)
    ndata.to_log(1)
    #raw_input()
    ndata.plot_ebar('median', 'med95ci', ecolor='r', linestyle = 'none', ms=3, marker='o')
    ndata.lay_bounds(sigma_choice = [68,95])
    ax = pl.gca()
    #ax.set_yscale('log')
    #pl.ylim(0.5, 20.0)
    pl.ylim(-1, 1.0)
    pl.xlim(-8, 10.0)
    pl.xlabel('ttype')
    pl.ylabel('logR$_{bulge, cir}$ [kpc]')
    pl.title(title)
    #pl.text(0.1, 0.1,str(np.sum(ndata.bin_number)), horizontalalignment='left',
    #     verticalalignment='center',transform=ax.transAxes)
    data_holder3.set_plot(ax)

    return

def get_data(selection, array_list):
    new_arr_list = []
    for a  in array_list:
        new_arr_list.append(np.where(selection==1, a, np.nan))
    return new_arr_list

