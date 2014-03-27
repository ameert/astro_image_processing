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

savepath = '/home/ameert/fit_catalog/output_tables/fits/ra_dec_'
this_dir = os.getcwd()

dba = 'catalog'
pwd = 'pymorph'
usr = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

bands = 'r'

casgm_entries = [ ('galcount','1J',''), ('C','1E',''),('C_err','1E',''),
                  ('A','1E',''),('A_err','1E',''),('A_flag','1E',''),
                  ('image_A','1E',''),('back_A','1E',''),('A_20','1E',''),
                  ('A_20_with_zsum','1E',''),('S','1E',''),('S_err','1E',''),
                  ('r20','1E',''),('r20e','1E',''),('r50','1E',''),
                  ('r50e','1E',''),('r80','1E',''),('r80e','1E',''),
                  ('r90','1E',''),('r90e','1E',''),
                  ('extraction_radius','1E',''),('G','1E',''),
                  ('G_res','1E',''),('G80','1E',''),('G50','1E',''),
                  ('G20','1E',''),('M','1E',''),('M_res','1E',''),
                  ('M80','1E',''),('M50','1E',''),('M20','1E','')
                  ]

# Now generate the fits image
fits_file = savepath +'casgm_values.fits'
c_fit = []
    
data_dict = meert_table(casgm_entries)

for column in data_dict.get_data('all'):
    print column

    # construct the query
    cmd = 'Select '
    cmd += column[3] 

    cmd += ' from raw_catalog_fits.CASGM_r_agmresult as a order by a.galcount;' 

    if int(column[1][0]) ==3:
        data = cursor.get_data(cmd)
    else:
        data, = cursor.get_data(cmd) 

    data = np.array(data).T
    print data.shape
    c_fit.append(pyfits.Column(name=column[0], format=column[1], unit=column[2], array=data))


tbhdu = pyfits.new_table(c_fit)

tbhdu.header.add_blank(' ')
tbhdu.header.add_history('Table created on '+str(datetime.date.today()))
tbhdu.header.add_history('Table created by Alan Meert')
tbhdu.header.add_history('Dept. of Physics, University of Pennsylvania')
tbhdu.header.add_history('email: ameert-at-sas.upenn.edu')
tbhdu.header.add_blank(' ')
tbhdu.header.add_comment('See Meert et al. (2013),Meert et al. (2014) for More Explanation')

hdu = pyfits.PrimaryHDU(np.array([0]))
hdu.header.add_blank(' ')
hdu.header.add_history('Table created on '+str(datetime.date.today()))
hdu.header.add_history('Table created by Alan Meert')
hdu.header.add_history('Dept. of Physics, University of Pennsylvania')
hdu.header.add_history('email: ameert-at-sas.upenn.edu')
hdu.header.add_blank(' ')
hdu.header.add_comment('The Extension of this fits file contains the CASgm parameter data')
hdu.header.add_comment('See Meert et al. (2013),Meert et al. (2014) for More Explanation')

thdulist = pyfits.HDUList([hdu, tbhdu])
thdulist.writeto(fits_file, clobber =1)

