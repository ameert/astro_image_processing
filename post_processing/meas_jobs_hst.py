#!/bin/bash
#$ -t 10-1001
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=4G
#$ -wd /data2/home/ameert/regen_galfit/
#$ -o /data2/home/ameert/regen_galfit/output/
#$ -e /data2/home/ameert/regen_galfit/output/
#$ -N mhr10
#$  -l low

/data2/home/ameert/regen_galfit/measure_hlight_hst.py $SGE_TASK_ID


