#++++++++++++++++++++++++++
#
# TITLE: table_functions
#
# PURPOSE: write out tables
#          of data to text version
#
# INPUTS: NONE
#
# OUTPUTS: txt files
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
# DATE: 25 MAY 2011
#
#-----------------------------------

from mysql_class import *
import os
import itertools
import pyfits
import datetime

import sys


this_dir = os.getcwd()

dba = 'pymorph'
pwd = 'pymorph9455'
usr = 'pymorph'

cursor = mysql_connect(dba, usr, pwd, 'shredder')

tables = ['CAST', 'M2010', 'NYUT', 'SSDR6', 'simard_sample', 'r_full_detail']

CAST_cols = ['galcount','spec1_phot0','badflag','objid','run','rerun','camCol','field','obj','stripe','startmu','ra_gal','dec_gal','z','specobjid','plate','mjd','fiberid','veldisp','veldispErr','eclass','devRad_u','devRad_g','devRad_r','devRad_i','devRad_z','devab_u','devab_g','devab_r','devab_i','devab_z','devmag_u','devmag_g','devmag_r','devmag_i','devmag_z','dered_u','dered_g','dered_r','dered_i','dered_z','fracdev_u','fracdev_g','fracdev_r','fracdev_i','fracdev_z','petroMag_u','petroMag_g','petroMag_r','petroMag_i','petroMag_z','petroR90_u','petroR90_g','petroR90_r','petroR90_i','petroR90_z','petroR50_u','petroR50_g','petroR50_r','petroR50_i','petroR50_z','extinction_u','extinction_g','extinction_r','extinction_i','extinction_z','aa_u','aa_g','aa_r','aa_i','aa_z','kk_u','kk_g','kk_r','kk_i','kk_z','airmass_u','airmass_g','airmass_r','airmass_i','airmass_z','p_el_debiased','p_cs_debiased','spiral','elliptical','uncertain','rowc_u','rowc_g','rowc_r','rowc_i','rowc_z','colc_u','colc_g','colc_r','colc_i','colc_z']  

CAST_fits_format = ['1J','1I','1J','1K','1I','1I','1I','1I','1I','1I','1J','1E','1E','1E','1K','1I','1J','1I','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1I','1I','1I','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E']

CAST_fits_units = ['','','','','','','','','','','','decimal degrees','decimal degrees','','','','','','km/s','km/s','','arcsec','arcsec','arcsec','arcsec','arcsec','','','','','','mag','mag','mag','mag','mag','mag','mag','mag','mag','mag','','','','','','mag','mag','mag','mag','mag','arcsec','arcsec','arcsec','arcsec','arcsec','arcsec','arcsec','arcsec','arcsec','arcsec','mag','mag','mag','mag','mag','mag','mag','mag','mag','mag','mag','mag','mag','mag','mag','mag','mag','mag','mag','mag','','','','','','pixels','pixels','pixels','pixels','pixels','pixels','pixels','pixels','pixels','pixels']  

M2010_cols = ['galcount','id_marc','specObjID_marc','ra_marc','dec_marc','z_marc','probaE','probaEll','probaS0','probaSab','probaScd','ask_class']

M2010_fits_format = ['1J','1J','1K','1E','1E','1E','1E','1E','1E','1E','1E','1E']

M2010_fits_units = ['','','','decimal degrees','decimal degrees','','','','','','','']

NYUT_cols = [ 'galcount','dis','Id_nyu','ra_nyu','dec_nyu','A_u','A_g','A_r','A_i','A_z','r0_u','r0_g','r0_r','r0_i','r0_z','n_ser_u','n_ser_g','n_ser_r','n_ser_i','n_ser_z']

NYUT_fits_format = ['1J', '1E', '1J', '1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E']

NYUT_fits_units = ['','arcsec','','decimal degrees','decimal degrees','nanomaggies/arcsec','nanomaggies/arcsec','nanomaggies/arcsec','nanomaggies/arcsec','nanomaggies/arcsec','arcsec','arcsec','arcsec','arcsec','arcsec','','','','','']

SSDR6_cols = ['galcount','plate_dr6','mjd_dr6','fiberID_dr6','ra_dr6','dec_dr6','kcorrNg','kcorrNr','BkLRGg','BkLRGr','Bkmu','Bkmg','Bkmr','Bkpu','Bkpg','Bkpr','z_dr6','gmr','gmrN','gmrpetro','umr','umrPetro','Vmaxwti','dr6vdisp','logS','logRedeV','logRedeV_g','regrad','logRePetro','absmagdev','absmagpetro','sdsslogMstar','logRetot','absmagtot','sdsslogMstartot','ab_dev_g','ab_dev_r','fracdev_r_dr6','cir','Ga50','Ga50z0','Ga16','Ga84','Gz50']

SSDR6_fits_format = ['1J', '1I', '1J', '1I', '1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E']

SSDR6_fits_units = ['','','','','decimal degrees','decimal degrees','mag','mag','','','','','','','','','','mag','mag','mag','mag','mag','','km/s','','','','','','mag','mag','','','mag','','','','','','','','','','']

