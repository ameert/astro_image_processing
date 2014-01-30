#!/data2/home/ameert/python/bin/python2.5
import os

for job in range(11829, 11872):
    os.system('qdel ' + str(job))

    
