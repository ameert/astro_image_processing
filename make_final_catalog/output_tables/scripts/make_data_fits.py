#++++++++++++++++++++++++++
#
# TITLE: table_functions
#
# PURPOSE: write out tables
#          of data to fits version
#
# INPUTS: NONE
#
# OUTPUTS: fits files
#
# PROGRAM CALLS: mysql_class, table_defs
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 25 MAY 2011
#
#-----------------------------------

from mysql.mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys
from table_defs import *

save_loc = '/home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/'
this_dir = os.getcwd()

dba = 'catalog'
pwd = 'pymorph'
usr = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

bands = 'gri'

def get_table(ext_dict, suffix,mysqltable, Table_name):
    c_fit = []
    for column in ext_dict.get_data('all'):
        # construct the query
        cmd = 'Select '
        cmd += column[3]+suffix
        cmd += ' from %s order by galcount;' %mysqltable

        data, = cursor.get_data(cmd) 

        data = np.array(data).T
        c_fit.append(pyfits.Column(name=column[0], format=column[1], unit=column[2], array=data))
    
    tbhdu = pyfits.new_table(c_fit)

    
    tbhdu.header.add_blank(' ')
    tbhdu.header.add_history('Table created on '+str(datetime.date.today()))
    tbhdu.header.add_history('Table created by Alan Meert')
    tbhdu.header.add_history('Dept. of Physics, University of Pennsylvania')
    tbhdu.header.add_history('email: ameert-at-sas.upenn.edu')
    tbhdu.header.add_blank(' ')
    
    tbhdu.header.add_comment(Table_name)
    tbhdu.header.add_comment('See Meert et al. (2014) for Table Explanation')
    return tbhdu

for tablename, table, data_dict,ext_names in [('CAST','CAST', CAST, ('CAST Table')),('H2011','M2010', H2010, ('H2010 Table',)),('CASTmodels','CAST',CAST_models, ('CASTmodels g band','CASTmodels r band','CASTmodels i band'))]:

    # Now generate the fits image
    fits_file = save_loc + tablename+'.fits'
    
    tabs = []
    #all tables are band independant except for CAST_models
    if tablename=='CASTmodels':
        for a in zip(data_dict, ext_names, ['_g','_r','_i']):
            tabs.append(get_table(a[0], a[2],table, a[1]))
    else:
        for a in zip(data_dict, ext_names, ['']):
            tabs.append(get_table(a[0], a[2],table, a[1]))

    hdu = pyfits.PrimaryHDU(np.array([0]))
    hdu.header.add_blank(' ')
    hdu.header.add_history('Table created on '+str(datetime.date.today()))
    hdu.header.add_history('Table created by Alan Meert')
    hdu.header.add_history('Dept. of Physics, University of Pennsylvania')
    hdu.header.add_history('email: ameert-at-sas.upenn.edu')
    hdu.header.add_blank(' ')
    hdu.header.add_comment('The Extension(s) of this fits file contain the %s data' %tablename)
    hdu.header.add_comment('See Meert et al. (2014) for Table Explanation')

    thdulist = pyfits.HDUList([hdu]+tabs)
    thdulist.writeto(fits_file, clobber =1)

