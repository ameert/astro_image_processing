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


CAST_entries = [ [('galcount','1J',''), ('objid','1K',''),
                  ('SDSSIAU','24A','','SDSS_IAU'),('badflag','1J',''), 
                 ('nchild','1I',''), ('mode','1I',''),
                  ('run','1I',''), ('rerun','1I',''), 
                 ('camCol','1I',''), ('field','1I',''), ('obj','1I',''), 
                 ('stripe','1J',''), ('startmu','1J','arcsec'),
                 ('specobjid','1K',''),  ('plate','1I',''), 
                 ('mjd','1J','MJD'), ('fiberid','1I',''),
                 ('ra','1E','decimal degrees', 'ra_gal'), 
                 ('dec','1E','decimal degrees', 'dec_gal'), 
                 ('z','1E',''), ('veldisp','1E','km/s'), 
                 ('veldispErr','1E','km/s'), ('eclass','1E',''),
                 ('p_el_debiased','1E',''), ('p_cs_debiased','1E',''), 
                 ('spiral','1J',''),('elliptical','1J',''),
                 ('uncertain','1J','')],

                 [('petroR90','1E','arcsec'), ('petroR50','1E','arcsec'), 
                 ('petroMag','1E','mag'), ('petroMagErr','1E','mag'), 
                 ('ModelMagErr','1E','mag'), ('ModelMag','1E','mag'), 
                 ('devRad','1E','arcsec'), ('devab','1E',''),
                 ('devmag','1E','mag'),  ('devPhi','1E','degrees'),
                  ('expRad','1E','arcsec'), ('expab','1E',''),
                 ('expmag','1E','mag'), ('expPhi','1E','degrees'),
                  ('fracdev','1E',''),
                 ('extinction','1E','mag'),
                 ('aa','1E','mag'), ('kk','1E','mag'),
                 ('airmass','1E',''), ('gain','1E','electrons/DN'),
                 ('darkvariance','1E',''), ('sky','1E','magnitude/arcsec^2'),
                 ('skyErr','1E','magnitude/arcsec^2'),
                 ('psfWidth','1E','arcsec'), ('rowc','1E','pixels'),
                 ('colc','1E','pixels') ]]

CAST = [meert_table(CAST_entries[0])]

CAST_models = [meert_table(CAST_entries[1]),meert_table(CAST_entries[1]),
               meert_table(CAST_entries[1])]

H2010_entries =[ ('galcount','1J',''), ('id_marc','1J',''), 
                 ('specObjID','1K','','specObjID_marc'),
                 ('ra','1E','decimal degrees', 'ra_marc'), 
                 ('dec','1E','decimal degrees','dec_marc'),
                 ('z','1E','','z_marc'), ('probaE','1E',''), 
                 ('probaEll','1E',''), ('probaS0','1E',''),
                 ('probaSab','1E',''), ('probaScd','1E',''), 
                 ('ask_class','1E','') ]
H2010 = [meert_table(H2010_entries)]


DERT_entries = [ [('galcount','1J',''), ('dismod' ,'1E', 'mag'),
                 ('kpc_per_arcsec' ,'1E', 'kpc per arcsec'), 
                 ('Vmax' ,'1E', 'Mpc^3')],

                 [('SN' ,'1E', ''),  ('kcorr' ,'1E', 'mag')]
                 ]

DERT = [meert_table(DERT_entries[0]),meert_table(DERT_entries[1]),
        meert_table(DERT_entries[1]),meert_table(DERT_entries[1])]


