#!/bin/bash
#$ -t 1-120
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=2G
#$ -wd /data2/home/ameert/final_sim/fits/sn4/ser/
#$ -o /data2/home/ameert/regen_galfit/output/
#$ -e /data2/home/ameert/regen_galfit/output/
#$ -N mhrese

/data2/home/ameert/catalog/scripts/measure_and_clean.py sn4_ser ser $SGE_TASK_ID

# 9-16
# 21-28
# 87-94
# 99

