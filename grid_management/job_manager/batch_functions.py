import sys
import os
import grid_management.SGE as SGE
from grid_management.job_manager.is_complete import *

# for job submission
def sub_job(jobs, running_jobs):
    key_to_pop = sorted(jobs.keys(), key=lambda job_key: int(job_key[-4:]))[0]
    job_to_pop = jobs[key_to_pop]
    # now submit the job
    os.system(job_to_pop['qsub'])
    # and move the job to the running list
    running_jobs[key_to_pop] = job_to_pop
    del jobs[key_to_pop]

    return

def find_closed_jobs(running_jobs, username):
    closed_jobs = []
    active_jobs = SGE.getactive(username)

    for job in running_jobs.keys():
        if job not in active_jobs.keys():
            closed_jobs.append(job)

    return closed_jobs

def test_complete(closed_jobs, running_jobs):
    completed_jobs = []
    for key in closed_jobs:
        if check_done(running_jobs[key]['data_loc']+'/'+running_jobs[key]['incat'],running_jobs[key]['out_loc']+'/'+running_jobs[key]['outcat'],
                      doneness = 0.05):
            # job is at least 95% done             
            completed_jobs.append(key)
        else:
            # resubmit the job
            os.system(running_jobs[key]['qsub'])

    return completed_jobs

def post_process(comp_job):
    #this measures halflight radii and cleans
    os.system(comp_job['hrad_qsub'])
    
    return
