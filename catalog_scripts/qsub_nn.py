#!/bin/bash
#$ -t 1-180
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=2G
#$ -wd /data2/home/ameert/catalog/scripts/
#$ -o /data2/home/ameert/catalog/job_output/
#$ -e /data2/home/ameert/catalog/job_output/
#$ -N nn_s
#$ -tc 60
#$ -h

/data2/home/ameert/catalog/scripts/count_neighbors.py rerun_short_r_ser ser $SGE_TASK_ID


