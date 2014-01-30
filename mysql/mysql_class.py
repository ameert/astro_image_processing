#++++++++++++++++++++++++++
#
# TITLE: mysql_connect
#
# PURPOSE: this program connects to
#          mysql and returns the cursor
#          if sucessful
#
# INPUTS: dba: string of database name that you want
#              to use
#         usr: the username to use
#         pwd: the password of the user
#
# OUTPUTS: If sucessful, returns the cursor used by mysql
#          If it fails, it causes the program to exit
#
# PROGRAM CALLS: calls functions from MySQLdb module that
#                is imported by the program
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# DATE: 14 JAN 2011
#
#-----------------------------------

import MySQLdb as mysql
import numpy as np
import sys

class mysql_connect():
    """Connects to mysql and lets you submit queries"""
    def __init__(self, dba, usr, pwd, lhost = "localhost"):
        """dba: database name
usr: user name
pwd: password
host: hostname (default should work on most machines)
"""
        try:
            Conn = mysql.connect(host = "%s" %lhost,
                                 user = "%s" %usr,
                                 passwd = "%s" %pwd,
                                 db = "%s" %dba)
            Conn.autocommit(True)
        except mysql.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)
        self.cursor = Conn.cursor()

        return
    
    def get_data_dict(self, cmd, object_names, dtype):
        """runs query, fetches data to arrays of type given, returns results in dictionary form"""
        dat_dict = {}
        data = self.get_data(cmd)
        for dat, ob_name, ob_type in zip(data, object_names, dtype):
            dat_dict[ob_name] = np.array(dat, dtype=ob_type)
        
        return dat_dict


    def get_data(self, cmd):
        self.cursor.execute(cmd)
        rows = self.cursor.fetchall()
        rows = list(rows)

        num_col = len(rows[0])

        output = [ [] for col in range(num_col) ]

        for row in rows:
            for row_num, row_el in enumerate(row):
                output[row_num].append(row_el)

        return output


    def execute(self, cmd):
        self.cursor.execute(cmd)

        return


    def __del__(self):
        self.cursor.close()

        return


if __name__ == "__main__":
    import random
    dba = 'test'
    usr = 'test'
    pwd = ''
    
    cursor =  mysql_connect(dba, usr, pwd)
    
    print "creating table TEST"
    cursor.execute('create table IF NOT EXISTS TEST (number int primary key, data1 float, data2 varchar(20));')
    
    for count in range(1,5):
        data1 = random.random()
        cursor.execute("insert ignore into TEST value (%d, %f, 'This is entry %d');" %(count, data1, count))
    
    number, data1, data2 = cursor.get_data('select number, data1, data2 from TEST;')

    print "data in TEST"
    for a in zip(number, data1, data2):
        print a

    print "data in dict form"
    data_dict = cursor.get_data_dict('select number, data1, data2 from TEST;', ['number', 'data1', 'data2'], [int, float, str])
    
    print data_dict

    print "dropping table TEST"
    cursor.execute('drop table IF EXISTS TEST;')
    
        
        


        
            
