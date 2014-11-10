import os
import os.path
import sys
from is_complete import *
from prep_job import *
import time
from nicecount import *
import subprocess as sub
from getactive import *
import pickle
import sys

username='ameert'
band = sys.argv[1]
models = ['ser']#['exp', 'dev','ser','devexp','serexp']#['cmodel']#['ser','serexp']#['dev','ser','devexp','serexp']
pymorph_loc = '/data2/home/ameert/pymorph/pymorph.py'
path_stem ='/data2/scratch/ameert/CMASS/'
#path_stem ='/data2/home/ameert/andre_bcg/'
#path_stem ='/data2/home/ameert/des_sims/'
#jobs_to_run = np.concatenate((np.arange(1,41),np.arange(81,121)))
#jobs_to_run = np.arange(1,2684)
jobs_to_run = range(260,351)
#folders = np.loadtxt('/data2/home/ameert/catalog/scripts/folders_sample.txt', unpack=True)
#jobs_to_run = folders.astype(int)

restart =0

minnumqueuedtorun= 10
maxnumqueuedtorun= 120
maxwaiting = 10

minnumqueuedholding = 30

# execute the command and return the results
def exec_cmd(job_str):
    p1=sub.Popen(job_str, shell=True, stdout = sub.PIPE)
    output = p1.communicate()[0]
    output = output.strip()
    return output

# make the catalog 
def make_config(outdir, model, band, datadir, tablename, cat_name):
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
    #if not os.path.isdir(datadir):
    #    os.mkdir(datadir)
    # NOTE YOU MUST CHANGE SKY VALUE FOR CHIPS
    write_config('%s/config.py' %(outdir), cat_name, tablename, outdir, datadir, fit_type= model, fit_sky = 1, band = band)
    pass

# construct job names
def make_job(job_name, outdir, jobdir, pymorph_loc, hrad = 0):
    job = "qsub -V -h -l low -l h_vmem=2G -o %s/%s.out -e %s/%s.err -N NAME_BLANK -wd %s " %(jobdir, job_name, jobdir, job_name, outdir)

    if hrad:
        job = job.replace('-h', '')
        job = job.replace('NAME_BLANK', 'hrad')
        job += " /data2/home/ameert/catalog/scripts/measure_and_clean.py " 
#        job += " /data2/home/ameert/grid_scripts/clean_dir.py "        
    else:
        job = job.replace('NAME_BLANK', job_name)
        job += " %s\n"  %pymorph_loc
    
    return job

# construct job info dictionary
def make_job_dict(job_name, count, model, band, pymorph_loc):
    a = {}
    a['incat'] = 'sdss_%s_%d.cat' %(band,count)
    a['outcat'] = 'result.csv'
    a['data_loc'] = '%s/%s/data/%04d/' %(path_stem,band,count)
    a['job_loc'] = '%s/%s/job_output' %(path_stem, band)
    #a['out_loc'] = '%s/%s/fits/rerun/%s/%04d' %(path_stem,band, model, count)
    #a['out_loc'] = '%s/%s/fits/deep/%s/%04d' %(path_stem,band, model, count)
    a['out_loc'] = '%s/%s/fits/%s/%04d' %(path_stem,band, model, count)
    a['qsub'] = make_job(job_name, a['out_loc'],a['job_loc'], pymorph_loc) 
    a['tablename'] = 'CMASS_%s_%s' %(band,model)
    a['model'] = model
    a['count'] = count
    a['band'] = band
    a['hrad_qsub'] = make_job(job_name, a['out_loc'],a['job_loc'], pymorph_loc, hrad=1) + a['tablename'] + ' '+model+ ' '+str(count)
    a['clean_qsub'] = make_job(job_name, a['out_loc'],a['job_loc'], pymorph_loc, hrad=1) + a['tablename'] + ' '+model+ ' '+str(count)
    a['timestamp'] = ''
    a['istransferred'] = 0
    return a

