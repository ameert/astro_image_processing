from MatplotRc import *

import pylab as pl
from pylab import plt
from pylab import cm, colors
import matplotlib.font_manager as fm
from matplotlib.patches import Ellipse
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
import matplotlib.ticker as mticker
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import astro_utils.user_params as params

prop = fm.FontProperties(size=10)

d1_color = {'dev':'g', 'ser':'m', 'devexp':'b', 'serexp':'r', 'data':'k' }
d1_styles= {'total':'-', 'resid':'-', 'bulge':'--', 'disk':':', 'data':'.' }

def get_min_max(data_dict):
    data_tmp = data_dict['data']
    vmax = np.max(data_tmp[5*data_tmp.shape[0]/12:7*data_tmp.shape[0]/12,
                   5*data_tmp.shape[1]/12:7*data_tmp.shape[1]/12])
    vmin = np.min(data_tmp[5*data_tmp.shape[0]/12:7*data_tmp.shape[0]/12,
                           5*data_tmp.shape[1]/12:7*data_tmp.shape[1]/12])
    print "min max %f %f" %(vmin, vmax)
    #vmin, vmax = pl.gci().get_clim()
    return vmin, vmax

def make_plot(data_dict, arcsec = True):          
    new_extent = np.array([np.array(data_dict['xext'], dtype=float)-data_dict['xctr'], np.array(data_dict['yext'], dtype=float)-data_dict['yctr']])
    new_extent = new_extent.flatten()
    if arcsec:
        new_extent = new_extent*params.defaults['pixsz']
    print 'plotting extent ',        
    pl.imshow(data_dict['data'], cmap=cm.jet_r, interpolation = 'nearest', 
              extent = new_extent, origin = 'lower',
              aspect = abs((new_extent[1]-new_extent[0])/(new_extent[3]-new_extent[2])))

    ax1 = pl.gca()
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(7, prune='both'))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(7, prune='both'))
    # requires knowledge about image dimensions that I currently do not have
    #ax = pl.gca()
    #ells = [Ellipse(xy=(0.0,0.0),width=1.0, height=3.0, angle=0.0, linestyle = "dashed"),
    #        Ellipse(xy=(0.0,0.0),width=1.0, height=3.0, angle=0.0, linestyle = "dotted")]
    #for e in ells:
    #    ax.add_artist(e)
    #    e.set_clip_box(ax.bbox)
    #    e.set_alpha(0.5)
    #    e.set_facecolor('none')
    #    e.set_edgecolor('k')

    return

