import os

for count in range(1,63):
  for band in 'gr':
    os.system('python make_chip_ICL.py %d %s' %(count, band))
    os.system('python make_chip_ICL.py %d %s icl' %(count, band))

