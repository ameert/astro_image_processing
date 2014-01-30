#!/data2/home/ameert/python/bin/python2.5
import pyfits as p
import os
os.system('ls 0*stamp*.fits > file.list') #filter

f = open('file.list', 'r')
for l in f:
 v = l.split()[0]
 fz = p.open(v, 'update')
 fz[0].data = fz[0].data / 53.907456
 fz.close()

