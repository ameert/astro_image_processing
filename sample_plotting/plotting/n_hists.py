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
 
def get_val(data, percentile):
    indicies = np.argsort(data)
    sdata = data[indicies]
    sweights = np.ones_like(sdata)/sdata.size
    cumweight = np.cumsum(sweights)
    pos = np.where(cumweight<=percentile)[0]
    if len(pos)<1:
        pos = 0
    else:
        pos = np.max(pos)
    return sdata[pos]

options = get_options_main()

cursor = mysql_connect('catalog','pymorph','pymorph','')

data1 = get_data(cursor, 'r_band_serexp', 'r_lackner_nb1', flags = options['use_flags'], flagmodel = options['flagmodel'], add_tables = ", r_lackner_fit as lfit " , conditions = "  and lfit.galcount = a.galcount and lfit.model = 'nb1' and (x.flag&pow(2,11)>1  or x.flag&pow(2,12)>1) and  a.n_bulge < 7.95 ")
data4 = get_data(cursor, 'r_band_serexp', 'r_lackner_nb4', flags = options['use_flags'], flagmodel = options['flagmodel'], add_tables = ", r_lackner_fit as lfit " , conditions = "  and lfit.galcount = a.galcount and lfit.model = 'nb4' and (x.flag&pow(2,11)>1  or x.flag&pow(2,12)>1) and a.n_bulge < 7.95 ")
print 'num_objects: ', len(data1['galcount'])
print 'num_objects: ', len(data4['galcount'])

pl.ylim(0,0.4)
pl.xlim(-0.5, 8.5)

nbins = np.arange(-0.25,8.51, 0.5)
pl.hist(data1['nbulge_1'], bins=nbins, normed=True, histtype='step', color='b', linestyle = 'dashed', label='nb1')
pl.errorbar([get_val(data1['nbulge_1'], 0.5)], [0.1], xerr=[[get_val(data1['nbulge_1'], 0.5)-get_val(data1['nbulge_1'], 0.16)],[get_val(data1['nbulge_1'], 0.84)-get_val(data1['nbulge_1'], 0.5)]], color = 'b', ms=5, marker = 'o')

print get_val(data1['nbulge_1'], 0.5), get_val(data1['nbulge_1'], 0.16),get_val(data1['nbulge_1'], 0.84)
pl.hist(data4['nbulge_1'], bins=nbins, normed=True, histtype='step', color='g', linestyle = 'solid', label='nb4')
pl.errorbar([get_val(data4['nbulge_1'], 0.5)], [0.05], xerr=[[get_val(data4['nbulge_1'], 0.5)-get_val(data4['nbulge_1'], 0.16)],[get_val(data4['nbulge_1'], 0.84)-get_val(data4['nbulge_1'], 0.5)]], color = 'g', ms=5, marker = 's')
print get_val(data4['nbulge_1'], 0.5), get_val(data4['nbulge_1'], 0.16),get_val(data4['nbulge_1'], 0.84)

#pl.legend()
pl.xlabel('n$_{bulge, serexp}$')
pl.ylabel('fraction of galaxies')
pl.savefig('rband_serexp_bulge_n.eps')
sys.exit()

oplot = outlier_fig()
oplot.set_ticks(0.5, 0.05, '%02.1f',1.0, 0.5,'%02.1f' )
oplot.setdenselims(1,10 )
oplot.setminval(10)
oplot.makeplot(data1['BT_2']-data1['BT_1'],data1['nbulge_1']-1, (-0.5,0.5),(-1,3.0))
pl.xlabel('BT')
pl.ylabel(ylabs['nbulge'].replace('{band}', options['band']))
oplot.bin_it(np.arange(-0.50,0.51,0.1), -8.0,8.0)
oplot.add_bars('r')
pl.ylim(-1,3)
pl.show()

pl.scatter(data1['BT_1'],data1['BT_2']-data1['BT_1'])
pl.xlim(0,1)
pl.ylim(-1,1)
#pl.show()

pl.scatter(data4['BT_1'],data4['BT_2']-data4['BT_1'])
pl.xlim(0,1)
pl.ylim(-1,1)
#pl.show()

pl.scatter(data1['nbulge_1']-1,data1['BT_2']-data1['BT_1'])
pl.xlim(-1,7)
pl.ylim(-1,1)
#pl.show()

pl.scatter(data4['nbulge_1']-4,data4['BT_2']-data4['BT_1'])
pl.xlim(-4,4)
pl.ylim(-1,1)
#pl.show()

data = get_data(cursor, 'i_band_serexp', 'g_band_serexp', flags = options['use_flags'], flagmodel = options['flagmodel'], conditions = " and (x.flag&pow(2,11)>1  or x.flag&pow(2,12)>1) and  d.kpc_per_arcsec* a.r_bulge>0.1 and a.n_bulge<7.95")

oplot = outlier_fig()
oplot.set_ticks(0.1, 0.05, '%02.1f',1.0, 0.5,'%02.1f' )
oplot.setdenselims(1,1000 )
oplot.setminval(10)
oplot.makeplot(data['z'],data['nbulge_1']-4, (0,0.3),
              ylims['nbulge'])
pl.xlabel('z')
pl.ylabel(ylabs['nbulge'].replace('{band}', options['band']))
oplot.bin_it(np.arange(0.0,0.301,0.05), -4.0,4.0, weight = 1.0/data['vmax'])
oplot.add_bars('r')

pl.show()

oplot = outlier_fig()
oplot.set_ticks(0.1, 0.05, '%02.1f',1.0, 0.5,'%02.1f' )
oplot.setdenselims(1,1000 )
oplot.setminval(10)
oplot.makeplot(data['mtot_2']-data['mtot_1'],data['nbulge_1']-4, (0.5,2.5),
              ylims['nbulge'])
pl.xlabel('g-i')
pl.ylabel(ylabs['nbulge'].replace('{band}', options['band']))
oplot.bin_it(np.arange(0.5,2.5,0.05), -4.0,4.0)#, weight = 1.0/data['vmax'])
oplot.add_bars('r')

pl.show()
