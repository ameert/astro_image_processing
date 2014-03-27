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

from mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys
from table_defs import *

save_loc = '/home/ameert/fit_catalog/output_tables/fits/'
this_dir = os.getcwd()

dba = 'catalog'
pwd = 'pymorph'
usr = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

bands = 'gri'

for table, data_dict in [('CAST', CAST), ('M2010', M2010),('DERT', DERT)]:
    # Now generate the fits image
    fits_file = save_loc + table+'.fits'
    c_fit = []

    for column in data_dict.get_data('all'):
        # construct the query
        cmd = 'Select '
        if int(column[1][0]) ==3:
            cmd += ', '.join(['%s_%s' %(column[3], band) for band in bands])
        else:
            cmd += column[3] 

        cmd += ' from %s order by galcount;' %table

        if int(column[1][0]) ==3:
            data = cursor.get_data(cmd)
        else:
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
    tbhdu.header.add_comment('See Meert et al. (2014) for Table Explanation')

    hdu = pyfits.PrimaryHDU(np.array([0]))
    hdu.header.add_blank(' ')
    hdu.header.add_history('Table created on '+str(datetime.date.today()))
    hdu.header.add_history('Table created by Alan Meert')
    hdu.header.add_history('Dept. of Physics, University of Pennsylvania')
    hdu.header.add_history('email: ameert-at-sas.upenn.edu')
    hdu.header.add_blank(' ')
    hdu.header.add_comment('The Extension of this fits file contains the %s data' %table)
    hdu.header.add_comment('See Meert et al. (2014) for Table Explanation')

    thdulist = pyfits.HDUList([hdu, tbhdu])
    thdulist.writeto(fits_file, clobber =1)

