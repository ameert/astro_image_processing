import os
import sys
import time

from grid_management.utilities import exec_cmd

def release(username, conditions):
    """This function will release anything currently on hold belonging to the user in the queue satisfying the conditions passed by the user. If no conditions are present, it tries to release every held job beloging to the user."""

    cmd = ['qstat',""" '%s' """ %username, """ '-h' """] + conditions
    cmd[-1] = 'CMD_BLANK' + cmd[-1]

    cmd = ' | grep '.join(cmd)

    countstr = cmd.replace('CMD_BLANK', '-c')
    jobstr = cmd.replace('CMD_BLANK', '-m1')
    
    while 1:
        num_jobs = int(exec_cmd(countstr))
        print 'Jobs to release: %d' %num_jobs

        if num_jobs < 1:
            break
        else:
            output = exec_cmd(jobstr)
            output = output.split()[0]

            print "qalter -h U ", output
            exec_cmd("qalter -h U %s" %output)
            time.sleep(0.5)
    return

if __name__ == '__main__':
    try:
        username = sys.argv[1]
    except:
        print "To run release as a standalone program,\nausername must be supplied as the first argument!!!!!\nAdditional constaints may also be passed"
        sys.exit()

    try:
        conditions = [""" '%s' """ %a for a in sys.argv[2:]] 
    except:
        conditions = []

    release(username, conditions)
    
