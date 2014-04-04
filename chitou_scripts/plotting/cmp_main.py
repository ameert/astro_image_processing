

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
from mysql.mysql_class import *
from cmp_functions import *
from MatplotRc import *
from plot_info import *
from get_data import *


options = get_options_main()

if options['model2']==None:
    options['model2']=options['model1']

cursor = mysql_connect('catalog','pymorph','pymorph','')

data = get_data(cursor, '%s_%s_%s' %(options['band'], options['table1'],options['model1']), '%s_%s_%s' %(options['band'], options['table2'],options['model2']), flags = options['use_flags'], flagmodel = options['flagmodel'], add_tables = options['add_tables'], conditions = options['conditions'])

print 'num_objects: ', len(data['galcount'])
print data[options['xchoice']+'_1'],data[options['ychoice']+'_1'],data[options['ychoice']+'_2']

# we want radial differences in percents
# this sets up the calculation so that the plotting below works
for name in ['hrad', 'rbulge', 'rdisk']:
    data[name+'_2'] =  (data[name+'_2']/data[name+'_1'])-1.0 +data[name+'_1']

if options['model2'] == 'dev':
    if options['table2'] in ['sdss', 'lackner']:
        data['mtot_2'] = data['mtot_2']-0.071648 #corrects for mag offset due to truncation
        data['mtot_abs_2'] = data['mtot_abs_2']-0.071648
if options['model2'] == 'exp':
    if options['table2'] in ['sdss', 'lackner']:
        data['mtot_2'] = data['mtot_2']-0.0103 #corrects for mag offset due to truncation
        data['mtot_abs_2'] = data['mtot_abs_2']-0.0103


if options['model2'] == 'devexp':
    if options['table2'] in ['lackner']:
        data['mbulge_2'] = data['mbulge_2']-0.071648 #corrects for mag offset due to truncation
        data['mdisk_2'] = data['mdisk_2']-0.0103 #corrects for mag offset due to truncation
        
        data['mtot_2'] = -2.5*np.log10(10**(-0.4*data['mdisk_2'])+10**(-0.4*data['mbulge_2']))
        data['mtot_abs_2'] = data['mtot_2'] - data['magcorr']
        data['surf_bright_2'] = -2.5*np.log10(10**(-0.4*data['mtot_2'])/(2.0*np.pi*data['hrad_2']**2))
    

data['sky_1'] =100.0*( 10.0**(-0.4*(data['sky_1']-data['sky_2']))-1) # quote sky in percent difference
data['sky_2'] = 0.0*data['sky_2'] # makes sky on the y axis work 

print data[options['xchoice']+'_1'],data[options['ychoice']+'_1'],data[options['ychoice']+'_2']

#do plot
oplot = outlier_fig()

if options['xtmaj']!=None:
    ticksx[options['key_x']][0] = options['xtmaj']
if options['xtmin']!=None:
    ticksx[options['key_x']][1] = options['xtmin']
if options['xtlab']!=None:
    ticksx[options['key_x']][2] = options['xtlab']
if options['ytmaj']!=None:
    ticksy[options['key_y']][0] = options['ytmaj']
if options['ytmin']!=None:
    ticksy[options['key_y']][1] = options['ytmin']
if options['ytlab']!=None:
    ticksy[options['key_y']][2] = options['ytlab']


oplot.set_ticks(ticksx[options['key_x']][0], ticksx[options['key_x']][1], ticksx[options['key_x']][2], 
                ticksy[options['key_y']][0], ticksy[options['key_y']][1], ticksy[options['key_y']][2])
oplot.setdenselims(1,options['upper_dense'] )
oplot.setminval(0.01*options['upper_dense'])
#oplot.makeplot(data[options['xchoice']+'_1'],data[options['ychoice']+'_1']-data[options['ychoice']+'_2'], xlims[options['xchoice']],

if options['xlims']!= None:
    xlims[options['xchoice']]=options['xlims']
if options['ylims']!= None:
    ylims[options['ychoice']]=options['ylims']

oplot.makeplot(data[options['xchoice']+'_1'],data[options['ychoice']+'_1']-data[options['ychoice']+'_2'], xlims[options['xchoice']],
              ylims[options['ychoice']]) 

if options['model1'] == 'ser':
    if options['ychoice'] == 'nbulge':
        ylabs[options['ychoice']]=ylabs[options['ychoice']].replace('bulge', 'ser')

pl.xlabel(xlabs[options['xchoice']].replace('{band}', options['band']))
pl.ylabel(ylabs[options['ychoice']].replace('{band}', options['band']))
oplot.bin_it(bins[options['key_x']], bin_lims[options['key_x']][options['key_y']][0],
            bin_lims[options['key_x']][options['key_y']][1])
oplot.add_bars('r')
pl.title(options['title'], fontsize=8)
oplot.savefig('%s_%s_%s_%s_%s_%s%s.eps' %(options['band'], options['table1'],options['table2'], options['model2'], options['xchoice'], options['ychoice'], options['postfix']))


