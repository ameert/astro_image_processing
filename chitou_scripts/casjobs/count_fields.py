from mysql_class import *
import numpy as np

out_table = 'CAST'

cursor = mysql_connect('catalog', 'pymorph', 'pymorph')

run, rerun, field, camcol= cursor.get_data("select run, rerun, field, camcol from CAST;")

run = np.array(run)
rerun = np.array(rerun)
field = np.array(field)
camcol = np.array(camcol)

gal_list = run* 10**7 + rerun*10**4 + field*10 + camcol

real_list = np.unique(gal_list)

print len(gal_list)
print len(real_list)
