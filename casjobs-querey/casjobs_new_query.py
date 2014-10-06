#++++++++++++++++++++++++++
#
# TITLE: casjobs_new_query
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
from make_new_query import *
import subprocess as sub
import sys

def exec_cmd(job_str):
    print job_str
    p1=sub.Popen(job_str, shell=True, stdout = sub.PIPE)
    output = p1.communicate()[0]
    output = output.strip()
    return output

def get_filename(casjobs_out):
    casjobs_out = casjobs_out.split('Saved as: ')[1]
    filename = casjobs_out.split()[0]
    return filename

def casjobs(gal_cat, casjobs_info):
    os.system('rm {data_dir}{filename}'.format(**gal_cat))

    thisdir = os.getcwd()
    casjobs='java -jar %s ' %casjobs_info['cas_jar_path']

    # write config file used by casjobs
    config_str = """wsid={wsid}
password={password}
default_target={search_target}
default_queue=1
default_days=1
verbose=true
debug=false
jobs_location=http://skyserver.sdss3.org/casjobs/services/jobs.asmx
""".format(**casjobs_info)
    
    config_file = open('CasJobs.config','w')
    config_file.write(config_str)
    config_file.close()

    full_jobname = "%s_%s" %(casjobs_info['jobname'],str(datetime.date.today()).replace('-','_'))
    table_count = 1
    job_info = {'full_jobname':full_jobname,
                'casjobs':casjobs,
                'table_count':0,
                'lastnum':'-99',
                'chunk':100#10000
                }
    
    while True:
        job_info['table_count']+=1
        job_info['jobname']='{full_jobname}_{table_count}'.format(**job_info)
        job_info['query_name']='query_{jobname}.txt'.format(**job_info)
        job_info['tablename'] = job_info['jobname']
        
        print 'CUT PIPE: Preparing mydb input/output tables'
        exec_cmd('{casjobs} execute -t "mydb" -n "drop output table" "drop table {tablename}"'.format(**job_info))
        exec_cmd('{casjobs} -j '.format(**job_info))
        print 'NOTICE:It is OK if it said error just then.'
        raw_input()
        fid = open(job_info['query_name'],'w')
        fid.write(catalog_query(job_info))
        fid.close()
        raw_input()
        print 'CUT PIPE: Running Query'
        job_info['cmd']='{casjobs} run -n "{jobname}" -f {query_name}'.format(**job_info)
        print job_info['cmd']
        exec_cmd(job_info['cmd'])
        raw_input()
        print 'GALMORPH: Downloading Results'
        job_info['cmd']='{casjobs} extract -force -type "csv" -download {jobname} -table {tablename}'.format(**job_info)
        print job_info['cmd']
        casjobs_out = exec_cmd(job_info['cmd'])
        print casjobs_out
        raw_input()
        down_file = get_filename(casjobs_out)
        cmd = 'cat %s >> %s' %(down_file, 
                               gal_cat['data_dir']+gal_cat['filename'])
        os.system(cmd)
        num_out, lastline = get_file_info(down_file)
        job_info['lastnum'] = lastline.split(',')[0]
        os.system('rm %s' %down_file)
        if num_out<chunk:
            break #because we must be at the end of the list
        if job_info['table_count']>1:
            break
    return 0
    
def get_file_info(filename):
    """returns the last line of the file and the number of lines in the file."""

    infile = open(filename)
    lines = infile.readlines()
    infile.close()

    numlines = len(lines)
    lastline = lines[-1]

    return numlines, lastline


    
    
