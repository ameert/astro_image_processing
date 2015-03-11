l#++++++++++++++++++++++++++
#
# TITLE: casjobs
#
# PURPOSE: queries casjobs for galaxies
#
#
# DATE: 17 OCT 2014
#
#-----------------------------------

import os
import datetime
import sys
from astro_image_processing.casjobs_query.casjobs_functions import *
from astro_image_processing.casjobs_query.make_new_query import *
import astro_image_processing.casjobs_query.casjobs_functions as cas_func
import traceback

class conematch_query(query_class):
    """This implements the query_casjobs class for a ra/dec cone search"""

    def cone_query(self):
        try:
            cmd = """
declare @thing_id int, @ra float, @dec float, @zgal float;

DECLARE my_cursor cursor read_only
FOR
SELECT mt.thing_id, mt.ra_gal, mt.dec_gal, mt.zgal FROM MYDB.{in_tablename} as mt
OPEN my_cursor

DECLARE @BRIGHT bigint SET 
@BRIGHT=dbo.fPhotoFlags('BRIGHT')
DECLARE @CHILD bigint SET @CHILD=dbo.fPhotoFLAGS('CHILD')
DECLARE @DEBLENDED_AS_PSF bigint 
    SET @DEBLENDED_AS_PSF=dbo.fPhotoFLAGS('DEBLENDED_AS_PSF')
DECLARE @EDGE bigint SET @EDGE=dbo.fPhotoFlags('EDGE')
DECLARE @SATURATED bigint SET @SATURATED=dbo.fPhotoFlags('SATURATED')
DECLARE @NODEBLEND bigint SET @NODEBLEND=dbo.fPhotoFlags('NODEBLEND')
DECLARE @bad_flags bigint SET
@bad_flags=(@SATURATED|@BRIGHT|@EDGE|@NODEBLEND|@CHILD|@DEBLENDED_AS_PSF)
WHILE(1=1)
BEGIN
  FETCH NEXT from my_cursor into @thing_id, @ra, @dec, @zgal
  IF (@@fetch_status < 0) break
  INSERT MYDB.{tablename}



SELECT top 1
@thing_id, @zgal, N.distance,
p.objid, (p.flags & @bad_flags)  as badflag, p.nchild, 
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
p.colc_u, p.colc_g, p.colc_r, p.colc_i, p.colc_z,
x.z as photoz, x.zErr as photoz_err,
x.kcorr_u,x.kcorr_g,x.kcorr_r,x.kcorr_i,x.kcorr_z
p.lnLStar_u,p.lnLStar_g,p.lnLStar_r,p.lnLStar_i,p.lnLStar_z,
p.type
INTO
mydb.{tablename}
FROM
(photoobj as p LEFT OUTER JOIN SpecObj as s on p.objID = s.BestObjID) 
LEFT OUTER JOIN Photoz as x on x.objid =p.objid, chunk c,  field f, segment g, dbo.fGetNearbyObjEq(@ra,@dec,3.0) as N  
WHERE
p.objid=N.objid and 
g.segmentID = f.segmentID and
f.fieldID = p.fieldID and  c.chunkID=g.chunkID
and p.run={run} and p.rerun = {rerun} and p.camcol = {camcol} 
and p.field = {field}
order by N.distance
END

CLOSE my_cursor
  DEALLOCATE my_cursor;
""".format(**self.job_info)
        except KeyError:
            print """WARNING: Not all query info was supplied:
You must supply a run, rerun, camcol, field, and table name"""
            traceback.print_exc()

        return cmd







def create_table(tabname):
    """creates the table for cone search output"""
    cmd = """create table {tabname} (galcount int, zgal float, 
distance float, objid bigint, 
run int, rerun int, camcol tinyint, field int, obj int,
rowc_g float,rowc_r float,rowc_i float,
colc_g float,colc_r float,colc_i float,
petroR50_g float, petroR50_r float, petroR50_i float, 
petroMag_g float, petroMag_r float, petroMag_i float, 
ModelMag_g float,  ModelMag_r float, ModelMag_i float, 
CModelMag_g float, CModelMag_r float, CModelMag_i float, 
fracdev_g float, fracdev_r float, fracdev_i float, 
devmag_g float, devmag_r float, devmag_i float, 
expmag_g float, expmag_r float, expmag_i float,
extinction_g float, extinction_r float, extinction_i float,
type int, lnLStar_r float);""".format(tabname=tabname)

    return cmd

