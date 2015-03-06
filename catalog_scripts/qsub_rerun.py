#!/bin/bash
#$ -t 1-2
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=2G
#$ -wd /data2/home/ameert/catalog/g/fits/
#$ -o /data2/home/ameert/catalog/g/job_output/
#$ -e /data2/home/ameert/catalog/g/job_output/
#$ -N fsere
#$ -h

/data2/home/ameert/catalog/scripts/rerun_missing.py $SGE_TASK_ID


