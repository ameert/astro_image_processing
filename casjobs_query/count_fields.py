import numpy as np
import astro_image_processing.mysql as mysql
from astro_image_processing.user_settings import mysql_params

out_table = 'CAST'

cursor = mysql.mysql_connect(mysql_params['dba'],mysql_params['user'],
                       mysql_params['pwd'],mysql_params['host'])

run, rerun, field, camcol= cursor.get_data("select run, rerun, field, camcol from CAST;")

run = np.array(run)
rerun = np.array(rerun)
field = np.array(field)
camcol = np.array(camcol)

gal_list = run* 10**7 + rerun*10**4 + field*10 + camcol

real_list = np.unique(gal_list)

print len(gal_list)
print len(real_list)
