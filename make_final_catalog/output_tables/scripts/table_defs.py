#++++++++++++++++++++++++++
#
# TITLE: table_defs
#
# PURPOSE: This contains the information 
#          required to make fits tables for 
#          all the DR7 data
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
# DATE:
#
#-----------------------------------

import numpy as np
import pylab as pl
import scipy as sc

class meert_table():
    """this class holds the table info used to access mysql and write to 
    fits tables for distribution"""
    def __init__(self, input_entries = []):
        self.counter = 0
        self.data = {}
        
        for entry in input_entries:
            try:
                mysqlname = entry[3]
            except IndexError:
                mysqlname = entry[0]
            self.add_entry(entry[0],entry[1],entry[2],mysqlname)

        return
    
    def add_entry(self, fitsname, fitstype, fitsunit, mysqlname):
        self.counter +=1
        self.data[self.counter] = [fitsname, fitstype, fitsunit, mysqlname]
        return

    def get_fitsnames(self):
        return self.get_data(0)
    
    def get_fitstypes(self):
        return self.get_data(1)
    
    def get_fitsunits(self):
        return self.get_data(2)
    
    def get_mysqlnames(self):
        return self.get_data(3)
    
    def get_data(self, unitnum):
        keys = list(self.data.keys())
        keys.sort()
        if unitnum == 'all':
            values = [self.data[a] for a in keys]
        else:
            values = [self.data[a][unitnum] for a in keys]
        return values



CAST_entries = [ ('galcount','1J',''), ('objid','1K',''),('badflag','1J',''), 
                 ('nchild','1I',''), ('run','1I',''), ('rerun','1I',''), 
                 ('camCol','1I',''), ('field','1I',''), ('obj','1I',''), 
                 ('stripe','1J',''), ('startmu','1J','arcsec'),
                 ('specobjid','1K',''),  ('plate','1I',''), 
                 ('mjd','1J','MJD'), ('fiberid','1I',''),
                 ('ra','1E','decimal degrees', 'ra_gal'), 
                 ('dec','1E','decimal degrees', 'dec_gal'), 
                 ('z','1E',''), ('veldisp','1E','km/s'), 
                 ('veldispErr','1E','km/s'), ('eclass','1E',''),
                 ('p_el_debiased','1E',''), ('p_cs_debiased','1E',''), 
                 ('petroR90','3E','arcsec'), ('petroR50','3E','arcsec'), 
                 ('petroMag','3E','mag'), ('petroMagErr','3E','mag'), 
                 ('ModelMagErr','3E','mag'), ('ModelMag','3E','mag'), 
                 ('devRad','3E','arcsec'), ('devab','3E',''),
                 ('devmag','3E','mag'), ('fracdev','3E',''),
                 ('extinction','3E','mag'),
                 ('aa','3E','mag'), ('kk','3E','mag'),
                 ('airmass','3E',''), ('gain','3E','electrons/DN'),
                 ('darkvariance','3E',''), ('sky','3E','magnitude/arcsec^2'),
                 ('skyErr','3E','magnitude/arcsec^2'),
                 ('psfWidth','3E','arcsec'), ('rowc','3E','pixels'),
                 ('colc','3E','pixels') ]
CAST = meert_table(CAST_entries)

M2010_entries =[ ('galcount','1J',''), ('id_marc','1J',''), 
                 ('specObjID','1K','','specObjID_marc'),
                 ('ra','1E','decimal degrees', 'ra_marc'), 
                 ('dec','1E','decimal degrees','dec_marc'),
                 ('z','1E','','z_marc'), ('probaE','1E',''), 
                 ('probaEll','1E',''), ('probaS0','1E',''),
                 ('probaSab','1E',''), ('probaScd','1E',''), 
                 ('ask_class','1E','') ]
M2010 = meert_table(M2010_entries)


DERT_entries = [ ('galcount','1J',''), ('dismod' ,'1E', 'mag'),
                 ('kpc_per_arcsec' ,'1E', 'kpc per arcsec'), 
                 ('Vmax' ,'1E', 'Mpc^3'), ('SN' ,'3E', ''),  
                 ('kcorr' ,'3E', 'mag')
                 ]

DERT = meert_table(DERT_entries)


