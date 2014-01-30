#!/data2/home/ameert/python/bin/python2.5
import os
os.system('ls *.fits > file.list')
for l in open('file.list'):
 v = l.split()[0]
 cmd = 'mv ' + str(v) + ' 00' + str(v)
 os.system(cmd)
