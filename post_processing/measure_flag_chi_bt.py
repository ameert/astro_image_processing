#!/data2/home/ameert/python/bin/python2.5

from regen_functions import *
import os
import sys
from mysql_class import *
import pickle
from flag_funcs import *
import pickle

this_dir = os.getcwd()

band = sys.argv[3]
model = sys.argv[2]
folder_num = int(sys.argv[1])


if model=='serexp' and band=='i':
  if folder_num in [2498, 2508, 2513, 2516, 2520, 2523, 2524, 2525, 2526, 2527, 2530, 2531, 2533, 2534, 2535, 2536, 2537, 2538, 2539, 2540, 2541, 2542, 2543, 2544, 2545, 2546, 2547, 2548, 2549, 2550, 2551, 2552, 2553, 2554, 2555, 2556, 2557, 2558, 2559, 2560, 2561, 2562, 2563, 2564, 2565, 2566, 2567, 2569, 2571, 2572, 2574, 2575, 2576, 2579, 2583, 2585, 2586, 2587, 2588, 2589, 2592, 2596, 2597, 2601, 2604, 2607, 2608, 2613, 2615, 2616, 2622, 2626, 2629]:
    pass
  else:    
    sys.exit()


new_dir = '/scratch/%04d_%s_%s' %(folder_num, band, model)
try:
    os.mkdir(new_dir)
except:
    pass

os.chdir(new_dir)

file_path = '/data2/home/ameert/catalog/%s/fits/%s/%04d' %(band,model, folder_num)
mask_path = '/data2/home/ameert/catalog/%s/fits/%s/%04d' %(band,'masks', folder_num)
data_path = '/data2/home/ameert/catalog/%s/data/%04d' %(band,folder_num)

infile = open('/data2/home/ameert/flagging/%s/full_catalog_info_%s_%s.pickle' %(band,band,model))
indata = pickle.load(infile)
infile.close()

indata['galcount'] = np.array(indata['galcount'], dtype=int)
selected_gals = np.where(indata['galcount']<=folder_num*250, 1, 0)*np.where(indata['galcount']>(folder_num-1)*250, 1, 0)

data = {'galcount': np.extract(selected_gals==1, indata['galcount']),
        'r_tot': np.extract(selected_gals==1, indata['r_tot']),
        'tot_counts': np.extract(selected_gals==1, indata['tot_counts']),
        'r_sex': np.extract(selected_gals==1, indata['r_sex']),
        'BT': np.extract(selected_gals==1, indata['BT'])
        }


data['ofile']=['O_%s_%08d_%s_stamp.fits' %(band, gc,band) for gc in data['galcount']]
data['mfile']=['%s/EM_%s_%08d_%s_stamp.fits' %(mask_path,band, gc,band) for gc in data['galcount']]
data['wfile']=['%s/%08d_%s_stamp_W.fits' %(data_path, gc,band) for gc in data['galcount']]
data['dfile']=['%s/%08d_%s_stamp.fits' %(data_path, gc,band) for gc in data['galcount']]
data['outfile']='/data2/home/ameert/flagging/%s/%s/total_profile_%d.pickle' %(band, model,folder_num)
galfit = '/data2/home/ameert/galfit/galfit'


for gc, rt, tc, rs, bt_s in zip(data['galcount'], data['r_tot'], data['tot_counts'], data['r_sex'], data['BT']):
    #if gc != 88623:
    #    continue
    infile = '%s/G_%s_%08d_%s_stamp.out' %(file_path,band, gc,band)
    outfile = "G_tmp.in"
    stem = infile.split('G_')[1]
    stem = stem.split('.out')[0]
    print infile
    if not os.path.exists(infile):
        continue
    new_mask = "%s/M_%s.fits" %(mask_path,stem)
    if not os.path.exists(new_mask):
        new_mask = new_mask.replace('/%s/' %model, '/masks/')
        print new_mask
        if not os.path.exists(new_mask):
            print 'new_mask not found!!!'
            continue
        
    new_constraints = '%s/%s.con' %(file_path, stem)
    
    remake_G_file(infile, outfile, "NO_CHANGE", "NO_CHANGE",
                  "NO_CHANGE", 'NO_CHANGE', new_mask,
                  new_constraints, fix_constraints = True, cir_ser = -1,
                  cir_disk = -1)

    os.system('%s %s' %(galfit, outfile))

flag_profs(folder_num, data, model)

#for fstring in ['galfit.*','fit.log','*.fits','file.list', 'G_tmp.in']:
#    os.system('rm ./%s' %fstring)

os.chdir(this_dir)
os.system('rm -rf %s' %new_dir)
