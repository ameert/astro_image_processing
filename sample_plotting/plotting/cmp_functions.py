import numpy as np
import pylab as pl
from scipy import ndimage
from astro_image_processing.MatplotRc import *
import matplotlib
import matplotlib.colors as col
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import sys
from optparse import OptionParser, OptParseError

from astro_image_processing.statistics.bin_stats import *

def get_options():
    usage = 'program OPTIONS'
    desc = 'makes comparison plots'
    parser = OptionParser(usage=usage, description = desc)
    parser.add_option("-t","--tablestem", action="store", type="string",
                      dest="tablestem", default = None,
                      help="table to be matched against")
    parser.add_option("-m","--model", action="store", type="string",
                      dest="model", default = None,
                      help="model being matched")
    parser.add_option("-b","--band", action="store", type="string",
                      dest="band", default = 'r',
                      help="band being compared")
    parser.add_option("-x","--xchoice", action="store", type="string",
                      dest="xchoice", 
                      default = None,
                      help="pymorph x value for plot")
    parser.add_option("-y","--ychoice", action="store", type="string",
                      dest="ychoice", 
                      default = None,
                      help="y value for plot")
    
    parser.add_option("-f","--FLAGS", action="store_true", 
                      dest="use_flags", default=False,
                      help="cut galaxies based on flags")

    parser.add_option("-z","--FMODEL", action="store", type="string", 
                      dest="flagmodel", default='serexp',
                      help="model to use for flags")

    parser.add_option("-c","--twocom", action="store_true", 
                      dest="use_twocom", default=False,
                      help="limit comparison to good twocom models")
    
    parser.add_option("--xl", action="store", type="string", 
                      dest="xlims", default=None,
                      help="xlimit override")
    parser.add_option("--yl", action="store", type="string", 
                      dest="ylims", default=None,
                      help="ylimit override")

    parser.add_option("--xlabel", action="store", type="string", 
                      dest="xlab", default=None,
                      help="xlabel override")
    parser.add_option("--ylabel", action="store", type="string", 
                      dest="ylab", default=None,
                      help="ylabel override")
    # parses command line aguments for pymorph
    (options, args) = parser.parse_args()

    key_x = get_key(options.xchoice)
    key_y = get_key(options.ychoice)

    try:
        options.xlims = (float(options.xlims.split(',')[0]),
                         float(options.xlims.split(',')[1]))
    except:
        options.xlims = None
    try:
        options.ylims = (float(options.ylims.split(',')[0]),
                         float(options.ylims.split(',')[1]))
    except:
        options.ylims = None


    return options.tablestem, options.model, options.band, options.xchoice, options.ychoice, key_x, key_y, options.use_flags, options.flagmodel, options.use_twocom, options.xlims, options.ylims

