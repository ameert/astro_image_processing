import os
from mysql_class import * 
import sys
import numpy as np

model = 'devexp'
table_nm = 'full_dr7_r_%s' %model
file_path = '/data2/home/ameert/catalog/r/fits/%s' %model

cursor = mysql_connect('pymorph', 'pymorph','pymorph9455', 'shredder')

tot_fixed = 0

cmd = 'select a.galcount from CAST as a left join %s as b on a.galcount = b.galcount where b.galcount is null;' %table_nm

failed_galcount, = cursor.get_data(cmd)

failed_galcount = np.array(failed_galcount, dtype = int)
failed_folders = (failed_galcount -1)/250 +1
folder_bins = np.arange(-0.5, 2683.6, 1.0)
folder_counts,edges = np.histogram(failed_folders, folder_bins)

for folder, num_failed in enumerate(folder_counts):
    print folder, num_failed
    if num_failed > 0:
        gals_to_find = np.extract(failed_folders == folder, failed_galcount)
        
        filename = '%s/%04d/result.csv' %(file_path, folder)
    
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

        cols = ','.join(cols) +',galcount'

        curr_ent_str += '('+cols+') Values ('

        for line in infile.readlines():
            galcount = int(line.split(',')[0].split('_')[1])
            if galcount in gals_to_find: 
                line = line.replace('-nan', '-9999.99')
                line = line.replace('nan', '-9999.99')
                line = line.replace('-inf', '-6666.66')
                line = line.replace('inf', '-6666.66')
                line = line.replace('--', '9999')
                line = line.strip()
                line = line.split(',')
                for cc in cols_to_str:
                    line[cc] = "'" + line[cc] + "'"

                cmd = curr_ent_str + ','.join(line) + ','+str(galcount)+');'

                print cmd
                cursor.execute(cmd)
                tot_fixed +=1

        infile.close()

print tot_fixed
