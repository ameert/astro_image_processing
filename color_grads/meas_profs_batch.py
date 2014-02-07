#!/data2/home/ameert/python/bin/python2.5

import sys
import os
from mysql_class import *

#folder_num = int(sys.argv[1])
galtype = sys.argv[1]

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'

#cursor = mysql_connect(dba, usr, pwd, 'shredder')

#galcount, = cursor.get_data("""select galcount from CAST where galcount between %d and %d;""" %((folder_num-1)*250, folder_num*250))

#os.system('rm /data2/home/ameert/color_grads/data/%04d/*ser.out' %folder_num)
#os.system('rm /data2/home/ameert/color_grads/data/%04d/*ser.resid' %folder_num)
#os.system('rm /data2/home/ameert/color_grads/data/%04d/*ser_mag_colors.out' %folder_num)

#galcount = range((folder_num-1)*250+1,  folder_num*250+1)
#print galcount


galcount = np.loadtxt('grads_%s.txt' %galtype, usecols=[0], skiprows=1, unpack=True)

galcount = galcount.astype(int)


for count in galcount:
#range((folder_num-1)*250+1, folder_num*250+1):
    os.system('python /home/ameert/git_projects/alans-image-processing-pipeline/color_grads/measure_profs_data.py %d' %count)


