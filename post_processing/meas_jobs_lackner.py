#!/bin/bash
#$ -t 264-2431
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=4G
#$ -wd /data2/home/ameert/catalog/r/
#$ -o /data2/home/ameert/catalog/r/job_output/
#$ -e /data2/home/ameert/catalog/r/job_output/
#$ -N mln
#$ -l low
#$ -tc 80
#$ 
/data2/home/ameert/regen_galfit/measure_corrected_lackner.py devexp $SGE_TASK_ID