simard_sample_cols = ['galcount','objid','z','SpecClass','arcsec_per_kpc','V_max','f_test_ser','f_test_devexp' ,'Ie_ser','Ie_devexp','Ie_serexp','Ie_err_ser','Ie_err_devexp','Ie_err_serexp','Id_ser','Id_devexp','Id_serexp','Id_err_ser','Id_err_devexp','Id_err_serexp','BT_ser','BT_devexp','BT_serexp','BT_err_ser','BT_err_devexp','BT_err_serexp','re_kpc_ser','re_kpc_devexp','re_kpc_serexp','re_err_kpc_ser','re_err_kpc_devexp','re_err_kpc_serexp','eb_ser','eb_devexp','eb_serexp','eb_err_ser','eb_err_devexp','eb_err_serexp','rd_kpc_ser','rd_kpc_devexp','rd_kpc_serexp','rd_err_kpc_ser','rd_err_kpc_devexp','rd_err_kpc_serexp','n_ser','n_devexp','n_serexp','n_err_ser','n_err_devexp','n_err_serexp']

simard_sample_fits_format = ['1J','1K','1E','1J','1E','1E','1E','1E' ,'1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E','1E']

simard_sample_fits_units = ['','','','','arcsec/kpc','','','' ,'mag','mag','mag','mag','mag','mag','mag','mag','mag','mag','mag','mag','','','','','','','kpc','kpc','kpc','kpc','kpc','kpc','','','','','','','kpc','kpc','kpc','kpc','kpc','kpc','','','','','','']

r_full_cols = ['galcount','Name_r', 'Date', 'Filter', 'z', 'dis_modu', 'MorphType', 'SexSky', 'mag_auto', 'mag_err_auto', 'sex_halflight_pix', 'zeropoint_pymorph', 'C', 'C_err', 'A', 'A_err', 'S', 'S_err', 'G', 'M', 'Comments', 'Ie_Dev', 'Ie_DevExp', 'Ie_Ser', 'Ie_SerExp', 'Ie_err_Dev', 'Ie_err_DevExp', 'Ie_err_Ser', 'Ie_err_SerExp', 'AbsMagBulge_Dev', 'AbsMagBulge_DevExp', 'AbsMagBulge_Ser', 'AbsMagBulge_SerExp', 're_pix_Dev', 're_pix_DevExp', 're_pix_Ser', 're_pix_SerExp', 're_err_pix_Dev', 're_err_pix_DevExp', 're_err_pix_Ser', 're_err_pix_SerExp', 're_kpc_Dev', 're_kpc_DevExp', 're_kpc_Ser', 're_kpc_SerExp', 're_err_kpc_Dev', 're_err_kpc_DevExp', 're_err_kpc_Ser', 're_err_kpc_SerExp', 'n_Dev', 'n_DevExp', 'n_Ser', 'n_SerExp', 'n_err_Dev', 'n_err_DevExp', 'n_err_Ser', 'n_err_SerExp', 'eb_Dev', 'eb_DevExp', 'eb_Ser', 'eb_SerExp', 'eb_err_Dev', 'eb_err_DevExp', 'eb_err_Ser', 'eb_err_SerExp', 'bboxy_Dev', 'bboxy_DevExp', 'bboxy_Ser', 'bboxy_SerExp', 'bboxy_err_Dev', 'bboxy_err_DevExp', 'bboxy_err_Ser', 'bboxy_err_SerExp', 'Id_Dev', 'Id_DevExp', 'Id_Ser', 'Id_SerExp', 'Id_err_Dev', 'Id_err_DevExp', 'Id_err_Ser', 'Id_err_SerExp', 'AbsMagDisk_Dev', 'AbsMagDisk_DevExp', 'AbsMagDisk_Ser', 'AbsMagDisk_SerExp', 'rd_pix_Dev', 'rd_pix_DevExp', 'rd_pix_Ser', 'rd_pix_SerExp', 'rd_err_pix_Dev', 'rd_err_pix_DevExp', 'rd_err_pix_Ser', 'rd_err_pix_SerExp', 'rd_kpc_Dev', 'rd_kpc_DevExp', 'rd_kpc_Ser', 'rd_kpc_SerExp', 'rd_err_kpc_Dev', 'rd_err_kpc_DevExp', 'rd_err_kpc_Ser', 'rd_err_kpc_SerExp', 'ed_Dev', 'ed_DevExp', 'ed_Ser', 'ed_SerExp', 'ed_err_Dev', 'ed_err_DevExp', 'ed_err_Ser', 'ed_err_SerExp', 'dboxy_Dev', 'dboxy_DevExp', 'dboxy_Ser', 'dboxy_SerExp', 'dboxy_err_Dev', 'dboxy_err_DevExp', 'dboxy_err_Ser', 'dboxy_err_SerExp', 'BT_Dev', 'BT_DevExp', 'BT_Ser', 'BT_SerExp', 'BT_err_Dev', 'BT_err_DevExp', 'BT_err_Ser', 'BT_err_SerExp', 'BD_Dev', 'BD_DevExp', 'BD_Ser', 'BD_SerExp', 'BD_err_Dev', 'BD_err_DevExp', 'BD_err_Ser', 'BD_err_SerExp', 'fit_Dev', 'fit_DevExp', 'fit_Ser', 'fit_SerExp', 'flag_Dev', 'flag_DevExp', 'flag_Ser', 'flag_SerExp', 'chi2nu_Dev', 'chi2nu_DevExp', 'chi2nu_Ser', 'chi2nu_Serexp', 'GalSky_Dev', 'GalSky_DevExp', 'GalSky_Ser', 'GalSky_SerExp', 'bpa_Dev', 'bpa_DevExp', 'bpa_Ser', 'bpa_Serexp', 'dpa_Dev', 'dpa_DevExp', 'dpa_Ser', 'dpa_SerExp', 'bxc_Dev', 'bxc_DevExp', 'bxc_Ser', 'bxc_SerExp', 'byc_Dev', 'byc_DevExp', 'byc_Ser', 'byc_SerExp', 'dxc_Dev', 'dxc_DevExp', 'dxc_Ser', 'dxc_SerExp', 'dyc_Dev', 'dyc_DevExp', 'dyc_Ser', 'dyc_SerExp']


