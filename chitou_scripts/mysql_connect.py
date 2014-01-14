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

def mysql_connect(dba,usr,pwd):
    try:
        Conn = mysql.connect (host = "localhost",
                                     user = "%s" %usr,
                                     passwd = "%s" %pwd,
                                     db = "%s" %dba)
    except mysql.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit (1)
    cursor = Conn.cursor()

    return cursor
