#!/bin/bash
#$ -t 1-1076
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=2G
#$ -wd /data2/home/ameert/catalog/r/
#$ -o /data2/home/ameert/catalog/r/job_output/
#$ -e /data2/home/ameert/catalog/r/job_output/
#$ -N hrs
#$ -l low
#$ -tc 80
#$ -hold_jid 600397
/data2/home/ameert/regen_galfit/measure_corrected_psf.py ser CMASS i $SGE_TASK_ID
