#!/bin/bash
#$ -t 1-120 
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=2G
#$ -l md3000=1
#$ -wd /data2/home/ameert/bcgfukugita/r/fits/
#$ -o /data2/home/ameert/regen_galfit/output/
#$ -e /data2/home/ameert/regen_galfit/output/
#$ -N mhbcgd

/data2/home/ameert/regen_galfit/measure_corrected_psf.py dev bcg_fukugita_r $SGE_TASK_ID
