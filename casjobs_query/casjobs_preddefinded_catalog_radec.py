#++++++++++++++++++++++++++
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
from astro_image_processing.casjobs_query.make_new_query import *
import subprocess as sub
import sys
from astro_image_processing.casjobs_query.casjobs_new_query import get_file_info, write_config,get_filename, exec_cmd
from astro_image_processing.mysql import *
from astro_image_processing.user_settings import *

def cone_search_query(job_info):
    """The cone serch query used in building the correlated luminostiy function"""
    cmd = """declare @thing_id int, @ra float, @dec float, @zgal float;

DECLARE my_cursor cursor read_only
FOR
SELECT mt.thing_id, mt.ra_gal, mt.dec_gal, mt.zgal FROM MYDB.{in_tablename} as mt
OPEN my_cursor

WHILE(1=1)
BEGIN
  FETCH NEXT from my_cursor into @thing_id, @ra, @dec, @zgal
  IF (@@fetch_status < 0) break
  INSERT MYDB.{tablename}
  SELECT top 1 @thing_id, @zgal, N.distance, p.objid, 
p.run, p.rerun, p.camcol, p.field, p.obj,
p.rowc_g,p.rowc_r,p.rowc_i,
p.colc_g,p.colc_r,p.colc_i,
p.petroR50_g, p.petroR50_r, p.petroR50_i, 
p.petroMag_g, p.petroMag_r, p.petroMag_i, 
p.ModelMag_g, p.ModelMag_r, p.ModelMag_i, 
p.CModelMag_g, p.CModelMag_r, p.CModelMag_i, 
p.fracdev_g, p.fracdev_r, p.fracdev_i, 
p.devmag_g, p.devmag_r, p.devmag_i, 
p.expmag_g, p.expmag_r, p.expmag_i,
p.extinction_g, p.extinction_r, p.extinction_i, 
p.type, p.lnLStar_r
  FROM PhotoPrimary as p,
dbo.fGetNearbyObjEq(@ra,@dec,3.0) as N where p.objid=N.objid 
order by N.distance
END

CLOSE my_cursor
  DEALLOCATE my_cursor""".format(**job_info)

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


def casjobs(gal_cat, casjobs_info):
    os.system('rm {data_dir}{filename}'.format(**gal_cat))

    thisdir = os.getcwd()
    casjobs='java -jar %s ' %casjobs_info['cas_jar_path']

    write_config(casjobs_info)

    full_jobname = "%s_%s" %(casjobs_info['jobname'],str(datetime.date.today()).replace('-','_'))
    job_info = {'full_jobname':full_jobname,
                'tablename':full_jobname,
                'in_tablename':"in_"+full_jobname,
                'casjobs':casjobs,
                'chunknum':0,
                'chunk':100
                }
    
    print 'CUT PIPE: Preparing mydb output tables'
    exec_cmd('{casjobs} execute -t "mydb" -n "drop output table" "drop table {tablename}"'.format(**job_info))
    exec_cmd('{casjobs} -j '.format(**job_info))

    exec_cmd('{casjobs} execute -t "mydb" -n "create output table" "{cmd}"'.format(cmd=create_table(job_info['tablename']),**job_info))
    exec_cmd('{casjobs} -j '.format(**job_info))
    
    print 'CUT PIPE: Preparing mydb input tables'
    exec_cmd('{casjobs} execute -t "mydb" -n "drop input table" "drop table {in_tablename}"'.format(**job_info))
    exec_cmd('{casjobs} -j '.format(**job_info))
    
    exec_cmd('{casjobs} execute -t "mydb" -n "create input table" "CREATE table {in_tablename} (thing_id int, ra_gal float, dec_gal float, zgal float);"'.format(**job_info))
    exec_cmd('{casjobs} -j '.format(**job_info))

    cursor = mysql_connect('catalog',mysql_params['user'],mysql_params['pwd'])

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
