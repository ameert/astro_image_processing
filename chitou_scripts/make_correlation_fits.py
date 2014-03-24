import os
from mysql_class import *
import numpy as np
import sys
import sys
from plotting_funcs import magsum
import pylab as pl
import matplotlib.cm as cm
import pyfits as pf
import pickle 
from datetime import date 

today = date.today()

inmodel = sys.argv[1]

outfits_name = '%s_correlation.fits' %inmodel

phdu = pf.PrimaryHDU()
hdulist = pf.HDUList([phdu])
prihdr = hdulist[0].header

prihdr.update('InModel', 'ser', 'simulated model')
prihdr.update('creator1','Alan Meert','')
prihdr.update('creator2','Vinu Vikram','')
prihdr.update('creator3','Mariangela Bernardi','')
prihdr.update('PaperRef','See Meert et al 2012','')
prihdr.add_history('file created %s' %(today.isoformat()))
prihdr.add_comment('This is the correlation matrix of errors for simulations')

for fitmodel in ['ser','devexp','serexp']:
    print 
    infile = open('./%s_%s_correlation.pickle' %(inmodel, fitmodel))
    correlation_mat, names, group_labels=pickle.load(infile)
    infile.close()

    collist = []
    for dat, nm, longn in zip(correlation_mat, names, group_labels):
        print nm, longn
        fmat = str(len(dat))+'E'
        collist.append(pf.Column(name = nm, format = fmat, array = dat, 
                                 unit = longn))

    tbhdu = pf.new_table(collist)
    tbhdu.header.update('FitModel',fitmodel,'the fitted model')
    tbhdu.header.add_comment('column titles retain same order as rows')
    tbhdu.header.add_comment('units contain LaTeX defs of variables')
   
    hdulist.append(tbhdu)

print 'writing %s' %outfits_name    
hdulist.writeto(outfits_name, clobber = 1)
print 'done'


