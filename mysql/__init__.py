#++++++++++++++++++++++++++
#
# TITLE: mysql 
#
# PURPOSE: This module contains all the scripts
#          I use to interact with mysql using the
#          MySQLdb module. This just makes the 
#          MySQLdb code a little more useful
#
# INPUTS: NONE, BUT make sure the top directory  
#         is in your PYTHONPATH
#
# OUTPUTS: NONE, at least not directly
#
# PROGRAM CALLS: MySQLdb module
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# DATE: Module constructed 10 OCT 2013
#       Component code written prior to this date
#
#-----------------------------------

try:
    import MySQLdb
except ImportError:
    import sys
    print """This mysql module requires MySQLdb!!!!
If you have already installed MySQLdb, make sure
it is in you PYTHONPATH. Otherwise, please install it!!!"""
    sys.exit()

from mysql_class import * # all the mysql

if __name__ == "__main__":
    print "mysql module successfully loads!"