Meert_entries = [ [('SexMag','1E','mag'),
                   ('SexMag_Err','1E','mag'),
                   ('SexHrad','1E','arcsec', 'SexHrad'),
                   ('SexSky','1E','mag/arcsec^2'),
                   ('num_targets','1I',''),
                   ('num_neighborfit','1I',''),
                   ('AperRad', '1E', 'arcsec','r_aper'),
                   ('C','1E',''), ('C_err','1E',''),
                   ('A','1E',''), ('A_err','1E',''),
                   ('S','1E',''), ('S_err','1E',''),
                   ('G','1E',''), ('M20','1E',''),
                   ('extinction','1E','mag','c.extinction_{band}'),
                   ('dismod' ,'1E', 'mag', 'd.dismod'),
                   ('kpc_per_arcsec' ,'1E', 'kpc per arcsec', 'd.kpc_per_arcsec'), 
                   ('Vmax' ,'1E', 'Mpc^3', 'd.Vmax'),
                   ('SN' ,'1E', '', 'd.SN_{band}'),  
                   ('kcorr' ,'1E', 'mag','d.kcorr_{band}')
                   ],


                  [('m_tot', '1E', 'mag'), 
                   ('m_aper', '1E', 'mag'), 
                   ('BT','1E',''), 
                   ('r_tot', '1E', 'arcsec', 'Hrad_corr'),
                   ('ba_tot', '1E', '', 'ba_tot_corr'),
                   ('BT_aper','1E',''),
                   ('xctr_bulge','1E','pixels'),
                   ('xctr_bulge_err','1E','pixels'),
                   ('yctr_bulge','1E','pixels'),
                   ('yctr_bulge_err','1E','pixels'),
                   ('m_bulge','1E','mag'),
                   ('m_bulge_err','1E','mag'),
                   ('r_bulge','1E','arcsec'), 
                   ('r_bulge_err','1E','arcsec'),
                   ('n_bulge','1E',''), ('n_bulge_err','1E',''),
                   ('ba_bulge','1E',''), ('ba_bulge_err','1E',''),
                   ('pa_bulge','1E','degrees'), ('pa_bulge_err','1E','degrees'),
                   ('xctr_disk','1E','pixels'),
                   ('xctr_disk_err','1E','pixels'),
                   ('yctr_disk','1E','pixels'),
                   ('yctr_disk_err','1E','pixels'),
                   ('m_disk','1E','mag'),
                   ('m_disk_err','1E','mag'),
                   ('r_disk','1E','arcsec'), 
                   ('r_disk_err','1E','arcsec'),
                   ('n_disk','1E',''), ('n_disk_err','1E',''),
                   ('ba_disk','1E',''), ('ba_disk_err','1E',''),
                   ('pa_disk','1E','degrees'), ('pa_disk_err','1E','degrees'),
                   ('GalSky','1E','mag/arcsec^2'),
                   ('GalSky_err','1E','mag/arcsec^2'),
                   ('chi2nu','1E',''),
                   ('finalflag','1J','','f.flag'),
                   ('autoflag','1J','','f.flag'),
                   ('pyflag','1J','','flag'),
                   ('pyfitflag','1J','','FitFlag')]]

meert = [meert_table(Meert_entries[0])]
meert_models = [meert_table(Meert_entries[1])]


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

UKIDSS_entries = [[('galcount','1J',''),  
                   ('objid','1K',''), 
                   ('SourceID','1K', ''), 
                   ('FrameSetID', '1K',  ''),  
                   ('ra_ukidss' , '1D', 'radians'),  
                   ('dec_ukidss' , '1D', 'radians'),  
                   ('distance_arcmin' , '1E', 'arcmins'),  
                   ('epoch', '1K', 'years'), 
                   ('PriOrSec', '1E', ''), 
                   ('PGalaxy', '1E', ''), 
                   ('eBV', '1E', '')
                   ],
          
                  [('a', '1E', 'mag','a_{band[0]}'), 
                   ('PetroMag', '1E', 'mag','PetroMag_{band}'), 
                   ('PetroMagErr', '1E', 'mag','PetroMagErr_{band}'), 
                   ('SerMag2D', '1E', 'mag','SerMag2D_{band}'),   
                   ('SerMag2DErr', '1E', 'mag','SerMag2DErr_{band}'), 
                   ('AperMag3', '1E', 'mag','AperMag3_{band}'), 
                   ('AperMag3Err', '1E', 'mag','AperMag3Err_{band}'),   
                   ('Ell', '1E', '','Ell_{band}'), 
                   ('PA', '1E', 'degrees','PA_{band}'),  
                   ('ErrBits', '1J', '','ErrBits_{band}'), 
                   ('Deblend', '1J', '','Deblend_{band}')       
                   ] 
                  ]
