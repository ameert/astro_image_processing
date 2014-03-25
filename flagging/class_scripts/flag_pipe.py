#++++++++++++++++++++++++++
#
# TITLE: flag pipe
#
# PURPOSE: carries out the automated flags
#          and u-flags as described in the
#          Meert catalog paper
#
# INPUTS: fit values (total_flag)
#         and fit profiles (total_profile)
#         
# OUTPUTS: autoflag pickle files 
#
# PROGRAM CALLS: auto_flags.py
#                u_flags.py
#                numpy
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# WITH: Mariangela Bernardi
#       Department of Physics and Astronomy
#       University of Pennsylvania
#
# DATE: 15 JAN 2014 (revised)
#       1 OCT 2013 (Original)  
#
#-----------------------------------

import numpy as np
import os
import sys

from mysql_class import *
from create_flag_file_catalog import *
from auto_flags import *
from u_flags import *


if __name__ == "__main__":
    info_dict = {'dba':'catalog', 'usr':'pymorph', 'pwd':'pymorph', 'host':'',
                 'band':'r', 'model':'serexp','autoflag_ftype':'r',
                 'uflag_ftype':'u',
                 }
    info_dict['cursor']=mysql_connect(info_dict['dba'],info_dict['usr'],info_dict['pwd'],info_dict['host'])
    


    for folder_number in range(1,2684):
        print "folder number:", folder_number
        create_flag_pickle(folder_number, info_dict, print_info=False)
        run_auto_flags('serexp','r', folder_number, print_flags=False)
        load_autoflag(folder_number, info_dict, print_info = False)

        galcount, uflags_out = run_uflags(folder_number, info_dict,print_flags = False)
        load_uflags(galcount, uflags_out, info_dict, print_info = False)
