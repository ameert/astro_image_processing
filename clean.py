#!/data2/home/ameert/python/bin/python2.5
#some junk
import os
import sys

table_name = sys.argv[1]
model = sys.argv[2]
job_num = int(sys.argv[3])

def move_masks(model):
    thisdir = os.getcwd()
    targetdir = thisdir.replace(model, 'masks')

    if not os.path.isdir(targetdir):
        os.system('mkdir '+targetdir)

    os.system('mv %s/*.fits %s/' %(thisdir, targetdir))
    
    return


to_remove = ['OEM_*.fits', 'SO_*.fits', 'R_*.html', 'seg.fits', 'SegCat.cat',
             'index.html', 'restart.cat', 'P_*.png', 'pymorph.html',
             'E_*.txt', 'OE_*.txt', 'BackMask.fits','check.fits','config.pyc',
             'O_*.fits']
    
for del_file in to_remove:
    os.system('rm %s' %del_file)

# and move the masks
move_masks(model)

