#++++++++++++++++++++++++++
#
# TITLE: grid_management 
#
# PURPOSE: This module contains all the scripts
#          I use on the cluster for job management.
#          It is desgned to be extendable although
#          I currently only use it for pymorph jobs
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

import grid_management.job_manager as job_manager# the job manager scripts
import grid_management.SGE as SGE# basic scripts for queue manipulation 
import grid_management.utilities as ut # utilities used by the programs


