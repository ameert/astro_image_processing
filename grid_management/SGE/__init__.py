#++++++++++++++++++++++++++
#
# TITLE: SGE 
#
# PURPOSE: This module contains all the scripts
#          used for automated interaction with the
#          queue.
#
# INPUTS: NONE, BUT make sure the module is in your
#         PYTHONPATH
#
# OUTPUTS: Depends on the program being run....
#          Generally, there is little physical
#          output although many tasks are performed
#
# PROGRAM CALLS: all calls are internal to the module
#                except for basic python modules
#                and possibly numpy and scipy
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: Module constructed 16 AUG 2012
#       Component code written prior to this date
#
#-----------------------------------

from grid_management.SGE.getactive import * # returns active jobs and job info
from grid_management.SGE.nicecount import * # job counting and categoriztion
from grid_management.SGE.ezdel import *     # automated deletion of scripts