Meert_entries = [ ('galcount','1J',''),
                  ('SexMag','3E','mag'),
                  ('SexMag_Err','3E','mag'),
                  ('Sex_Rad','3E','arcsec', 'SexHrad'),
                  ('SexSky','3E','mag/arcsec^2'),
                  ('C','3E',''), ('C_err','3E',''),
                  ('A','3E',''), ('A_err','3E',''),
                  ('S','3E',''), ('S_err','3E',''),
                  ('G','3E',''), ('M20','3E',''),
                  ('m_tot', '3E', 'mag'), ('BT','3E',''), 
                  ('m_bulge','3E','mag'),
                  ('m_bulge_err','3E','mag'),
                  ('r_bulge','3E','arcsec'), 
                  ('r_bulge_err','3E','arcsec'),
                  ('n_bulge','3E',''), ('n_bulge_err','3E',''),
                  ('ba_bulge','3E',''), ('ba_bulge_err','3E',''),
                  ('pa_bulge','3E','degrees'), ('pa_bulge_err','3E','degrees'),
                  ('xctr_bulge','3E','pixels'),
                  ('xctr_bulge_err','3E','pixels'),
                  ('yctr_bulge','3E','pixels'),
                  ('yctr_bulge_err','3E','pixels'),
                  ('m_disk','3E','mag'),
                  ('m_disk_err','3E','mag'),
                  ('r_disk','3E','arcsec'), 
                  ('r_disk_err','3E','arcsec'),
                  ('ba_disk','3E',''), ('ba_disk_err','3E',''),
                  ('pa_disk','3E','degrees'), ('pa_disk_err','3E','degrees'),
                  ('xctr_disk','3E','pixels'),
                  ('xctr_disk_err','3E','pixels'),
                  ('yctr_disk','3E','pixels'),
                  ('yctr_disk_err','3E','pixels'),
                  ('fit','3E',''), ('flag','3E',''),
                  ('chi2nu','3E',''), ('GalSky','3E','mag/arcsec^2'),
                  ]



tables = {}



tables['NYUT'] = {1: [ 'galcount', '1J', ''],2:['dis_arcsec', '1E','arcsec'],3:['Id_nyu', '1J', ''],
                  4:['ra_gal',  '1E', 'decimal degrees'],5:['dec_gal',  '1E', 'decimal degrees'],
                  6:['A',  '3E', 'nanomaggies/arcsec' ],
                  7:[ 'r0',  '3E',  'arcsec'], 8:['n_ser',  '3E', ''] }
 
tables['simard_sample'] = {1 :['galcount','1J',''], 2 :['objid','1K',''], 3 :['z','1E',''], 4 :['SpecClass','1J',''],
                           5 :['kpc_per_arcsec','1E','kpc/arcsec'], 6 :['V_max','1E',''], 7 :['f_test_ser','1E',''],
                           8 :['f_test_devexp','1E',''], 9 :['Ie_ser','1E','mag'], 10 :['Ie_devexp','1E','mag'],
                           11 :['Ie_serexp','1E','mag'], 12 :['Ie_err_ser','1E','mag'], 13 :['Ie_err_devexp','1E','mag'],
                           14 :['Ie_err_serexp','1E','mag'], 15 :['Id_ser','1E','mag'], 16 :['Id_devexp','1E','mag'],
                           17 :['Id_serexp','1E','mag'], 18 :['Id_err_ser','1E','mag'], 19 :['Id_err_devexp','1E','mag'],
                           20 :['Id_err_serexp','1E','mag'], 21 :['BT_ser','1E',''], 22 :['BT_devexp','1E',''],
                           23 :['BT_serexp','1E',''], 24 :['BT_err_ser','1E',''], 25 :['BT_err_devexp','1E',''],
                           26 :['BT_err_serexp','1E',''], 27 :['re_kpc_ser','1E','kpc'], 28 :['re_kpc_devexp','1E','kpc'],
                           29 :['re_kpc_serexp','1E','kpc'], 30 :['re_err_kpc_ser','1E','kpc'], 
                           31 :['re_err_kpc_devexp','1E','kpc'], 32 :['re_err_kpc_serexp','1E','kpc'],
                           33 :['eb_ser','1E',''], 34 :['eb_devexp','1E',''], 35 :['eb_serexp','1E',''],
                           36 :['eb_err_ser','1E',''], 37 :['eb_err_devexp','1E',''], 38 :['eb_err_serexp','1E',''],
                           39 :['rd_kpc_ser','1E','kpc'], 40 :['rd_kpc_devexp','1E','kpc'],
                           41 :['rd_kpc_serexp','1E','kpc'], 42 :['rd_err_kpc_ser','1E','kpc'],
                           43 :['rd_err_kpc_devexp','1E','kpc'], 44 :['rd_err_kpc_serexp','1E','kpc'],
                           45 :['n_ser','1E',''], 46 :['n_devexp','1E',''], 47 :['n_serexp','1E',''],
                           48 :['n_err_ser','1E',''], 49 :['n_err_devexp','1E',''], 50 :['n_err_serexp','1E',''],
                           51 :['absmag_r_tot_ser','1E','mag'], 52 :['absmag_r_tot_devexp','1E','mag'],
                           53 :['absmag_r_tot_serexp','1E','mag'], 54 :['absmag_r_tot_ser_err','1E','mag'],
                           55 :['absmag_r_tot_devexp_err','1E','mag'], 56 :['absmag_r_tot_serexp_err','1E','mag'],
                           57 :['re_hl_r_ser','1E','kpc'], 58 :['re_hl_r_devexp','1E','kpc'],
                           59 :['re_hl_r_serexp','1E','kpc'], 60 :['ed_ser','1E',''], 61 :['ed_devexp','1E',''],
                           62 :['ed_serexp','1E','']}


