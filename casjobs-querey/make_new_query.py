#++++++++++++++++++++++++++
#
# TITLE: make_new_querey 
#
# PURPOSE: This function makes the
#          casjobs query used to get
#          the necessary data from casjobs.
#          
# INPUTS: stripe_82: if set to 1, the stripe 82 is searched
#         if set to 0, the DR7 is searched
#         default = 0
#
#         start_objid: the minimum objID used to extract 
#                      from the database. It is used 
#                      to extract from the database in chunks
#
# OUTPUTS: The query string used by casjobs
#
# PROGRAM CALLS: NONE
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
#-----------------------------------
import traceback

def start_query():
    """The first part of the query"""
    return """DECLARE @BRIGHT bigint SET @BRIGHT=dbo.fPhotoFlags('BRIGHT')
DECLARE @CHILD bigint SET @CHILD=dbo.fPhotoFLAGS('CHILD')
DECLARE @DEBLENDED_AS_PSF bigint 
    SET @DEBLENDED_AS_PSF=dbo.fPhotoFLAGS('DEBLENDED_AS_PSF')
DECLARE @EDGE bigint SET @EDGE=dbo.fPhotoFlags('EDGE')
DECLARE @SATURATED bigint SET @SATURATED=dbo.fPhotoFlags('SATURATED')
DECLARE @NODEBLEND bigint SET @NODEBLEND=dbo.fPhotoFlags('NODEBLEND')
DECLARE @bad_flags bigint SET
@bad_flags=(@SATURATED|@BRIGHT|@EDGE|@NODEBLEND|@CHILD|@DEBLENDED_AS_PSF)
SELECT 
"""

def mid_query():
    """The middle part of the query"""
    return """p.objid, (p.flags & @bad_flags)  as badflag, p.nchild, 
p.run,p.rerun,p.camCol,p.field,p.obj, c.stripe,
c.startmu, s.specobjid, s.plate, s.mjd, s.fiberid,  
p.ra as ra_gal, p.dec as dec_gal, s.z, 
s.veldisp, s.veldispErr, s.eclass,  p.probPSF,
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
p.extinction_u, p.extinction_g, p.extinction_r, p.extinction_i,
    p.extinction_z, 
f.aa_u, f.aa_g, f.aa_r, f.aa_i, f.aa_z,
f.kk_u, f.kk_g, f.kk_r, f.kk_i, f.kk_z,
f.airmass_u, f.airmass_g, f.airmass_r, f.airmass_i, f.airmass_z,
f.gain_u, f.gain_g, f.gain_r, f.gain_i, f.gain_z,
f.darkvariance_u, f.darkvariance_g, f.darkvariance_r, f.darkvariance_i,
    f.darkvariance_z,
f.sky_u, f.sky_g, f.sky_r, f.sky_i, f.sky_z,
f.skySig_u, f.skySig_g, f.skySig_r, f.skySig_i, f.skySig_z,
f.skyErr_u, f.skyErr_g, f.skyErr_r, f.skyErr_i, f.skyErr_z,
f.psfWidth_u, f.psfWidth_g, f.psfWidth_r, f.psfWidth_i, f.psfWidth_z,
p.rowc_u, p.rowc_g, p.rowc_r, p.rowc_i, p.rowc_z,
p.colc_u, p.colc_g, p.colc_r, p.colc_i, p.colc_z
x.z as photoz, x.zErr as photoz_err,
x.kcorr_u,x.kcorr_g,x.kcorr_r,x.kcorr_i,x.kcorr_z
INTO
mydb.{tablename}
FROM
(photoobj as p LEFT OUTER JOIN SpecObj as s on p.objID = s.BestObjID) 
LEFT OUTER JOIN Photoz as x on x.objid =p.objid, chunk c
WHERE
g.segmentID = f.segmentID and
f.fieldID = p.fieldID and  c.chunkID=g.chunkID
""" 

def end_query():
    """The end of the query common to all query types"""
    return """ORDER BY p.objid\n"""

def catalog_query(job_info):
    """Takes a dictionary called job_info, with relevant target, chunksize, and starting point and returns the chunk of size chunksize containing galaxies with objid>starting point. Searches for galaxies with PetroMag_r-extinction_r between 14 and 17.77 that are part of the spectroscopic database"""

    out = start_query()
    out += "top {chunk}\n"
    out += mid_query()
    out += """and p.objid > {lastnum} and 
(p.petroMag_r - p.extinction_r) between 14.0 and 17.77 and p.type = 3 and s.specclass = 2\n""" 
    out += end_query()  

    try:
        out = out.format(**job_info)
    except KeyError:
        print """WARNING: Not all query info was supplied to the querey generator:
You must supply a limiting chunk size, a starting photoobjid, and table name"""
        traceback.print_exc()

    return out


def field_query(job_info):
    """returns a catalog of all objects in a given field"""

    out = start_query() + mid_query()
    out += """and p.run={run} and p.rerun = {rerun} and p.camcol = {camcol} 
and p.field = {field}\n""" 
    out += end_query()  

    try:
        out = out.format(**job_info)
    except KeyError:
        print """WARNING: Not all query info was supplied to the querey generator:
You must supply a run, rerun, camcol, field, and table name"""
        traceback.print_exc()

    return out

        
        


   
