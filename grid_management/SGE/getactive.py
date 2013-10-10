#!/data2/home/ameert/python/bin/python2.5

import os
import sys
import subprocess as sub
import time

def IsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def getactive(username='*'):
    qstatin="""qstat -u '%s'""" %(username)

    p1=sub.Popen(qstatin, shell=True, stdout = sub.PIPE)
    (stdout, stderr) = p1.communicate()

    stdout = stdout.strip()
    stdout = stdout.split('\n') 

    active_jobs = {}
    
    for line in stdout:
        line = line.strip()
        line = line.split()

        try:
            if IsInt(line[0]):
                jobid =int(line[0])
                state = line[4]
                jobname = line[2]
            
                # if 'r' in state:
                #    active_jobs.append(jobid)
                # elif 'qw' == state:
                #    active_jobs.append(jobid)

                active_jobs[jobname] = jobid
        except:
            pass
        
            
    return active_jobs 


#print getactive('ameert')

