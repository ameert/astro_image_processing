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
    p1=sub.Popen(job_str, shell=True, stdout = sub.PIPE)
    output = p1.communicate()[0]
    output = output.strip()
    return output

def get_filename(casjobs_out):
    casjobs_out = casjobs_out.split('Saved as: ')[1]
    filename = casjobs_out.split()[0]
    return filename

def casjobs(gal_cat, data_dir, username, wsid, password, search_82 = 0):

    os.system('rm %s'%(data_dir + gal_cat['filename']))

    lastnum = '-99'
    chunk = 10000

    thisdir = os.getcwd()
    # Uses the version of casjobs installed with galmorph for now.
    cas_path = '/home/ameert/galmorph/matlab/casjobs'
    casjobs='java -jar %s/casjobs.jar ' %cas_path

    # write config file used by casjobs
    config_file = open('CasJobs.config','w')
    
    if search_82:
        config_file.write('wsid=' + wsid + '\n' +
                          'password=' + password + '\n' +
                          'default_target=Stripe82\n' +
                          'default_queue=1\n' +
                          'default_days=1\n' +
                          'verbose=true\n' +
                          'debug=false\n' +
                          'jobs_location=http://casjobs.sdss.org/'+
                          'casjobs/services/jobs.asmx\n')
    else:    
        config_file.write('wsid=' + wsid + '\n' +
                          'password=' + password + '\n' +
                          'default_target=DR7\n' +
                          'default_queue=1\n' +
                          'default_days=1\n' +
                          'verbose=true\n' +
                          'debug=false\n' +
                          'jobs_location=http://casjobs.sdss.org/'+
                          'casjobs/services/jobs.asmx\n')

    config_file.close()
    # name that will appear in the users casjobs query list. This is the current date
    jn = datetime.date.today()
    table_count = 1
    while 1:
        jn_tmp = str(jn) + '_' + str(table_count)
        print 'CUT PIPE: Preparing mydb input/output tables'
        exec_cmd(casjobs + 'execute -t "mydb" -n "drop output table" "drop table cl_out"')
        print 'It is ok if it said error just then. -AMM'

        fid = open('query%d.txt' %table_count, 'w')
        fid.write(make_query(stripe_82 = search_82, start_objid = lastnum,
                             chunk_size=chunk))
        fid.close()

        print 'CUT PIPE: Running Query'
        cmd = 'run -n "%s" -f query%d.txt' %(jn_tmp, table_count)
        exec_cmd(casjobs + cmd)
        print 'GALMORPH: Downloading Results'
        cmd = 'extract -force -type "csv" -download %s -table cl_out' %(jn_tmp)
        print casjobs + cmd 
        casjobs_out = exec_cmd(casjobs + cmd)
        down_file = get_filename(casjobs_out)
        cmd = 'cat %s >> %s' %(down_file, data_dir + gal_cat['filename'])
        os.system(cmd)
        num_out, lastline = get_file_info(down_file)
        lastnum = lastline.split(',')[0]
        #os.system(cmd)
        # os.system('rm CasJobs.config')
        # os.system('rm query.txt')
        if float(num_out)/chunk < .95:
#        if table_count > 1:
            break
        table_count+=1

    return 0
    
def get_file_info(filename):
    """returns the last line of the file and the number of lines in the file."""

    infile = open(filename)
    lines = infile.readlines()
    infile.close()

    numlines = len(lines)
    lastline = lines[-1]

    return numlines, lastline


    
    
