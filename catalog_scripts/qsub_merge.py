#!/bin/bash
#$ -t 2-2683
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=2G
#$ -wd /data2/home/ameert/catalog/r/fits/
#$ -o /data2/home/ameert/catalog/r/job_output/
#$ -e /data2/home/ameert/catalog/r/job_output/
#$ -N md

/data2/home/ameert/catalog/scripts/merge_fits.py r $SGE_TASK_ID