UKIDSS = [meert_table(UKIDSS_entries[0])] + [meert_table(UKIDSS_entries[1]) for count in range(0,5)]


GALEX_entries = [[('gid', '1K', ''),
         ('photoExtractID',  '1K', ''), 
         ('imgID', '1K', ''),  
         ('band',   '1I', ''), 
         ('survey', '10A',  ''), 
         ('ra_galex',  '1E', 'deg'), 
         ('dec_galex', '1E', 'deg'),
         ('ra_galex_band_merged', '1E', 'deg'),
         ('dec_galex_band_merged', '1E', 'deg'),
         ('misc_flags', '1J', ''),
         ('primary_flag', '1J', ''),
         ('galextype',   '1J', ''), 
         ('e_bv','1E', 'mag'), 
         ('IsThereSpectrum', '1J', ''),
         ('GToSDstArcSec','1E', 'arcsec'),
         ('distanceRank', '1J', ''), 
         ('reverseDistanceRank', '1J', ''),
         ('multipleMatchCount', '1J', ''), 
         ('reverseMultipleMatchCount', '1J', ''), 
         ('SDSSobjid',  '1K', ''),
         ('SDSStype', '1J', ''),
         ('SDSSprobPSF', '1E', ''),
         ('nuv_fileNPath',  '125A', '')], 

         [('ExposureTime', '1E',  'seconds','{band}ExposureTime'),
         ('det_x', '1J', 'pix','{band}_det_x'),
         ('det_y', '1J', 'pix','{band}_det_y'),
         ('mag', '1E', 'mag', '{band}_mag'),
         ('magerr', '1E', 'mag','{band}_magerr'), 
         ('artifact', '1J','','{band}_artifact'), 
         ('skybg', '1E', 'counts','{band}_skybg'), 
         ('rad50','1E', 'arcsec','{band}_rad50'),
         ('rad90','1E', 'arcsec','{band}_rad90'), 
         ('zpmag', '1E', 'mag','{band[0]}_zpmag'),
         ('sxsfwhm','1E', 'arcsec','{band[0]}sxsfwhm')] 
                   ]


GALEX = [meert_table(GALEX_entries[0]), meert_table(GALEX_entries[1]), meert_table(GALEX_entries[1])]

YANG_entries = [('groupID', '1J', ''),
                 ('brightest','1J',''),
                 ('most_massive','1J',''),
                 ('L_group' ,'1E'   ,''),
                 ('Mstar_group','1E' ,''),
                 ('HaloMass_1','1E' ,''),
                 ('HaloMass_2','1E' ,''),
                 ('fEdge' ,'1E'  ,''),
                 ('ID1','1J',''),
                 ('ID2','1J',''),
                 ('group_counts','1J',''),
                 ('group_Z','1E' ,''),
                 ('zgal_yang','1E','')
                 ]

YANG = [meert_table(YANG_entries)]

JHU_matches_entries = [('SPECOBJID', '1K',''),
                       ('objid'    , '1K' ,''),
                       ('plate' ,'1J',''),
                       ('mjd'  ,'1J',''),
                       ('fiberID' ,'1J','')
                       ]
JHU_matches = [meert_table(JHU_matches_entries)]


#count = 0
#for a_col, b_col, c_col in zip(r_full_cols, r_full_fits_format, r_full_fits_units):
#    count +=1
#    print "%d :['%s','%s','%s']," %(count, a_col, b_col,  c_col)

#sys.exit()
