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
from make_pymorph_fits import get_table


save_loc = '/home/ameert/git_projects/alans-image-processing-pipeline/make_final_catalog/output_tables/fits/UPenn_PhotDec_'
this_dir = os.getcwd()


dba = 'catalog'
pwd = 'pymorph'
usr = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)


bands = 'gri'

if __name__=="__main__":
#    for tablename, table, data_dict,ext_names in [('CAST','CAST', CAST, ('CAST Table')),('H2011','M2010', H2010, ('H2010 Table',)),('CASTmodels','CAST',CAST_models, ('CASTmodels g band','CASTmodels r band','CASTmodels i band')),('UKIDSS','UKIDSS',UKIDSS, ('nonParam', 'Y band','J1 band','H band','K band')),('GALEX','GALEX',GALEX, ('nonParam', 'nuv band','fuv band')),]:
    for tablename, table, data_dict,ext_names in [('JHU','JHU_matches',JHU_matches, ('JHU matching data')), ('YANG','YANG',YANG, ('YANG matching data')),]:
        
        table_pre = {'m':' M2010 as m ', 'c':' CAST as c ',
                  'd':' DERT as d ',  'u':' UKIDSS as u ',  'g':' GALEX as g '
                     ,  'j':' JHU_matches as j ' ,  'y':' yang_groupsC as y '}

        # Now generate the fits image
        fits_file = save_loc + tablename+'.fits'


        tabs = []
        #all tables are band independant except for CAST_models
        if tablename=='CASTmodels':
            for a in zip(data_dict, ext_names, ['_g','_r','_i']):
                tabs.append(get_table(a[0], a[2],table, a[1]))
        elif tablename=='UKIDSS':
            for a in zip(data_dict, ext_names, ['','Y','J1',
                                                'J2', 'H', 'K']):
                table_pre['blank']=table_pre['u']
                tabs.append(get_table(cursor, a[0], a[2],  table_pre, a[1]))
        elif tablename=='GALEX':
            for a in zip(data_dict, ext_names, ['','nuv','fuv']):
                table_pre['blank']=table_pre['g']
                tabs.append(get_table(cursor, a[0], a[2],  table_pre, a[1]))
        elif tablename=='JHU':
            table_pre['blank']=table_pre['j']
            for a in zip(data_dict, ext_names, ['']):
                tabs.append(get_table(cursor, a[0], a[2],  table_pre, a[1]))
        elif tablename=='YANG':
            table_pre['blank']=table_pre['y']
            for a in zip(data_dict, ext_names, ['',]):
                tabs.append(get_table(cursor, a[0], a[2],  table_pre, a[1]))
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

