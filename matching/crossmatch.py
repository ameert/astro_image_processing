#!/usr/bin/python

import os
import itertools
import pyfits
import datetime
import sys
import string
import numpy as np
import healpy as hp
from optparse import OptionParser, OptParseError

sys.path.append('/home/ameert/python/alan_code/')

from mysql_class import *
from generate_table import *
from create_healpy_map import *


dba = 'catalog'
pwd = 'visitor'
usr = 'visitor'
    
cursor = mysql_connect(dba, usr, pwd)

usage = """crossmatch.py OPTIONS"""
desc = """This program will crossmatch an input catalog of ra/dec coordinates to our catalog and output the results

In general, you need to specify an input table, column file, output table, and a table name."""

parser = OptionParser(usage=usage, description = desc)
parser.add_option("-i","--input-cat", action="store", type="string",
                      dest="incat", default = 'test.incat',
                      help="input catalog to be crossmatched, default:test.incat")
parser.add_option("-c","--columns", action="store", type="string",
                      dest="in_file", default = '/home/ameert/alans-image-processing-pipeline/matching/test.columns',
                      help="columns to be in final catalog, default:/home/ameert/alans-image-processing-pipeline/matching/test.columns")
parser.add_option("-o","--output-file", action="store", type="string",
                      dest="outfile", default = '/tmp/output.txt',
                      help="output file for crossmatched catalog, default:/tmp/output.txt")
parser.add_option("-t","--table-file", action="store", type="string",
                      dest="tbl_file", 
     default = '/home/ameert/alans-image-processing-pipeline/matching/mysql.tables',
                      help="table file containing mysql table list, default:/home/ameert/alans-image-processing-pipeline/matching/mysql.tables")
parser.add_option("-n","--table-name", action="store", type="string",
                      dest="tablename", default = 'temp.incat',
                      help="name of temporary table for crossmatched catalog, default: temp.incat")

# parses command line aguments for pymorph
(options, args) = parser.parse_args()

drop_temp_table(cursor, options.tablename) 
create_temp_table(cursor, tablename=options.tablename)
load_matches(cursor, options.incat, options.tablename)

match_table = 'CAST'
NSIDE = 256

cmd = 'select galcount, ra_gal, dec_gal, healpix from %s_healpy order by healpix ;' %(match_table)
galcount, ra, dec, healpix = cursor.get_data(cmd)

cmd = 'select healpix, start_count, end_count from %s_healpy_info;' %match_table
healpy_in, start, end = cursor.get_data(cmd)

cmd = 'select rowcount, ra_gal, dec_gal from %s;' %options.tablename
galcount2, ra2, dec2 = cursor.get_data(cmd)

cat1 = catalog(galcount, ra, dec, NSIDE=256)
#cat1.map_sample()
cat1.pix = np.array(healpix, dtype=int)
cat1.set_pixel_list()
cat1.pix_info = dict(zip(healpy_in, zip(start, end)))
#cat1.get_pix_info()

print "Meert catalog loaded!!!"
cat2 = catalog(galcount2, ra2, dec2, NSIDE=256)
cat2.map_sample()
print "MAPPED!!!!!"

print "now matching!!!"
formatch = cat1.forward_match(cat2, 3.0)
backmatch = cat2.forward_match(cat1, 3.0)
print "now cross-matching!!!"
matches = get_crossmatch(formatch, backmatch)

print "catalogs matched!!!"
print "%d matches found...continuing" %(len(matches))
print "loading matches to db for table generation"

for match in matches:
    cmd = "update %s set galcount = %d, dis = %f where rowcount= %d;" %(options.tablename, match[0],match[2],match[1])
    cursor.execute(cmd)
print "matches loaded"
print "writing table to text file"
test_q = query(table_file = options.tbl_file, outfile = options.outfile)
test_q.add_table('%s,temp_tab' %options.tablename)
test_q.set_lead_table(options.tablename)

infile = open(options.in_file)
for line in infile.readlines():
    line =  line.strip()
    test_q.add_column(line)
infile.close()
test_q.clean_tables()

print "query"
test_q.gen_query()
print test_q.query

cursor.execute(test_q.query)
drop_temp_table(cursor, options.tablename) 
print "completed table available at %s" %test_q.outputname


    
