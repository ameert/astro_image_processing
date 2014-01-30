#!/data2/home/ameert/python/bin/python2.5

import numpy as np
from mysql_class import *
import sys

table_name = sys.argv[1]
try:
    leading = sys.argv[2]
except:
    print "leading value assumed 0!"
    leading = "0"
try:
    length = sys.argv[3]
except:
    print "length assumed to be 8!"
    length = "8"
    
dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
host = 'shredder'

conn = mysql_connect(dba, usr, pwd, host)

conn.execute('alter table '+table_name+' add column galcount int first;')

conn.execute("update %s set galcount = SUBSTRING(Name,locate('%s', Name), %s) ;" %(table_name, leading, length))
             
conn.execute('alter table %s add primary key (galcount);' %table_name)

