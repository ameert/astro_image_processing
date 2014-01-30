#!/data2/home/ameert/python/bin/python2.5
import os
import time
import datetime as dt
import sys

job_file = 'jobs.out'
job_oe_loc = '/data2/home/ameert/job_output_folio/'
input_location = '/data2/home/ameert/sdss_sample/fit_new_data/'
output_location = '/data2/home/ameert/sdss_sample/fits_new_out/'
job_output = 'jobs_output.txt'
job_loc = '/data2/home/ameert/run_pymorph_cas.txt'


# first establish the jobs to be tracked

in_jobs = os.popen('qstat')
track_job = {}

for line_num, line in enumerate(in_jobs.readlines()):
    print line
    if line_num > 1:
        split_line = line.split()
        choice = 'blank'
        while choice not in ['n', 'y']:
            print 'Track this job?\n'
            choice = raw_input('answer (n or y): ')
            if choice not in ['n', 'y']:
                print "choice must be either 'n' or 'y'!!!\n\n"
                print line+"\n\n"
        if choice == 'y':
            track_job[split_line[0]]=[split_line[0], split_line[2], split_line[5],split_line[6]]
                        
in_jobs.close()

print track_job.keys()
start_time = (time.ctime()).split()[3]
today = str(dt.date.today())
today = today.split('-')
today = today[1]+'/'+today[2]+'/'+today[0]

print "starting time is "+start_time
print "start date is "+str(today)

print "\nJobs to monitor:"
print "Job\tName\tStart date\tStart time"
print "------------------------------------"

for p_job, p_info in track_job.iteritems():
    print p_info[0],'\t', p_info[1], '\t', p_info[2], '\t', p_info[3]


not_done = 1

while not_done:
    print "Monitoring jobs ...."
    time.sleep(300)

    curr_time = (time.ctime()).split()[3]
    curr_date = str(dt.date.today())
    curr_date = curr_date.split('-')
    curr_date = curr_date[1]+'/'+curr_date[2]+'/'+curr_date[0]

    print "Checking jobs at: " + curr_date + ' '+ curr_time

    curr_jobs = os.popen('qstat')

    curr_jobs_list = []
    curr_jobs.readline()
    curr_jobs.readline()
    for line in curr_jobs.readlines():
        print line
        curr_jobs_list.append(line.split()[0])

    term_list = []

    for job_num in track_job.keys():
        if job_num not in curr_jobs_list:
            term_list.append(job_num)

    if len(term_list) > 0:
        print "Jobs died at " +curr_date + ' '+ curr_time
        for term_item in term_list:
            print term_item
        print '\n'
        
        job_qsub = open(job_loc, 'r')
        qsub_com = []
        corr_term_job = []
        for line in job_qsub.readlines():
            for term_item in term_list:
                if ('-N '+track_job[term_item][1]) in line:
                    print '-N '+track_job[term_item][1]
                    qsub_com.append(line)
                    corr_term_job.append(term_item)
                    
        job_qsub.close
        
        for log, corr_job in zip(qsub_com,corr_term_job):
            
            out_log = log.split('-o ')[1]
            out_log = out_log.split()[0]
            model =out_log.split('_')[-2]
            out_log = open(out_log, 'r')
            tmp_num = 0
            cat_num = log.split('-N ')[1]
            cat_num = cat_num.split()[0]
            cat_num = cat_num.split('_')[1]
            
            for line in out_log.readlines():
                if "B) O_" in line:
                    tmp_num = int(line.split('_')[1])
            out_log.close()

            tmp_cat = open(input_location+'tmpsdss_r_'+model+'_'+cat_num+'.cat', 'w')
            old_cat = open(input_location+'sdss_r_'+model+'_'+cat_num+'.cat', 'r')

            tmp_cat.write(old_cat.readline())
            skip_check = 0
            tot_unfinished = 0

            for line in old_cat.readlines():
                if skip_check == 0:
                    old_num = int(line.split('_')[0])
                    if old_num >= int(tmp_num):
                        skip_check = 1
                else:
                    tmp_cat.write(line)
                    tot_unfinished += 1
            old_cat.close()
            tmp_cat.close()
                
            os.system('cp '+input_location+'tmpsdss_r_'+model+'_'+cat_num+
                      '.cat'+' '+input_location+'sdss_r_'+model+'_'+cat_num+'.cat')

            print track_job.keys()
            
            if tot_unfinished > 10:
                print "job "+corr_job+' smells fishy. Restarting the job.'
                os.system(log)

                updated_jobs = os.popen('qstat')
                for line_num, line in enumerate(updated_jobs.readlines()):
                    print line
                    print log
                    if len(line.split()) > 2:
                        print line.split()[2]
                        if line.split()[2] in log:
                            print line
                            print log.split('-N ')[1].split()[0]
                            split_line = line.split()
                            track_job[split_line[0]]=[split_line[0], split_line[2], split_line[5],split_line[6]]
            
                updated_jobs.close()
            else:
                print "job "+corr_job+' probably finished OK. Letting it die peacefully.'

            del track_job[corr_job]

        print track_job.keys()
        
        if len(track_job.keys()) == 0:
            not_done = 0
        else:
            not_done = 1
                
            
    else:
        print "alls well"
        not_done = 1
