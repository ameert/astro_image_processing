#++++++++++++++++++++++++++
#
# TITLE: get_field_cat
#
# PURPOSE: queries casjobs for all targets in a field
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
from make_new_query import field_query
import subprocess as sub
import sys
from clean_cat import clean_cat

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

    thisdir = os.getcwd()
    # Uses the version of casjobs installed with galmorph for now.
    cas_path = '/home/ameert/git_projects/alans-image-processing-pipeline/casjobs-querey'
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
    jn = 'field-%d-%d-%d-%d' %(gal_cat['run'], gal_cat['rerun'], 
                               gal_cat['camcol'], gal_cat['field'])
    print 'CUT PIPE: Preparing mydb input/output tables'
    exec_cmd(casjobs + 'execute -t "mydb" -n "drop output table" "drop table cl_out"')
    print 'It is ok if it said error just then. -AMM'

    fid = open('query%s.txt' %jn, 'w')
    fid.write(field_query(gal_cat['run'], gal_cat['rerun'], 
                          gal_cat['camcol'], gal_cat['field']))
    fid.close()

    print 'CUT PIPE: Running Query'
    cmd = 'run -n "%s" -f query%s.txt' %(jn,jn)
    print casjobs + cmd
    exec_cmd(casjobs + cmd)
    print 'GALMORPH: Downloading Results'
    cmd = 'extract -force -type "csv" -download %s -table cl_out' %(jn)
    print casjobs + cmd 
    casjobs_out = exec_cmd(casjobs + cmd)
    down_file = get_filename(casjobs_out)
    clean_cat(down_file, jn)
#    cmd = 'cat %s >> %s' %(jn, data_dir + gal_cat['filename'])
    cmd = 'cp %s %s' %(jn, data_dir + gal_cat['filename'])
 
    print cmd
    os.system(cmd)
    for a in [down_file, jn]:
        cmd = 'rm %s' %(a)
        print cmd
        os.system(cmd)
    #os.system('rm CasJobs.config')
    #os.system('rm query.txt')
    
    return 0
    
def get_file_info(filename):
    """returns the last line of the file and the number of lines in the file."""

    infile = open(filename)
    lines = infile.readlines()
    infile.close()

    numlines = len(lines)
    lastline = lines[-1]

    return numlines, lastline


    
if __name__ == "__main__":
    
    data_dir = '/home/ameert/RESEARCH/clusters/data/field_cat/'

    username = 'upenn_pymorph'
    wsid = '396840617'
    password = 'pymorph_upenn'

    for a in [(138529, 2583, 40, 4, 130, 419),
              (142447,  2662, 40, 3, 285, 210),
              (149162,  2738, 40, 4, 24, 201),
              (558387,  3325, 41, 1, 136, 212),
              (561842,  3325, 41, 4, 180, 133)]:
        gal_cat = {'galcount':a[0], 'run':a[1], 'rerun':a[2],
                   'camcol':a[3], 'field':a[4], 
                   'filename':'field_%06d.fits'%a[0]}

        print gal_cat
        casjobs(gal_cat, data_dir, username, wsid, password)
        

