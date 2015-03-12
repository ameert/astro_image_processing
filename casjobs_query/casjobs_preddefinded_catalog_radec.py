
import os
import datetime
import sys
import traceback
import numpy as np
import astro_image_processing.casjobs_query.casjobs_functions as query_casjobs
import astro_image_processing.mysql as mysql
from astro_image_processing.user_settings import mysql_params

class conematch_query(query_casjobs.query_class):
    """This implements the query_casjobs class for a ra/dec cone search"""

    def __init__(self,  gal_cat, casjobs_info):
        super(conematch_query, self).__init__(gal_cat, casjobs_info)

        self.job_info['chunktable']=gal_cat['chunktable']

        self.cursor = mysql.mysql_connect(mysql_params['dba'],mysql_params['user'],
                       mysql_params['pwd'],mysql_params['host'])

        return

    def catalog_query(self):
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
p.run,p.rerun,p.camCol,p.field,p.obj, 
s.specobjid, s.plate, s.mjd, s.fiberid,  
p.ra as ra_gal, p.dec as dec_gal, s.z, 
s.veldisp, s.veldispErr, p.probPSF,
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
x.kcorrU,x.kcorrG,x.kcorrR,x.kcorrI,x.kcorrZ,
p.lnLStar_u,p.lnLStar_g,p.lnLStar_r,p.lnLStar_i,p.lnLStar_z,
p.type
FROM
(photoobj as p LEFT OUTER JOIN SpecObj as s on p.objID = s.BestObjID) 
LEFT OUTER JOIN Photoz as x on x.objid =p.objid, field f, dbo.fGetNearbyObjEq(@ra,@dec,3.0) as N  
WHERE
p.objid=N.objid and 
f.fieldID = p.fieldID 
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

    def create_table_output(self):
        """creates the table for cone search output"""
        cmd = """create table {tablename} (
galcount int, zgal float, distance float,
objid bigint, badflag bigint, nchild int, 
run int,rerun int, camCol tinyint, field int, obj int, 
specobjid bigint, plate int, mjd int, fiberid int,  
ra_gal float, dec_gal float, z float, 
veldisp float, veldispErr float, probPSF float,
petroR90_u float, petroR90_g float, petroR90_r float, petroR90_i float, petroR90_z float,
petroR50_u float, petroR50_g float, petroR50_r float, petroR50_i float, petroR50_z float,
petroMag_u float, petroMag_g float, petroMag_r float, petroMag_i float, petroMag_z float,
devRad_u float, devRad_g float, devRad_r float, devRad_i float, devRad_z float, 
devab_u float, devab_g float, devab_r float, devab_i float, devab_z float, 
devPhi_u float,devPhi_g float,devPhi_r float,devPhi_i float,devPhi_z float,
devmag_u float, devmag_g float, devmag_r float, devmag_i float, devmag_z float, 
fracdev_u float, fracdev_g float, fracdev_r float, fracdev_i float, fracdev_z float, 
expRad_u float, expRad_g float, expRad_r float, expRad_i float, expRad_z float, 
expab_u float, expab_g float, expab_r float, expab_i float, expab_z float, 
expPhi_u float,expPhi_g float,expPhi_r float,expPhi_i float,expPhi_z float,
expmag_u float, expmag_g float, expmag_r float, expmag_i float, expmag_z float, 
PSFmag_u float, PSFmag_g float, PSFmag_r float, PSFmag_i float, PSFmag_z float, 
Cmodelmag_u float, Cmodelmag_g float, Cmodelmag_r float, Cmodelmag_i float, Cmodelmag_z float, 
Modelmag_u float, Modelmag_g float, Modelmag_r float, Modelmag_i float, Modelmag_z float, 
extinction_u float, extinction_g float, extinction_r float, extinction_i float,
    extinction_z float, 
gain_u float, gain_g float, gain_r float, gain_i float, gain_z float,
darkvariance_u float, darkvariance_g float, darkvariance_r float, darkvariance_i float,
    darkvariance_z float,
sky_u float, sky_g float, sky_r float, sky_i float, sky_z float,
skySig_u float, skySig_g float, skySig_r float, skySig_i float, skySig_z float,
skyErr_u float, skyErr_g float, skyErr_r float, skyErr_i float, skyErr_z float,
psfWidth_u float, psfWidth_g float, psfWidth_r float, psfWidth_i float, psfWidth_z float,
rowc_u float, rowc_g float, rowc_r float, rowc_i float, rowc_z float,
colc_u float, colc_g float, colc_r float, colc_i float, colc_z float,
photoz float, photoz_err float,
kcorrU float,kcorrG float,kcorrR float,kcorrI float,kcorrZ float,
lnLStar_u float,lnLStar_g float,lnLStar_r float,lnLStar_i float,lnLStar_z float,
ptype int);
""".format(**self.job_info)

        return cmd

    def truncate_table(self):
        """truncates a table"""
        cmd = """truncate table {tablename};""".format(**self.job_info)
        return cmd


    def load_chunk(self, chunkdata):
        """creates a command to load data to a table denoted by tabname"""
        cmd = """insert into {in_tablename} """.format(**self.job_info) + """ VALUES {values};"""

        values = ','.join([str(a) for a in zip(chunkdata['thing_id'],chunkdata['ra'],chunkdata['dec'],chunkdata['zgal'])])
        return cmd.format(values=values)


    def get_chunk(self):
        """returns a chunk of objects for the cone search. This must be done in chuncks to aoid overfilling the casjobs mydb storage space"""
        chunknum = self.job_info['chunknum']
        chunksize = self.job_info['chunk']

        cmd = """select galcount, ra_gal, dec_gal, zgal from {chunktable}  
order by galcount limit {offset},{chunksize};""".format(offset = max((chunknum-1)*chunksize,0), chunksize=chunksize, chunktable=self.job_info['chunktable'])


        try:
            chunkdata = self.cursor.get_data_dict(cmd, ['thing_id', 'ra','dec','zgal'], 
                                                  [int, float, float, float])
        except IndexError:
            #the table returned zero rows or failed for some reason so return empty thing
            chunkdata={'thing_id':np.array([], dtype=int), 'ra':np.array([], dtype=float),'dec':np.array([], dtype=float),
                       'zgal':np.array([], dtype=float)} 

        return chunkdata
    
    
    def prep_next_job(self):
        self.job_info['table_count']+=1
        self.job_info['chunknum']+=1
        self.job_info['jobname']='{full_jobname}_{chunknum}'.format(**self.job_info)
        self.job_info['query_name']='query_{jobname}.txt'.format(**self.job_info)
        self.job_info['tablename'] = self.job_info['jobname']

        print 'CUT PIPE: Preparing MyDB input/output tables'
        self.prep_output_table()
        self.prep_input_table()
        return True

    def create_table_input(self):
        """creates the table for cone search input"""
        cmd = """create table {in_tablename} (thing_id int, ra_gal float, dec_gal float, zgal float);""".format(**self.job_info)
        return cmd

    
    def run_full_query(self):
        while True:
            self.prep_next_job()

            self.build_query()

            print 'CUT PIPE: Loading Chunk'
            chunkdata = self.get_chunk()
            
            if chunkdata['thing_id'].size<self.job_info['chunk']:
                # This loop exits when prep_next_job returns false. ie there is not a next job
                break

            self.exec_cmd('{casjobs_jar} execute -t "mydb" -n "load chunk" "{cmd}"'.format(cmd=self.load_chunk(chunkdata), **self.job_info))
            print 'CUT PIPE: Chunk successfully loaded!'

            print 'CUT PIPE: Running Query'
            self.job_info['cmd']='{casjobs_jar} run -n "{jobname}" -f {query_name}'.format(**self.job_info)
            print self.job_info['cmd']
            self.exec_cmd(self.job_info['cmd'])

            print 'GALMORPH: Downloading Results'
            self.job_info['cmd']='{casjobs_jar} extract -force -type "csv" -download {jobname} -table {tablename}'.format(**self.job_info)
            print self.job_info['cmd']
            self.casjobs_out = self.exec_cmd(self.job_info['cmd'])
            print self.casjobs_out

            self.get_job_output()

        return
 
if __name__ == "__main__":
    from astro_image_processing.user_settings import casjobs_info

    casjobs_info.update({ 'jobname':'test_name',
                          'search_target':'DR12'})

    gal_cat = {'filename':'conematch_sample_raw.cat',
               'data_dir':'/home/alan/Desktop/test/data/',
               'chunksize':10,
               'chunktable':'manga_gals'
                   }

    our_query = conematch_query(gal_cat, casjobs_info)
    
    our_query.run_full_query()


