import os
import sys
import time
import grid_management.utilities as ut
import grid_management.SGE as SGE

# for monitoring jobs
def mon_queue(minnumqueuedtorun, maxnumqueuedtorun, maxwaiting, username):
    h_str = """qstat | grep '%s' | grep -c 'hqw'""" %username
        
    while int(ut.exec_cmd(h_str))>0:  #while there are still queued, held jobs
        
        countsAll, countsMe = SGE.nicecount(username)
        
        reactivate=0
        print "Total %s jobs: %d" %(username, countsMe['r']+countsMe['qw'])
        print "Approx. open slots: %d" %(124-countsAll['r'])
        print "Waiting jobs for %s: %d" %(username, countsMe['qw']-countsMe['hqw'])
        if (countsMe['r']+countsMe['qw']-countsMe['hqw'])<minnumqueuedtorun:
            reactivate=1
        elif countsMe['qw']-countsMe['hqw']<maxwaiting:
            # we will only submit jobs if there are not too many
            # queued and waiting
            # you can also check with check this with "qstat -g c"
            if (countsMe['r']+countsMe['qw']-countsMe['hqw'])<maxnumqueuedtorun:
                reactivate=1;

        if reactivate==1: 
            jobtostartline="""qstat | grep '%s' | grep -m1 'hqw'""" %username
            jobtostartline=ut.exec_cmd(jobtostartline)
        
            jobtostart = jobtostartline.split()[0]
            print "qalter -h U %s" %jobtostart
            os.system("qalter -h U %s" %jobtostart)
        
            time.sleep(5)
        else:
            time.sleep(60)

    return

if __name__ == '__main__':
    try:
        minnumqueuedtorun=int(sys.argv[1])
        maxnumqueuedtorun=int(sys.argv[2])
        maxwaiting= int(sys.argv[3])
        username = sys.argv[4]
    except:
        print """To run mon_queue as a standalone program,
        a minnumqueuedtorun, maxnumqueuedtorun, maxwaiting, username
        must be supplied as the arguments!!!!!"""
        sys.exit()

    mon_queue(minnumqueuedtorun, maxnumqueuedtorun, maxwaiting, username)
    
