import sys
import os
import numpy as np
import astro_image_processing.statistics.bin_stats as bs
import pylab as pl
from astro_image_processing.MatplotRc import *

def plot_figs(log_Mstar_bulge,n_bulge, BT,  r_bulge_cir, plotstart, 
              fig, nrow_plots, ncol_plots, title='', xlim=(-8,10.0), 
              xlabel='ttype', xbin=np.arange(-8,10.0,.5)):
    xmaj = 3.0
    xstr = "%d"
    xmin = 0.5
    pub_plots(xmaj, xmin, xstr, 2.0, 0.5, '%d')

    ax = fig.add_subplot(nrow_plots,ncol_plots,plotstart)
    data_holder = pub_plots(xmaj, xmin, xstr, 2.0, 0.5, '%d')
    ndata = bs.bin_stats(log_Mstar_bulge, n_bulge, xbin, 0.0, 8.0)
    ndata.plot_ebar('median', 'med95ci', ecolor='r', linestyle = 'none', ms=3, marker='o')
    ndata.lay_bounds(sigma_choice = [68,95])
    pl.ylim(0.0, 8.0)
    pl.xlim(xlim)
    pl.xlabel(xlabel)
    pl.ylabel('n$_{bulge}$')
    pl.title(title)
    #pl.text(0.1, 0.1,str(np.sum(ndata.bin_number)), horizontalalignment='left',
    #     verticalalignment='center',transform=ax.transAxes)
    data_holder.set_plot(ax)

    ax = fig.add_subplot(nrow_plots,ncol_plots,plotstart+1)
    data_holder2 = pub_plots(xmaj, xmin, xstr, 0.2, 0.05, '%0.1f')
    ndata = bs.bin_stats(log_Mstar_bulge, BT, xbin, 0.0, 8.0)
    ndata.plot_ebar('median', 'med95ci', ecolor='r', linestyle = 'none', ms=3, marker='o')
    ndata.lay_bounds(sigma_choice = [68,95])
    pl.ylim(0.0, 1.0)
    pl.xlim(xlim)
    pl.xlabel(xlabel)
    pl.ylabel('BT')
    pl.title(title)
    #pl.text(0.1, 0.1,str(np.sum(ndata.bin_number)), horizontalalignment='left',
    #     verticalalignment='center',transform=ax.transAxes)
    data_holder2.set_plot(ax)

    ax = fig.add_subplot(nrow_plots,ncol_plots,plotstart+2)
    data_holder3 = pub_plots(xmaj, xmin, xstr, 0.5, 0.1, '%0.1f')

    ndata = bs.bin_stats(log_Mstar_bulge, r_bulge_cir, xbin, -100.0, 100.0)
    ndata.to_log(1)
    #raw_input()
    ndata.plot_ebar('median', 'med95ci', ecolor='r', linestyle = 'none', ms=3, marker='o')
    ndata.lay_bounds(sigma_choice = [68,95])
    ax = pl.gca()
    #ax.set_yscale('log')
    #pl.ylim(0.5, 20.0)
    pl.ylim(-1.0, 1.0)
    pl.xlim(xlim)
    pl.xlabel(xlabel)
    pl.ylabel('logR$_{bulge, cir}$ [kpc]')
    #pl.ylabel('r$_{bulge, cir}$/r$_{tot, cir}$ -1')
    pl.title(title)
    #pl.text(0.1, 0.1,str(np.sum(ndata.bin_number)), horizontalalignment='left',
    #     verticalalignment='center',transform=ax.transAxes)
    data_holder3.set_plot(ax)

    return

