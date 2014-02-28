#++++++++++++++++++++++++++
#
# TITLE: 
#
# PURPOSE: sets final flag parameter in
#          mysql catalog (OLD flagging)
#
# INPUTS: 
#
# OUTPUTS: 
#
# PROGRAM CALLS:
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# WITH: Mariangela Bernardi
#       Department of Physics and Astronomy
#       University of Pennsylvania
#
# DATE:2012
#
#-----------------------------------

import numpy as np
import pylab as pl
import scipy as sc
from mysql_class import *
from flag_dict import *

cursor = mysql_connect('catalog','pymorph','pymorph','')

# look at flag first

bands = 'gri'
models = ['dev','ser','devexp','serexp']
flagcheck = [(2**GetFlag('NEIGHBOUR_FIT'), 2**Get_FinalFlag('neighbor fit'))]
fitflagcheck = [(2**Get_FitFlag('IE_AT_LIMIT'), 2**Get_FinalFlag('m_bulge')),
                (2**Get_FitFlag('RE_AT_LIMIT'), 2**Get_FinalFlag('r_bulge')),
                (2**Get_FitFlag('N_AT_LIMIT'), 2**Get_FinalFlag('n_bulge')),
                (2**Get_FitFlag('EB_AT_LIMIT'), 2**Get_FinalFlag('ba_bulge')),
                (2**Get_FitFlag('ID_AT_LIMIT'), 2**Get_FinalFlag('m_disk')),
                (2**Get_FitFlag('RD_AT_LIMIT'), 2**Get_FinalFlag('r_disk')),
                (2**Get_FitFlag('ED_AT_LIMIT'), 2**Get_FinalFlag('ba_disk'))]
                

for band in bands:
    for model in models:
        table = '%s_band_%s' %(band, model)

        # clear the flag
        cmd = 'update {table} set FinalFlag=0;'.format(table=table)
        print cmd
        cursor.execute(cmd)

        for tmpflag in flagcheck:
            cmd = """update {table} set 
FinalFlag = FinalFlag | {finalval} where (flag & {flagval}) and not (FinalFlag & {finalval});
""".format(table = table, flagval = tmpflag[0], finalval = tmpflag[1])
            print cmd
            cursor.execute(cmd)

        for tmpflag in fitflagcheck:
            cmd = """update {table} set 
FinalFlag = FinalFlag | {finalval} where (FitFlag & {flagval}) and not (FinalFlag & {finalval});
""".format(table = table, flagval = tmpflag[0], finalval = tmpflag[1])
            print cmd
            cursor.execute(cmd)

