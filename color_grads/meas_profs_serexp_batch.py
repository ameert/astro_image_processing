#!/data2/home/ameert/python/bin/python2.5

import sys
import os
from mysql_class import *

folder_num = int(sys.argv[1])

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'

cursor = mysql_connect(dba, usr, pwd, 'shredder')

data = zip(cursor.get_data("""select galcount from full_dr7_r_serexp where galcount between %d and %d;""" %((folder_num-1)*250, folder_num*250)))

print data

for dat in data:
    os.system('/data2/home/ameert/color_grads/scripts/measure_profs_new.py %d' %count)


