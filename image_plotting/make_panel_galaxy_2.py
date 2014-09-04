import pyfits as pf
import pylab as pl
import numpy as np
from pylab import cm
from MatplotRc import *
from mysql_class import *
from pylab import rcParams


dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)

def resize_image(image, rad_pix):
    center = np.array(image.shape, dtype = int)/2
    edges = [center[0]- rad_pix*6, center[0]+rad_pix*6, 
             center[1]- rad_pix*6, center[1]+rad_pix*6] 

    new_image = image[edges[0]:edges[1],edges[2]:edges[3]]

    return new_image

def equal_margins():
    pl.subplots_adjust(left = 0.01,  # the left side of the subplots of the figure
                          right = 0.97,    # the right side of the subplots of the figure
                          bottom = 0.01,   # the bottom of the subplots of the figure
                          top = 0.97,      # the top of the subplots of the figure
                          wspace = 0.15,   # the amount of width reserved for blank space between subplots
                          hspace = 0.15)   # the amount of height reserved for white space between subplots
    return

def load_image(filename, frame_num = 0):
    infile = pf.open(filename)
    data = infile[frame_num].data
    infile.close()
    return data

def make_panel(image, color=cm.gray, zmin = None, zmax = None, pix_sz = 0.396):
    imshape_arcsec = np.array(image.shape)*pix_sz

    if zmin == None:
        zmin = np.min(image)
    if zmax == None:
        zmax = np.max(image)

    pl.imshow(image, cmap=color, interpolation = 'nearest', extent = (-imshape_arcsec[1]/2, imshape_arcsec[1]/2,-imshape_arcsec[1]/2, imshape_arcsec[1]/2), origin = 'lower')
    pl.clim(zmin,zmax)
    
    return zmin, zmax

simu_gals = [5927, 6833, 7233, 10235]
mask_gals = [7780,7782,7976,8346]

for gal in simu_gals + mask_gals:

    cmd = 'select hrad_corr/0.396 from r_band_serexp where galcount = %d;' %gal
    hrad, = cursor.get_data(cmd)
    hrad = hrad[0]

    fig_size = get_fig_size()

    fig = pl.figure(figsize = fig_size)
    MatPlotParams = {'xtick.major.pad' :0, 'ytick.major.pad' :0,'xtick.minor.pad' :0, 'ytick.minor.pad' :0}
    rcParams.update(MatPlotParams)
    pticks = pub_plots(xmaj = 10, xmin = 5, xstr = '%d', ymaj = 10, ymin = 5, ystr = '%d')
    equal_margins()
    data_mask = load_image('./mask_ims/M_r_%08d_r_stamp.fits' %gal, frame_num = 0)
    data_mask = resize_image(data_mask, hrad)
    make_panel(data_mask, color = cm.gray_r, zmin = 0, zmax =1 )
    ax = pl.gca()
    pticks.set_plot(pl.gca())
    ax.set_xticks([])
    ax.set_yticks([])
    pl.savefig('./%08d_mask.eps' %gal, bbox_inches = 'tight')
    pl.close('all')
    
    fig = pl.figure(figsize = fig_size)
    MatPlotParams = {'xtick.major.pad' :0, 'ytick.major.pad' :0,'xtick.minor.pad' :0, 'ytick.minor.pad' :0}
    rcParams.update(MatPlotParams)
    pticks = pub_plots(xmaj = 10, xmin = 5, xstr = '%d', ymaj = 10, ymin = 5, ystr = '%d')
    equal_margins()
    data = load_image('./mask_ims/O_r_%08d_r_stamp.fits' %gal, frame_num = 2)
    data = resize_image(data, hrad)
    data = np.log10(data)
    zmin, zmax = make_panel(data, color = cm.gray_r)
    ax = pl.gca()
    pticks.set_plot(pl.gca())
    ax.set_xticks([])
    ax.set_yticks([])
    pl.savefig('./%08d_output.eps' %gal, bbox_inches = 'tight')
    pl.close('all')

    fig = pl.figure(figsize = fig_size)
    MatPlotParams = {'xtick.major.pad' :0, 'ytick.major.pad' :0,'xtick.minor.pad' :0, 'ytick.minor.pad' :0}
    rcParams.update(MatPlotParams)
    pticks = pub_plots(xmaj = 10, xmin = 5, xstr = '%d', ymaj = 10, ymin = 5, ystr = '%d')
    equal_margins()
    data = load_image('./mask_ims/O_r_%08d_r_stamp.fits' %gal, frame_num = 1)
    data = resize_image(data, hrad)
    data = np.log10(data)
    make_panel(data, color = cm.gray_r, zmin = zmin, zmax =zmax )
    ax = pl.gca()
    pticks.set_plot(pl.gca())
    ax.set_xticks([])
    ax.set_yticks([])
    pl.savefig('./%08d_input.eps' %gal, bbox_inches = 'tight')
    pl.close('all')    

    fig = pl.figure(figsize = fig_size)
    MatPlotParams = {'xtick.major.pad' :0, 'ytick.major.pad' :0,'xtick.minor.pad' :0, 'ytick.minor.pad' :0}
    rcParams.update(MatPlotParams)
    pticks = pub_plots(xmaj = 10, xmin = 5, xstr = '%d', ymaj = 10, ymin = 5, ystr = '%d')
    equal_margins()
    data_mask = np.where(data_mask>0.5, np.nan, 1.0)
    data = load_image('./mask_ims/O_r_%08d_r_stamp.fits' %gal, frame_num = 3)+5
    data = resize_image(data, hrad)
    data = np.log10(data)
    data = data*data_mask
    make_panel(data, color = cm.gray_r)
    ax = pl.gca()
    pticks.set_plot(pl.gca())
    ax.set_xticks([])
    ax.set_yticks([])
    pl.savefig('./%08d_residual.eps' %gal, bbox_inches = 'tight')
    pl.close('all')
