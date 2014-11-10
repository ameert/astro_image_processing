from astro_image_processing import user_settings as user_info
from astro_image_processing.regeneration.regen_functions import *
import os
import sys

this_dir = os.getcwd()

model = sys.argv[1]
galcount = int(sys.argv[2])
folder_num = (galcount-1)/250 + 1

band = 'r'#sys.argv[4]

file_path = '/data2/home/ameert/catalog/r/fits/%s/%04d/' %(model, folder_num)
mask_path = '/data2/home/ameert/catalog/r/fits/%s/%04d/' %('masks', folder_num)



infile = '%s/G_%s_%08d_%s_stamp.out' %(file_path, band, galcount, band)
print infile
if os.path.exists(infile):
    
    outfile = "G_%08d_%s_tmp.in" %(galcount, band)
    print outfile
    stem = infile.split('G_')[1]
    stem = stem.split('.out')[0]

    new_mask = "%s/M_%s.fits" %(mask_path,stem)
    print new_mask
    if not os.path.exists(new_mask):
        new_mask = new_mask.replace('/%s/' %model, '/masks/')
        print new_mask
        if not os.path.exists(new_mask):
            print 'new_mask not found!!!'
            #sys.exit()
            new_mask = 'none'
            
    new_constraints = '%s/%s.con' %(file_path, stem)

    remake_G_file(infile, outfile, "NO_CHANGE", "NO_CHANGE",
                  "NO_CHANGE", 'NO_CHANGE', new_mask,
                  new_constraints, fix_constraints = True,
                  cir_ser = -1, cir_disk = -1)

    os.system('%s %s' %(user_info.galfit_path, outfile))





