#!/data2/home/ameert/python/bin/python2.5

from regen_functions import *
import os
import sys
from mysql_class import *
import numpy as np

this_dir = os.getcwd()

model = sys.argv[1]
folder_num = int(sys.argv[2])

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
cursor = mysql_connect(dba, usr, pwd, 'shredder')

tablename = 'r_lackner_%s' %(model)

new_dir = '/scratch/%04d' %folder_num
try:
  os.mkdir(new_dir)
except:
  print new_dir, ' creation failed!!!!'
os.chdir(new_dir)

file_path = '/data2/home/ameert/catalog/r/fits/lackner/%s/%04d' %(model, folder_num)

file_list = 'file.list'
galfit = '/data2/home/ameert/galfit/galfit'

os.system('ls %s/G_*.out > %s' %(file_path, file_list))
f_list = open(file_list)

for line in f_list.readlines():
  outfile = line.strip()
  
  os.system('%s %s' %(galfit, outfile))


os.system('/data2/home/ameert/regen_galfit/measure_hlight.py %s corr' %(tablename))


for fstring in ['galfit.*','fit.log','file.list', 'O_*.fits']:
    os.system('rm %s' %fstring)

os.chdir(this_dir)
os.system('rm -rf %s' %new_dir)



