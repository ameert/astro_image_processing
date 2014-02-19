#!/usr/bin/python

from mysql_class import *
import numpy as np
from load_table import *

infile = '../galflags_upenn_pymorph.csv'
table_name = 'CAST_flags'

cursor = mysql_connect('catalog', 'pymorph', 'pymorph')

columns = ['objid','flag']

column_types = ['bigint primary key', 'bigint']

load_table(cursor, table_name, infile, columns, column_types, make_table = 0)


for band in 'ugriz':
    #cmd = 'Update CAST_raw set skyErr_%s = 2.5/log(10) *skyErr_%s/sky_%s;' %(band,band, band)
    #cursor.execute(cmd)
    
    #cmd = 'Alter table CAST_raw drop column skySig_%s;' %band
    #cursor.execute(cmd)
    
    #cmd = 'Update CAST_raw set sky_%s = 22.5 - 2.5*log10(sky_%s*pow(10,9));' %(band, band)
   # cursor.execute(cmd)
    pass
