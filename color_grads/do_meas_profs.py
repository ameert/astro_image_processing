#!/bin/bash
#$ -t 1-2683
#$ -S /bin/bash
#$ -V
#$ -l h_vmem=2G
#$ -wd /data2/home/ameert/color_grads/scripts/
#$ -o /data2/home/ameert/color_grads/output/
#$ -e /data2/home/ameert/color_grads/output/
#$ -N mcg
#$ -l low
#$ -tc 100

/data2/home/ameert/color_grads/scripts/meas_profs_batch.py $SGE_TASK_ID

