#!/data2/home/ameert/python/bin/python2.5

from regen_functions import *
import os
import sys
from mysql_class import *

this_dir = os.getcwd()

model = sys.argv[1]
table_stem = sys.argv[2]
tablename = '%s_%s' %(table_stem, model)

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
cursor = mysql_connect(dba, usr, pwd, 'shredder')

for folder_num in range(1,2):
    
    cmd = 'select galcount, Name from %s where hrad_pix_psf < 0 and galcount >%d and galcount <= %d;' %(tablename, (folder_num - 1)*250, folder_num *250)
    print cmd
    
    galcounts, names = cursor.get_data(cmd)
    
    new_dir = '/var/tmp/%04d' %folder_num
    try:
        os.mkdir(new_dir)
    except:
        print "failed to make dir %s" %new_dir


    os.chdir(new_dir)

#    file_path = '/data2/home/ameert/catalog/short_sample/r/fits/%s/%04d' %(model, folder_num)
#    mask_path = '/data2/home/ameert/catalog/short_sample/r/fits/%s/%04d' %('masks', folder_num)
#    file_path = '/data2/home/ameert/bcg/r/fits/%s/highN_%04d' %(model, folder_num)
#    mask_path = '/data2/home/ameert/bcg/r/fits/%s/highN_%04d' %('masks', folder_num)
    file_path = '/data2/home/ameert/final_sim/fits/flat/%s/%04d' %(model, folder_num)
    mask_path = '/data2/home/ameert/final_sim/fits/flat/%s/%04d' %('masks', folder_num)

    galfit = '/data2/home/ameert/galfit/galfit'

    for galcount, name in zip(galcounts, names):
        infile = '%s/G_%s.out' %(file_path, name)
        outfile = "G_tmp.in"
        
        new_mask = "%s/M_%s.fits" %(mask_path,name)

        if not os.path.exists(infile):
            print "infile %s not found!!!" %infile
            continue
        if not os.path.exists(new_mask):
            new_mask = new_mask.replace('/%s/' %model, '/masks/')
            print new_mask
            if not os.path.exists(new_mask):
                print 'new_mask not found!!!'
                continue

        new_constraints = '%s/%s.con' %(file_path, name)

        remake_G_file(infile, outfile, "NO_CHANGE", "NO_CHANGE",
                      "NO_CHANGE", "NO_CHANGE", new_mask,
                      new_constraints, fix_constraints = True)

        os.system('%s %s' %(galfit, outfile))



    os.system('/data2/home/ameert/regen_galfit/measure_hlight.py %s psf' %(tablename))

    for fstring in ['galfit.*','fit.log','*.fits','file.list', 'G_tmp.in']:
        os.system('rm %s' %fstring)

    os.chdir(this_dir)
    os.system('rm -rf %s' %new_dir)
    


