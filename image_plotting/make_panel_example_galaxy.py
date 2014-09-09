import pyfits as pf
import pylab as pl
import numpy as np
from pylab import cm
from astro_image_processing.MatplotRc import *
from astro_image_processing.mysql import *
from pylab import rcParams
from matplotlib import rc

rc('text', usetex=True)
fsize = 7

cursor = mysql_connect('catalog','pymorph','pymorph','')

def resize_image(image, rad_pix):
    center = np.array(image.shape, dtype = int)/2
    edges = [np.max([center[0]- rad_pix*6, 0]), np.min([center[0]+rad_pix*6, image.shape[0]]), 
             np.max([center[1]- rad_pix*6, 0]), np.min([center[1]+rad_pix*6, image.shape[1]])] 

    new_image = image[edges[0]:edges[1], edges[2]:edges[3]]
    print edges
    return new_image

def equal_margins():
    pl.subplots_adjust(left = 0.1,  # the left side of the subplots of the figure
                          right = 0.97,    # the right side of the subplots of the figure
                          bottom = 0.05,   # the bottom of the subplots of the figure
                          top = 0.95,      # the top of the subplots of the figure
                          wspace = 0.1,   # the amount of width reserved for blank space between subplots
                          hspace = 0.1)   # the amount of height reserved for white space between subplots
    return

def load_image(filename, frame_num = 0):
    infile = pf.open(filename)
    data = infile[frame_num].data
    infile.close()
    return data

def make_panel(image, color=cm.gray, zmin = None, zmax = None, pix_sz = 0.396):
    imshape_arcsec = np.array(image.shape)*pix_sz

    if zmin == None:
        zmin = np.nanmin(image)
    if zmax == None:
        zmax = np.nanmax(image)

    pl.imshow(image, cmap=color, interpolation = 'nearest', extent = (-imshape_arcsec[1]/2, imshape_arcsec[1]/2,-imshape_arcsec[1]/2, imshape_arcsec[1]/2), origin = 'lower')
    pl.clim(zmin,zmax)
    ax = pl.gca()
    pticks.set_plot(pl.gca())
    ax.set_xticks([])
    ax.set_yticks([])
    print zmin, zmax
    return zmin, zmax

gals = [

    [6833, 'No Flags'],  
    [7780, 'No Flags'],
    [35521, 'No Flags'],  
    [408774, 'No Flags'],
    [19384,'No Flags'],
    [86055, 'Good Ser, Good Exp (Some Flags)'],  
    [163409, 'Good Ser, Good Exp (Some Flags)']
]
 

