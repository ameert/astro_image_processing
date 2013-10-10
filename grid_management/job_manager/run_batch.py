import os
import sys
import time
import grid_management.utilities as ut
import grid_management.SGE as SGE
from grid_management.job_manager.prep_job import job_creator
from grid_management.job_manager.mon_queue import mon_queue 
from grid_management.job_manager.batch_functions import *


###################################################
# IMPORT SETTINGS
###################################################

from grid_management.job_manager.settings import *

##################################################
# here is initalization of the job_creator
###################################################
job_maker = job_creator(incat_stem = 'sdss', outcat = 'result.csv', 
                        path_stem =  '/data2/home/ameert/catalog/', 
                        pymorph_loc = '/data2/home/ameert/pymorph/pymorph/pymorph.py',
                        hrad_script_loc = '/data2/home/ameert/catalog/scripts/measure_and_clean.py',
                        mysql_table_stem = 'full_dr7',
                        band = band, UN = 8.0, fit_sky = 1,
                        cas_model = 'dev', models = models, 
                        jobs_to_run = jobs_to_run,
                        job_prefix = job_prefix
                        )
                        

#######################################################
# MAIN
#######################################################

def run_batch():
        
    # first construct the job dictionary
    # if we are restarting the run, read in the currently running jobs and the
    # completed jobs
    if restart:
        running_jobs = ut.un_pickle_data('%s/running_jobs.backup' %pickle_path)
        completed_jobs = ut.un_pickle_data('%s/completed_jobs.backup' %pickle_path)

    else:
        running_jobs = {} # this is the submitted jobs
        completed_jobs = {} # this is the completed jobs

    # Now create the jobs that have not yet run
    jobs = job_maker.fill_job_dict(running_jobs, completed_jobs)

    ut.pickle_data(jobs, '%s/current_jobs.backup' %pickle_path)

    # Now we must start submitting the jobs and monitoring for completion
    lengths = np.array([len(jobs.keys()),len(running_jobs.keys()),len(completed_jobs.keys())])

    while lengths[0] > 0 or lengths[1]>0: #if jobs are waiting or running
        countsAll, countsMe = SGE.nicecount(username) # get queue job info

        while countsMe['hqw'] < minnumqueuedholding and lengths[0] > 0:
            # if too few jobs are queued and waiting
            sub_job(jobs, running_jobs) # submit a job 
            time.sleep(1)
            countsAll, countsMe = SGE.nicecount(username)

        mon_queue(minnumqueuedtorun,maxnumqueuedtorun,maxwaiting,username)

        # Now check for completion
        closed_jobs = find_closed_jobs(running_jobs, username)

        complete = test_complete(closed_jobs, running_jobs)
        # run jobs ready for postprocessing and cleaning
        for comp_job in complete:
            post_process(running_jobs[comp_job])
            print "job %s complete!!! removing job!!!" %comp_job
            ut.send_mail(comp_job, address = email_address)
            completed_jobs[comp_job] = running_jobs[comp_job]
            completed_jobs[comp_job]['timestamp'] = time.strftime("%d %b %Y %H:%M:%S", time.localtime())
            del running_jobs[comp_job]
        time.sleep(15)
        ut.pickle_data(jobs, '%s/current_jobs.backup' %pickle_path)
        ut.pickle_data(running_jobs, '%s/running_jobs.backup' %pickle_path)
        ut.pickle_data(completed_jobs, '%s/completed_jobs.backup' %pickle_path)
        lengths = np.array([len(jobs.keys()),len(running_jobs.keys()),len(completed_jobs.keys())])

        print "=============STATUS=============="
        print "Time: %s" %time.strftime("%d %b %Y %H:%M:%S", time.localtime())
        print "Waiting jobs: %d" %lengths[0]    
        print "Running jobs: %d" %lengths[1]    
        print "Completed jobs: %d" %lengths[2]
        print "Total jobs: %d" %np.sum(lengths)
        print "---------------------------------"

if __name__ == '__main__':
    run_batch()
    
