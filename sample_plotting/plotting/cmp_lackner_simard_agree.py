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


tablestem, model, band, xchoice, ychoice, key_x, key_y = get_options()

cursor = mysql_connect('catalog','pymorph','pymorph','')

data = get_data(cursor, '%s_band_%s' %(band, model), '%s_%s_%s' %(band, tablestem, model), add_tables=', r_lackner_ser as c', conditions=' and c.galcount = a.galcount')

print 'num_objects: ', len(data['galcount'])

# we want radial differences in percents
# this sets up the calculation so that the plotting below works
for name in ['hrad', 'rbulge', 'rdisk']:
    data[name+'_2'] = (data[name+'_2']/data[name+'_1']) - 1.0 +data[name+'_1']

#do plot
oplot = outlier_fig()
oplot.set_ticks(ticksx[key_x][0], ticksx[key_x][1], ticksx[key_x][2], 
               ticksy[key_y][0], ticksy[key_y][1], ticksy[key_y][2])
oplot.setdenselims(0,100 )
oplot.makeplot(data[xchoice+'_1'],data[ychoice+'_1']-data[ychoice+'_2'], xlims[xchoice],
              ylims[ychoice]) 
pl.xlabel(xlabs[xchoice].replace('{band}', band))
pl.ylabel(ylabs[ychoice].replace('{band}', band))
oplot.bin_it(bins[key_x], bin_lims[key_x][key_y][0],
            bin_lims[key_x][key_y][1])
oplot.add_bars('r')
oplot.savefig('%s_%s_lacknermatch_%s_%s_%s.eps' %(band, tablestem, model, xchoice, ychoice))
