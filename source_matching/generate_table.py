#!/usr/bin/python

import os
import itertools
import pyfits
import datetime
import sys
import string
from optparse import OptionParser, OptParseError

sys.path.append('/home/ameert/python/alan_code/')
from mysql_class import *

# create table to hold matches temporarily
def create_temp_table(cursor, tablename=None):
    """Creates a temporary table of sources that have been matched to our data, this table is used to carry out the query to draw the data from the database."""

    if tablename==None:
        tablename='temp.matches'

    cmd = "create table %s (rowcount int primary key auto_increment, ra_gal float default -999, dec_gal float default -999, galcount int default -999, dis float default -999);" %tablename
    cursor.execute(cmd)

    cmd = "alter table %s add unique key (rowcount, galcount);" %tablename
    cursor.execute(cmd)

    return

def drop_temp_table(cursor, tablename):
    """Creates a temporary table of sources that have been matched to our data, this table is used to carry out the query to draw the data from the database."""

    cmd = "drop table IF EXISTS %s ;" %tablename
    cursor.execute(cmd)
    return

# load list to mysql temp database
def load_matches(cursor, listname, tablename):
    indat = open(listname)
    
    good_load = False

    for line in indat.readlines():
        line = line.split()

        try:
            ra_gal = float(line[0])
        except ValueError:
            print "RA improperly formatted in line %s\n exiting!!!!!" %' '.join(line)
            break
        try:
            dec_gal = float(line[1])
        except ValueError:
            print "DEC improperly formatted in line %s\n exiting!!!!!" %' '.join(line)
            break
        try:
            galcount = int(line[2])
        except:
            galcount = -999
            

        cmd = "insert into %s (ra_gal, dec_gal, galcount) values (%f, %f, %d);" %(tablename, ra_gal, dec_gal, galcount)
        cursor.execute(cmd)
    else:
        failed_load = True
    
    return good_load

# decide what data is wanted or read output file
class query():
    """this class holds all the data for a querey to mysql. This includes the tables used, the columns, and the format of the output. Columns are output in the order listed in the data_columns list"""
    def __init__(self, data_columns=[], outfile = None, table_file=None):
        """Creates the instance based on the data columns supplied. If nothing is supplied, creates an empty list"""
        self.columns = []
        self.set_outfile_delimiter()
        self.set_outfile_name(outfile)
        self.set_tables(table_file)
        
        for  col in data_columns:
            self.add_column(line)

        return
    
    def set_tables(self, table_file):
        """read tables from a file of tables in 'table,nickame' format"""
        self.tables = {}
        self.table_count = 0
        
        if table_file != None:
            infile = open(table_file)
            for line in infile:
                self.add_table(line)
            infile.close()
        return

    def add_table(self, line):
        """ add a single table to the table list. Table and table nickname must be in single string, separated by comma, NO WHITESPACE!!!"""
        line = line.strip().split(',')
        self.tables[line[0]]= [line[1], self.table_count]
        self.table_count +=1

    def set_lead_table(self, table_name):
        """Choose which table will be the lead table on which all matching will occurr"""
        self.tables[table_name][1]=-1
        return
    
    def clean_tables(self):
        """remove all tables not used in a column to improve matching speed and query readability"""
        all_cols = ','.join(self.columns)
        for table, table_info in self.tables.items():
            if table_info[0] not in all_cols:
                del self.tables[table]
        return

    def set_outfile_name(self, name):
        """sets the name of the outfile used to dump the query. Does not check if you have permission to write to this directory...thats your job!"""
        if name == None:
            name = '/tmp/output.txt'
        while os.path.isfile(name):
            print "output file %s already exists folder!!!\n" %name
            name = raw_input("enter a new filename>>> ")
        self.outputname = name
        return
    
    def set_outfile_delimiter(self, delimiter = ' '):
        """sets delimiter used in outfiles""" 
        self.output_delimiter = delimiter
        return

    def add_column(self, column):
        """adds a column to the column list based on the name supplied. the name should be in the format dba.table.columnname"""
        for col_name, col_info in self.tables.items():
            column = column.replace(col_name+'.', col_info[0]+'.')

        self.columns.append(column)
        
        return

    def gen_query(self):
        """makes the mysql querey that selects the needed data and outputs to a text file"""
        self.query = 'select \n'
        #add the columns
        cols = [ 'ROUND(ifnull(%s, -999),4)' %a for a in self.columns]
        self.query += ','.join(cols)
        self.query += '\nfrom\n'
        # add the tables
        table_list = [ (a[1][1], a[0]) for a in  self.tables.items()]
        table_list.sort(key=lambda x: x[0])
        sorted_tables = [a[1] for a in table_list]
        print sorted_tables
        lead_table = sorted_tables[0]
        self.query += '%s as %s ' %(lead_table, self.tables[lead_table][0])  
        add_tbl = ['left join %s as %s on %s.galcount = %s.galcount' %(a, self.tables[a][0], self.tables[lead_table][0],self.tables[a][0]) for a in sorted_tables[1:] ]
        
        add_tbl = ' '.join(add_tbl)
        self.query += add_tbl +'\n'

        #order according to the first column in the colfile
        self.query += 'order by %s\n' %self.columns[0]
        self.query +="into outfile '%s' fields terminated by '%s';" %(self.outputname,  self.output_delimiter)

        return

# main program if called
if __name__ == '__main__':

    dba = 'catalog'
    pwd = 'visitor'
    usr = 'visitor'
    
    cursor = mysql_connect(dba, usr, pwd)

    usage = """Usage: generate_table.py OPTIONS"""
    desc = """This program, when run alone, will generate an ascii txt table of data from all of our catalogs.
 
In general, you need to specify at least a column file, output file name, and a table name."""
    parser = OptionParser(usage=usage, description = desc)
    parser.add_option("-c","--columns", action="store", type="string",
                      dest="infile", default = '/home/ameert/alans-image-processing-pipeline/matching/SSDR6.columns',
                      help="columns to be in final catalog, default:/home/ameert/alans-image-processing-pipeline/matching/SSDR6.columns")
    parser.add_option("-o","--output-file", action="store", type="string",
                      dest="outfile", default = '/tmp/output.txt',
                      help="output file for crossmatched catalog, default:/tmp/output.txt")
    parser.add_option("-t","--table-file", action="store", type="string",
                      dest="tbl_file", 
                      default = '/home/ameert/alans-image-processing-pipeline/matching/mysql.tables',
                      help="table file containing mysql table list, default:/home/ameert/alans-image-processing-pipeline/matching/mysql.tables")
    parser.add_option("-l", "--lead-cat", action="store", type="string",
                      dest="lead_table", default = 'catalog.CAST',
                      help="the table by which the selection will be made, default: catalog.CAST")
 
    # parses command line aguments for pymorph
    (options, args) = parser.parse_args()

    test_q = query(table_file = options.tbl_file, outfile = options.outfile)

    infile = open(options.infile)
    for line in infile.readlines():
        line =  line.strip()
        test_q.add_column(line)
    infile.close()
    test_q.set_lead_table(options.lead_table)
    test_q.clean_tables()
    test_q.gen_query()
    print test_q.query
    cursor.execute(test_q.query)

