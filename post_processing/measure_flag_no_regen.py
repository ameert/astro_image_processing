#!/data2/home/ameert/python/bin/python2.5

import os
import sys
import pickle

from astro_image_processing.mysql.mysql_class import *
from flag_funcs import *

this_dir = os.getcwd()

folder_num = int(sys.argv[1])
model = sys.argv[2]
band = 'i'

file_path = '/data2/scratch/ameert/CMASS/i/fits/%s/%04d' %(model, folder_num)
mask_path = '/data2/scratch/ameert/CMASS/i/fits/%s/%04d' %('masks', folder_num)
data_path = '/data2/scratch/ameert/CMASS/i/data/%04d' %(folder_num)

#mask_path = '/data2/home/ameert/final_sim/fits/psf/masks/%04d' %(folder_num)
#data_path = '/data2/home/ameert/final_sim/data/20/' 
#fit_path = '/data2/home/ameert/final_sim/fits/psf/%s/%04d' %(model,folder_num)

#infile = open('/data2/home/ameert/regen_galfit/simulation_catalog_info_%s.pickle' %model)
infile = open('/data2/scratch/ameert/CMASS/CMASS_info_%s_%s.pickle' %(band,model))
indata = pickle.load(infile)
infile.close()

indata['galcount'] = np.array(indata['galcount'], dtype=int)
selected_gals = np.where(indata['galcount']<=folder_num*500, 1, 0)*np.where(indata['galcount']>(folder_num-1)*500, 1, 0)

print indata['galcount']

data = {'galcount': np.extract(selected_gals==1, indata['galcount']),
        'r_tot': np.extract(selected_gals==1, indata['r_tot']),
        'tot_counts': np.extract(selected_gals==1, indata['tot_counts']),
        'r_sex': np.extract(selected_gals==1, indata['r_sex']),
        'BT': np.extract(selected_gals==1, indata['BT'])
        }

data['ofile']=['%s/O_i_%08d_i_stamp.fits' %(file_path, gc) for gc in data['galcount']]
data['mfile']=['%s/EM_i_%08d_i_stamp.fits' %(mask_path, gc) for gc in data['galcount']]
data['wfile']=['%s/%08d_i_stamp_W.fits' %(data_path, gc) for gc in data['galcount']]
data['dfile']=['%s/%08d_i_stamp.fits' %(data_path, gc) for gc in data['galcount']]
data['outfile']='/data2/scratch/ameert/CMASS/%s/prof/%s/total_profile_%d.pickle' %(band, model,folder_num)

galfit = '/data2/home/ameert/galfit/galfit'

for a in data.keys():
    print a, data[a]


flag_profs(folder_num, data, model)

