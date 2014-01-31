#!/data2/home/ameert/python/bin/python2.5

from regen_functions import *
import os
import sys

thisdir = os.getcwd()

galcount = int(sys.argv[1])
model = sys.argv[2]
folder_num = int(sys.argv[3])
band = sys.argv[4]
save_dir = sys.argv[5]

os.chdir(save_dir)

file_path = '/data2/home/ameert/catalog/%s/fits/%s/%04d' %(band, model, folder_num)
mask_path = '/data2/home/ameert/catalog/%s/fits/%s/%04d' %(band, 'masks', folder_num)

galfit = '/data2/home/ameert/galfit/galfit'

infile = '%s/G_%s_%08d_%s_stamp.out' %(file_path, band, galcount, band)
outfile = "G_%08d_%s_tmp.in" %(galcount, band)
stem = infile.split('G_')[1]
stem = stem.split('.out')[0]
    
new_mask = "%s/M_%s.fits" %(mask_path,stem)
print new_mask
if not os.path.exists(new_mask):
    new_mask = new_mask.replace('/%s/' %model, '/masks/')
    print new_mask
    if not os.path.exists(new_mask):
        print 'new_mask not found!!!'
        sys.exit()
        
new_constraints = '%s/%s.con' %(file_path, stem)

remake_G_file(infile, outfile, "NO_CHANGE", "NO_CHANGE",
              "NO_CHANGE", "NO_CHANGE", new_mask,
              new_constraints, fix_constraints = True,
              cir_ser = -1, cir_disk = -1)
                  
os.system('%s %s' %(galfit, outfile))

os.chdir(thisdir)





