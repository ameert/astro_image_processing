import sys
import os
import numpy as np
import statistics.bin_stats as bs
import pylab as pl
from MatplotRc import *

data = np.load('ba_data_serexp.npz')
fig = pl.figure(figsize = (6,5))
fig.subplots_adjust(left = 0.14, right = 0.9, top = 0.9, bottom = 0.1, 
                    wspace = 0.75, hspace = 0.75)

flags = np.where(data['flags']&(2**10)>0, np.where(data['n_bulge']>7.95, data['flags']^(2**10+2**27),data['flags']),data['flags'])

flags = np.where(flags&(2**1)>0,1,0)+np.where(flags&(2**4)>0,2,0)+np.where(flags&(2**10),3,0)+np.where(flags&(2**14)>0,4,0)+np.where(flags&(2**27)>0,5,0)+np.where(flags&(2**20)>0,6,0)


for count, gal_opt in enumerate([('bulges',1),('2com',3),
                                 ('bad 2com',4),('n8',5),('bad',6)]):
    ttype =  np.where(flags==gal_opt[1],1,0)
    ba_bulge = np.where( ttype==1, data['ba_bulge'], np.nan)
    BT = np.where( ttype==1, data['BT'], np.nan)
    
    print 'Type ', gal_opt[0]
    print np.extract(ba_bulge<0.1, data['galcount'])
    pl.subplot(3,2,count+1)
    n, bins, patches = pl.hist(ba_bulge, range=(0,1), bins = 50, log = True)
    pl.ylabel('counts')
    pl.xlabel('b/a bulge')
    pl.title( gal_opt[0])
    
    nmax = np.ceil(np.log10(float(max(n))))
    
    pl.ylim(1,10**nmax)
pl.savefig('ba_bulge_serexp_flag.eps')
pl.close(fig)

fig = pl.figure(figsize = (6,5))
fig.subplots_adjust(left = 0.14, right = 0.9, top = 0.9, bottom = 0.1, 
                    wspace = 0.75, hspace = 0.75)
for count, gal_opt in enumerate([('disks',2),('2com',3),
                                 ('bad 2com',4),('n8',5),('bad',6)]):
    ttype =  np.where(flags==gal_opt[1],1,0)
    ba_disk = np.where( ttype==1, data['ba_disk'], np.nan)
    BT = np.where( ttype==1, data['BT'], np.nan)
    
    print 'Type ', gal_opt[0]
    print np.extract(ba_bulge<0.1, data['galcount'])
    pl.subplot(3,2,count+1)
    n, bins, patches = pl.hist(ba_disk, range=(0,1), bins = 50, log = True)
    pl.ylabel('counts')
    pl.xlabel('b/a disk')
    pl.title( gal_opt[0])
    
    nmax = np.ceil(np.log10(float(max(n))))
    
    pl.ylim(1,10**nmax)
pl.savefig('ba_disk_serexp_flag.eps')
