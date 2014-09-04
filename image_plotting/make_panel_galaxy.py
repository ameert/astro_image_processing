import pyfits as pf
import pylab as pl
import numpy as np
from pylab import cm
from astro_image_processing.MatplotRc import *
from astro_image_processing.mysql import *
from pylab import rcParams
from matplotlib import rc

rc('text', usetex=True)

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
    
    return zmin, zmax

gals = [
#[391640, r'Centering'],
#[578903, r'Parallel Components'],
#[618376, r'No \texttt{Ser} Likely'],
#[85253, r'No \texttt{Exp} Likely'],
#[21378, r'\texttt{Ser} Contaminated'],
#[37358, r'\texttt{Ser} is Sky'],
#[206144, r'High e \texttt{Ser}'],
#[342358, r'\texttt{Ser} PA Problem'],
#[107405, r'\texttt{Ser} Fitting Outer'],
#[122333 , r'\texttt{Ser} is Disk'],
#[207915, r'\texttt{Ser} Dominates Always'],
#[42921, r'Low Sersic index \texttt{Ser}'],
#[15535, r'\texttt{Exp} is Sky'],
#[14600, r'\texttt{Exp} Contaminated'],
#[580870, r'High e \texttt{Exp}'],
#[120056, r'\texttt{Exp} PA Problem'],
#[284108, r'\texttt{Exp} Fitting Inner'],
#[450412, r'\texttt{Exp} Dominates Always']
#]
    [246717, r"No \texttt{Exp} Component, n$_{\texttt{Ser}}>=$2"],
    [167097, r"No \texttt{Exp} Component, n$_{\texttt{Ser}}>=$2"],

    [557050, r"\texttt{Ser} Dominates Always, n$_{\texttt{Ser}}>=$2"],
    [255297, r"\texttt{Ser} Dominates Always, n$_{\texttt{Ser}}>=$2"],

    [12474,r"No \texttt{Ser} Component"],
    [223566,r"No \texttt{Ser} Component"],

    [84055,r"No \texttt{Exp}, n$_{\texttt{Ser}}<$2, Flip Components"],
    [355,r"No \texttt{Exp}, n$_{\texttt{Ser}}<$2, Flip Components"],

    [135981 ,r"\texttt{Ser} Dominates Always, n$_{\texttt{Ser}}<$2"],
    [413052 ,r"\texttt{Ser} Dominates Always, n$_{\texttt{Ser}}<$2"],

    [656426,r"\texttt{Exp} Dominates Always"],
    [157120,r"\texttt{Exp} Dominates Always"],

    [543174 ,r"Parallel Components"],
    [642141,r"Parallel Components"],

    
    [182763,r"\texttt{Ser} Outer Only"],
    [532728,r"\texttt{Ser} Outer Only"],

    [520456,r"\texttt{Exp} Inner Only"],
    [541105,r"\texttt{Exp} Inner Only"],

    [117380,r"Good \texttt{Ser}, Bad \texttt{Exp}, B/T$>=$0.5"],
    [242460,r"Good \texttt{Ser}, Bad \texttt{Exp}, B/T$>=$0.5"],

    [554147,r"Bad \texttt{Ser}, Good \texttt{Exp}, B/T$<$0.5"],
    [22342,r"Bad \texttt{Ser}, Good \texttt{Exp}, B/T$<$0.5"],

    [35521, 'No Flags'],  
    [408774, 'No Flags'],

    [86055, 'Good Ser, Good Exp (Some Flags)'],  
    [163409, 'Good Ser, Good Exp (Some Flags)'],      

    [48927,r"Flip Components"],  
    [645918,r"Flip Components"],

    [670464,r"Bulge is Point"],
    [642128,r"Bulge is Point"],

]