tables['DERT'] = {1: ['galcount','1J',''], 2:['dismod' ,'1E', ''],  3:['DERT_flag' ,'1K',''],
                  4:['mag_zp_g','1E', 'mag'],   5:['mag_zp_r','1E' , 'mag'], 6:['mag_zp_i','1E', 'mag'],
                  7:['total_cor_g' ,'1E', 'mag'], 8:['total_cor_r' ,'1E', 'mag'], 9:['total_cor_i' ,'1E', 'mag'],
                  10:['kcorr_g' ,'1E', 'mag'], 11:['kcorr_r' ,'1E', 'mag'], 12:['kcorr_i'  ,'1E', 'mag']}

tables['UKIDSS'] = {1: ['galcount','1J',''],  2:['objid','1K',''], 3:['SourceID','1K', ''], 4:['FrameSetID', '1K',  ''],  
                    5:['ra_ukidss' , '1D', 'radians'],  6:['dec_ukidss' , '1D', 'radians'],  7:['distance_arcmin' , '1E', 'arcmins'],  
                    8:['epoch', '1K', 'years'], 9:['PriOrSec', '1E', ''], 10:['PGalaxy', '1E', ''], 11:['eBV', '1E', ''],
                    12:['a_Y', '1E', 'mag'], 13:['a_J', '1E', 'mag'],  14:['a_H', '1E', 'mag'],  15:['a_K', '1E', 'mag'], 
                    16:['PetroMag_Y', '1E', 'mag'], 17:['PetroMagErr_Y', '1E', 'mag'], 18:['SerMag2D_Y', '1E', 'mag'],   
                    19:['SerMag2DErr_Y', '1E', 'mag'], 20:['AperMag3_Y', '1E', 'mag'], 21:['AperMag3Err_Y', '1E', 'mag'],   
                    22:['Ell_Y', '1E', ''], 23:['PA_Y', '1E', 'degrees'],  24:['ErrBits_Y', '1J', ''], 25:['Deblend_Y', '1J', ''],       
                    26:['PetroMag_J1', '1E', 'mag'], 27:['PetroMagErr_J1', '1E', 'mag'],  28:['SerMag2D_J1', '1E', 'mag'],     
                    29:['SerMag2DErr_J1', '1E', 'mag'],  30:['AperMag3_J1', '1E', 'mag'], 31:['AperMag3Err_J1', '1E', 'mag'],  
                    32:['Ell_J1', '1E', ''], 33:['PA_J1', '1E', 'degrees'],  34:['ErrBits_J1', '1E', ''], 35:['Deblend_J1', '1E', ''],      
                    36:['PetroMag_J2', '1E', 'mag'], 37:['PetroMagErr_J2', '1E', 'mag'],  38:['SerMag2D_J2', '1E', 'mag'],     
                    39:['SerMag2DErr_J2', '1E', 'mag'], 40:['AperMag3_J2', '1E', 'mag'], 41:['AperMag3Err_J2', '1E', 'mag'],  
                    42:['Ell_J2', '1E', ''], 43:['PA_J2', '1E', 'degrees'],  44:['ErrBits_J2', '1J', ''], 45:['Deblend_J2', '1J', ''],      
                    46:['PetroMag_H', '1E', 'mag'], 47:['PetroMagErr_H', '1E', 'mag'],   48:['SerMag2D_H', '1E', 'mag'],      
                    49:['SerMag2DErr_H', '1E', 'mag'],  50:['AperMag3_H', '1E', 'mag'],      51:['AperMag3Err_H', '1E', 'mag'],   
                    52:['Ell_H', '1E', ''], 53:['PA_H', '1E', 'degrees'],  54:['ErrBits_H', '1J', ''], 55:['Deblend_H', '1J', ''],       
                    56:['PetroMag_K', '1E', 'mag'], 57:['PetroMagErr_K', '1E', 'mag'],   58:['SerMag2D_K', '1E', 'mag'],      
                    59:['SerMag2DErr_K', '1E', 'mag'],  60:['AperMag3_K', '1E', 'mag'],  61:['AperMag3Err_K', '1E', 'mag'],   
                    62:['Ell_K', '1E', ''], 63:['PA_K', '1E', 'degrees'], 64:['ErrBits_K', '1J', ''], 65:['Deblend_K', '1J', '']
                    }

