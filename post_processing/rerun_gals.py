import os
from mysql_class import *
import numpy as np

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
cursor = mysql_connect(dba, usr, pwd, 'shredder')

for model in ['dev','ser','devexp','serexp']:
    galcount, = cursor.get_data('select galcount from full_dr7_r_%s where hrad_pix_corr < 0 and galcount < 412500 order by galcount;' %model)
    galbins = np.arange(0,250*1650 + 1, 250)
    gals = np.digitize(galcount, galbins)

    for count in range(50, 1651):
        print count
        print len(np.where(gals == count)[0])
        if len(np.where(gals == count)[0]) > 10:
            print '/data2/home/ameert/regen_galfit/measure_corrected_psf.py %s full_dr7_r %d' %(model, count)
            os.system('/data2/home/ameert/regen_galfit/measure_corrected_psf.py %s full_dr7_r %d' %(model, count))
            
