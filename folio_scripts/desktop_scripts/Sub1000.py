#!/home/vinu/64bit/Python2.5_64/bin/python
import pyfits as p
import os
#os.system('ls 0*psf*.fits > file.list')

os.system('ls 0*.fit.gz > file.list')

f = open('file.list', 'r')
for l in f:
 v = l.split()[0]
 fz = p.open(v, 'update')
 fz[0].data = fz[0].data - 1000.0
 fz.close()

