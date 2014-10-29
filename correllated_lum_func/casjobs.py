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
from match_query_functions import *


def get_chunk(cursor, chunksize, chunknum):
    """returns a chunk of objects for the cone search. This must be done in chuncks to aoid overfilling the casjobs mydb storage space"""
    
    cmd = """select thing_id, plate, mjd, fibre, zspec from claudia_values where zspec between 0.50 and 0.505 
order by thing_id limit {offset},{chunksize};""".format(offset = max((chunknum-1)*chunksize,0), chunksize=chunksize)


    chunkdata = cursor.get_data_dict(cmd, ['thing_id', 'plate','mjd','fiber','zspec'], [int, int, int, int, float])
    return chunkdata

def get_chunk_blanksky(cursor, chunksize, chunknum):
    """returns a chunk of objects for the cone search. This must be done in chuncks to aoid overfilling the casjobs mydb storage space"""
    
    cmd = """select thing_id, zspec, ra_gal, dec_gal from claudia_blanksky where zspec between 0.50 and 0.505 
order by thing_id limit {offset},{chunksize};""".format(offset = max((chunknum-1)*chunksize,0), chunksize=chunksize)


    chunkdata = cursor.get_data_dict(cmd, ['thing_id', 'zspec','ra_gal','dec_gal'], [int, float, float, float])
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
                'chunk':1000
                }
    
    print 'CUT PIPE: Preparing mydb output tables'
    exec_cmd('{casjobs} execute -t "mydb" -n "drop output table" "drop table {tablename}"'.format(**job_info))
    exec_cmd('{casjobs} -j '.format(**job_info))

    exec_cmd('{casjobs} execute -t "mydb" -n "create output table" "{cmd}"'.format(cmd=create_table(job_info['tablename']),**job_info))
    exec_cmd('{casjobs} -j '.format(**job_info))
    
    print 'CUT PIPE: Preparing mydb input tables'
    exec_cmd('{casjobs} execute -t "mydb" -n "drop input table" "drop table {in_tablename}"'.format(**job_info))
    exec_cmd('{casjobs} -j '.format(**job_info))
    
#    exec_cmd('{casjobs} execute -t "mydb" -n "create input table" "CREATE table {in_tablename} (thing_id int, plate smallint, mjd int, fiber int, zspec float);"'.format(**job_info))
#    exec_cmd('{casjobs} -j '.format(**job_info))
    exec_cmd('{casjobs} execute -t "mydb" -n "create input table" "CREATE table {in_tablename} (thing_id int, zspec float, ra_gal float, dec_gal float);"'.format(**job_info))
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
        chunkdata = get_chunk_blanksky(cursor, job_info['chunk'],job_info['chunknum'])
        exec_cmd('{casjobs} execute -t "mydb" -n "load chunk" "{cmd}"'.format(cmd=load_chunk_blanksky(chunkdata, job_info['in_tablename']),**job_info))
        exec_cmd('{casjobs} -j '.format(**job_info))
        print 'CUT PIPE: Chunk successfully loaded!'
        
        fid = open(job_info['query_name'],'w')
        fid.write(cone_search_blanksky_query(job_info))
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

    casjobs_info.update({ 'cas_jar_path':'/home/ameert/git_projects/astro_image_processing/casjobs_query/casjobs.jar',
                          'jobname':'correlation_lum_blanks',
                          'search_target':'DR10'})
    gal_cat = {'filename':'correlated_sample_raw_blanks.cat',
               'data_dir':'/home/ameert/claudia/data/',
               'out_file':'correlated_sample_blanks.cat'
               }

    casjobs(gal_cat, casjobs_info)