def get_options_main():
    usage = 'program OPTIONS'
    desc = 'makes comparison plots'
    parser = OptionParser(usage=usage, description = desc)
    parser.add_option("-1","--table1", action="store", type="string",
                      dest="table1", default = 'band',
                      help="table1 to be matched against")
    parser.add_option("-2","--table2", action="store", type="string",
                      dest="table2", default = 'sdss',
                      help="table2 to be matched against")
    parser.add_option("-m","--model1", action="store", type="string",
                      dest="model1", default = None,
                      help="model being matched")
    parser.add_option("-n","--model2", action="store", type="string",
                      dest="model2", default = None,
                      help="model being matched")
    parser.add_option("-b","--band1", action="store", type="string",
                      dest="band1", default = 'r',
                      help="first band being compared")
    parser.add_option("-d","--band2", action="store", type="string",
                      dest="band2", default = 'r',
                      help="second band being compared")
    parser.add_option("-x","--xchoice", action="store", type="string",
                      dest="xchoice", 
                      default = None,
                      help="pymorph x value for plot")
    parser.add_option("-y","--ychoice", action="store", type="string",
                      dest="ychoice", 
                      default = None,
                      help="y value for plot")
    parser.add_option("-p","--postfix", action="store", type="string",
                      dest="postfix", 
                      default = '',
                      help="additional string to put in output name")
    parser.add_option("-f","--FLAGS", action="store_true", 
                      dest="use_flags", default=False,
                      help="cut galaxies based on flags")
    parser.add_option("-z","--FMODEL", action="store", type="string", 
                      dest="flagmodel", default='serexp',
                      help="model to use for flags")
    parser.add_option("-c","--twocom", action="store_true", 
                      dest="use_twocom", default=False,
                      help="limit comparison to good twocom models")
    parser.add_option("--add_tables", action="store", type="string", 
                      dest="add_tables", default='',
                      help="any additional tables to include (must start with ,)")

    parser.add_option("--conditions", action="store", type="string", 
                      dest="conditions", default='',
                      help="any additional condtions to include (must start with and)")
    parser.add_option("-u","--upper-dense", action="store", type="float",
                      dest="upper_dense", 
                      default = 1000,
                      help="y value for plot")

    parser.add_option("--title", action="store", type="string", 
                      dest="title", default='',
                      help="plot title")

    parser.add_option("--xl", action="store", type="string", 
                      dest="xlims", default=None,
                      help="xlimit override")
    parser.add_option("--yl", action="store", type="string", 
                      dest="ylims", default=None,
                      help="ylimit override")

    parser.add_option("--xtM", action="store", type="float", 
                      dest="xtmaj", default=None,
                      help="xtickmajor override")
    parser.add_option("--xtm", action="store", type="float", 
                      dest="xtmin", default=None,
                      help="xtickminor override")
    parser.add_option("--xtl", action="store", type="string", 
                      dest="xtlab", default=None,
                      help="xticklabel override")

    parser.add_option("--ytM", action="store", type="float", 
                      dest="ytmaj", default=None,
                      help="ytickmajor override")
    parser.add_option("--ytm", action="store", type="float", 
                      dest="ytmin", default=None,
                      help="ytickminor override")
    parser.add_option("--ytl", action="store", type="string", 
                      dest="ytlab", default=None,
                      help="yticklabel override")
    parser.add_option("--xlabel", action="store", type="string", 
                      dest="xlab", default=None,
                      help="xlabel override")
    parser.add_option("--ylabel", action="store", type="string", 
                      dest="ylab", default=None,
                      help="ylabel override")

    parser.add_option("--bins", action="store", type="string", 
                      dest="bins", default=None,
                      help="bins override")


    # parses command line aguments for pymorph
    (options, args) = parser.parse_args()

    options.key_x = get_key(options.xchoice)
    options.key_y = get_key(options.ychoice)

    try:
        options.bins = np.arange(float(options.bins.split(',')[0]),
                        float(options.bins.split(',')[1]),
                        float(options.bins.split(',')[2]))
    except:
        options.bins = None

    try:
        options.xlims = (float(options.xlims.split(',')[0]),
                         float(options.xlims.split(',')[1]))
    except:
        options.xlims = None
    try:
        options.ylims = (float(options.ylims.split(',')[0]),
                         float(options.ylims.split(',')[1]))
    except:
        options.ylims = None

    return vars(options)

def get_key(choice):
    """converts the axis choice to the common dictionary keys used to define axis labels, plot ranges, bin sizes, etc."""
    if choice in ['mtot', 'mtot_app', 'mbulge', 'mdisk','petromag']:
        key_choice = 'mag'
    elif choice in ['mtot_abs', 'petromag_abs', 'mbulge_abs', 'mdisk_abs']:
        key_choice = 'absmag'
    elif choice in ['hrad','hrad_psf','rbulge','rdisk', 'petrorad']:
        key_choice = 'rad'
    elif choice in ['n', 'nbulge']:
        key_choice = 'n'
    elif choice in ['pabulge', 'padisk']:
        key_choice = 'pa' 
    elif choice in ['babulge', 'badisk', 'batot']:
        key_choice = 'ba' 
    else:
        key_choice = choice
    
    return key_choice

class outlier_fig():
    def __init__(self, figsize = None):
        if figsize == None:
            self.figsize = get_fig_size()
        else:
            self.figsize= figsize
        print "figsize ", self.figsize
        self.fig = pl.figure(figsize = self.figsize)
        pl.subplots_adjust(left = 0.25,
                           right = 0.96,
                           bottom = 0.25,
                           top = 0.9,    
                           wspace = 0.20,
                           hspace = 0.15)
        self.bins = (60,60)
        self.denselims = [1,1000]
        self.minval = 5
        self.nsamples = 2
        return
    
    def set_bootsamples(self, bootnum):
        self.nsample = bootnum
        return

    def setbins(self, bins):
        self.bins = bins
        return

    def setdenselims(self, dlow, dhigh):
        self.denselims = [dlow, dhigh]
        return

    def setminval(self, minval):
        self.minval = minval
        return

    def set_ticks(self, xmaj, xmin, xstr, ymaj, ymin, ystr):
        self.ticks = pub_plots(xmaj, xmin, xstr, ymaj, ymin, ystr)
        return

    def makeplot(self,xdat,ydat, xlim,ylim):
        self.xdat = xdat
        self.ydat = ydat
        H, xedges, yedges = plot_dense(xdat,ydat, '' ,'' ,xlim,ylim,self.bins,
                                       self.denselims[0],self.denselims[1],
                                       self.minval, self.figsize,scale = 1.0)

        #plot_low_scat(xdat,ydat, H, xedges, yedges, self.minval)

        ax = pl.gca()
        self.ticks.set_plot(ax)
        return
    
    def bin_it(self, bins, binlow, binhigh, weight = None, err_type = 'median'):
        if weight == None:
            self.barbin = bin_stats(self.xdat, self.ydat,bins,
              binlow, binhigh, err_type = err_type, nsamples = self.nsamples)
        else:
            self.barbin = bin_stats(self.xdat, self.ydat,bins,
              binlow, binhigh, weight = weight, err_type = err_type,
                                    nsamples = self.nsamples)
        return
    
    def add_bars(self, ebar_color,marker = 'o', **kwargs): 
        self.barbin.plot_ebar('median', 'med95ci', marker = marker, 
                              color = ebar_color, ms = 4, 
                              markerfacecolor = ebar_color,  
                              ecolor = ebar_color, capsize = 5, 
                              linestyle = 'None', elinewidth = 2, 
                              barsabove=True, zorder = 10)
        self.barbin.lay_bounds(sigma_choice = [68], zorder = 9, color='b')
        return

    def savefig(self, figname):
        try:
            self.barbin.write_stats(figname.split('.')[0]+'.tbl')
        except AttributeError:
            pass

        pl.savefig(figname)
        pl.clf()
        pl.close('all')
        return

