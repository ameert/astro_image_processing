#!/data2/home/ameert/python/bin/python2.5

from regen_functions import *
import os
import sys
from mysql_class import *

this_dir = os.getcwd()

model = sys.argv[1]
fit_type = sys.argv[2]
folder_num = int(sys.argv[3])

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
cursor = mysql_connect(dba, usr, pwd, 'shredder')


tablename = 'i_%s_%s' %(fit_type,model)

new_dir = '/scratch/%04d_%s' %(folder_num,model)
try:
    os.mkdir(new_dir)
except:
    print new_dir, ' creation failed!!!!'

os.chdir(new_dir)

mask_path = '/data2/home/ameert/catalog/i/fits/%s/%04d' %('masks', folder_num)  
file_path = '/data2/home/ameert/catalog/i/fits/%s/%04d' %(model, folder_num)

galstart = np.max(np.array([0,250*(folder_num-2)]))
cmd = 'select galcount from %s where galcount between %d and %d order by galcount ;' %(tablename, galstart, galstart +2000)
print cmd

galcount,  = cursor.get_data(cmd)

galcount = np.array(galcount, dtype = int)

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
        
  new_constraints = '%s/%s.con' %(file_path, stem)

  rad = -1
  rad_disk = -1
  
  remake_G_file(infile, outfile, "NO_CHANGE", "NO_CHANGE",
                "NO_CHANGE", 'NONE', new_mask,
                new_constraints, fix_constraints = True, cir_ser = rad,
                cir_disk = rad_disk)
                  

  os.system('%s %s' %(galfit, outfile))



os.system('/data2/home/ameert/regen_galfit/measure_hlight.py %s corr' %(tablename))

for fstring in ['galfit.*','fit.log','*.fits','file.list', 'G_tmp.in']:
  os.system('rm %s' %fstring)

os.chdir(this_dir)
os.system('rm -rf %s' %new_dir)



