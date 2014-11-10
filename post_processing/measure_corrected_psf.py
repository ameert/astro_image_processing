#!/data2/home/ameert/python/bin/python2.5

from regen_functions import *
import os
import sys
from mysql_class import *
import numpy as np

this_dir = os.getcwd()

model = sys.argv[1]
fit_type = sys.argv[2]
band = sys.argv[3]
folder_num = int(sys.argv[4])

#count_num = int(sys.argv[4])
#if count_num <= 10735:
#        band = 'r'
#elif count_num <= 2*10735:
#        band = 'g'
#	count_num -= 10735
#else:
#	count_num -= 2*10735
#        band = 'i'
#folder_num = count_num%2684
#model =models[count_num/2684]

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
cursor = mysql_connect(dba, usr, pwd, 'shredder')

tablename = '%s_%s_%s' %(fit_type,band,model)

#new_dir = '/scratch/%04d' %folder_num

new_dir = '/scratch/%s_%s_%04d' %(model, band,folder_num)
try:
  os.mkdir(new_dir)
except:
  print new_dir, ' creation failed!!!!'
  
os.chdir(new_dir)

#mask_path = '/data2/home/ameert/andre_bcg/%s/sims/fits/%s/%04d' %(band,'masks', folder_num)
#file_path = '/data2/home/ameert/andre_bcg/%s/sims/fits/%s/%04d' %(band,model, folder_num)


file_path = '/data2/scratch/ameert/CMASS/%s/fits/%s/%04d' %(band,model, folder_num)
mask_path = '/data2/scratch/ameert/CMASS/%s/fits/masks/%04d' %(band,folder_num)
#os.chdir(file_path)

#file_path = '/data2/home/ameert/final_sim/fits/mask%d/thresh%d/%s/%04d/' %(mask_num, thresh_num, model, folder_num)
#mask_path = '/data2/home/ameert/final_sim/fits/mask%d/thresh%d/%s/%04d/' %(mask_num, thresh_num, 'masks', folder_num)
#file_path = '/data2/home/ameert/catalog/short_sample/r/fits/%s/%04d' %(model, folder_num)
#file_path = '/data2/home/ameert/z_sims/%s/fits/%s/%04d' %(fit_type.split('_')[1],model, folder_num)
#mask_path = '/data2/home/ameert/z_sims/%s/fits/%s/%04d' %(fit_type.split('_')[1],'masks', folder_num)
#mask_path = file_path
#file_path = '/data2/home/ameert/catalog/short_sample/r/fits/%s/%04d' %(model, folder_num)
#mask_path = '/data2/home/ameert/catalog/short_sample/r/fits/%s/%04d' %('masks', folder_num)
#file_path = '/data2/home/ameert/andre_bcg/r/fits/%s/%04d' %(model, folder_num)
#mask_path = '/data2/home/ameert/andre_bcg/r/fits/%s/%04d/' %('masks',folder_num)
#file_path = '/data2/home/ameert/bcg/r/fits/%s/%04d' %(model, folder_num)
#mask_path = '/data2/home/ameert/bcg/r/fits/%s/%04d/' %('masks',folder_num)
#file_path = '/data2/home/ameert/fukugita/r/fits/%s/%04d' %(model, folder_num)
#mask_path = '/data2/home/ameert/fukugita/r/fits/%s/%04d/' %('masks',folder_num)

#cmd = 'select galcount, re_pix, eb, n, rd_pix, ed from %s where galcount between %d and %d;' %(tablename, 250*(folder_num-1), 250*folder_num)
cmd = 'select galcount, re_pix, eb, n, rd_pix, ed from %s where galcount >%d order by galcount limit 1000;' %(tablename, np.max(np.array([0,500*(folder_num-2)]))) #  and hrad_pix_corr < 0 and re_pix<9999
print cmd

galcount, re_pix, eb, nser, rd_pix, ed = cursor.get_data(cmd)

galcount = np.array(galcount, dtype = int)
re_pix = np.array(re_pix, dtype = float)
eb = np.array(eb, dtype = float)
nser = np.array(nser, dtype = float)
rd_pix = np.array(rd_pix, dtype = float)
ed = np.array(ed, dtype = float)

print galcount

re_pix = -1*np.ones_like(re_pix)# *np.sqrt(eb)
rd_pix = -1*np.ones_like(rd_pix)# *np.sqrt(ed)
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
  if cur_gal not in galcount:
	  continue
    
  new_mask = "%s/M_%s.fits" %(mask_path,stem)
  print new_mask
  if not os.path.exists(new_mask):
        new_mask = new_mask.replace('/%s/' %model, '/masks/')
        print new_mask
        if not os.path.exists(new_mask):
            print 'new_mask not found!!!'
            continue

  new_O_file =  './O_r_%08d_r_stamp_no_psf.fits' %(cur_gal)
  new_constraints = '%s/%s.con' %(file_path, stem)

  rad = -1#np.extract(cur_gal == galcount, re_pix)[0]
  rad_disk = -1#np.extract(cur_gal == galcount, rd_pix)[0]
  print rad, rad_disk

  remake_G_file(infile, outfile, "NO_CHANGE", new_O_file,#"NO_CHANGE",#
                "NO_CHANGE", 'NONE', new_mask,
                new_constraints, fix_constraints = True, cir_ser = rad,
                cir_disk = rad_disk)


  os.system('%s %s' %(galfit, outfile))



os.system('/data2/home/ameert/regen_galfit/measure_hlight.py %s corr' %(tablename))


#for fstring in ['galfit.*','fit.log','file.list', 'G_tmp.in']:
#    os.system('rm %s' %fstring)
#'*.fits',

os.chdir(this_dir)
os.system('rm -rf %s' %new_dir)



