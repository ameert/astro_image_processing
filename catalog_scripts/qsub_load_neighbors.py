#!/bin/bash
#$ -t 100-2683
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=2G
#$ -wd /data2/home/ameert/catalog/r/fits/
#$ -o /data2/home/ameert/catalog/r/job_output/
#$ -e /data2/home/ameert/catalog/r/job_output/
#$ -N sn
#$ -tc 100
/data2/home/ameert/catalog/scripts/load_neighbors.py ser r $SGE_TASK_ID


