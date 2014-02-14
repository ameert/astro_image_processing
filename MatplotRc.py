from pylab import rcParams
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import pylab
import numpy as np

print 'importing Matplotlib rc'


class plot_dats:
    def __init__(self, xmajLocator, xmajFormatter, xminLocator, ymajLocator, ymajFormatter, yminLocator):
        self.xmajLocator=xmajLocator
        self.xmajFormatter=xmajFormatter
        self.xminLocator=xminLocator
        self.ymajLocator=ymajLocator
        self.ymajFormatter=ymajFormatter
        self.yminLocator=yminLocator
        return

    def set_plot(self, ax):
        ax.yaxis.set_major_locator(self.ymajLocator)
        ax.yaxis.set_major_formatter(self.ymajFormatter)
        ax.yaxis.set_minor_locator(self.yminLocator)
        
        ax.xaxis.set_major_locator(self.xmajLocator)
        ax.xaxis.set_major_formatter(self.xmajFormatter)
        ax.xaxis.set_minor_locator(self.xminLocator)

        return

def get_fig_size(fullwidth=0,fullheight=0):
 # Get this from LaTeX using \showthe\columnwidth and subtract 0.5 * \showthe\columnsep
    inches_per_pt = 1.0/72.27               # Convert pt to inches
    golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
    
    if fullwidth:
        fig_width_pt = 504.0  
    else:
        # I have hard-coded it for the paper
        fig_width_pt = 220.0-0.5*24.0
    
    fig_width = fig_width_pt*inches_per_pt  # width in inches
    
    if fullheight:
        fig_height = 8.
    else:
        fig_height =fig_width*golden_mean       # height in inches
    
    fig_size = [fig_width,fig_height]
    return fig_size

# this is the settings I use to make publication quality plots...
def pub_plots(xmaj = 5, xmin = 1, xstr = '%03.2f', ymaj = 5, ymin = 1, ystr = '%d'):
    MatPlotParams = {'axes.xaxis.labelpad': 40, 'axes.titlesize': 12, 'axes.linewidth' : 1.5, 'axes.labelsize': 14, 'xtick.labelsize': 12, 'ytick.labelsize': 12, 'xtick.major.size': 10, 'ytick.major.size' : 10, 'xtick.minor.size': 4, 'ytick.minor.size': 4, 'xtick.major.pad' : 8, 'ytick.major.pad' : 6}
    rcParams.update(MatPlotParams)
    
    xmajLocator   = MultipleLocator(xmaj)
    xmajFormatter = FormatStrFormatter(xstr)
    xminLocator   = MultipleLocator(xmin)
    
    ymajLocator   = MultipleLocator(ymaj)
    ymajFormatter = FormatStrFormatter(ystr)
    yminLocator   = MultipleLocator(ymin)
    
    data_holder = plot_dats(xmajLocator, xmajFormatter, xminLocator, ymajLocator,
                 ymajFormatter, yminLocator)
    return data_holder

def matrc1():
    MatPlotParams = {'axes.titlesize': 15, 'axes.linewidth' : 2.5, 'axes.labelsize': 12, 'xtick.labelsize': 10, 'ytick.labelsize': 10, 'xtick.major.size': 12, 'ytick.major.size' : 12, 'xtick.minor.size': 14, 'ytick.minor.size': 14, 'figure.figsize' : [10.0, 8.0], 'xtick.major.pad' : 8, 'ytick.major.pad' : 6}
    rcParams.update(MatPlotParams)

def matrc1color():
    MatPlotParams = {'axes.titlesize': 15, 'axes.linewidth' : 2.5, 'axes.labelsize': 14, 'xtick.labelsize': 20, 'ytick.labelsize': 20, 'xtick.major.size': 22, 'ytick.major.size' : 22, 'xtick.minor.size': 14, 'ytick.minor.size': 14, 'figure.figsize' : [10.0, 8.0], 'xtick.major.pad' : 8, 'ytick.major.pad' : 6}
    rcParams.update(MatPlotParams)

def matrc2():
    MatPlotParams = {'axes.titlesize': 12, 'axes.linewidth' : 1.0, 'axes.labelsize': 12, 'xtick.labelsize': 10, 'ytick.labelsize': 10, 'xtick.major.size': 12, 'ytick.major.size' : 12, 'xtick.minor.size': 10, 'ytick.minor.size': 10, 'figure.figsize' : [6.0, 10.0], 'xtick.major.pad' : 6, 'ytick.major.pad' : 4, 'figure.subplot.hspace' : 0.0}
    rcParams.update(MatPlotParams)


