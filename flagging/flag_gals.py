#++++++++++++++++++++++++++
#
# TITLE: flag_gals
#
# PURPOSE: builds a txt file that has the
#          median difference in a set of 
#          parameters and the one-simga 
#          scatter as estimated by the
#          16-84 percentile range of the
#          distribution. This file can
#          be used by set_flags.py to 
#          flag galaxies that vary alot 
#          from band-to-band
#
# INPUTS: ?
#
# OUTPUTS: params.txt file
#
# PROGRAM CALLS:
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# DATE: written 2012, modified 2013
#-----------------------------------

from mysql.mysql_class import *
import random as rand
import pylab as pl
import pyfits as pf
import numpy as np
import scipy as sci
import os
import sys
from scipy.stats.mstats import mquantiles

def cmp_func(model, param, bands, pdata, outfile, percent = False):
    if percent:
        d = 100.0*(pdata[0]-pdata[1])/pdata[1]
    else:
        d = (pdata[0]-pdata[1])
    fiftyp = np.percentile(d,50) 
    d = d -fiftyp
    outfile.write( "(%f,%f) " %(fiftyp,(np.percentile(d,84)-np.percentile(d,16))/2))
    #print np.percentile(d,2.5), np.percentile(d,5),np.percentile(d,25),np.percentile(d,50),np.percentile(d,75),np.percentile(d,95),np.percentile(d,97.5)
    quants = mquantiles(d)
    pl.hist(d, range = (np.percentile(d,5), np.percentile(d,95)), bins = 40,normed = True)
    pl.title(bands[0]+'-'+bands[1])

    return

def get_dat(param, bands, data):
    bandpos = {'g':0, 'r':1, 'i':2}
    lead = bandpos[bands[0]]
    follow = bandpos[bands[1]]
 

    if param == 'pa_bulge':
        outdata = [data[lead]*(1.-data[follow+3]), (1.-data[follow]*data[follow+3]) ]
    elif param == 'pa_disk':
        outdata = [data[lead]*(1.-data[follow+6]), data[follow]*(1.-data[follow+6]) ]
    else:
        outdata = [data[lead], data[follow]]
    return outdata

cursor = mysql_connect('classify','pymorph','pymorph','')

info = [('dev',['r_bulge', 'ba_bulge','pa_bulge']), 
        ('ser',['r_bulge', 'n_bulge','ba_bulge','pa_bulge']),
        #('devexp',['r_bulge','ba_bulge','pa_bulge','r_disk','ba_disk','pa_disk','BT']) ,
        #('serexp',['r_bulge','n_bulge','ba_bulge','pa_bulge','r_disk','ba_disk','pa_disk','BT'])
]
outfile = open("params.txt",'w')
for model, params in info:
    for param in params:
        outfile.write('%s %s ' %(model, param))
        data = cursor.get_data('select a.galcount, a.{param}, b.{param}, c.{param},a.ba_bulge, b.ba_bulge, c.ba_bulge,a.ba_disk, b.ba_disk, c.ba_disk from catalog.g_band_{model} as a, catalog.r_band_{model} as b, catalog.i_band_{model} as c where a.galcount = b.galcount and a.galcount = c.galcount;'.format(model = model, param = param))
        data = [np.array(d) for d in data]
        pdata = [np.where(np.abs(d) > 600, np.nan, d) for d in data[1:]]

        fig = pl.figure()

        fig.add_subplot(2,3,1)
        tmp_dat = get_dat(param, 'gr', pdata)
        cmp_func(model, param, 'gr', tmp_dat, outfile, percent = False)

        fig.add_subplot(2,3,2)
        tmp_dat = get_dat(param, 'gi', pdata)
        cmp_func(model, param, 'gi', tmp_dat, outfile, percent = False)

        fig.add_subplot(2,3,3)
        tmp_dat = get_dat(param, 'ri', pdata)
        cmp_func(model, param, 'ri', tmp_dat, outfile, percent = False)
        
        fig.add_subplot(2,3,4)
        tmp_dat = get_dat(param, 'gr', pdata)
        cmp_func(model, param, 'gr', tmp_dat, outfile, percent = True)

        fig.add_subplot(2,3,5)
        tmp_dat = get_dat(param, 'gi', pdata)
        cmp_func(model, param, 'gi', tmp_dat, outfile, percent = True)

        fig.add_subplot(2,3,6)
        tmp_dat = get_dat(param, 'ri', pdata)
        cmp_func(model, param, 'ri', tmp_dat, outfile, percent = True)

        pl.suptitle(param)
        pl.show()


outfile.close()
