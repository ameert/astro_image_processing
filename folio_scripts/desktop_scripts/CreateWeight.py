#!/data2/home/ameert/python/bin/python2.5
import pyfits as p
import os
import numpy as n

os.system('ls 0*stamp*.fits > file.list') #filter

f = open('file.list', 'r')
for l in f:
 v = l.split()[0]
 wf = str(v.split('stamp')[0]) + '_r_W.fits' #filter
 fz = p.open(v)
 wz = n.sqrt(fz[0].data / 4.6) / 53.907456
 fz.close()
 os.system('rm -f ' + str(wf)) 
 hdu = p.PrimaryHDU(wz.astype(n.float32))
 hdu.writeto(wf)
