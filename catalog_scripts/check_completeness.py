import os
import numpy as np

filters = 'gri'
main_path ='/data2/home/ameert/catalog/'
dirs = range(100,241)

bad_files = open('missing_files.txt', 'w')

for cur_fil in filters:
    for cur_dir in dirs:
        dir_fp = '%s%s/data/%04d/' %(main_path, cur_fil, cur_dir)
        
        if not os.path.isfile('%ssdss_%s_%04d.cat' %(dir_fp,cur_fil, cur_dir)):
            bad_files.write('%ssdss_%s_%04d.cat\n' %(dir_fp,cur_fil, cur_dir))
        
        file_num = np.arange((cur_dir-1)*250 +1, cur_dir*250+1)
        for cf in file_num:
            if not os.path.isfile('%s%08d_%s_psf.fits' %(dir_fp, cf, cur_fil)):
                bad_files.write('%s%08d_%s_psf.fits\n' %(dir_fp, cf, cur_fil))
            if not os.path.isfile('%s%08d_%s_stamp.fits' %(dir_fp, cf, cur_fil)):
                bad_files.write('%s%08d_%s_stamp.fits\n' %(dir_fp, cf, cur_fil))
            if not os.path.isfile('%s%08d_%s_stamp_W.fits' %(dir_fp, cf, cur_fil)):
                bad_files.write('%s%08d_%s_stamp_W.fits\n' %(dir_fp, cf, cur_fil))

        
bad_files.close()

