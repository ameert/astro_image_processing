#!/bin/bash
#$ -t 1-2683
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=2G
#$ -wd /data2/home/ameert/catalog/scripts/
#$ -o /data2/home/ameert/catalog/job_output/
#$ -e /data2/home/ameert/catalog/job_output/
#$ -N chi
#$ -tc 80

/data2/home/ameert/catalog/scripts/load_chi.py $SGE_TASK_ID