for gal in gals[7:8]:

    fig_size = (6.0,6.0)
    fig = pl.figure(figsize = fig_size)
    MatPlotParams = {'xtick.major.pad' :0, 'ytick.major.pad' :0,'xtick.minor.pad' :0, 'ytick.minor.pad' :0, 'axes.labelsize': 14, 'xtick.labelsize': 12, 'ytick.labelsize': 12}
    rcParams.update(MatPlotParams)
    equal_margins()

    cmd = 'select a.objid, a.petroR50_r, a.petromag_r, b.Hrad_corr/0.396, b.BT, b.m_tot from r_band_serexp as b, CAST as a where a.galcount = b.galcount and a.galcount = %d;' %gal[0]
    objid, petrorad, petromag, hrad,BT, mag_tot = cursor.get_data(cmd)
    objid = objid[0]
    petromag = petromag[0]
    petrorad = petrorad[0]
    hrad = hrad[0]
    BT = BT[0]
    mag_tot = mag_tot[0]

    mask_data = load_image('./data/EM_%08d_r_stamp_plotting.fits' %gal[0], frame_num = 0)
    mask_data = resize_image(mask_data, hrad)
    
    pl.subplot(2,2,1)
    pticks = pub_plots(xmaj = 10, xmin = 5, xstr = '%d', ymaj = 10, ymin = 5, ystr = '%d')
    MatPlotParams = {'xtick.major.pad' :10, 'ytick.major.pad' :10,'xtick.minor.pad' :10, 'ytick.minor.pad' :10, 'axes.labelsize': 8, 'xtick.labelsize': 8, 'ytick.labelsize': 8}
    rcParams.update(MatPlotParams)
    data = load_image('./data/O_r_%08d_r_stamp_serexp.fits' %gal[0], frame_num = 2)
    data = resize_image(data, hrad)
    data = np.log10(data)
    zmin, zmax = make_panel(data, color = cm.gray_r)
    pl.title('model',fontsize=12)
    ax = pl.gca()
    pl.text(0.05, 0.9, 'm$_{tot}$=%3.1f' %mag_tot, fontsize=12, 
            horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes)
    pl.text(0.95, 0.9, 'r$_{hl}$=%4.2f"' %(hrad*0.396), fontsize=12, 
            horizontalalignment='right', verticalalignment='center',
            transform=ax.transAxes)
    pl.text(0.05, 0.1, 'B/T=%03.2f' %BT, fontsize=12, 
            horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes)


    pl.subplot(2,2,2)
    pticks = pub_plots(xmaj = 10, xmin = 5, xstr = '%d', ymaj = 10, ymin = 5, ystr = '%d')
    MatPlotParams = {'xtick.major.pad' :10, 'ytick.major.pad' :10,'xtick.minor.pad' :10, 'ytick.minor.pad' :10, 'axes.labelsize': 8, 'xtick.labelsize': 8, 'ytick.labelsize': 8}
    rcParams.update(MatPlotParams)
    data = load_image('./data/O_r_%08d_r_stamp_serexp.fits' %gal[0], frame_num = 1)
    data = resize_image(data, hrad)
    data = np.log10(data)
    make_panel(data, color = cm.gray_r, zmin = zmin, zmax =zmax )
    pl.title('data', fontsize=12)
    ax = pl.gca()
    pl.text(0.05, 0.9, 'm$_{petro}$=%3.1f' %petromag, fontsize=12, 
            horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes)
    pl.text(0.95, 0.9, 'r$_{petro}$=%4.2f"' %petrorad, fontsize=12, 
            horizontalalignment='right', verticalalignment='center',
            transform=ax.transAxes)
    pl.text(0.05, 0.1, 'galnum=%s' %gal[0], fontsize=12, 
            horizontalalignment='left', verticalalignment='center',
            transform=ax.transAxes)



    pl.subplot(2,2,4)
    pticks = pub_plots(xmaj = 10, xmin = 5, xstr = '%d', ymaj = 10, ymin = 5, ystr = '%d')
    MatPlotParams = {'xtick.major.pad' :10, 'ytick.major.pad' :10,'xtick.minor.pad' :10, 'ytick.minor.pad' :10, 'axes.labelsize': 8, 'xtick.labelsize': 8, 'ytick.labelsize': 8}
    rcParams.update(MatPlotParams)
    data = load_image('./data/O_r_%08d_r_stamp_serexp.fits' %gal[0], frame_num = 3)+5
    data = resize_image(data, hrad)
    data = np.log10(data)
    data = np.where(mask_data<0.5, np.nan, data)
    make_panel(data, color = cm.gray_r)
    pl.title('masked residual',fontsize=12)

    ax = pl.subplot(2,2,3)#, aspect = 5.0/8.0)
    MatPlotParams = {'xtick.major.pad' :10, 'ytick.major.pad' :10,'xtick.minor.pad' :10, 'ytick.minor.pad' :10, 'axes.labelsize': 8, 'xtick.labelsize': 8, 'ytick.labelsize': 8}
    rcParams.update(MatPlotParams)

    inrad, inmag, inmagerr = np.loadtxt('./data/r_%08d_r_stamp_mag_arc_profile_serexp.txt' %gal[0], unpack=True)
    fitrad, fitmag, fitmagerr = np.loadtxt('./data/r_%08d_r_stamp_mag_arc_model_profile_serexp.txt' %gal[0], unpack=True)
    bfitrad, bfitmag, bfitmagerr = np.loadtxt('./data/r_%08d_r_stamp_model_bulge_mag_serexp.txt' %gal[0], unpack=True)
    dfitrad, dfitmag, dfitmagerr = np.loadtxt('./data/r_%08d_r_stamp_model_disk_mag_serexp.txt' %gal[0], unpack=True)

    pl.title('1D Profile', fontsize=12)
    pl.plot(fitrad, fitmag, 'b-')
    pl.plot(bfitrad, bfitmag, 'b--')
    pl.plot(dfitrad, dfitmag, 'b:')
    #pl.errorbar(inrad, inmag, inmagerr, fmt='', ecolor='#686868', linewidth=0,
    #            elinewidth=1, capsize=3,marker='o', ms=4, mfc='#686868')
    pl.plot(inrad, inmag, ls='', color='#686868', linewidth=0,
                marker='o', ms=4, mfc='#686868')
    pl.xlim(0.0,4.0*hrad*0.396)
    pl.ylim(27,19)
    pl.xlabel('r$_{hl}$')
    pl.ylabel('$\mu$')

    #pl.suptitle( gal[1], fontsize=12)
    equal_margins()
    ax.set_aspect((pl.xlim()[0]-pl.xlim()[1])/(pl.ylim()[1]-pl.ylim()[0]))
    pl.savefig('./%08d_strip.eps' %gal[0])#, bbox_inches = 'tight')
    pl.close('all')
    
