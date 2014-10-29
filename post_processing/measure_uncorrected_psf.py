#!/data2/home/ameert/python/bin/python2.5

from regen_functions import *
import os
import sys

this_dir = os.getcwd()

model = sys.argv[1]
fit_type = sys.argv[2]
tablename = '%s_%s' %(fit_type,model)
folder_num = int(sys.argv[3])

new_dir = '/var/tmp/%04d' %folder_num
try:
    os.mkdir(new_dir)
except:
    pass

os.chdir(new_dir)

file_path = '/data2/home/ameert/final_sim/fits/flat/%s/%04d' %(model, folder_num)
mask_path = '/data2/home/ameert/final_sim/fits/flat/%s/%04d' %('masks', folder_num)

file_list = 'file.list'
galfit = '/data2/home/ameert/galfit/galfit'

os.system('ls %s/G_*.out > %s' %(file_path, file_list))
f_list = open(file_list)

for line in f_list.readlines():
    infile = line.strip()
    outfile = "G_tmp.in"
    stem = infile.split('G_')[1]
    stem = stem.split('.out')[0]

    new_mask = "%s/M_%s.fits" %(mask_path,stem)
    print new_mask
    if not os.path.exists(new_mask):
        new_mask = new_mask.replace('/%s/' %model, '/masks/')
        print new_mask
        if not os.path.exists(new_mask):
            print 'new_mask not found!!!'
            continue
        
    new_constraints = '%s/%s.con' %(file_path, stem)

    remake_G_file(infile, outfile, "NO_CHANGE", "NO_CHANGE",
                  "NO_CHANGE", "NO_CHANGE", new_mask,
                  new_constraints, fix_constraints = True)

    os.system('%s %s' %(galfit, outfile))



os.system('/data2/home/ameert/regen_galfit/measure_hlight.py %s psf' %(tablename))

for fstring in ['galfit.*','fit.log','*.fits','file.list', 'G_tmp.in']:
    os.system('rm %s' %fstring)

os.chdir(this_dir)
os.system('rm -rf %s' %new_dir)



