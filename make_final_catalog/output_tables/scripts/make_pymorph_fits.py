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

from mysql.mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys
from table_defs import *

def get_table(ext_dict, suffix,mysqltable, Table_name, model='none'):
    print ext_dict
    print suffix
    print mysqltable
    print Table_name

    c_fit = []
    for column in ext_dict.get_data('all'):
        # construct the query
        cmd = 'Select '
        addstr= ''
        cmd += column[3].format(band=suffix)
        for pref in ['c','d', 'f']:
            if '%s.' %pref in column[3]:
                tmp_table = mysqltable[pref]
                break
        else :
            tmp_table = mysqltable['blank']

        if 'f.' in column[3]:
            if column[0]=='finalflag':
                addstr = "where f.model = '%s' and f.band = '%s' and f.ftype = 'u' "%(model, suffix)
            elif column[0]=='autoflag':
                addstr = "where f.model = '%s' and f.band = '%s' and f.ftype = 'r' "%(model, suffix)
        cmd += ' from %s %s order by galcount;' %(tmp_table,addstr)

        print cmd
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


if __name__=="__main__":

    save_loc = '/home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/'
    this_dir = os.getcwd()

    dba = 'catalog'
    pwd = 'pymorph'
    usr = 'pymorph'

    cursor = mysql_connect(dba, usr, pwd)

    band = 'r'

    tablename = 'ModTab'
    table = {'blank':'r_band_fit', 'c':'CAST as c ','d':'DERT as d ',
             'f':'Flags_optimize as f '}
    data_dict = meert[0]
    ext_names ='ModTab Table'

    # Now generate the fits image
    fits_file = save_loc + tablename+'.fits'
    if 0:
        tabs = []
        tabs.append(get_table(data_dict, band, table, ext_names))

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

    band = 'r'

    tablename = 'ModTabModels'
    data_dict = meert_models[0]
    ext_names ='ModTab Table'

    # Now generate the fits image
    fits_file = save_loc + tablename+'.fits'

    tabs = []
    for model in ['dev','ser','devexp','serexp']:
        table = {'blank':'r_band_%s' %model, 'c':'CAST as c ','d':'DERT as d ',
                 'f':'Flags_optimize as f '}
        ext_names ='ModTab %s Table' %model

        tabs.append(get_table(data_dict, band, table, ext_names, model=model))
    
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


#('ModTabmodels','r_band',CAST_models, ('CASTmodels g band','CASTmodels r band','CASTmodels i band'))]:


