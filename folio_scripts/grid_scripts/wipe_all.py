#!/data2/home/ameert/python/bin/python2.5

import os
import sys

to_remove = ['OEM_*.fits', 'SO_*.fits', 'R_*.html', 'seg.fits', 'SegCat.cat',
             'index.html', 'restart.cat', 'P_*.png', 'pymorph.html',
             'E_*.txt', 'OE_*.txt', 'BackMask.fits','check.fits','config.pyc',
             'O_*.fits', 'agm_result_with_radius.csv', '*.sex', 'EM_*.fits',
             '*.log', 'G_*', 'M_*.fits', '*.con', 'result.csv', '*_out.cat',
             '*.cat.Shallow']

try:
    targetdir = sys.argv[1]
except:
    targetdir = './'
    
thisdir = os.getcwd()

os.chdir(targetdir)
for del_file in to_remove:
    os.system('rm %s' %del_file)

os.chdir(thisdir)

