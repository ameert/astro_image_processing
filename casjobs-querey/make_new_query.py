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

def make_query(stripe_82 = 0, start_objid = '-99', chunk_size = 10):
    # These mod operations ensure that the input will be either 1 or 2
    stripe_82 = stripe_82 % 2

    # Now build the part of the query that is common to all of the queries 
    out = """declare @BRIGHT bigint set @BRIGHT=dbo.fPhotoFlags('BRIGHT')
declare @CHILD bigint set @CHILD=dbo.fPhotoFLAGS('CHILD')
declare @DEBLENDED_AS_PSF bigint 
    set @DEBLENDED_AS_PSF=dbo.fPhotoFLAGS('DEBLENDED_AS_PSF')
declare @EDGE bigint set @EDGE=dbo.fPhotoFlags('EDGE')
declare @SATURATED bigint set @SATURATED=dbo.fPhotoFlags('SATURATED')
declare @NODEBLEND bigint set @NODEBLEND=dbo.fPhotoFlags('NODEBLEND')
declare @bad_flags bigint set
@bad_flags=(@SATURATED|@BRIGHT|@EDGE|@NODEBLEND|@CHILD|@DEBLENDED_AS_PSF)
select top %d
p.objid, (p.flags & @bad_flags)  as badflag, p.nchild, 
p.run,p.rerun,p.camCol,p.field,p.obj, c.stripe,
c.startmu, s.specobjid, s.plate, s.mjd, s.fiberid,  
p.ra as ra_gal, p.dec as dec_gal, s.z as redshift, 
s.veldisp, s.veldispErr, s.eclass, 
k.p_el_debiased, k.p_cs_debiased, k.spiral, k.elliptical, k.uncertain,
p.petroR90_u, p.petroR90_g, p.petroR90_r, p.petroR90_i, p.petroR90_z,
p.petroR50_u, p.petroR50_g, p.petroR50_r, p.petroR50_i, p.petroR50_z,
p.petroMag_u, p.petroMag_g, p.petroMag_r, p.petroMag_i, p.petroMag_z,
p.devRad_u, p.devRad_g, p.devRad_r, p.devRad_i, p.devRad_z, 
p.devab_u, p.devab_g, p.devab_r, p.devab_i, p.devab_z, 
p.devmag_u, p.devmag_g, p.devmag_r, p.devmag_i, p.devmag_z, 
p.fracdev_u, p.fracdev_g, p.fracdev_r, p.fracdev_i, p.fracdev_z, 
p.dered_u, p.dered_g, p.dered_r, p.dered_i, p.dered_z, 
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
INTO
mydb.cl_out
FROM
(photoobj as p LEFT OUTER JOIN public.galaxyzoo.GalaxyZoo1_DR_table2 as k 
ON p.objid = k.OBJID ) LEFT OUTER JOIN SpecObj as s on p.objID = s.BestObjID,
segment g, field f,  chunk c\n""" %chunk_size

    if stripe_82:
        # This cross apply pulls out objects in stripe 82
        # if we are searching by ra dec. If not searching
        # by ra dec then objid already selects objects in stripe 82
        #out = out + """CROSS APPLY
        #(SELECT TOP 1 f.* FROM dbo.fGetNearbyObjEq(mt.ra, mt.dec, 0.5) as f,
        #PhotoObjAll as p WHERE p.objid = f.objID and p.run in (106,206))  as a
        #WHERE
        #a.objid = p.objid and
        #g.segmentID = f.segmentID and
        #f.fieldID = p.fieldID and  c.chunkID=g.chunkID\n"""
        pass
    else:
        # This next line is common to all other queries
        out = out + """WHERE
g.segmentID = f.segmentID and
f.fieldID = p.fieldID and  c.chunkID=g.chunkID 
and p.objid > %s 
and 
(p.petroMag_r - p.extinction_r) between 14.0 and 17.77 and p.type = 3 and s.specclass = 2\n""" %start_objid
        
    # These lines are included in all queries
    out = out + """ORDER BY p.objid\n"""

    # Now return the query string
    return out


