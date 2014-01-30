#!/home/ameert/python/bin/python2.5

from mysql_class import *
import os
import numpy as np
import sys

folder = int(sys.argv[1])
bands = 'gri'

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
cursor = mysql_connect(dba, usr, pwd, 'shredder')

#galcounts, = cursor.get_data('select galcount from chi_catalog_%s where %s_dof <= 0;' %(band, model) )
galcounts = range(250*(folder-1)+1, 250*folder+1)#np.array(galcounts, dtype = int)

for model in ['dev','ser','devexp','serexp']:
    for band in bands:
        for galcount in galcounts:
            filenm = '/data2/home/ameert/catalog/%s/fits/%s/%04d/G_%s_%08d_%s_stamp.out' %(band, model, folder, band, galcount, band) 
            if os.path.isfile(filenm):
                infile = open(filenm)
                line = infile.readlines()
                line = line[1]
                line = line.replace(',',' ')
                line = line.split('=')
                vals = [a.split()[0] for a in line[1:]]
                cmd = 'update chi_catalog_%s set %s_chi = %f, %s_dof = %f where galcount =%d;' %(band, model, float(vals[1]), model, float(vals[2]), galcount)
                cursor.execute(cmd)
            else:
                print filenm+" not found!!!!!!!!!!!!!"

