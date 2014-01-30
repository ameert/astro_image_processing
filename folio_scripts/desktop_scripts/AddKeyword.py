#!/data2/home/ameert/python/bin/python2.5
import pyfits as p
import os

os.system('ls 0*stamp*.fits > file.list')
f = open('file.list', 'r')
for l in f:
 v = l.split()[0]
 fz = p.open(v, 'update')
 fz[0].header.update('EXPTIME', 1.0)
 fz[0].header.update('RDNOISE', 2.0)
 fz[0].header.update('GAIN', 215.62982400000001)
 fz[0].header.update('NCOMBINE', 1)
 fz.close()