def matrc3():
    MatPlotParams = {'axes.titlesize': 15, 'axes.linewidth' : 2.5, 'axes.labelsize': 22, 'xtick.labelsize': 20, 'ytick.labelsize': 20, 'xtick.major.size': 22, 'ytick.major.size' : 22, 'xtick.minor.size': 14, 'ytick.minor.size': 14, 'figure.figsize' : [6.0, 18.0], 'xtick.major.pad' : 8, 'ytick.major.pad' : 6, 'figure.subplot.hspace' : 0.00001}
    rcParams.update(MatPlotParams)

def matrc4():
    MatPlotParams = {'axes.titlesize': 12, 'axes.linewidth' : 1.0, 'axes.labelsize': 12, 'xtick.labelsize': 10, 'ytick.labelsize': 10, 'xtick.major.size': 12, 'ytick.major.size' : 12, 'xtick.minor.size': 10, 'ytick.minor.size': 10, 'figure.figsize' : [12.0, 10.0], 'xtick.major.pad' : 6, 'ytick.major.pad' : 4, 'figure.subplot.hspace' : 0.0}
    rcParams.update(MatPlotParams)
    pylab.subplots_adjust(left = 0.07,  # the left side of the subplots of the figure
                          right = 0.97,    # the right side of the subplots of the figure
                          bottom = 0.05,   # the bottom of the subplots of the figure
                          top = 0.95,      # the top of the subplots of the figure
                          wspace = 0.15,   # the amount of width reserved for blank space between subplots
                          hspace = 0.15)   # the amount of height reserved for white space between subplots

def matrc4X6():
    MatPlotParams = {'axes.titlesize': 12, 'axes.linewidth' : 1.0, 'axes.labelsize': 12, 'xtick.labelsize': 10, 'ytick.labelsize': 10, 'xtick.major.size': 12, 'ytick.major.size' : 12, 'xtick.minor.size': 10, 'ytick.minor.size': 10, 'figure.figsize' : [12.0, 10.0], 'xtick.major.pad' : 6, 'ytick.major.pad' : 4, 'figure.subplot.hspace' : 0.0}
    rcParams.update(MatPlotParams)
    pylab.subplots_adjust(left = 0.07,  # the left side of the subplots of the figure
                          right = 0.97,    # the right side of the subplots of the figure
                          bottom = 0.05,   # the bottom of the subplots of the figure
                          top = 0.95,      # the top of the subplots of the figure
                          wspace = 0.15,   # the amount of width reserved for blank space between subplots
                          hspace = 0.15)   # the amount of height reserved for white space between subplots

def galplot6():
    MatPlotParams = {'axes.titlesize': 12, 'axes.linewidth' : 1.0, 'axes.labelsize': 12, 'xtick.labelsize': 10, 'ytick.labelsize': 10, 'xtick.major.size': 12, 'ytick.major.size' : 12, 'xtick.minor.size': 10, 'ytick.minor.size': 10, 'figure.figsize' : [10.0, 10.5], 'xtick.major.pad' : 6, 'ytick.major.pad' : 6, 'figure.subplot.hspace' : 0.0,'legend.fontsize': 10}
    rcParams.update(MatPlotParams)
    pylab.subplots_adjust(left = 0.2,  # the left side of the subplots of the figure
                          right = 0.8,    # the right side of the subplots of the figure
                          bottom = 0.1,#.05   # the bottom of the subplots of the figure
                          top = 0.95,      # the top of the subplots of the figure
                          wspace = 0.30,   # the amount of width reserved for blank space between subplots
                          hspace = 0.45)#.15   # the amount of height reserved for white space between subplots