# for job submission
def sub_job(jobs, running_jobs):
    counts = [a['count'] for a in jobs.values()]
    minval = np.min(np.array(counts))
    for model in models:
        if '%s%04d' %(name_dict[model], minval) in jobs.keys():
            print '%s%04d' %(name_dict[model], minval) 
            key_to_pop = '%s%04d' %(name_dict[model], minval)
            break
    job_to_pop = jobs[key_to_pop]
    # tranfser the data 
    #if not os.path.isdir(job_to_pop['data_loc']):
    #    os.system('scp -r ameert@chitou.physics.upenn.edu:/media/SDSS2/fit_catalog/data/%s/%04d /data2/home/ameert/catalog/%s/data/' %(job_to_pop['band'],job_to_pop['count'],job_to_pop['band']))
    #os.system('rsync -u ameert@chitou.physics.upenn.edu:/media/SDSS2/fit_catalog/data/%s/%04d/* %s' %(job_to_pop['band'], job_to_pop['count'], job_to_pop['data_loc']))
    #os.system('rsync -u ameert@chitou.physics.upenn.edu:/home/ameert/bcgfukugita/%04d/* %s' %(job_to_pop['count'], job_to_pop['data_loc']))
    # now submit the job
    os.system(job_to_pop['qsub'])
    # and move the job to the running list
    running_jobs[key_to_pop] = job_to_pop
    del jobs[key_to_pop]

    return


# for monitoring jobs
def mon_queue(minnumqueuedtorun, maxnumqueuedtorun, maxwaiting, running_jobs, username = 'ameert'):
    h_str = """qstat | grep '%s'| grep -c 'hqw'""" %username


    print exec_cmd(h_str)
    while int(exec_cmd(h_str))>0:  #while there are still queued, held jobs
        
        countsAll ,countsMe = nicecount()
        
        reactivate=0
        print countsMe['r']+countsMe['qw']
        print 128-(countsAll['r']+countsAll['qw'])
        if (countsMe['r']+countsMe['qw'])<minnumqueuedtorun:
            reactivate=1
        elif countsMe['qw']<maxwaiting:
            # we will only submit jobs if there are not too many queued and waiting
            # check this with "qstat -g c"
            if (countsMe['r']+countsMe['wq'])<maxnumqueuedtorun:
                reactivate=1;

        if reactivate==1: 
            jobtostartline="""qstat| grep '%s'| grep -m1 'hqw'""" %username
            jobtostartline=exec_cmd(jobtostartline)
            jobtostartline = jobtostartline.strip()
        
            jobtostart = jobtostartline.split()[0]
            print "qalter -h U %s" %jobtostart
            os.system("qalter -h U %s" %jobtostart)
        
            time.sleep(1)
        else:
            time.sleep(2)


def find_closed_jobs(running_jobs, username = username):
    closed_jobs = []
    active_jobs = getactive(username)

    for job in running_jobs.keys():
        if job not in active_jobs.keys():
            closed_jobs.append(job)

    return closed_jobs

def test_complete(closed_jobs, running_jobs):
    completed_jobs = []
    for key in closed_jobs:
        if check_done(running_jobs[key]['data_loc']+'/'+running_jobs[key]['incat'],running_jobs[key]['out_loc']+'/'+running_jobs[key]['outcat']):
            # job is at least 95% done             
            completed_jobs.append(key)
        else:
            # resubmit the job
            os.system(running_jobs[key]['qsub'])

    return completed_jobs

def post_process(comp_job):
    #this measures halflight radii and cleans
    os.system(comp_job['hrad_qsub'])
    #os.system(comp_job['clean_qsub'])
    # now transfer the fit data back to chitou 
    #os.system('rsync -ur %s ameert@chitou.physics.upenn.edu:/media/ACTIVE/fit_catalog/fits/%s/ ' %(comp_job['outdir'], comp_job['model']))
    pass
    return

