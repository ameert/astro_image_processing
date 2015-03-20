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

def search_query(job_info):
    """The serch query used"""
    cmd = """SELECT  mt.objid_n, p.flags_g, p.flags_r, p.flags_i 
INTO MYDB.{tablename}
FROM  PhotoPrimary as p, MYDB.{in_tablename} as mt where mt.objid_n = p.objid;
""".format(**job_info)

    return cmd

def create_table(tabname):
    """creates the table for cone search output"""
    cmd = """create table {tabname} (objid_n bigint, flags_g bigint,
flags_r bigint, flags_i bigint);""".format(tabname=tabname)

    return cmd

def truncate_table(tabname):
    """truncates a table"""
    cmd = """truncate table {tabname};""".format(tabname=tabname)
    return cmd


def load_chunk(chunkdata, tabname):
    """creates a command to load data to a table denoted by tabname"""
    cmd = """insert into {tabname} VALUES {values};"""

    values = '('+'),('.join([str(a) for a in chunkdata['objid_n']]) + ')'
    return cmd.format(tabname=tabname, values=values)

def get_chunk(cursor, chunksize, chunknum):
    """returns a chunk of objects for the cone search. This must be done in chuncks to aoid overfilling the casjobs mydb storage space"""
    
    cmd = """select objid_n from CMASS_neigh  
order by objid_n limit {offset},{chunksize};""".format(offset = max((chunknum-1)*chunksize,0), chunksize=chunksize)

    data, = cursor.get_data(cmd)
    chunkdata = {'objid_n': data}
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
                'chunk':5000
                }
    
    print 'CUT PIPE: Preparing mydb output tables'
    exec_cmd('{casjobs} execute -t "mydb" -n "drop output table" "drop table {tablename}"'.format(**job_info))
    exec_cmd('{casjobs} -j '.format(**job_info))

    print 'CUT PIPE: Preparing mydb input tables'
    exec_cmd('{casjobs} execute -t "mydb" -n "drop input table" "drop table {in_tablename}"'.format(**job_info))
    exec_cmd('{casjobs} -j '.format(**job_info))
    
    exec_cmd('{casjobs} execute -t "mydb" -n "create input table" "CREATE table {in_tablename} (objid_n bigint);"'.format(**job_info))
    exec_cmd('{casjobs} -j '.format(**job_info))

    cursor = mysql_connect('catalog',mysql_params['user'],mysql_params['pwd'])

    while True:
        job_info['chunknum']+=1
        job_info['jobname']='{full_jobname}_{chunknum}'.format(**job_info)
        job_info['query_name']='query_{jobname}.txt'.format(**job_info)
                
        print 'CUT PIPE: Truncate input tables'
        exec_cmd('{casjobs} execute -t "mydb" -n "Truncate input table" "{cmd}"'.format(cmd=truncate_table(job_info['in_tablename']),**job_info))
        exec_cmd('{casjobs} -j '.format(**job_info))
        
        print 'CUT PIPE: Loading Chunk'
        chunkdata = get_chunk(cursor, job_info['chunk'],job_info['chunknum'])

        exec_cmd('{casjobs} execute -t "mydb" -n "load chunk" "{cmd}"'.format(cmd=load_chunk(chunkdata, job_info['in_tablename']),**job_info))
        exec_cmd('{casjobs} -j '.format(**job_info))
        print 'CUT PIPE: Chunk successfully loaded!'
        
        
        fid = open(job_info['query_name'],'w')
        fid.write(search_query(job_info))
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
        
        print 'CUT PIPE: Preparing mydb output tables'
        exec_cmd('{casjobs} execute -t "mydb" -n "drop output table" "drop table {tablename}"'.format(**job_info))
        exec_cmd('{casjobs} -j '.format(**job_info))

        #os.system('rm %s' %down_file)
        
        if len(chunkdata['objid_n'])<job_info['chunk']:
            break #because we must be at the end of the list
    return 0
 
if __name__ == "__main__":
    from astro_image_processing.user_settings import casjobs_info

    casjobs_info.update({ 'cas_jar_path':'/home/ameert/git_projects/astro_image_processing/casjobs_query/casjobs.jar',
                          'jobname':'correlation_adddat',
                          'search_target':'DR10'})
    gal_cat = {'filename':'correlated_adddat.cat',
               'data_dir':'/home/ameert/claudia/data/',
               'out_file':'correlated_adddat.cat'
               }

    casjobs(gal_cat, casjobs_info)
