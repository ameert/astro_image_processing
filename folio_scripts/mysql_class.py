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
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 14 JAN 2011
#
#-----------------------------------

import MySQLdb as mysql
import sys

class mysql_connect():
    """Connects to mysql and lets you submit queries"""
    def __init__(self, dba, usr, pwd, host="localhost"):
        try:
            Conn = mysql.connect (host = "%s" %host,
                                  user = "%s" %usr,
                                  passwd = "%s" %pwd,
                                  db = "%s" %dba)
        except mysql.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit (1)
        self.cursor = Conn.cursor()

        return
    
    def get_data(self, cmd, vars = [], num_col = -1):
        self.cursor.execute(cmd)
        rows = self.cursor.fetchall()
        rows = list(rows)

        cmd = cmd.lower()
        if len(vars) != num_col:
            vars = cmd.split(' from')[0]
            vars = vars.strip()
            print vars
            vars = vars.split('select')[1]
            vars = vars.split(',')
            num_col = len(vars)
        
        output = [ [] for col in vars ]

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


    
        
        


        
            
