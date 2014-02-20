#++++++++++++++++++++++++++
#
# TITLE: util.py
#
# PURPOSE: contains the utilities 
#          used in the matching 
#          module
#
# INPUTS: NONE
#
# OUTPUTS: NONE
#
# PROGRAM CALLS: NONE
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
##
# DATE: 12 JUNE 2013
#
#-----------------------------------

import numpy as np
import pylab as pl
import scipy as sc

class MatchError:
    """An error class for handling errors during matching of catalogs"""
    def __init__(self,etype):
        self.etype = etype
        return

    def __repr__(self):
        return "There was a matching error!!!"

