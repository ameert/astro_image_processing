#!/bin/bash
#$ -t 1-670000
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=2G
#$ -wd /data2/home/ameert/color_grads/scripts/
#$ -o /data2/home/ameert/color_grads/output/
#$ -e /data2/home/ameert/color_grads/output/
#$ -N mcg
#$ -l low

/data2/home/ameert/color_grads/scripts/meas_profs_new.py $SGE_TASK_ID

