#!/bin/bash
#$ -t 1-2683
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=2G
#$ -wd /data2/home/ameert/catalog/g/
#$ -o /data2/home/ameert/catalog/g/job_output/
#$ -e /data2/home/ameert/catalog/g/job_output/
#$ -N cn
#$ -l low
#$ -tc 40

/data2/home/ameert/catalog/scripts/count_neighbors.py full_dr7_neighborcount ser i $SGE_TASK_ID

