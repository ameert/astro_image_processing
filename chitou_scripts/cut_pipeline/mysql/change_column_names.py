from mysql_connect import *

dba = 'pymorph_data' # 'sdss_sample'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba,usr,pwd)


file = open('dr4_columns.txt', 'r')#('column_names.txt', 'r')

columns = file.readline()
for column in columns.split(','):
    if not (column in ['gal_count', 'objid', 'run', 'rerun', 'camCol', 'field', 'rowc', 'colc']):
        
        print column
        cmd = 'ALTER TABLE sdss_sample ALTER COLUMN %s SET DEFAULT -888;' %(column)
        #cmd = 'UPDATE sdss_sample SET %s = -888 where %s IS NULL;' %(column, column)
        cursor.execute(cmd)


file.close()
cursor.close()
