from mysql_class import * 
import sys

cursor = mysql_connect('pymorph', 'pymorph','pymorph9455', 'shredder')

table_nm = sys.argv[1]
filename = sys.argv[2]

curr_ent_str = 'insert ignore into '+table_nm+" "

str_cols = ['Name', 'Comments', 'Date', 'Filter', 'rootname', 'Morphology']

infile = open(filename)

cols = infile.readline()

cols = cols.split(',')
cols = ["_".join(a.split('_')[0:-1]) for a in cols]
cols_to_str = []
for count, cc in enumerate(cols):
    if cc in str_cols:
        cols_to_str.append(count)

cols = ','.join(cols)

curr_ent_str += '('+cols+') Values ('

for line in infile.readlines():
    line = line.replace('nan', '-99.99')
    line = line.replace('inf', '-99.99')
    line = line.split(',')
    for cc in cols_to_str:
        line[cc] = "'" + line[cc] + "'"
        
    cmd = curr_ent_str + ','.join(line) + ');'

    cursor.execute(cmd)


infile.close()
    
        
