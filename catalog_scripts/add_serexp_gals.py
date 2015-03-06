# this short script inserts some galaxies that I accidentally deleted from the mysql database...oops
# it is probably unnecessary now, but I am keeping it just in case...


from mysql_class import *
from image_info import *
import numpy as np
import os
import pyfits as pf
import sys
from util_funcs import *
import time

def insert_gals(cursor, filename, gals):
    curr_ent_str = 'insert ignore into full_dr7_r_serexp '
    
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
        cur_gal = int(line[0].split('_')[1])
        if cur_gal in gals:
            for cc in cols_to_str:
                line[cc] = "'" + line[cc] + "'"
        
            cmd = curr_ent_str + ','.join(line) + ');'

            #print cmd
            cursor.execute(cmd)


    infile.close()
    
    return


dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
cursor = mysql_connect(dba, usr, pwd, 'shredder')

cmd = 'select galcount from tmp_table where n = 4 order by galcount;'

galcount, = cursor.get_data(cmd)
galcount = np.array(galcount, dtype = int)

bins = np.arange(0, 2201,1, dtype = int)

bin_locs = np.digitize(galcount, bins*250)
bin_amounts, junk = np.histogram(bin_locs, bins = bins)
print bins
print bin_amounts

for cur_bin, bin_count in zip(bins, bin_amounts):
    if bin_count > 0:
        gals_to_find = np.extract(bin_locs == cur_bin, galcount)
        filename = "/data2/home/ameert/catalog/r/fits/serexp/%04d/result.csv" %cur_bin
        #print "count %d" %bin_count
        #print "gals ", gals_to_find
        #insert_gals(cursor, filename, gals_to_find)

        print "qsub -V -l h_vmem=2G -N mhrese -e /data2/home/ameert/regen_galfit/output/ -o /data2/home/ameert/regen_galfit/output/ -wd /data2/home/ameert/catalog/r/fits/ /data2/home/ameert/regen_galfit/measure_corrected_psf.py serexp full_dr7_r %d"%cur_bin
        os.system("qsub -V -l h_vmem=2G -N mhrese -e /data2/home/ameert/regen_galfit/output/ -o /data2/home/ameert/regen_galfit/output/ -wd /data2/home/ameert/catalog/r/fits/ /data2/home/ameert/regen_galfit/measure_uncorrected_psf.py serexp full_dr7_r %d"%cur_bin)
        time.sleep(100)
        sys.exit()
print len(np.extract(bin_amounts >0, bins))
