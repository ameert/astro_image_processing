#!/data2/home/ameert/python/bin/python2.5

import os
import sys
import time

from grid_management.utilities import exec_cmd, IsInt

def nicecount(username):
    qstatin="""qstat -u '*'"""

    countsAll = {'r':0,'qw':0,'h':0,'s':0,'e':0, 'hqw':0, 'total':0}
    countsMe = {'r':0,'qw':0,'h':0,'s':0,'e':0, 'hqw':0, 'total':0}

    stdout = exec_cmd(qstatin)
    stdout = stdout.split('\n') 

    for line in stdout:
        line = line.strip()
        line = line.split()
        if IsInt(line[0]):
            jobid, prior, jobname, user, state, subdate, subtime =line[0:7]

            countsAll['total'] += 1
            if user == username:
                countsMe['total'] += 1
            for key in countsAll.keys():
                if key in state:
                    countsAll[key] +=1
                    if user == username:
                        countsMe[key] +=1
                        
    return countsAll ,countsMe

if __name__ == '__main__':
    try:
        username = sys.argv[1]
    except:
        print "To run nicecount as a standalone program,\nausername must be supplied as the argument!!!!!"
        sys.exit()

    print nicecount(username)
    
