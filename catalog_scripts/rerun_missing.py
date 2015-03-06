#!/data2/home/ameert/python/bin/python2.5

import os
import sys

model = 'serexp'

#count = int(sys.argv[1])
for count in range(1,2684):
    os.chdir('/data2/home/ameert/catalog/i/fits/%s/%04d' %(model,count))
    os.system('/data2/home/ameert/pymorph/pymorph/pymorph.py')
    os.system('/data2/home/ameert/catalog/scripts/measure_and_clean.py full_dr7_i_%s %s %d' %(model, model, count))

