import pylab
from MatplotRc import *
from pylab import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as n
from pylab import plt
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter

def plot_galaxy_fit(save_name, d2_data, d2_model, d2_resid, mask, d1_rad, d1_flux, d1_error, d1_styles, d1_labels, d1_rad_resid, d1_flux_resid, d1_styles_resid, d1_labels_resid,d1_max_rad,one_percent_sky,full_sky, title='blank', add_info = '', add_names = '', label_string = ''):
    """ plot_galaxy_fit(save_name, d2_data, d2_model, d2_resid, mask, d1_rad, d1_flux, d1_error, d1_styles,
                        d1_labels, d1_rad_resid, d1_flux_resid, d1_styles_resid, d1_labels_resid,d1_max_rad,
                        one_percent_sky,full_sky, title='blank', add_info = '', add_names = '',
                        label_string = '')

    This function plots the data for a galaxy fit including the 2d data, model and residual. It also plots
    the 1d surface brightness profile and residual.

    Inputs to be provided:
    save_name: name of the file to save the plot to (should be a png file)
    d2_data: 2d array of data values in magnitudes
    d2_model: 2d array of fit values in magnitudes
    d2_resid: 2d residual between the data and model
    mask: The image mask used in fitting (this is used to scale the residual color scale)
    d1_rad: radii of the 1d surface brightness profile measurements
    d1_flux: the flux at the 1d radii
    d1_error: the error on the 1d flux used to add error bars on the plot
    d1_styles: the plotting styles for the 1d data
    d1_labels: Labels for the legend for 1d data
    d1_rad_resid: radii of the 1d residual (model - data)
    d1_flux_resid: residual at the d1_rad_resid locations
    d1_styles_resid: plotting styles for the residual
    d1_labels_resid: labels for the residual plot (currently unused)
    d1_max_rad: the maximum radius to plot in the 1d plot
    one_percent_sky: the one percent sky label
    full_sky: the full sky level
    title='blank' : the title to place on the plot
    add_info = '' : info to plot in the left margin
    add_names = '' : names to be paired with info in the left margin
    label_string = '' : text to put in the footer
    """


    # switches for plotting
    plot = 'surf' # or "pixel"   -sets the 3d residual to be pixelized or smoothed into a surface
    yes_leg = 1   # turns on the legend in the left margin
    pix_sz = 0.396 # pixel size used for converting pixel values to arcseconds 
    yes_error = 0 # turns on the errorbars on 1d plots

    # pix_rad is used to select the 3d residual window and set residual range
    pix_rad = d1_max_rad/pix_sz

    # convert the 2d data to invert the color scale
    adj_data = n.abs(d2_data - n.max(d2_model))/n.max(n.abs(d2_model - n.max(d2_model)))
    adj_model = n.abs(d2_model - n.max(d2_model))/n.max(n.abs(d2_model - n.max(d2_model)))

    # select the window size used for the 3d residual, also trim the mask and set coordinates in arcsec
    norm_window = d2_resid[int(n.shape(d2_resid)[0]/2) -pix_rad :int(n.shape(d2_resid)[0]/2) + pix_rad,int(n.shape(d2_resid)[1]/2) -pix_rad :int(n.shape(d2_resid)[1]/2) + pix_rad]
    norm_mask = mask[int(n.shape(d2_resid)[0]/2) -pix_rad :int(n.shape(d2_resid)[0]/2) + pix_rad,int(n.shape(d2_resid)[1]/2) -pix_rad :int(n.shape(d2_resid)[1]/2) + pix_rad]

    zmax = n.max(n.extract(norm_mask, norm_window)) 
    zmin = n.min(n.extract(norm_mask, norm_window))

    window_xstart = int(n.shape(d2_resid)[0]/2) -pix_rad
    window_ystart = int(n.shape(d2_resid)[1]/2) -pix_rad

    big_yedges = (n.arange(n.shape(d2_data)[0]+1)-n.shape(d2_data)[0]/2.0)*pix_sz
    big_xedges = (n.arange(n.shape(d2_data)[1]+1)-n.shape(d2_data)[1]/2.0)*pix_sz
    
    big_xpos, big_ypos = n.meshgrid(big_xedges, big_yedges)

    # now begin the plotting
    fig = plt.figure(figsize = (12.0,13.0))
    matrc6()

    # print the title and additional info in the left margin 
    pylab.suptitle(title,fontsize = 14)
    sup_y = .94
    for var_name, var_val in zip(add_names[1:-1].split(','),add_info[1:-1].split(',')):
        pylab.suptitle(var_name + '=' + var_val, fontsize = 10, y = sup_y , x = 0.07)
        sup_y -= .02 

    pylab.suptitle('Note: units are magnitude/arcsec$^2$ for 2d/3d plots and arcsec for axes', x = .58, y = .66, fontsize = 8)
    pylab.suptitle(label_string, fontsize = 12, y = .03)

    # Now add the plots
    # 2d data
    ax = fig.add_subplot(321)
    pylab.pcolor(big_xpos,big_ypos,adj_data)
    pylab.clim(0,1)
    cbar=pylab.colorbar(ticks=[0,.2,.4,.6,.8,1])
    cbar.ax.set_yticklabels(['%3.1f'%(n.max(d2_model)),'%3.1f'%(n.max(d2_model)-.2*(n.max(d2_model) -n.min(d2_model))),'%3.1f'%(n.max(d2_model)-.4*(n.max(d2_model) -n.min(d2_model))),'%3.1f'%(n.max(d2_model)-.6*(n.max(d2_model) -n.min(d2_model))),'%3.1f'%(n.max(d2_model)-.8*(n.max(d2_model) -n.min(d2_model))),'%3.1f'%(n.min(d2_model))])
    pylab.title('Data')

    # 2d model
    ax = fig.add_subplot(322)
    pylab.pcolor(big_xpos,big_ypos,adj_model)
    pylab.clim(0,1)
    pylab.title('Model')
    cbar=pylab.colorbar(ticks=[0,.2,.4,.6,.8,1])
    cbar.ax.set_yticklabels(['%3.1f'%(n.max(d2_model)),'%3.1f'%(n.max(d2_model)-.2*(n.max(d2_model) -n.min(d2_model))),'%3.1f'%(n.max(d2_model)-.4*(n.max(d2_model) -n.min(d2_model))),'%3.1f'%(n.max(d2_model)-.6*(n.max(d2_model) -n.min(d2_model))),'%3.1f'%(n.max(d2_model)-.8*(n.max(d2_model) -n.min(d2_model))),'%3.1f'%(n.min(d2_model))])

    # 2d residual
    ax = fig.add_subplot(323)
    pylab.pcolor(big_xpos,big_ypos,d2_resid)
    pylab.title('Residual')
    pylab.clim(zmin,zmax)
    pylab.colorbar()

    # Now plot the 3d residual 
    if plot == 'pixel':
        ax = fig.add_subplot(324,projection='3d')
        yedges = (n.arange(n.shape(norm_window)[0]+1)-n.shape(norm_window)[0]/2.0)*pix_sz
        xedges = (n.arange(n.shape(norm_window)[1]+1)-n.shape(norm_window)[1]/2.0)*pix_sz
        elements = (len(xedges) ) * (len(yedges) )
        xpos, ypos = n.meshgrid(xedges, yedges)
        xpos = xpos.flatten()
        ypos = ypos.flatten()
        zpos = n.zeros(elements)
        dx = .5 * n.ones_like(zpos)
        dy = dx.copy()
        dz = norm_window.flatten()
                
        pylab.title('3D normalized residual')
        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color = 'b', zsort='average')

    elif plot == 'surf':
        ax = fig.add_subplot(324,projection='3d')
        yedges = (n.arange(n.shape(norm_window)[0]+1)-n.shape(norm_window)[0]/2.0)*pix_sz
        xedges = (n.arange(n.shape(norm_window)[1]+1)-n.shape(norm_window)[1]/2.0)*pix_sz
        elements = (len(xedges) ) * (len(yedges) )
        xpos, ypos = n.meshgrid(xedges, yedges)
        
        surf = ax.plot_surface(xpos, ypos, norm_window, rstride=1, cstride=1, cmap=cm.jet,
                               linewidth=0, antialiased=False, vmin = zmin, vmax = zmax)
        
        ax.set_zlim3d(zmin, zmax)
        
        ax.w_zaxis.set_major_locator(LinearLocator(10))
        ax.w_zaxis.set_major_formatter(FormatStrFormatter('%.03f'))
        
        fig.colorbar(surf, shrink=0.5, aspect=5)

    # 1d galaxy profile
    ax = fig.add_subplot(325)
    pylab.title('1D Sky Subtracted Surface Brightness Profile')
    pylab.ylabel('$\mu$ [mag/arcsec$^2$]')
    pylab.xlabel('r [arcsec]')
    
    # place the limits on the plot (these are hard-coded but should maybe be changed)
    pylab.xlim(0,d1_max_rad)
    pylab.ylim(28,18)

    # now plot the galaxy profiles
    label_legend = d1_labels
    label_legend_lines = []
    for rad, flux, plot_style, label_names, error in zip(d1_rad, d1_flux, d1_styles, d1_labels, d1_error):
        label_legend_lines.append(pylab.plot(rad,flux, plot_style, label = label_names))
        if yes_error:
            pylab.errorbar(rad,flux,yerr = error, fmt = None,ecolor = plot_style[0])    

    # plot the 1% and full sky values
    label_legend_lines.append(pylab.plot([0,d1_max_rad],[full_sky,full_sky], 'k--'))
    label_legend.append('full sky')
    label_legend_lines.append(pylab.plot([0,d1_max_rad],[full_sky + 5,full_sky + 5], 'k:'))
    label_legend.append('1% sky')

    # now add legend if the switch is on 
    if yes_leg:
        pylab.figlegend(label_legend_lines, label_legend, loc = 3,bbox_to_anchor=(0.01, 0.13, 0.09, .30), title="1D Legend")

    # 1d residuals
    ax = fig.add_subplot(326)
    pylab.title('1D Residual')
    pylab.ylabel('$\mu$ [mag/arcsec$^2$]')
    pylab.xlabel('r [arcsec]')
    pylab.xlim(0,d1_max_rad)
    pylab.ylim(-0.5,0.5)
    
    # plot the zero-line
    pylab.plot([0,100],[0,0], 'k-')

    # plot the residuals
    for rad, flux, plot_style, label_names in zip(d1_rad_resid, d1_flux_resid, d1_styles_resid, d1_labels_resid):
        pylab.plot(rad,flux, plot_style, label = label_names)
    


    # now save the figure
    pylab.savefig(save_name, format = 'png')

    # done!!!!
    return



