#++++++++++++++++++++++++++
#
# TITLE: cut_pipeline.get_data
#
# PURPOSE: this is the __init__ file
#          for getting data from sdss
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
import os

# I need to find the location of the current directory so that I can execute
# the casjobs java application included in this program

casjobs_path = ''
for test_path in sys.path:
    if os.path.isdir(test_path + '/' + __path__[0]):
        casjobs_path = test_path + '/' + __path__[0]+'/'
        break

if not os.path.isfile(casjobs_path + 'casjobs.jar'):
    print "WARNING:"
    print "-----------------------"
    print "I cant find casjobs.jar."
    print "cut_pipeline.get_data.casjobs will likely crash."
    print "Examine search paths in cut_pipeline.get_data __init__.py"
    print "modify as necessary to find casjobs.jar."
    print "------------------------\n\n\n"
    
from casjobs import *
from download_files import *
from make_query import *



if __name__ == "main":
    print "Casjobs.py"
    print "------------------------------"
    print "This module will query databases for galaxy"
    print "information but it is not ready yet"
    print "Terminating program!"
    print "------------------------------"
    sys.exit()


# Thats all that will load automatically
