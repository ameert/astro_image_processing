#++++++++++++++++++++++++++
#
# TITLE: table_functions
#
# PURPOSE: write out Pymorph tables
#          of data to FITS version
#
# INPUTS: NONE
#
# OUTPUTS: fits files
#
# PROGRAM CALLS: mysql_class
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 14 MARCH 2013
#
#-----------------------------------

from mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys
from table_defs import *

savepath = '/home/ameert/fit_catalog/output_tables/fits/gama_'
this_dir = os.getcwd()

dba = 'catalog'
pwd = 'pymorph'
usr = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

bands = 'gri'

for model in ['ser','serexp']:#['dev','ser','devexp','serexp']
    # Now generate the fits image
    fits_file = savepath +model+'.fits'
    c_fit = []
    
    data_dict = meert_table(Meert_entries)

    for column in data_dict.get_data('all'):
        # construct the query
        cmd = 'Select '
        if int(column[1][0]) ==3:
            if ('Sex' in column[3]) or (column[3] in ['C','C_err','A','A_err','S','S_err','G', 'M20']):
                cmd += ', '.join(['%s.%s' %(comb[0], column[3]) for comb in zip('def',bands)])
            else:
                cmd += ', '.join(['%s.%s' %(comb[0], column[3]) for comb in zip('abc',bands)])
        else:
            cmd += 'b.'+column[3] 

        cmd += ' from g_band_%s as a, r_gama_%s as b, i_band_%s as c, g_band_fit as d, r_gama_fit as e, i_band_fit as f  where a.galcount = b.galcount and b.galcount = c.galcount and a.galcount = d.galcount and b.galcount = e.galcount and c.galcount = f.galcount order by b.galcount;' %(model,model,model)

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
    tbhdu.header.add_comment('See Meert et al. (2013) for Table Explanation')

    hdu = pyfits.PrimaryHDU(np.array([0]))
    hdu.header.add_blank(' ')
    hdu.header.add_history('Table created on '+str(datetime.date.today()))
    hdu.header.add_history('Table created by Alan Meert')
    hdu.header.add_history('Dept. of Physics, University of Pennsylvania')
    hdu.header.add_history('email: ameert-at-sas.upenn.edu')
    hdu.header.add_blank(' ')
    hdu.header.add_comment('The Extension of this fits file contains the %s data' %model)
    hdu.header.add_comment('See Meert et al. (2013) for Table Explanation')

    thdulist = pyfits.HDUList([hdu, tbhdu])
    thdulist.writeto(fits_file, clobber =1)