for gal in gals:

    fig_size = get_fig_size(fullwidth=True)
    fig_size[1] = 3.0

    fig = pl.figure(figsize = fig_size)
    MatPlotParams = {'xtick.major.pad' :0, 'ytick.major.pad' :0,'xtick.minor.pad' :0, 'ytick.minor.pad' :0, 'axes.labelsize': 14, 'xtick.labelsize': 12, 'ytick.labelsize': 12}
    rcParams.update(MatPlotParams)
    equal_margins()

    cmd = 'select a.objid, a.petroR50_r, a.petromag_r-a.extinction_r, b.Hrad_corr/0.396, b.BT, b.m_tot-a.extinction_r from r_band_serexp as b, CAST as a where a.galcount = b.galcount and a.galcount = %d;' %gal[0]
    objid, petrorad, petromag, hrad,BT, mag_tot = cursor.get_data(cmd)
    objid = objid[0]
    petromag = petromag[0]
    petrorad = petrorad[0]
    hrad = hrad[0]
    BT = BT[0]
    mag_tot = mag_tot[0]

    mask_data = load_image('./data/M_r_%08d_r_stamp.fits' %gal[0], frame_num = 0)
    mask_data = resize_image(mask_data, hrad)
    
    if 1:
        fig.add_subplot(1,4,3)
        pticks = pub_plots(xmaj = 10, xmin = 5, xstr = '%d', ymaj = 10, ymin = 5, ystr = '%d')
        MatPlotParams = {'xtick.major.pad' :10, 'ytick.major.pad' :10,'xtick.minor.pad' :10, 'ytick.minor.pad' :10, 'axes.labelsize': 8, 'xtick.labelsize': 8, 'ytick.labelsize': 8}
        rcParams.update(MatPlotParams)
        data = load_image('./data/O_r_%08d_r_stamp_serexp.fits' %gal[0], frame_num = 2)
        data = resize_image(data, hrad)
        data = np.log10(data)
        zmin, zmax = make_panel(data, color = cm.gray_r, zmin=2.0*np.nanmin(data)-np.percentile(np.extract(np.isnan(data)==0,data), 95.0))
        pl.title('model',fontsize=12)
        ax = pl.gca()
        pl.text(0.05, 0.9, 'm$_{tot}$=%3.1f' %mag_tot, fontsize=fsize, 
                horizontalalignment='left', verticalalignment='center',
                transform=ax.transAxes)
        pl.text(0.95, 0.9, 'r$_{hl}$=%4.2f"' %(hrad*0.396), fontsize=fsize, 
                horizontalalignment='right', verticalalignment='center',
                transform=ax.transAxes)
        pl.text(0.05, 0.1, 'B/T=%03.2f' %BT, fontsize=fsize, 
                horizontalalignment='left', verticalalignment='center',
                transform=ax.transAxes)
    if 1:

        fig.add_subplot(1,4,2)
        pticks = pub_plots(xmaj = 10, xmin = 5, xstr = '%d', ymaj = 10, ymin = 5, ystr = '%d')
        MatPlotParams = {'xtick.major.pad' :10, 'ytick.major.pad' :10,'xtick.minor.pad' :10, 'ytick.minor.pad' :10, 'axes.labelsize': 8, 'xtick.labelsize': 8, 'ytick.labelsize': 8}
        rcParams.update(MatPlotParams)
        make_panel(mask_data, color = cm.gray_r, zmin=0, zmax=1)
        pl.title('mask',fontsize=12)

    if 1:
        fig.add_subplot(1,4,1)
        pticks = pub_plots(xmaj = 10, xmin = 5, xstr = '%d', ymaj = 10, ymin = 5, ystr = '%d')
        MatPlotParams = {'xtick.major.pad' :10, 'ytick.major.pad' :10,'xtick.minor.pad' :10, 'ytick.minor.pad' :10, 'axes.labelsize': 8, 'xtick.labelsize': 8, 'ytick.labelsize': 8}
        rcParams.update(MatPlotParams)
        data = load_image('./data/O_r_%08d_r_stamp_serexp.fits' %gal[0], frame_num = 1)
        data = resize_image(data, hrad)
        data = np.log10(data)
        make_panel(data, color = cm.gray_r, zmin = zmin, zmax =zmax )
        pl.title('data', fontsize=12)
        ax = pl.gca()
        pl.text(0.05, 0.9, 'm$_{petro}$=%3.1f' %petromag, fontsize=fsize, 
                horizontalalignment='left', verticalalignment='center',
                transform=ax.transAxes)
        pl.text(0.95, 0.9, 'r$_{petro}$=%4.2f"' %petrorad, fontsize=fsize, 
                horizontalalignment='right', verticalalignment='center',
                transform=ax.transAxes)
        pl.text(0.05, 0.1, 'galnum=%s' %gal[0], fontsize=fsize, 
                horizontalalignment='left', verticalalignment='center',
                transform=ax.transAxes)

    if 1:
        fig.add_subplot(1,4,4)
        pticks = pub_plots(xmaj = 10, xmin = 5, xstr = '%d', ymaj = 10, ymin = 5, ystr = '%d')
        MatPlotParams = {'xtick.major.pad' :10, 'ytick.major.pad' :10,'xtick.minor.pad' :10, 'ytick.minor.pad' :10, 'axes.labelsize': 8, 'xtick.labelsize': 8, 'ytick.labelsize': 8}
        rcParams.update(MatPlotParams)
        data = load_image('./data/O_r_%08d_r_stamp_serexp.fits' %gal[0], frame_num = 3)+5
        data = resize_image(data, hrad)
        data = np.log10(data)
        data = np.where(mask_data>0.5, np.nan, data)
        make_panel(data, color = cm.gray_r)
        pl.title('masked residual',fontsize=12)
        equal_margins()
        #ax = pl.gca()
        #ax.set_aspect((pl.xlim()[0]-pl.xlim()[1])/(pl.ylim()[1]-pl.ylim()[0]))
    #pl.suptitle( gal[1], fontsize=12)
        
    #pl.show()

    pl.savefig('./%08d_strip_example.eps' %gal[0], bbox_inches = 'tight')
    pl.close('all')