def plot_figs2(log_Mstar_bulge,color, M_tot,  z, concentration, plotstart, 
              fig, nrow_plots, ncol_plots, title='', xlim=(-8,10.0), 
              xlabel='ttype', xbin=np.arange(-8,10.0,.5)):
    xmaj = 1.0
    xstr = "%d"
    xmin = 0.25
   
    ax = fig.add_subplot(nrow_plots,ncol_plots,plotstart)
    data_holder = pub_plots(xmaj, xmin, xstr, 0.5,0.05, '%0.1f')
    ndata = bs.bin_stats(log_Mstar_bulge, color, xbin, -2.0, 2.0)
    ndata.plot_ebar('median', 'med95ci', ecolor='r', linestyle = 'none', ms=3, marker='o')
    ndata.lay_bounds(sigma_choice = [68,95])
    pl.ylim(0.0, 1.0)
    pl.xlim(xlim)
    pl.xlabel(xlabel)
    pl.ylabel('g-r (petro)')
    pl.title(title)
    #pl.text(0.1, 0.1,str(np.sum(ndata.bin_number)), horizontalalignment='left',
    #     verticalalignment='center',transform=ax.transAxes)
    data_holder.set_plot(ax)

    ax = fig.add_subplot(nrow_plots,ncol_plots,plotstart+1)
    data_holder2 = pub_plots(xmaj, xmin, xstr, 2, 0.2, '%d')
    ndata = bs.bin_stats(log_Mstar_bulge, M_tot, xbin, -100.0, 100.0)
    ndata.plot_ebar('median', 'med95ci', ecolor='r', linestyle = 'none', ms=3, marker='o')
    ndata.lay_bounds(sigma_choice = [68,95])
    pl.ylim(-24.0, -17.0)
    pl.xlim(xlim)
    pl.xlabel(xlabel)
    pl.ylabel('M$_r$')
    pl.title(title)
    #pl.text(0.1, 0.1,str(np.sum(ndata.bin_number)), horizontalalignment='left',
    #     verticalalignment='center',transform=ax.transAxes)
    data_holder2.set_plot(ax)

    ax = fig.add_subplot(nrow_plots,ncol_plots,plotstart+2)
    data_holder3 = pub_plots(xmaj, xmin, xstr, 0.1, 0.01, '%0.1f')
    
    ndata = bs.bin_stats(log_Mstar_bulge, z, xbin, -100.0, 100.0)
    #ndata.to_log(1)
    #raw_input()
    ndata.plot_ebar('median', 'med95ci', ecolor='r', linestyle = 'none', ms=3, marker='o')
    ndata.lay_bounds(sigma_choice = [68,95])
    ax = pl.gca()
    #ax.set_yscale('log')
    #pl.ylim(0.5, 20.0)
    pl.ylim(0.0, 0.3)
    pl.xlim(xlim)
    pl.xlabel(xlabel)
    pl.ylabel('z')
    #pl.ylabel('r$_{bulge, cir}$/r$_{tot, cir}$ -1')
    pl.title(title)
    #pl.text(0.1, 0.1,str(np.sum(ndata.bin_number)), horizontalalignment='left',
    #     verticalalignment='center',transform=ax.transAxes)
    data_holder3.set_plot(ax)

    ax = fig.add_subplot(nrow_plots,ncol_plots,plotstart+3)
    data_holder4 = pub_plots(xmaj, xmin, xstr, 1.0, 0.1, '%d')
    
    ndata = bs.bin_stats(log_Mstar_bulge, concentration, xbin, -100.0, 100.0)
    #ndata.to_log(1)
    #raw_input()
    ndata.plot_ebar('median', 'med95ci', ecolor='r', linestyle = 'none', ms=3, marker='o')
    ndata.lay_bounds(sigma_choice = [68,95])
    ax = pl.gca()
    #ax.set_yscale('log')
    #pl.ylim(0.5, 20.0)
    pl.ylim(1.0, 4.0)
    pl.xlim(xlim)
    pl.xlabel(xlabel)
    pl.ylabel('C(petroR90$_r$/petroR50$_r$)')
    #pl.ylabel('r$_{bulge, cir}$/r$_{tot, cir}$ -1')
    pl.title(title)
    #pl.text(0.1, 0.1,str(np.sum(ndata.bin_number)), horizontalalignment='left',
    #     verticalalignment='center',transform=ax.transAxes)
    data_holder4.set_plot(ax)

    return

def get_data(selection, array_list):
    new_arr_list = []
    for a  in array_list:
        new_arr_list.append(np.where(selection==1, a, np.nan))
    return new_arr_list

