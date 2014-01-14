#++++++++++++++++++++++++++
#
# TITLE: cut_pipeline.utilities 
#
# PURPOSE: this is the __init__ file
#          for utilities
#          
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 21 Feb 2011
#
#-----------------------------------

import sys

if __name__ == "main":
    print "------------------------------"
    print "This module will simulate galaxies"
    print "but it cannot be called as a standalone"
    print "program!"
    print "------------------------------"
    sys.exit()

from read_list import *
from mysql_connect import *


# Thats all that will load automatically
