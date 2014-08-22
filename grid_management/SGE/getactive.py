#!/data2/home/ameert/python/bin/python2.5

import os
import sys
import time

from grid_management.utilities import exec_cmd, IsInt

def getactive(username='*'):
    """This function will get all submitted jobs for the user """
    qstatin="""qstat -u '%s'""" %(username)

    stdout = exec_cmd(qstatin).split('\n') 

    active_jobs = {}
    
    for line in stdout:
        line = line.strip()
        line = line.split()

        try:
            if IsInt(line[0]):
                jobid =int(line[0])
                state = line[4]
                jobname = line[2]
            
                active_jobs[jobname] = jobid
        except:
            pass
        
            
    return active_jobs 


if __name__ == '__main__':
    try:
        username = sys.argv[1]
    except:
        print "To run getactive as a standalone program,\nausername must be supplied as the first argument!!!!!"
        sys.exit()

    getactive(username)
    

