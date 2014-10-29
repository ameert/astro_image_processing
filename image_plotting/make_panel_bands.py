import pyfits as pf
import pylab as pl
import numpy as np
from pylab import cm
from astro_image_processing.MatplotRc import *
from astro_image_processing.mysql import *
from pylab import rcParams
from matplotlib import rc

rc('text', usetex=True)
fsize = 9

cursor = mysql_connect('catalog','pymorph','pymorph','')

def resize_image(image, rad_pix):
    center = np.array(image.shape, dtype = int)/2
    edges = [np.max([center[0]- rad_pix*6, 0]), np.min([center[0]+rad_pix*6, image.shape[0]]), 
             np.max([center[1]- rad_pix*6, 0]), np.min([center[1]+rad_pix*6, image.shape[1]])] 

    new_image = image[edges[0]:edges[1], edges[2]:edges[3]]
    print edges
    return new_image

def equal_margins():
    pl.subplots_adjust(left = 0.05,  # the left side of the subplots of the figure
                          right = 0.95,    # the right side of the subplots of the figure
                          bottom = 0.05,   # the bottom of the subplots of the figure
                          top = 0.95,      # the top of the subplots of the figure
                          wspace = 0.0,   # the amount of width reserved for blank space between subplots
                          hspace = 0.0)   # the amount of height reserved for white space between subplots
    return

def load_image(filename, frame_num = 0):
    infile = pf.open(filename)
    data = infile[frame_num].data
    infile.close()
    return data

def make_panel(image, pticks, color=cm.gray, zmin = None, zmax = None, pix_sz = 0.396):
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


def do_band(gal, band, pos):
    cmd = 'select a.objid, a.petroR50_{band}, a.petromag_{band}-a.extinction_{band}, a.petroR50_r/0.396, b.BT, b.m_tot-a.extinction_{band}, m.probaE  from {band}_band_serexp as b, CAST as a, M2010 as m where a.galcount = m.galcount and a.galcount = b.galcount and a.galcount = {galcount};'.format(band=band, galcount=gal)
    print cmd
    objid, petrorad, petromag, hrad,BT, mag_tot, probaE = cursor.get_data(cmd)
    objid = objid[0]
    petromag = petromag[0]
    petrorad = petrorad[0]
    hrad = hrad[0]
    BT = BT[0]
    mag_tot = mag_tot[0]
    probaE = probaE[0]


    fig.add_subplot(1,3,pos)
    pticks = pub_plots(xmaj = 10, xmin = 5, xstr = '%d', ymaj = 10, ymin = 5, ystr = '%d')
    MatPlotParams = {'xtick.major.pad' :10, 'ytick.major.pad' :10,'xtick.minor.pad' :10, 'ytick.minor.pad' :10, 'axes.labelsize': 8, 'xtick.labelsize': 8, 'ytick.labelsize': 8}
    rcParams.update(MatPlotParams)
    data = load_image('/media/SDSS2/fit_catalog/data/{band}/{folder}/{galcount}_{band}_stamp.fits'.format(band=band, galcount='%08d' %gal, folder = '%04d' %((gal-1)/250 +1)))
    data = resize_image(data, hrad)
    data = np.log10(data)
    zmin, zmax = make_panel(data, pticks, color = cm.gray_r, zmin=2.0*np.nanmin(data)-np.percentile(np.extract(np.isnan(data)==0,data), 95.0))
    pl.title('{band}-band'.format(band=band),fontsize=12)
    ax = pl.gca()
    pl.text(0.05, 0.9, 'm$_{petro}$=%3.1f' %(petromag), 
            fontsize=fsize, 
            horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes)
    pl.text(0.95, 0.9, 'r$_{petro}$=%4.2f"' %(petrorad), 
            fontsize=fsize, 
            horizontalalignment='right', verticalalignment='center',
            transform=ax.transAxes)
    pl.text(0.05, 0.1, 'galnum=%s' %gal, fontsize=fsize, 
            horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes)
    pl.text(0.95, 0.1, 'P(Early)=%03.2f' %(probaE), 
            fontsize=fsize, 
            horizontalalignment='right', verticalalignment='center',
            transform=ax.transAxes)
   
    return

etype = 'early'
all_gals = {'early': [21399 ,    57356 ,    107851 ,   
                      185809 ,   193875 , 257306 ,   260211 ,   
                      267820 ,    470073 ,   
                      519927 ,   545973 ,   589415],
            
            'late':[ 27176 ,    47251 ,   131431 ,   175674 ,   177112 ,   
                     411116 ,   509289 ,   514868 ,   553195 ,   
                     560684 ,   622001 ,   648782],

            'mid':[ 23030 ,    35210 ,   113000 ,   136072 ,      
                    263873 ,   264133 ,   276310 ,   371022 ,   531628 ,   
                    548130 ,    628585 ,   637561]
            }


for gal in all_gals[etype]:

    fig_size = get_fig_size(fullwidth=True)
    fig_size[1] = 3.0

    fig = pl.figure(figsize = fig_size)
    MatPlotParams = {'xtick.major.pad' :0, 'ytick.major.pad' :0,'xtick.minor.pad' :0, 'ytick.minor.pad' :0, 'axes.labelsize': 14, 'xtick.labelsize': 12, 'ytick.labelsize': 12}
    rcParams.update(MatPlotParams)
    equal_margins()

    do_band(gal, 'g', 1)
    do_band(gal, 'r', 2)
    do_band(gal, 'i', 3)
    

    pl.savefig('./%08d_band_strip_%s.eps' %(gal, etype), bbox_inches = 'tight')
    pl.close('all')
    