r_full_fits_format = ['1J','30A', '30A', '20A', '1E', '1E', '1I', '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E', '40A', '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E',  '1E', '1E', '1E', '1E', '1E', '1E', '1E', '1E']


r_full_fits_units = ['','', '', '', '', '', '', 'counts/sec', 'mag', 'mag', 'pixels', 'mag', '', '', '', '', '', '', '', '', '', 'mag', 'mag', 'mag', 'mag', 'mag', 'mag', 'mag', 'mag',  'mag', 'mag', 'mag', 'mag', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'kpc', 'kpc', 'kpc', 'kpc', 'kpc', 'kpc', 'kpc', 'kpc', '', '', '', '',  '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '',  '', '', '', '',  'mag', 'mag', 'mag', 'mag', 'mag', 'mag', 'mag', 'mag',  'mag', 'mag', 'mag', 'mag', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'kpc', 'kpc', 'kpc', 'kpc', 'kpc', 'kpc', 'kpc', 'kpc', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '',  '', '', '', '', 'counts/sec', 'counts/sec', 'counts/sec', 'counts/sec',   'degrees',  'degrees', 'degrees' ,  'degrees',  'degrees',  'degrees',  'degrees', 'degrees', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels', 'pixels']



for curr_col in r_full_cols:
    cmd = "update r_full_detail set "+curr_col+"=-888 where "+curr_col+" is null;"
    cursor.execute(cmd)




for table,cols, fit_format, fit_unit in zip(tables, [CAST_cols, M2010_cols, NYUT_cols, SSDR6_cols, simard_sample_cols, r_full_cols], [CAST_fits_format, M2010_fits_format, NYUT_fits_format, SSDR6_fits_format, simard_sample_fits_format, r_full_fits_format],[CAST_fits_units, M2010_fits_units, NYUT_fits_units, SSDR6_fits_units, simard_sample_fits_units, r_full_fits_units]):

    if table != 'r_full_detail':
        continue
    
    # First write the sql table
    cmd = 'mysqldump -u pymorph -ppymorph9455 -h shredder -r /tmp/'+table + '.sql pymorph ' + table
    os.system(cmd)

    cmd = 'cp /tmp/'+table + '.sql '+this_dir+'/'+table + '.sql '
    os.system(cmd)

    # Now generate the text version
    
    cmd = 'select '
    cmd += ','.join(cols)
    cmd +=' from ' + table + ' order by galcount;' 

    print cmd
    data = cursor.get_data(cmd)

    # open the outfile
    ofile = open(table+'.txt', 'w')
    ofile.write(','.join(cols)+'\n')
    for row in zip(*data):
        row_max = len(row)-1
        for row_col_num, row_col in enumerate(row):
            if row_col_num != row_max:
                row_col = str(row_col) + ','
            else:
                row_col = str(row_col)
            ofile.write(str(row_col))
        ofile.write('\n')
    # close the file
    ofile.close()

    # Now generate the fits image
    fits_file = table+'.fits'

    c_fit = []
    for curr_data, curr_col, curr_format, curr_unit in zip(data, cols, fit_format, fit_unit):
        c_fit.append(pyfits.Column(name=curr_col, format=curr_format, unit=curr_unit, array=curr_data))

    tbhdu = pyfits.new_table(c_fit)

    tbhdu.header.add_blank(' ')
    tbhdu.header.add_history('Table created on '+str(datetime.date.today()))
    tbhdu.header.add_history('Table created by Alan Meert')
    tbhdu.header.add_history('Dept. of Physics, University of Pennsylvania')
    tbhdu.header.add_history('email: ameert-at-sas.upenn.edu')
    tbhdu.header.add_blank(' ')
    tbhdu.header.add_comment('Description of table available upon request')
    print tbhdu.header.ascardlist()
    

    tbhdu.writeto(table+'.fits', clobber =1)
    
