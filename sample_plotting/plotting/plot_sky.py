# standard python code imports
import numpy as np
import pylab as pl
import matplotlib
import matplotlib.colors as col
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import sys
import os
from matplotlib.backends.backend_pdf import PdfPages

# my personal code imports 
from mysql_class import *
from cmp_functions import *
from MatplotRc import *
from plot_info import *
from get_data import *


tablestem = 'dev'
model = 'dev'
band = 'r'
xchoice = 'mtot'
ychoice = 'sky'
key_x = 'mag'

cursor = mysql_connect('catalog','pymorph','pymorph','')

data = get_data(cursor, '%s_band_%s' %(band, model), '%s_sdss_%s' %(band, tablestem))

print 'num_objects: ', len(data['galcount'])

# we want radial differences in percents
# this sets up the calculation so that the plotting below works
for name in ['hrad', 'rbulge', 'rdisk']:
    data[name+'_2'] = (data[name+'_2']/data[name+'_1']) - 1.0 +data[name+'_1']

data['sky_1'] =100.0*( 10.0**(-0.4*(data['sky_1']-data['sky_2']))-1)

#do plot
oplot = outlier_fig()
oplot.set_ticks(ticksx[key_x][0], ticksx[key_x][1], ticksx[key_x][2], 
               .5, .05, '%2.1f')
oplot.makeplot(data[xchoice+'_2'],data['sky_1'], xlims[xchoice],(-2.0, 2.0))
               
pl.xlabel(xlabs[xchoice].replace('{band}', band))
pl.ylabel(ylabs['sky'].replace('{band}', band))
oplot.bin_it(bins[key_x], -2.0,2.0)
oplot.add_bars('r')
oplot.savefig('%s_%s_%s_%s_%s4.eps' %(band, tablestem, model, xchoice, ychoice))


