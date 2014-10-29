import os
import numpy as np
import subprocess as sub
import sys
import time

def exec_cmd(job_str):
    p1=sub.Popen(job_str, shell=True, stdout = sub.PIPE)
    output = p1.communicate()[0]
    output = output.strip()
    return output

model_dict = {'dev':'d', 'ser':'s','devexp':'de', 'serexp':'se'}

min_num = 1738
max_num = 2650

for count in range(int(np.ceil(min_num/10.0)), int(np.ceil(max_num/10.0) +1)):
    while int(exec_cmd('qstat | grep "ameert" | grep "qw" -c')) > 3:
        time.sleep(60)
        
    for model in ['ser']:#'dev','ser','devexp','serexp']:
        a = open('catalog.py', 'w')
        a.write("""#!/bin/bash
#$ -t %d-%d 
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=2G
#$ -wd /data2/home/ameert/catalog/r/fits/
#$ -o /data2/home/ameert/regen_galfit/output/
#$ -e /data2/home/ameert/regen_galfit/output/
#$ -N mhre%s

/data2/home/ameert/regen_galfit/measure_corrected_psf.py %s full_dr7_r $SGE_TASK_ID
""" %((count-1)*10+1, count*10, model_dict[model], model))

        os.system('qsub catalog.py')