def field_query(run, rerun, camcol, field, stripe_82=False):
    """returns a catalog of all objects in a given field"""
    # Now build the part of the query that is common to all of the queries 
    out = """declare @BRIGHT bigint set @BRIGHT=dbo.fPhotoFlags('BRIGHT')
declare @CHILD bigint set @CHILD=dbo.fPhotoFLAGS('CHILD')
declare @DEBLENDED_AS_PSF bigint 
    set @DEBLENDED_AS_PSF=dbo.fPhotoFLAGS('DEBLENDED_AS_PSF')
declare @EDGE bigint set @EDGE=dbo.fPhotoFlags('EDGE')
declare @SATURATED bigint set @SATURATED=dbo.fPhotoFlags('SATURATED')
declare @NODEBLEND bigint set @NODEBLEND=dbo.fPhotoFlags('NODEBLEND')
declare @bad_flags bigint set
@bad_flags=(@SATURATED|@BRIGHT|@EDGE|@NODEBLEND|@CHILD|@DEBLENDED_AS_PSF)
Select 
p.objid, (p.flags & @bad_flags)  as badflag, p.nchild, 
p.run,p.rerun,p.camCol,p.field,p.obj, c.stripe,
c.startmu, s.specobjid, s.plate, s.mjd, s.fiberid,  
p.ra as ra_gal, p.dec as dec_gal, s.z as redshift, 
s.veldisp, s.veldispErr, s.eclass, 
999,999,999,999,999,
p.petroR90_u, p.petroR90_g, p.petroR90_r, p.petroR90_i, p.petroR90_z,
p.petroR50_u, p.petroR50_g, p.petroR50_r, p.petroR50_i, p.petroR50_z,
p.petroMag_u, p.petroMag_g, p.petroMag_r, p.petroMag_i, p.petroMag_z,
p.devRad_u, p.devRad_g, p.devRad_r, p.devRad_i, p.devRad_z, 
p.devab_u, p.devab_g, p.devab_r, p.devab_i, p.devab_z, 
p.devmag_u, p.devmag_g, p.devmag_r, p.devmag_i, p.devmag_z, 
p.fracdev_u, p.fracdev_g, p.fracdev_r, p.fracdev_i, p.fracdev_z, 
p.dered_u, p.dered_g, p.dered_r, p.dered_i, p.dered_z, 
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
p.colc_u, p.colc_g, p.colc_r, p.colc_i, p.colc_z,
x.z as photoz, x.zErr as photoz_err,
x.kcorr_u,x.kcorr_g,x.kcorr_r,x.kcorr_i,x.kcorr_z
INTO
mydb.cl_out
FROM
photoobj as p LEFT OUTER JOIN SpecObj as s on p.objID = s.BestObjID,
segment g, field f,  chunk c, Photoz x\n""" 

    if stripe_82:
        # This cross apply pulls out objects in stripe 82
        # if we are searching by ra dec. If not searching
        # by ra dec then objid already selects objects in stripe 82
        #out = out + """CROSS APPLY
        #(SELECT TOP 1 f.* FROM dbo.fGetNearbyObjEq(mt.ra, mt.dec, 0.5) as f,
        #PhotoObjAll as p WHERE p.objid = f.objID and p.run in (106,206))  as a
        #WHERE
        #a.objid = p.objid and
        #g.segmentID = f.segmentID and
        #f.fieldID = p.fieldID and  c.chunkID=g.chunkID\n"""
        pass
    else:
        # This next line is common to all other queries
        out = out + """WHERE
g.segmentID = f.segmentID and
f.fieldID = p.fieldID and  c.chunkID=g.chunkID 
and x.objid =p.objid 
and p.run=%d and p.rerun = %d and p.camcol = %d and p.field = %d \n
""" %(run, rerun, camcol, field)
        
    # These lines are included in all queries
    out = out + """ORDER BY p.objid\n"""

    # Now return the query string
    return out
