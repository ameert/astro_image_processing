from mysql_class import *
import numpy as np
import pylab as pl
from MatplotRc import *
import ndimage
import pylab as pl
import sys
import os
from bin_stats import *
import matplotlib as mat
from matplotlib.patches import Rectangle

letters = ['(a)','(b)','(c)','(d)','(e)','(f)','(g)','(h)','(i)','(j)','(k)','(l)','(m)','(n)','(o)','(p)','(q)','(r)','(s)','(t)','(u)','(v)','(w)','(x)','(y)','(z)']

def magsum(mag1, mag2):
    mag1 = 10.0**( -.4*mag1)
    mag2 = 10.0**(-.4*mag2)

    mag_tot = mag1 + mag2
    bt = mag1/(mag1+mag2)
    mag_tot = -2.5 * np.log10(mag_tot)

    return mag_tot, bt


def start_fig(sizech = (13,13)):
    matrc4X6()

    fig = pl.figure(figsize =sizech, frameon = True)

    fig.subplots_adjust(left = 0.12,  # the left side of the subplots of the figure
                        right = 0.97,    # the right side of the subplots of the figure
                        bottom = 0.08,   # the bottom of the subplots of the figure
                        top = 0.95,      # the top of the subplots of the figure
                        wspace = 0.48,   # the amount of width reserved for blank space between subplots
                        hspace = 0.48)   # the amount of height reserved for white space between subplots

    return fig

def add_rec(fig, y_min, y_range, x_min = -0.5, x_range = 2.0, color = '0.9'):

    rec = Rectangle((x_min, y_min), x_range, y_range, color = color, transform = fig.transFigure, figure = fig, zorder = -10 )
    
    fig.patches.extend([rec])


    return fig


def decide_rec(fig, row_grouping):
    """this will decide how to make background shading
    accepts the active figure and the row groupings, i.e. (1,2,1,2)
    The total rows must add up to 6!!!!!!!"""
    
    ymax =0.95
    row_groups = list(row_grouping[:])
    row_groups.reverse()
    step = ymax/np.sum(np.array(row_groups))
    shade_row = 0
    ymin = 0.0
    for ptype in row_groups:
        y_range = step * ptype
        if shade_row:
            add_rec(fig, ymin, y_range)
        ymin += y_range
        shade_row = (shade_row+1)%2
        
    return fig

class big_plot():
    def __init__():
        self.letters = ['(a)','(b)','(c)','(d)','(e)','(f)','(g)','(h)','(i)','(j)','(k)','(l)','(m)','(n)','(o)','(p)','(q)','(r)','(s)','(t)','(u)','(v)','(w)','(x)','(y)','(z)']

        plots = {}

        return

    def add_plot(num):
        plots[num] = {}
        return







class plot_data():
    def __init__():
        self.title = ''
        return
    
