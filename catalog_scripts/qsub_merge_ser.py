#!/bin/bash
#$ -t 1-2683
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=2G
#$ -wd /data2/home/ameert/catalog/r/fits/
#$ -o /data2/home/ameert/catalog/r/job_output/
#$ -e /data2/home/ameert/catalog/r/job_output/
#$ -N mer

/data2/home/ameert/catalog/scripts/clean_ser.py r $SGE_TASK_ID


