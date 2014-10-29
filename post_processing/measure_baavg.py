#!/data2/home/ameert/python/bin/python2.5

from regen_functions import *
import os
import sys
from mysql_class import *

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

file_path = '/data2/home/ameert/catalog/r/fits/%s/%04d' %(model, folder_num)
#file_path = '/data2/home/ameert/z_sims/%s/fits/%s/%04d' %(fit_type.split('_')[1],model, folder_num)
#mask_path = '/data2/home/ameert/z_sims/%s/fits/%s/%04d' %(fit_type.split('_')[1],'masks', folder_num)
#mask_path = file_path
mask_path = '/data2/home/ameert/catalog/r/fits/%s/%04d' %('masks', folder_num)
#file_path = '/data2/home/ameert/catalog/short_sample/r/fits/%s/%04d' %(model, folder_num)
#mask_path = '/data2/home/ameert/catalog/short_sample/r/fits/%s/%04d' %('masks', folder_num)
#file_path = '/data2/home/ameert/final_sim/fits/%s/%s/%04d' %(fit_type,model, folder_num)
#mask_path = '/data2/home/ameert/final_sim/fits/%s/%s/%04d/' %(fit_type, 'masks',folder_num)
#file_path = '/data2/home/ameert/bcg/r/fits/%s/%04d' %(model, folder_num)
#mask_path = '/data2/home/ameert/bcg/r/fits/%s/%04d/' %('masks',folder_num)
#file_path = '/data2/home/ameert/fukugita/r/fits/%s/%04d' %(model, folder_num)
#mask_path = '/data2/home/ameert/fukugita/r/fits/%s/%04d/' %('masks',folder_num)

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
cursor = mysql_connect(dba, usr, pwd, 'shredder')
cmd = 'select galcount, re_pix, eb, n, rd_pix, ed from %s where galcount between %d and %d;' %(tablename, 250*(folder_num-1), 250*folder_num)

galcount, re_pix, eb, nser, rd_pix, ed = cursor.get_data(cmd)

galcount = np.array(galcount, dtype = int)
re_pix = np.array(re_pix, dtype = float)
eb = np.array(eb, dtype = float)
nser = np.array(nser, dtype = float)
rd_pix = np.array(rd_pix, dtype = float)
ed = np.array(ed, dtype = float)

re_pix = (re_pix +re_pix*eb)/2.0
rd_pix = (rd_pix +rd_pix*ed)/2.0
#re_pix = np.where(nser < 2.5, -1, re_pix)

file_list = 'file.list'
galfit = '/data2/home/ameert/galfit/galfit'

os.system('ls %s/G_*.out > %s' %(file_path, file_list))
f_list = open(file_list)

for line in f_list.readlines():
    infile = line.strip()
    outfile = "G_tmp.in"
    stem = infile.split('G_')[1]
    stem = stem.split('.out')[0]
    cur_gal = int(stem.split('_')[1])
    
    new_mask = "%s/M_%s.fits" %(mask_path,stem)
    print new_mask
    if not os.path.exists(new_mask):
        new_mask = new_mask.replace('/%s/' %model, '/masks/')
        print new_mask
        if not os.path.exists(new_mask):
            print 'new_mask not found!!!'
            continue
        
    new_constraints = '%s/%s.con' %(file_path, stem)

    rad = np.extract(cur_gal == galcount, re_pix)[0]
    rad_disk = np.extract(cur_gal == galcount, rd_pix)[0]
    print rad
    
    remake_G_file(infile, outfile, "NO_CHANGE", "NO_CHANGE",
                  "NO_CHANGE", 'NONE', new_mask,
                  new_constraints, fix_constraints = True, cir_ser = rad,
                  cir_disk = rad_disk)

    os.system('%s %s' %(galfit, outfile))



os.system('/data2/home/ameert/regen_galfit/measure_hlight.py %s baavg' %(tablename))

for fstring in ['galfit.*','fit.log','*.fits','file.list', 'G_tmp.in']:
    os.system('rm %s' %fstring)

os.chdir(this_dir)
os.system('rm -rf %s' %new_dir)



