#!/data2/home/ameert/python/bin/python2.5

import numpy as np
from mysql_class import *
import sys
import os



def get_neighbornum(file):
    if os.path.isfile(file):
        infile = open(file)
        inlines = infile.readlines()
        infile.close()

        inlines= '\n'.join(inlines)
        inlines = inlines.split(' 0) sky')[1]
        inlines = inlines.split(' 0) sersic')
    
        neighborcount = len(inlines)-1
    else:
        neighborcount = -999
    return neighborcount

table_name = sys.argv[1]
model = sys.argv[2]
band = sys.argv[3]
folder = int(sys.argv[4])

folder_path = '/data2/home/ameert/catalog/%s/fits/ser_new/%04d/' %(band,folder)
#folder_path = '/data2/home/ameert/catalog/short_sample/%s/fits/%s/%04d/' %(band,model,folder)

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
host = 'shredder'

conn = mysql_connect(dba, usr, pwd, host)

os.system('ls '+folder_path+'/G_*stamp.in > file%d.list' %folder)

infile = open('file%d.list' %folder)
for line in infile:
    line = line.strip()
    #print line
    galcount = line.split('/')[-1]
    galcount = int(galcount.split('_')[2])
    name = line.split('G_')[1]
    name = name.split('.in')[0]
    nn = get_neighbornum(line)
    cmd = 'Update %s set num_neigh_%s=%d where galcount=%d;' %(table_name,band, nn,galcount)
    #cmd = "Update %s set num_neigh=%d where Name='%s';" %(table_name,nn,name)
    #print cmd
    conn.execute(cmd)

infile.close()

os.system('rm file%d.list' %folder)

