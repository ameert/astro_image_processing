#!/bin/bash

band=$1;
model=$2;
count=$3;
folder=`printf "%04d\n" $count`;

mv /data2/home/ameert/catalog/${band}/fits/${model}_new_again/${folder}/*.in /data2/home/ameert/catalog/${band}/fits/${model}/${folder}/

mv /data2/home/ameert/catalog/${band}/fits/${model}_new_again/${folder}/*.out /data2/home/ameert/catalog/${band}/fits/${model}/${folder}/

mv /data2/home/ameert/catalog/${band}/fits/${model}_new_again/${folder}/*.con /data2/home/ameert/catalog/${band}/fits/${model}/${folder}/

mv /data2/home/ameert/catalog/${band}/fits/${model}_new_again/${folder}/sex*.txt /data2/home/ameert/catalog/${band}/fits/${model}/${folder}/

rm -rf /data2/home/ameert/catalog/${band}/fits/${model}_new_again/${folder}

rm /data2/home/ameert/catalog/${band}/fits/${model}/${folder}/sdss_r_out.cat
rm /data2/home/ameert/catalog/${band}/fits/${model}/${folder}/result*
rm /data2/home/ameert/catalog/${band}/fits/${model}/${folder}/*.log
rm /data2/home/ameert/catalog/${band}/fits/${model}/${folder}/sdss_sex.cat.Shallow