def plot_galaxy_fit(save_name, d2_data_wide, d2_data, d2_model, d2_resid,
                    d1_data, d1_max_rad, hrad,
                    one_percent_sky, full_sky, model,
                    title='blank', add_info_left = '', add_info_right = '', 
                    label_string = ''):

    """ plot_galaxy_fit(save_name, d2_data, d2_model, d2_resid,
d1_data, d1_styles, d1_labels, 
d1_resid_data, d1_styles_resid, d1_labels_resid,
d1_max_rad, one_percent_sky,full_sky, 
title='blank', add_info = '', label_string = '')

This function plots a galaxy fit including the 2d data, model and residual.
It also plots the 1d surface brightness profile and residual.

Inputs to be provided:
save_name: name of the file to save the plot to (should be a png file)
d2_data: 2d array of data values in magnitudes
d2_model: 2d array of fit values in magnitudes
d2_resid: 2d residual between the data and model
d1_data: radii,flux, error of the 1d surface brightness profile measurements
d1_styles: the plotting styles for the 1d data
d1_labels: Labels for the legend for 1d data
d1_data_resid: radii, residual, error of the 1d residual (model - data)
d1_styles_resid: plotting styles for the residual
d1_labels_resid: labels for the residual plot (currently unused)
one_percent_sky: the one percent sky label
full_sky: the full sky level
title='blank' : the title to place on the plot
add_info = '' : info to plot in the left margin
label_string = '' : text to put in the footer
"""
    plt.ioff()

    yes_leg = 1   # turns on the legend in the left margin
    yes_error = 0 # turns on the errorbars on 1d plots
    arcsec_or_pixels = True #true causes pixel coordinates to be converted to arcsec
    # now begin the plotting
    galplot6()
    fig = plt.figure()
    galplot6()

    # print the title and additional info in the left margin 
    #pl.suptitle(title,fontsize = 14)
    sup_y = .96
    textsize = 11
    for var_name in add_info_left:
        if 'FLAGS' in var_name:
            textsize = 8
        pl.figtext(0.02, sup_y, var_name, fontsize = textsize,
                    horizontalalignment = 'left')
        sup_y -= .0225 

    # print the title and additional info in the right margin 
    #pl.suptitle(title,fontsize = 14)
    sup_y = .96
    for var_name in add_info_right:
        pl.figtext(0.98, sup_y, var_name, fontsize = 11,
                    horizontalalignment = 'right')
        sup_y -= .0225 

    #pl.figtext(0.58, 0.66, 'Note: units are magnitude/arcsec$^2$ for 2d/3d plots and arcsec for axes', fontsize = 8,horizontalalignment = 'center')
    pl.figtext(0.5, 0.03, label_string, fontsize = 8,horizontalalignment = 'center')

    # Now add the plots
    
    # get the color limits of the model in the center halflight radius
    vmin, vmax = get_min_max(d2_model)

    # 2d model
    fig.add_subplot(424)
    make_plot(d2_model, arcsec = arcsec_or_pixels)
    pl.title('Zoomed in Model')
    pl.clim(vmin, vmax)
    pl.colorbar(shrink = 1.0)

    
    # 2d data
    fig.add_subplot(421)
    make_plot(d2_data_wide, arcsec = arcsec_or_pixels)
    pl.clim(vmin, vmax)
    pl.colorbar(shrink = 1.0)
    pl.title('Data')

    fig.add_subplot(422)
    make_plot(d2_data, arcsec = arcsec_or_pixels)
    pl.clim(vmin, vmax)
    pl.colorbar(shrink = 1.0)
    pl.title('Zoomed in Data')

    # 2d residual
    fig.add_subplot(423)
    make_plot(d2_resid, arcsec = arcsec_or_pixels)
    pl.title('Zoomed in Residual')

    vmin_r, vmax_r = get_min_max(d2_resid) 

    #make the residual symmetric about zero
    if np.abs(vmin_r)<vmax_r:
        vmin_r = -1.0*vmax_r
    else:
        vmax_r = -1.0*vmin_r

    print "min max %f %f" %(vmin, vmax)
    pl.clim(vmin_r, vmax_r)
    pl.colorbar(shrink = 1.0)

    
    # 1d galaxy profile
    ax = fig.add_subplot(425)
    pl.title('1D Sky Subtracted Surface Brightness Profile',fontsize = 10 )
    pl.ylabel('$\mu$ [mag/arcsec$^2$]')
    pl.xlabel('r [arcsec]')

    # now plot the galaxy profiles
    #for flux label_names, error in zip(d1_rad, d1_flux, d1_styles, d1_labels, d1_error):

    ux = 999
    for key in [('data','data'), 
                (model,'total'),(model,'bulge'),(model,'disk')]:
        try:
            pl.plot(d1_data['rad'],d1_data[key[1]], d1_color[key[0]]+d1_styles[key[1]], label = key[0]+' '+key[1], markersize=8)
            if  (d1_data[key[1]][0]-0.5) < ux:
                ux = (d1_data[key[1]][0]-0.5)
        except KeyError:
            print 'no %s entry...skipping 1d plot for this key' %(key[0]+' '+key[1])

    # plot the 1% and full sky values
    pl.plot([0,d1_max_rad],[full_sky,full_sky], 'k--', label='full sky')
    pl.plot([0,d1_max_rad],[one_percent_sky,one_percent_sky], 'k:', label='1\% sky')

    # place the limits on the plot (these are hard-coded but should maybe be changed)
    ax1_xlim = np.array(pl.xlim(0,d1_max_rad))
    ax1_ylim = np.array(pl.ylim(28,np.min( np.array([ux, 18.0]))))

    hrads = np.arange(1.0, 6.01,1.0)*hrad
    curr_ylims = pl.ylim()
    vlines = pl.vlines(hrads,curr_ylims[0], curr_ylims[1],color='#A8A8A8', linestyle='-.', label='r$_{hl}$')

    ax = pl.gca()
    # now add legend if the switch is on 
    if yes_leg:
        handles, labels = ax.get_legend_handles_labels()
        pl.figlegend(handles, labels, loc = 3,bbox_to_anchor=(0.005, 0.3, 0.07, .15), title="1D Legend", prop = prop)


    #ax2 = ax.twiny() # ax2 is responsible for "top" axis 
    #ax2.set_xlim(ax1_xlim/hrad)
    #ax2.xaxis.set_major_locator(mticker.MaxNLocator(7, prune=None))
    #set_xticks([0., .5*np.pi, np.pi, 1.5*np.pi, 2*np.pi])
    #ax2.set_xticklabels(["$0$", r"$\frac{1}{2}\pi$",
    #                 r"$\pi$", r"$\frac{3}{2}\pi$", r"$2\pi$"])

    #ax2.axis["right"].major_ticklabels.set_visible(False)


    # 1d residuals
    fig.add_subplot(426)
    pl.title('1D Residual')
    pl.ylabel('$\mu$ [mag/arcsec$^2$]')
    pl.xlabel('r [arcsec]')
    pl.xlim(0,d1_max_rad)
    pl.ylim(-0.5,0.5)

    hrads = np.arange(1.0, 6.01,1.0)*hrad
    curr_ylims = pl.ylim()
    vlines = pl.vlines(hrads,curr_ylims[0], curr_ylims[1],color='#A8A8A8', linestyle='-.', label='r$_{hl}$')

    # plot the zero-line
    pl.plot([0,100],[0,0], 'k-')

    # plot the residuals
    key = (model, 'resid')
    pl.plot(d1_data['rad'],d1_data[key[1]], d1_color[key[0]]+d1_styles[key[1]], markersize=8)

    # 1d bt plot
    fig.add_subplot(427)
    pl.title('BT(r)')
    pl.ylabel('BT')
    pl.xlabel('r [arcsec]')
    pl.xlim(0,d1_max_rad)
    pl.ylim(0.0,1.0)

    pl.plot(pl.xlim(),[1.0,1.0], 'k-')
    pl.plot(pl.xlim(),[0.5,0.5], 'k-')
    pl.plot(d1_data['bt_rad'],d1_data['bt_at_rad'], d1_color[model]+'--', label = 'bt(r)')
    pl.plot(d1_data['bt_rad'],d1_data['bt_cum'], d1_color[model]+'-', label = 'bt cum')

    hrads = np.arange(1.0, 6.01,1.0)*hrad
    curr_ylims = pl.ylim()
    vlines = pl.vlines(hrads,curr_ylims[0], curr_ylims[1],color='#A8A8A8', linestyle='-.', label='r$_{hl}$')


    ax = pl.gca()
    handles, labels = ax.get_legend_handles_labels()
    pl.figlegend(handles, labels, loc = 3,bbox_to_anchor=(0.005, 0.15, 0.07, .15), title="BT Legend", prop = prop)


    # 1d light plot
    fig.add_subplot(428)
    pl.title('L$_{inc}$(r)')
    pl.ylabel('L/L$_{tot}$')
    pl.xlabel('r [arcsec]')
    pl.xlim(0,d1_max_rad)
    pl.ylim(0.0,1.0)

    pl.plot(pl.xlim(),[1.0,1.0], 'k-')
    pl.plot(pl.xlim(),[0.9,0.9], 'k-')
    pl.plot(d1_data['bt_rad'],d1_data['light_cum'], d1_color[model]+'-')

    hrads = np.arange(1.0, 6.01,1.0)*hrad
    curr_ylims = pl.ylim()
    vlines = pl.vlines(hrads,curr_ylims[0], curr_ylims[1],color='#A8A8A8', linestyle='-.', label='r$_{hl}$')

    # now save the figure
    pl.savefig(save_name)
    # done!!!!
    plt.close('all')
    del ax
    return
