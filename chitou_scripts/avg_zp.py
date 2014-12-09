import numpy as np
import pylab as pl


indata = np.loadtxt('/home/ameert/lackdr8.csv', unpack = True, skiprows=1,
                    delimiter=',')


zp_diff = indata[-3]-indata[-2]
galcount = indata[0].astype(int)


pl.hist(zp_diff, bins=50, range=(-0.2,0.2))
ax = pl.gca()

#ax.set_yscale('log')
#pl.show()


good = np.where(zp_diff<0.2,1,0)*np.where(zp_diff>-0.2,1,0)
offsets = np.extract(good==1, zp_diff)

#galset = set(galcount)

#gal_diffs = [ (a,np.extract(galcount==a, zp_diff)) for a in galset]
    
#gal_baddifs = [(a[0], np.sum(np.abs(a[1]-np.mean(a[1])))) for a in gal_diffs]

#for a in gal_baddifs:
#    if a[1]>0.0001:
#        print a

print "loading tables"
from mysql.mysql_class import *

cursor = mysql_connect('catalog','pymorph','pymorph')
cmd = 'insert ignore into lackner_zp_corr values '+str(zip(galcount, zp_diff))[1:-1]+';'
cursor.execute(cmd)


print "mean ", np.mean(offsets)