def matrc6():
    MatPlotParams = {'axes.titlesize': 12, 'axes.linewidth' : 1.0, 'axes.labelsize': 12, 'xtick.labelsize': 10, 'ytick.labelsize': 10, 'xtick.major.size': 12, 'ytick.major.size' : 12, 'xtick.minor.size': 10, 'ytick.minor.size': 10, 'figure.figsize' : [10.0, 15.0], 'xtick.major.pad' : 6, 'ytick.major.pad' : 6, 'figure.subplot.hspace' : 0.0,'legend.fontsize': 10}
    rcParams.update(MatPlotParams)
    pylab.subplots_adjust(left = 0.20,  # the left side of the subplots of the figure
                          right = 0.97,    # the right side of the subplots of the figure
                          bottom = 0.1,#.05   # the bottom of the subplots of the figure
                          top = 0.9,      # the top of the subplots of the figure
                          wspace = 0.20,   # the amount of width reserved for blank space between subplots
                          hspace = 0.15)#.15   # the amount of height reserved for white space between subplots

def matrc8():
    MatPlotParams = {'axes.titlesize': 12, 'axes.linewidth' : 1.0, 'axes.labelsize': 12, 'xtick.labelsize': 10, 'ytick.labelsize': 10, 'xtick.major.size': 12, 'ytick.major.size' : 12, 'xtick.minor.size': 10, 'ytick.minor.size': 10, 'figure.figsize' : [10.0, 16.0], 'xtick.major.pad' : 6, 'ytick.major.pad' : 6, 'figure.subplot.hspace' : 0.0}
    rcParams.update(MatPlotParams)
    pylab.subplots_adjust(left = 0.07,  # the left side of the subplots of the figure
                          right = 0.97,    # the right side of the subplots of the figure
                          bottom = 0.07,#.05   # the bottom of the subplots of the figure
                          top = 0.94,      # the top of the subplots of the figure
                          wspace = 0.20,   # the amount of width reserved for blank space between subplots
                          hspace = 0.24)#.15   # the amount of height reserved for white space between subplots





def matrc22():
    MatPlotParams = {'axes.titlesize': 15, 'axes.linewidth' : 2.5, 'axes.labelsize': 22, 'xtick.labelsize': 20, 'ytick.labelsize': 20, 'xtick.major.size': 22, 'ytick.major.size' : 22, 'xtick.minor.size': 14, 'ytick.minor.size': 14, 'figure.figsize' : [12.0, 10.0], 'xtick.major.pad' : 8, 'ytick.major.pad' : 6, 'figure.subplot.hspace' : 0.0, 'figure.subplot.wspace' : 0.275}
    rcParams.update(MatPlotParams)

def matrc2X5():
    MatPlotParams = {'axes.titlesize': 14, 'axes.linewidth' : 2.5, 'axes.labelsize': 12, 'xtick.labelsize': 10, 'ytick.labelsize': 10, 'xtick.major.size': 14, 'ytick.major.size' : 14, 'xtick.minor.size': 12, 'ytick.minor.size': 12, 'figure.figsize' : [16.0, 22.0], 'xtick.major.pad' : 8, 'ytick.major.pad' : 6, 'figure.subplot.hspace' : 0.3, 'figure.subplot.wspace' : 0.3}
    rcParams.update(MatPlotParams)
    pylab.subplots_adjust(left = 0.07,  # the left side of the subplots of the figure
                          right = 0.97,    # the right side of the subplots of the figure
                          bottom = 0.07,   # the bottom of the subplots of the figure
                          top = 0.92,      # the top of the subplots of the figure
                          wspace = 0.3,   # the amount of width reserved for blank space between subplots
                          hspace = 0.38)   # the amount of height reserved for white space between subplots
    


def matrc4X5():
    MatPlotParams = {'axes.titlesize': 14, 'axes.linewidth' : 2.5, 'axes.labelsize': 12, 'xtick.labelsize': 10, 'ytick.labelsize': 10, 'xtick.major.size': 14, 'ytick.major.size' : 14, 'xtick.minor.size': 12, 'ytick.minor.size': 12, 'figure.figsize' : [20.0, 22.0], 'xtick.major.pad' : 8, 'ytick.major.pad' : 6, 'figure.subplot.hspace' : 0.3, 'figure.subplot.wspace' : 0.3}
    rcParams.update(MatPlotParams)
    pylab.subplots_adjust(left = 0.05,  # the left side of the subplots of the figure
                          right = 0.97,    # the right side of the subplots of the figure
                          bottom = 0.05,   # the bottom of the subplots of the figure
                          top = 0.94,      # the top of the subplots of the figure
                          wspace = 0.2,   # the amount of width reserved for blank space between subplots
                          hspace = 0.3)   # the amount of height reserved for white space between subplots
    


