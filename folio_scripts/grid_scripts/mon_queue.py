#!/data2/home/ameert/python/bin/python2.5

import os
import sys
import subprocess as sub
import time

from nicecount import *

def exec_cmd(job_str):
    p1=sub.Popen(job_str, shell=True, stdout = sub.PIPE)
    output = p1.communicate()[0]
    output = output.strip()
    return output

username='ameert'

minnumqueuedtorun=int(sys.argv[1])
maxnumqueuedtorun=int(sys.argv[2])
freeslots=int(sys.argv[3])

h_str = """qstat | grep '%s' | grep -c 'hqw'""" %username

prev_active_jobs = []

while int(exec_cmd(h_str))>0:  #while there are still queued, held jobs
    
    countall, countRall ,countQWall ,countHall ,countSall ,countEall ,countRme ,countQWme ,countHme ,countSme ,countEme = nicecount()

    
    reactivate=0
    print countRme+countQWme
    print 128-(countQWall+countRall)
    if (countRme+countQWme)<minnumqueuedtorun:
        reactivate=1
    elif (128-(countQWall+countRall))>freeslots:
        # 128 is the maximum number of jobs on the cluster at any gicen time
        # check this with "qstat -g c"
        if (countRme+countQWme)<maxnumqueuedtorun:
            reactivate=1;

    if reactivate==1: 
        jobtostartline="""qstat | grep '%s' | grep -m1 'hqw'""" %username
        jobtostartline=exec_cmd(jobtostartline)
        jobtostartline = jobtostartline.strip()
        
        jobtostart = jobtostartline.split()[0]
        print "qalter -h U %s" %jobtostart
        os.system("qalter -h U %s" %jobtostart)
        
        time.sleep(6)
    else:
        time.sleep(60)
