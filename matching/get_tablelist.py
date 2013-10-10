from mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys
import string

dba = 'information_schema'
pwd = 'pymorph'
usr = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

cmd = 'select table_name, TABLE_SCHEMA from tables;'
tables = cursor.get_data_dict(cmd, ['table_name','database'], [str,str])

outfile = open('mysql.tables', 'w')
for count, dba_table in enumerate(zip(tables['database'],tables['table_name'])):
    table_nick = 'nick_%s_%s' %(string.ascii_lowercase[count/26], string.ascii_lowercase[count % 26])


    outfile.write('.'.join(dba_table)+','+table_nick+'\n')

outfile.close()

