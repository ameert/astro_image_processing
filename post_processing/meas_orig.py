#!/bin/bash
#$ -t 80-120
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=2G
#$ -wd /data2/home/ameert/
#$ -o /data2/home/ameert/regen_galfit/output/
#$ -e /data2/home/ameert/regen_galfit/output/
#$ -N mhrse
#$ -l low

/data2/home/ameert/regen_galfit/measure_hlight_highres.py serexp $SGE_TASK_ID


