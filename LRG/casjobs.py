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
import subprocess as sub
import sys
from query_functions import *

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
                'chunk':casjobs_info['chunksize']
                }
    
    print 'CUT PIPE: Preparing mydb output tables'
    exec_cmd('{casjobs} execute -t "mydb" -n "drop output table" "drop table {tablename}"'.format(**job_info))
    exec_cmd('{casjobs} -j '.format(**job_info))

    exec_cmd('{casjobs} execute -t "mydb" -n "create output table" "{cmd}"'.format(cmd=create_table(job_info['tablename']),**job_info))
    exec_cmd('{casjobs} -j '.format(**job_info))
    
    print 'CUT PIPE: Preparing mydb input tables'
    exec_cmd('{casjobs} execute -t "mydb" -n "drop input table" "drop table {in_tablename}"'.format(**job_info))
    exec_cmd('{casjobs} -j '.format(**job_info))
    
    exec_cmd('{casjobs} execute -t "mydb" -n "create input table" "CREATE table   {in_tablename} (id int, ra_gal float, dec_gal float, zgal float, theta float, deltaz_photo float, deltaz_spec float);"'.format(**job_info))
    exec_cmd('{casjobs} -j '.format(**job_info))

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
        chunkdata = get_chunk(job_info['chunk'],job_info['chunknum'])
        exec_cmd('{casjobs} execute -t "mydb" -n "load chunk" "{cmd}"'.format(cmd=load_chunk(chunkdata, job_info['in_tablename']),**job_info))
        exec_cmd('{casjobs} -j '.format(**job_info))
        print 'CUT PIPE: Chunk successfully loaded!'
        
        fid = open(job_info['query_name'],'w')
        fid.write(cone_search_query(job_info,is_spec=casjobs_info['specsearch']))
        fid.close()
        raw_input()
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
        if chunkdata['id'].size<job_info['chunk']:
            break #because we must be at the end of the list
    return 0
 
if __name__ == "__main__":
    from astro_image_processing.user_settings import casjobs_info
    
    casjobs_info.update({'cas_jar_path':'../casjobs_query/casjobs.py',
                   'jobname':'test_spectro',
                   'search_target':'DR10',
                   'chunksize':1000,
                   'specsearch':True
                   })
    
    gal_cat = {'filename':'test_raw_spectro.cat',
               'data_dir':'./data/',
               'out_file':'test_spectro.cat'
           }

    casjobs(gal_cat, casjobs_info)
