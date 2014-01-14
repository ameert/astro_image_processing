from modify_data import *
from read_list import *

# These are things I set
dba = 'sdss_sample'
usr = 'pymorph'
pwd = 'pymorph'

table_number = 6
filter = 'r'
table_stem = filter + '_'
fit_types = ['Dev','DevExp','Ser', 'SerExp']
sdss_filename = 'sdss_list_out_large_ameert.csv'#'sdss_list_out_zp_ameert.csv'
data_dir = '/home/ameert/cut_pipe/'
pix_sz = 0.396

# End of settings

cursor = connect_to_mysql(dba,usr,pwd)

table_name = 'sdss_main' #table_stem + 'full'

gal = {}
gal.update(read_list(data_dir + sdss_filename, 'I,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X', delimiter = ','))
#gal.update(read_list(data_dir + sdss_filename, 'I,X,X,X,X,X,X,X,F,F,F,X,X,F,F,F,X', delimiter = ','))

gal['filter'] = filter
print gal.keys()

for count in range(len(gal['galcount'])):
    name = '%06d_%s_stamp' %(gal['galcount'][count], filter)

    #cmd = 'update '+ table_name+ ' SET fracdev_g = ' +str(gal['fracdev_g'][count]) +' ,fracdev_r = ' +str(gal['fracdev_r'][count]) + ' ,fracdev_i = ' +str(gal['fracdev_i'][count]) + ',extinction_g = ' +str(gal['extinction_g'][count]) + ',extinction_r = ' +str(gal['extinction_r'][count]) + ',extinction_i = ' +str(gal['extinction_i'][count]) +" where galcount =" +str(gal['galcount'][count])  +";"
    #cmd = 'update '+ table_name+ ' SET petroMag_r = ' +str(gal['petroMag_r'][count]) +' ,devmag_r = ' +str(gal['devmag_r'][count]) + ' ,devrad_r = ' +str(gal['devrad_r'][count]) + ',devab_r = ' +str(gal['devab_r'][count]) + " where galcount =" +str(gal['galcount'][count])  +";"
    #cmd = 'update '+ table_name+ ' SET kk_i = ' +str(gal['kk_i'][count]) +' ,airmass_i = ' +str(gal['airmass_i'][count])  + " where galcount =" +str(gal['galcount'][count])  +";"
    cmd = 'update '+ table_name+ ' SET petroR50_r = ' +str(gal['petroR50_r'][count]) + " where galcount =" +str(gal['galcount'][count])  +";"
    print cmd
    cursor.execute(cmd)
cursor.close()
