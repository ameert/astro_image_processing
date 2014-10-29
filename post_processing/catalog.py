#!/bin/bash
#$ -t 2641-2650 
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=2G
#$ -wd /data2/home/ameert/catalog/r/fits/
#$ -o /data2/home/ameert/regen_galfit/output/
#$ -e /data2/home/ameert/regen_galfit/output/
#$ -N mhres

/data2/home/ameert/regen_galfit/measure_corrected_psf.py ser full_dr7_r $SGE_TASK_ID
