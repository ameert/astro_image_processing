#++++++++++++++++++++++++++
#
# TITLE: casjobs_allspec
#
# PURPOSE: queries casjobs for all spectroscopic galaxies
#
# INPUTS: gal_cat :  a dictionary containing the keys: 
#                    'filename'- names the file that 
#                                downloaded data will
#                                be saved in  
#         data_dir:  the directory where all data will be stored
#         username:  string! username used for making queries
#         wsid:      string! id number used by casjobs
#         password:  string! the password for casjobs
#         search_82: set to 1 if searching stripe82 
# OUTPUTS: NONE, but does create the data file
#          named by 'filename'
#
# PROGRAM CALLS: make_query (this is imported)
#                also uses the 'os' module and
#                'datetime' module
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 9 FEB 2012
#
# NOTES: For now, casjobs program must be in the directory
#        that you are executing the python code from. I intend
#        to change this.
#
#-----------------------------------

import os
import datetime
import traceback
import astro_image_processing.casjobs_query.casjobs_functions as query_casjobs

class spec_query(query_casjobs.query_class):
    """This implements the query_casjobs class for a all-spectroscopic data search"""

    def catalog_query(self):
        try:
            cmd = """DECLARE @BRIGHT bigint SET 
@BRIGHT=dbo.fPhotoFlags('BRIGHT')
DECLARE @CHILD bigint SET @CHILD=dbo.fPhotoFLAGS('CHILD')
DECLARE @DEBLENDED_AS_PSF bigint 
    SET @DEBLENDED_AS_PSF=dbo.fPhotoFLAGS('DEBLENDED_AS_PSF')
DECLARE @EDGE bigint SET @EDGE=dbo.fPhotoFlags('EDGE')
DECLARE @SATURATED bigint SET @SATURATED=dbo.fPhotoFlags('SATURATED')
DECLARE @NODEBLEND bigint SET @NODEBLEND=dbo.fPhotoFlags('NODEBLEND')
DECLARE @bad_flags bigint SET
@bad_flags=(@SATURATED|@BRIGHT|@EDGE|@NODEBLEND|@CHILD|@DEBLENDED_AS_PSF)
SELECT top {chunk}
p.objid, (p.flags & @bad_flags)  as badflag, p.nchild, 
p.run,p.rerun,p.camCol,p.field,p.obj, 
s.specobjid, s.plate, s.mjd, s.fiberid,  
p.ra as ra_gal, p.dec as dec_gal, s.z, 
s.veldisp, s.veldispErr,  p.probPSF,
p.petroR90_u, p.petroR90_g, p.petroR90_r, p.petroR90_i, p.petroR90_z,
p.petroR50_u, p.petroR50_g, p.petroR50_r, p.petroR50_i, p.petroR50_z,
p.petroMag_u, p.petroMag_g, p.petroMag_r, p.petroMag_i, p.petroMag_z,
p.devRad_u, p.devRad_g, p.devRad_r, p.devRad_i, p.devRad_z, 
p.devab_u, p.devab_g, p.devab_r, p.devab_i, p.devab_z, 
p.devPhi_u,p.devPhi_g,p.devPhi_r,p.devPhi_i,p.devPhi_z,
p.devmag_u, p.devmag_g, p.devmag_r, p.devmag_i, p.devmag_z, 
p.fracdev_u, p.fracdev_g, p.fracdev_r, p.fracdev_i, p.fracdev_z, 
p.expRad_u, p.expRad_g, p.expRad_r, p.expRad_i, p.expRad_z, 
p.expab_u, p.expab_g, p.expab_r, p.expab_i, p.expab_z, 
p.expPhi_u,p.expPhi_g,p.expPhi_r,p.expPhi_i,p.expPhi_z,
p.expmag_u, p.expmag_g, p.expmag_r, p.expmag_i, p.expmag_z, 
p.PSFmag_u, p.PSFmag_g, p.PSFmag_r, p.PSFmag_i, p.PSFmag_z, 
p.Cmodelmag_u, p.Cmodelmag_g, p.Cmodelmag_r, p.Cmodelmag_i, p.Cmodelmag_z, 
p.Modelmag_u, p.Modelmag_g, p.Modelmag_r, p.Modelmag_i, p.Modelmag_z, 
p.extinction_u, p.extinction_g, p.extinction_r, p.extinction_i,
    p.extinction_z, 
f.gain_u, f.gain_g, f.gain_r, f.gain_i, f.gain_z,
f.darkvariance_u, f.darkvariance_g, f.darkvariance_r, f.darkvariance_i,
    f.darkvariance_z,
f.sky_u, f.sky_g, f.sky_r, f.sky_i, f.sky_z,
f.skySig_u, f.skySig_g, f.skySig_r, f.skySig_i, f.skySig_z,
f.skyErr_u, f.skyErr_g, f.skyErr_r, f.skyErr_i, f.skyErr_z,
f.psfWidth_u, f.psfWidth_g, f.psfWidth_r, f.psfWidth_i, f.psfWidth_z,
p.rowc_u, p.rowc_g, p.rowc_r, p.rowc_i, p.rowc_z,
p.colc_u, p.colc_g, p.colc_r, p.colc_i, p.colc_z,
x.z as photoz, x.zErr as photoz_err,
x.kcorrU,x.kcorrG,x.kcorrR,x.kcorrI,x.kcorrZ
INTO
mydb.{tablename}
FROM
(Galaxy as p LEFT OUTER JOIN SpecObj as s on p.objID = s.BestObjID) 
LEFT OUTER JOIN Photoz as x on x.objid =p.objid, field f
WHERE
f.fieldID = p.fieldID and  
p.objid > {lastnum} and
(p.petroMag_r - p.extinction_r) between 14.0 and 17.77 and p.type = 3 
and s.class ='GALAXY'
order by p.objid
""".format(**self.job_info)
        except KeyError:
            print """WARNING: Not all query info was supplied:
You must supply a limiting chunk size, a starting photoobjid, and table name"""
        traceback.print_exc()

        return cmd

    
    



if __name__ == "__main__":
    from astro_image_processing.user_settings import casjobs_info

    gal_cat = {'filename':'spectro_sample_raw.cat',
               'data_dir':'/home/alan/Desktop/test/data/',
               'out_file':'spectro_sample.cat',
               'chunksize':10,
               }

    casjobs_info.update({ 'jobname':'test_name',
                          'search_target':'DR12'})


    our_query = spec_query(gal_cat, casjobs_info)

    our_query.run_full_query()
    
