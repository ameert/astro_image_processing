#!/data2/home/ameert/python/bin/python2.5

from regen_functions import *
import os
import sys
from mysql_class import *

this_dir = os.getcwd()

mod = sys.argv[1]
table_stem = sys.argv[2]
start =int(sys.argv[3])
end = int(sys.argv[4])

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
cursor = mysql_connect(dba, usr, pwd, 'shredder')
galfit = '/data2/home/ameert/galfit/galfit'

for model in [mod]:
    tablename = '%s_%s' %(table_stem, model)
    for folder_num in range(start,end):

        new_dir = '/var/tmp/%04d' %folder_num
        try:
            os.mkdir(new_dir)
        except:
            pass

        os.chdir(new_dir)

        cmd = 'select galcount, Name from %s where hrad_pix_corr < 0 and galcount >%d and galcount <= %d;' %(tablename, (folder_num - 1)*250, folder_num *250)

        galcounts, names = cursor.get_data(cmd)
        
        #file_path = '/data2/home/ameert/catalog/short_sample/r/fits/%s/%04d' %(model, folder_num)
        #mask_path = '/data2/home/ameert/catalog/short_sample/r/fits/%s/%04d' %('masks', folder_num)
#        file_path = '/data2/home/ameert/catalog/r/fits/%s/%04d' %(model, folder_num)
#        mask_path = '/data2/home/ameert/catalog/r/fits/%s/%04d' %('masks', folder_num)

        file_path = '/data2/home/ameert/fukugita/r/fits/%s/%04d' %(model, folder_num)
        mask_path = '/data2/home/ameert/fukugita/r/fits/%s/%04d' %('masks', folder_num)

#        os.system('ls %s/G_*.out > file.list' %file_path)
#        galcounts = []
#        names = []
#        infile = open('file.list')
#        for line in infile:
#            galcounts.append(int(line.split('_')[-3]))
#            names.append(line.split('G_')[1].split('.out')[0])


        #file_path = '/data2/home/ameert/catalog/r/fits/%s/%04d' %(model, folder_num)
        #mask_path = '/data2/home/ameert/catalog/r/fits/%s/%04d' %('masks', folder_num)
        
        for galcount, name in zip(galcounts, names):
            print "galcount ", galcount
            infile = '%s/G_%s.out' %(file_path, name)
            print infile
            outfile = "G_tmp.in"

            new_mask = "%s/M_%s.fits" %(mask_path,name)

            if not os.path.exists(infile):
                continue
            if not os.path.exists(new_mask):
                new_mask = new_mask.replace('/%s/' %model, '/masks/')
                print new_mask
                if not os.path.exists(new_mask):
                    print 'new_mask not found!!!'
                    continue

            new_constraints = '%s/%s.con' %(file_path, name)

            remake_G_file(infile, outfile, "NO_CHANGE", "NO_CHANGE",
                          "NO_CHANGE", "NONE", new_mask,
                          new_constraints, fix_constraints = True)

            os.system('%s %s' %(galfit, outfile))



        os.system('/data2/home/ameert/regen_galfit/measure_hlight.py %s corr' %(tablename))

        for fstring in ['galfit.*','fit.log','*.fits','file.list', 'G_tmp.in']:
            os.system('rm %s' %fstring)

        os.chdir(this_dir)
        os.system('rm -rf %s' %new_dir)