def plot_dense(x_dat, y_dat, xtext, ytext, xlim, ylim, bin_num, dense_low, 
               dense_high, color_start, fig_size, colorbar = 0, line = None, 
               scale = False):
    
    if xlim[-1]<xlim[0]:
        xhist = xlim[::-1]
    else:
        xhist = xlim
    if ylim[-1]<ylim[0]:
        yhist = ylim[::-1]
    else:
        yhist = ylim

    H, xedges, yedges = np.histogram2d(x_dat, y_dat, range = [xhist,yhist], 
                                       bins = bin_num)

    Hpic = ndimage.rotate(H, 90.0)
    if scale=='log':
        Hpic = np.log10(Hpic)
    elif isinstance(scale, (long, int, float)):
        Hpic = Hpic*scale

    extent = [xlim[0], xlim[1], ylim[0], ylim[1]]
    #Hpic = H
    #extent = [ylim[0], ylim[1], xlim[1], xlim[0]]

    hmax = np.max(Hpic)
    
    #Hpic=Hpic/float(len(x_dat))
    
    if scale=='log':
        img = pl.imshow(Hpic,  interpolation='nearest', extent = extent,
                        vmax = np.log10(dense_high),vmin = np.log10(dense_low))
    else:
        img = pl.imshow(Hpic,  interpolation='nearest', extent = extent,
                        vmax = dense_high, vmin = dense_low)


    #print "color start ", float(color_start)/dense_high
    #print float(color_start)
    #print hmax
    #print dense_high
              
    if scale=='log':
        color_scale_start = np.log(float(color_start))/np.log(dense_high)
    else:
        color_scale_start = float(color_start)/dense_high

    cdict = {'red': ((0.0, 1.0, 1.0),
                     (color_scale_start, 1.0,0.6),
                     (1.0, 0.0, 0.0)),
             'green': ((0.0, 1.0, 1.0),
                       (color_scale_start, 1.0,0.6),
                       (1.0, 0.0, 0.0)),
             'blue': ((0.0, 1.0, 1.0),
                      (color_scale_start, 1.0,0.6),
                      (1.0, 0.0, 0.0))}

    my_cmap = col.LinearSegmentedColormap('my_colormap',cdict,8192)

    #img.set_cmap(pl.cm.gray_r)
    img.set_cmap(my_cmap)
    
    if colorbar:
        pl.colorbar(img, shrink = .90)
    
    pl.xlabel(xtext)
    pl.ylabel(ytext)
    pl.xlim((extent[0],extent[1]))
    pl.ylim((extent[2],extent[3]))

    ax = pl.gca()
    forceAspect(ax, aspect = fig_size[0]/fig_size[1] +0.25)
    #forceAspect(ax, aspect = 1)
    
    return H, xedges, yedges

def forceAspect(ax,aspect=1):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)
    return


def digitize_2D(xdat, ydat, xedges, yedges):
    xbins = np.digitize(xdat, xedges)-1
    ybins = np.digitize(ydat, yedges)-1
    return zip(xbins, ybins)
    
def plot_low_scat(xdat, ydat, H, xedges, yedges, minval):
    binpos = digitize_2D(xdat, ydat, xedges, yedges)

    hvals = []
    for pos in binpos:
        try:
            hvals.append(H[pos])
        except IndexError:
            hvals.append(9999)
    
    hvals=np.array(hvals)

    xscat = np.extract(hvals <= minval, xdat)
    yscat = np.extract(hvals <= minval, ydat)

    if len(xscat) >2:
        pl.scatter(xscat,yscat, s=1, c = 'k', edgecolor='none')

    return
