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


tablestem, model, band, xchoice, ychoice, key_x, key_y, use_flags, flagmodel, use_twocom = get_options()

cursor = mysql_connect('catalog','pymorph','pymorph','')

#and x.flag&pow(2,10)>0
if use_twocom:
    #conditions = "  and mmas.galcount = x.galcount and sfit.galcount = x.galcount and sfit.Prob_pS between 0 and 0.32 "
    conditions = "   and sfit.galcount = x.galcount and mmas.galcount = x.galcount and mmas.ProfType = 3 "
    add_tables = ', r_simard_fit as sfit, simard.Mendel_masses as mmas '
else:
    conditions = ""
    add_tables = ''
data = get_data(cursor, '%s_band_%s' %(band, model), '%s_%s_%s' %(band, tablestem, model), flags = use_flags, flagmodel = flagmodel, conditions = conditions, add_tables = add_tables)
# and (z.flag>-1 and x.flag >-1 and y.flag >-1)".format(band = band, model = model)
print 'num_objects: ', len(data['galcount'])

# we want radial differences in percents
# this sets up the calculation so that the plotting below works
for name in ['hrad', 'rbulge', 'rdisk']:
    data[name+'_2'] = 1.0- (data[name+'_2']/data[name+'_1']) +data[name+'_1']
if tablestem=='lackner':
    if model == 'dev':
        data['mtot_2'] = data['mtot_2']-0.09
    elif model == 'devexp':
        data['mbulge_2'] = data['mbulge_2']-0.09
        data['mdisk_2'] = data['mdisk_2']-0.09
data['sky_1'] =100.0*( 10.0**(-0.4*(data['sky_2']-data['sky_1']))-1)

print 'keys'
print key_x, key_y
#do plot
oplot = outlier_fig()
oplot.set_ticks(ticksx[key_x][0], ticksx[key_x][1], ticksx[key_x][2], 
               ticksy[key_y][0], ticksy[key_y][1], ticksy[key_y][2])
oplot.setdenselims(1,1000 )
oplot.makeplot(data[xchoice+'_1'],data[ychoice+'_1']-data[ychoice+'_2'], xlims[xchoice], ylims[ychoice]) 
pl.xlabel(xlabs[xchoice].replace('{band}', band))
pl.ylabel(ylabs[ychoice].replace('{band}', band))
oplot.bin_it(bins[key_x], bin_lims[key_x][key_y][0],
            bin_lims[key_x][key_y][1])
oplot.add_bars('r')

oplot.savefig('%s_%s_%s_%s_%s.eps' %(band, tablestem, model, xchoice, ychoice))
#_cleaned


