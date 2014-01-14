#++++++++++++++++++++++++++
#
# TITLE: __init__.py for generate_params 
#
# PURPOSE: initializes the generate_params
#          module
#
# INPUTS: NONE
#
# OUTPUTS: NONE 
#
# PROGRAM CALLS: just imports everything
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 20 FEB 2011
#
#-----------------------------------

import os
import sys
from generate_params import *

if __name__ == "main":
    print "------------------------------"
    print "This module will randomly choose galaxy"
    print "parameters but it cannot be called as a"
    print "standalone program!"
    print "------------------------------"
    sys.exit()


dist_stem = 'SerExp_'

for try_path in __path__:
    if os.path.isdir(try_path+'/curr_dist/'):
        dist_path = try_path+'/curr_dist/'

