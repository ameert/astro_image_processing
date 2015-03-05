#++++++++++++++++++++++++++
#
# TITLE: simulate_galaxies 
#
# PURPOSE: this is the __init__ file
#          for the galaxy simulation
#          
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 18 Feb 2011
#
# NOTE: All the code in this namespace
#       is in simulate_galaxies.py
#-----------------------------------

import numpy as n
import random as r
import sys
import os
from simulate_galaxies import *
import add_background as a
import generate_params as g
import redshift_gals as red


if __name__ == "main":
    print "------------------------------"
    print "This module will simulate galaxies"
    print "but it cannot be called as a standalone"
    print "program!"
    print "------------------------------"
    sys.exit()


# Thats all that will load automatically



