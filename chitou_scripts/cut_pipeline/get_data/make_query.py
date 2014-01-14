#++++++++++++++++++++++++++
#
# TITLE: make_querey 
#
# PURPOSE: This function makes the
#          casjobs query used to get
#          the necessary data from casjobs.
#          
# INPUTS: do_ra_dec: if 1 then query uses ra and dec
#                    if set to 0 then uses sdss objid
#                    default = 1
#         stripe_82: if set to 1, the stripe 82 is searched
#                    if set to 0, the DR7 is searched
#                    default = 0
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
# DATE: 5 JAN 2011
#
#-----------------------------------

def make_query_sdss(do_ra_dec = 1, stripe_82 = 0):
    # These mod operations ensure that the input will be either 1 or 2
    stripe_82 = stripe_82 % 2
    do_ra_dec = do_ra_dec % 2

    # Now build the part of the query that is common to all of the queries 
    out = """declare @BRIGHT bigint set @BRIGHT=dbo.fPhotoFlags('BRIGHT')
    declare @EDGE bigint set @EDGE=dbo.fPhotoFlags('EDGE')
    declare @SATURATED bigint set @SATURATED=dbo.fPhotoFlags('SATURATED')
    declare @NODEBLEND bigint set @NODEBLEND=dbo.fPhotoFlags('NODEBLEND')
    declare @bad_flags bigint set
    @bad_flags=(@SATURATED|@BRIGHT|@EDGE|@NODEBLEND)
    SELECT
    mt.myind as galcount, ((p.flags & @bad_flags) + p.nchild  ) as badflag,
    p.objid, p.run,p.rerun,p.camCol,p.field,p.obj, c.stripe,
    c.startmu,  p.ra, p.dec, s.z as redshift, s.specobjid, s.plate, s.mjd, s.fiberid,
    s.veldisp, s.veldispErr, s.eclass, p.devRad_r, p.devmag_r, p.fracdev_u, p.fracdev_g,
    p.fracdev_r, p.fracdev_i, p.fracdev_z, p.petroR90_r,
    p.petroR50_u, p.petroR50_g, p.petroR50_r, p.petroR50_i, p.petroR50_z,
    p.extinction_u, p.extinction_g, p.extinction_r, p.extinction_i,
    p.extinction_z, f.aa_u, f.aa_g, f.aa_r, f.aa_i, f.aa_z,
    p.rowc_u, p.rowc_g, p.rowc_r, p.rowc_i, p.rowc_z,
    p.colc_u, p.colc_g, p.colc_r, p.colc_i, p.colc_z, 
    INTO
    mydb.cl_out
    FROM
    photoobj as p LEFT OUTER JOIN SpecObj as s on p.objID = s.BestObjID,
    --photoobj p, specobj s,
    segment g, field f,  chunk c, mydb.cl_in mt\n"""

    if stripe_82 and do_ra_dec:
            # This cross apply pulls out objects in stripe 82
            # if we are searching by ra dec. If not searching
            # by ra dec then objid already selects objects in stripe 82
            out = out + """CROSS APPLY
            (SELECT TOP 1 f.* FROM dbo.fGetNearbyObjEq(mt.ra, mt.dec, 0.5) as f,
            PhotoObjAll as p WHERE p.objid = f.objID and p.run in (106,206))  as a
            WHERE
            a.objid = p.objid and
            g.segmentID = f.segmentID and
            f.fieldID = p.fieldID and  c.chunkID=g.chunkID\n"""
    else:
        # This next line is common to all other queries
        out = out + """WHERE
        --p.objid = s.bestobjid and
        g.segmentID = f.segmentID and
        f.fieldID = p.fieldID and  c.chunkID=g.chunkID\n"""
        if do_ra_dec:
            # This is included only if not searching stripe 82 and using ra/dec
            out = out + 'and p.objid = dbo.fGetNearestObjIdEq(mt.ra,mt.dec,0.5)\n'
        else:
            # This is included in any search by objid
            out = out + 'and p.objid = mt.sdssobjid\n'

    # These lines are included in all queries
    out = out + 'ORDER BY mt.myind\n'
    out = out + '--and p.petroR90_i/p.petroR50_i > 2.7\n--and p.fracDev_r > 0.8 \n'

    # Now return the query string
    return out

def make_query_galex(do_ra_dec = 1, stripe_82 = 0):
    cmd = 'SELECT\n'
    cmd +='mt.myind, a.distance, p.objid, p.photoExtractID, s.imgID, p.band,\n'
    cmd +='p.ra, p.dec, p.alpha_j2000_merged, p.delta_j2000_merged,\n'
    cmd +='p.primary_flag, p.type,p.misc_flags, p.nuv_mag, p.nuv_magerr,\n'
    cmd +='p.fuv_mag, p.fuv_magerr, p.nuv_artifact,p.fuv_artifact,\n'
    cmd +='s.n_zpmag, s.f_zpmag, s.nsxsfwhm, s.fsxsfwhm, z.nuv_fileNPath\n'
    cmd +='INTO\n'
    cmd +='mydb.cl_out\n'
    cmd +='FROM\n'
    cmd +='PhotoObjAll as p, PhotoExtract as s, Img as z, mydb.cl_in as mt\n'
    cmd +='CROSS APPLY\n'
    cmd +='(SELECT TOP 1 f.* FROM dbo.fGetNearbyObjEq(mt.ra,mt.dec,0.5) as f,\n'
    cmd +='PhotoObjAll as p WHERE p.objid = f.objID and p.primary_flag = 1) as a\n'
    cmd +='WHERE\n'
    cmd +='p.photoExtractID = s.photoExtractID and s.imgID = z.imgID\n'
    if do_ra_dec == 1:
        out = [ out 'and p.objid = a.objID\n'];
    else:
        print 'GALEX does not work with SDSS obj ids. You must use ra and dec\n'
        print 'EXITING PROGRAM!!!!!!!!!!!!!!!!!!'
        sys.exit()
    return cmd
