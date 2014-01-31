#!/data2/home/ameert/python/bin/python2.5

import sys
import os
from mysql_class import *

folder_num = int(sys.argv[1])

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'

save_dir = '/scratch/%04d' %folder_num
try:
    os.system('mkdir %s' %save_dir)
except:
    pass

os.chdir(save_dir)

cursor = mysql_connect(dba, usr, pwd, 'shredder')

galcount, eb, bpa, xctr, yctr = cursor.get_data("""select galcount, eb, ((bpa+90)/180.0)*PI(), bulge_xctr, bulge_yctr from full_dr7_r_ser where galcount between %d and %d;""" %((folder_num-1)*250, folder_num*250))

for g1,e1,b1,x1, y1 in zip(galcount, eb, bpa, xctr, yctr):
    os.system('/data2/home/ameert/color_grads/scripts/measure_profs_serexp.py %d %f %f %f %f' %(g1,e1,b1,x1, y1))


#os.system('rm -rf %s' %save_dir)