def pickle_data(data, filename):
    a = open(filename, 'w')
    pickle.dump(data,a)
    a.close()
    return

def un_pickle_data(filename):
    a = open(filename)
    data = pickle.load(a)
    a.close()
    return data

def send_mail(comp_job):
    cmd = """echo "pymorph %s job complete" | mail -s "pymorph %s job complete" alan.meert@gmail.com""" %(comp_job, comp_job)
    exec_cmd(cmd)
    return

#######################################################
# MAIN
#######################################################

jobs = {} # this is the waiting jobs
running_jobs = {} # this is the submitted jobs
completed_jobs = {} # this is the completed jobs
name_dict = {'cmodel':'cm','dev':'fd','exp':'fe', 'ser':'fs', 'devexp':'fde', 'serexp':'fse'}
    
# first construct the job dictionary
for job_count in jobs_to_run:
    for model in models:
        job_name = "%s%04d" %(name_dict[model],job_count)
        jobs[job_name] = make_job_dict(job_name, job_count,  model, band, pymorph_loc)
        make_config(jobs[job_name]['out_loc'], model, band, jobs[job_name]['data_loc'], jobs[job_name]['tablename'], jobs[job_name]['incat'])

print jobs.keys()

pickle_data(jobs, '/data2/home/ameert/grid_scripts/pickled_backup/current_jobs.backup')


if restart:
    running_jobs = un_pickle_data('/data2/home/ameert/grid_scripts/pickled_backup/running_jobs.backup')
    completed_jobs = un_pickle_data('/data2/home/ameert/grid_scripts/pickled_backup/completed_jobs.backup')

    for key in jobs.keys():
        if key in running_jobs.keys():
            del jobs[key]
        elif key in completed_jobs.keys():
            del jobs[key]

# Now we must start submitting the jobs

countsAll,countsMe = nicecount()
countHme = countsMe['h'] 
while len(jobs) > 0 or len(running_jobs)>0: #while there are jobs to submit or jobs running
    countHme = nicecount()[1]['h']
    
    while countHme < minnumqueuedholding and len(jobs)>0:
        # if too few jobs are queued and waiting
        sub_job(jobs, running_jobs) # submit a new job and remove it from the list
        #time.sleep(0.25)
        countHme = nicecount()[1]['h']
        
    mon_queue(minnumqueuedtorun, maxnumqueuedtorun, maxwaiting, running_jobs,
              username = username)

    # Now check for completion
    closed_jobs = find_closed_jobs(running_jobs, username = username)
    
    complete = test_complete(closed_jobs, running_jobs)
    # run jobs ready for postprocessing and cleaning
    for comp_job in complete:
        post_process(running_jobs[comp_job])
        print "job %s complete!!! removing job!!!" %comp_job
        send_mail(comp_job)
        completed_jobs[comp_job] = running_jobs[comp_job]
        completed_jobs[comp_job]['timestamp'] = time.strftime("%d %b %Y %H:%M:%S", time.localtime())
        del running_jobs[comp_job]
    time.sleep(2)
    pickle_data(jobs, '/data2/home/ameert/grid_scripts/pickled_backup/current_jobs.backup')
    pickle_data(running_jobs, '/data2/home/ameert/grid_scripts/pickled_backup/running_jobs.backup')
    pickle_data(completed_jobs, '/data2/home/ameert/grid_scripts/pickled_backup/completed_jobs.backup')
    lengths = np.array([len(jobs.keys()),len(running_jobs.keys()),len(completed_jobs.keys())])

    print "=============STATUS=============="
    print "Time: %s" %time.strftime("%d %b %Y %H:%M:%S", time.localtime())
    print "Waiting jobs: %d" %lengths[0]    
    print "Running jobs: %d" %lengths[1]    
    print "Completed jobs: %d" %lengths[2]
    print "Total jobs: %d" %np.sum(lengths)
    print "---------------------------------"
