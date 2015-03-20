#!/bin/bash
#$ -t 100-2683
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=2G
#$ -wd /data2/home/ameert/catalog/scripts/
#$ -o /data2/home/ameert/catalog/job_output/
#$ -e /data2/home/ameert/catalog/job_output/
#$ -N rm_s
#$ -tc 60
#$ -h

/data2/home/ameert/catalog/scripts/clean_ser.py $SGE_TASK_ID