tables['GALEX'] = {1:['galcount','1J',''],2:['gid', '1K', ''],
                   3:['photoExtractID',  '1K', ''], 4:['imgID', '1K', ''],  
                   5:['band',   '1I', ''], 6:['survey', '10A',  ''], 
                   7:['nuvExposureTime', '1E',  'seconds'],
                   8:['fuvExposureTime', '1E', 'seconds'],
                   9:['ra_galex',  '1E', 'deg'], 10:['dec_galex', '1E', 'deg'],
                   11:['ra_galex_band_merged', '1E', 'deg'],
                   12:['dec_galex_band_merged', '1E', 'deg'],
                   13:['misc_flags', '1J', ''],14:['primary_flag', '1J', ''],
                   15:['galextype',   '1J', ''], 16:['nuv_det_x', '1J', 'pix'],
                   17:['nuv_det_y', '1J', 'pix'],18:['fuv_det_x', '1J', 'pix'],
                   19:['fuv_det_y', '1J', 'pix'], 20:['nuv_mag', '1E', 'mag'],
                   21:['nuv_magerr', '1E', 'mag'], 22:['fuv_mag',  '1E','mag'],
                   23:['fuv_magerr',  '1E' ,'mag'], 
                   24:['nuv_artifact', '1J',''], 25:['fuv_artifact','1J', ''],
                   26:['nuv_skybg', '1E', 'counts'], 
                   27:['fuv_skybg','1E', 'counts'],  
                   28:['e_bv','1E', 'mag'], 29:['nuv_rad50','1E', 'arcsec'],
                   30:['nuv_rad90','1E', 'arcsec'], 
                   31:['fuv_rad50', '1E' , 'arcsec'],
                   32:['fuv_rad90','1E' , 'arcsec'],
                   33:['IsThereSpectrum', '1J', ''],
                   34:['GToSDstArcSec','1E' 'arcsec'],
                   35:['distanceRank', '1J', ''], 
                   36:['reverseDistanceRank', '1J', ''],
                   37:['multipleMatchCount', '1J', ''], 
                   38:['reverseMultipleMatchCount', '1J', ''], 
                   39:['SDSSobjid',  '1K', ''],40:['SDSStype', '1J', ''],
                   41:['SDSSprobPSF', '1E', ''],
                   42:['nuv_fileNPath',  '125A', ''], 
                   43:['n_zpmag', '1E', 'mag'],
                   44:['f_zpmag', '1E', 'mag'], 45:['nsxsfwhm','1E', 'arcsec'], 
                   46:['fsxsfwhm','1E', 'arcsec']
                   }

#count = 0
#for a_col, b_col, c_col in zip(r_full_cols, r_full_fits_format, r_full_fits_units):
#    count +=1
#    print "%d :['%s','%s','%s']," %(count, a_col, b_col,  c_col)

#sys.exit()