import matplotlib.colors as b
def cmap_map(function,cmap):
    """ Applies function (which should operate on vectors of shape 3:
    [r, g, b], on colormap cmap. This routine will break any discontinuous     points in a colormap.
    """
    
    # I don't use this anymore and I suspect it doesn't work correctly.
    # It was originally intended to invert the colormap so that it can be
    # used on observed magnitudes.

    cdict = cmap._segmentdata
    step_dict = {}
    # Firt get the list of points where the segments start or end
    for key in ('red','green','blue'):
        step_dict[key] = map(lambda x: x[0], cdict[key])
    step_list = sum(step_dict.values(), [])
    step_list = n.array(list(set(step_list)))
    # Then compute the LUT, and apply the function to the LUT
    reduced_cmap = lambda step : n.array(cmap(step)[0:3])
    old_LUT = n.array(map( reduced_cmap, step_list))
    #new_LUT = old_LUT[::-1]
    new_LUT = n.array(map( function, old_LUT))
    # Now try to make a minimal segment definition of the new LUT
    cdict = {}
    for i,key in enumerate(('red','green','blue')):
        this_cdict = {}
        for j,step in enumerate(step_list):
            if step in step_dict[key]:
                this_cdict[step] = new_LUT[j,i]
            elif new_LUT[j,i]!=old_LUT[j,i]:
                this_cdict[step] = new_LUT[j,i]
        colorvector=  map(lambda x: x + (x[1], ), this_cdict.items())
        colorvector.sort()
        cdict[key] = colorvector

    return b.LinearSegmentedColormap('colormap',cdict,1024)
