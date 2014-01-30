#!/usr/bin/env python
import os

f = open('result.csv.ser', 'r')
fitted = []
for l in f:
 v = l.split(',')
 fitted.append(v[0][:-6])

os.system('ls *_s0_stamp.fits > file')
i = 0
for l in open('file'):
 v = l.split()[0][3:-11]
 if v not in fitted:
  cmd = 'rm -f *' + v + '*'
  os.system(cmd)
  i += 1
print i

 
 