def truncate_table(tabname):
    """truncates a table"""
    cmd = """truncate table {tabname};""".format(tabname=tabname)
    return cmd


def load_chunk(chunkdata, tabname):
    """creates a command to load data to a table denoted by tabname"""
    cmd = """insert into {tabname} VALUES {values};"""

    values = ','.join([str(a) for a in zip(chunkdata['thing_id'],chunkdata['ra'],chunkdata['dec'],chunkdata['zgal'])])
    return cmd.format(tabname=tabname, values=values)


def get_chunk(cursor, chunksize, chunknum):
    """returns a chunk of objects for the cone search. This must be done in chuncks to aoid overfilling the casjobs mydb storage space"""
    
    cmd = """select galcount, ra_gal, dec_gal, zgal from manga_gals  
order by galcount limit {offset},{chunksize};""".format(offset = max((chunknum-1)*chunksize,0), chunksize=chunksize)


    chunkdata = cursor.get_data_dict(cmd, ['thing_id', 'ra','dec','zgal'], 
                                     [int, float, float, float])
    return chunkdata

    

    while True:
        job_info['chunknum']+=1
        job_info['jobname']='{full_jobname}_{chunknum}'.format(**job_info)
        job_info['query_name']='query_{jobname}.txt'.format(**job_info)
        
        
        print 'CUT PIPE: Truncate output tables'
        exec_cmd('{casjobs} execute -t "mydb" -n "Truncate output table" "{cmd}"'.format(cmd=truncate_table(job_info['tablename']),**job_info))
        exec_cmd('{casjobs} -j '.format(**job_info))
        
        print 'CUT PIPE: Truncate input tables'
        exec_cmd('{casjobs} execute -t "mydb" -n "Truncate input table" "{cmd}"'.format(cmd=truncate_table(job_info['in_tablename']),**job_info))
        exec_cmd('{casjobs} -j '.format(**job_info))
        
        print 'CUT PIPE: Loading Chunk'
        chunkdata = get_chunk(cursor, job_info['chunk'],job_info['chunknum'])

        exec_cmd('{casjobs} execute -t "mydb" -n "load chunk" "{cmd}"'.format(cmd=load_chunk(chunkdata, job_info['in_tablename']),**job_info))

        print 'CUT PIPE: Chunk successfully loaded!'
        
        fid = open(job_info['query_name'],'w')
        fid.write(cone_search_query(job_info))
        fid.close()

        print 'CUT PIPE: Running Query'
        cmd='{casjobs} run -n "{jobname}" -f {query_name}'.format(**job_info)
        print cmd
        exec_cmd(cmd)
    
        print 'CUT PIPE: Downloading Results'
        cmd='{casjobs} extract -force -type "csv" -download {jobname} -table {tablename}'.format(**job_info)
        print cmd
        casjobs_out = exec_cmd(cmd)
        print casjobs_out

        down_file = get_filename(casjobs_out)
        cmd = 'cat %s >> %s' %(down_file, 
                               gal_cat['data_dir']+gal_cat['filename'])
        os.system(cmd)
        
        #os.system('rm %s' %down_file)
        if chunkdata['thing_id'].size<job_info['chunk']:
            break #because we must be at the end of the list
    return 0
 
if __name__ == "__main__":
    from astro_image_processing.user_settings import casjobs_info

    casjobs_info.update({ 'cas_jar_path':'/home/alan/git_projects/astro_image_processing/casjobs_query/casjobs.jar',
                          'jobname':'mangatest',
                          'search_target':'DR10'})
    gal_cat = {'filename':'mangatest.cat',
               'data_dir':'/home/alan/Desktop/test/',
               'out_file':'mangatest.cat'
               }

    casjobs(gal_cat, casjobs_info)
