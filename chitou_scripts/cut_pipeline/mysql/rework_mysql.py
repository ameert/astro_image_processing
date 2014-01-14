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
sdss_filename = 'sdss_list_out_ex_ameert.csv'
data_dir = '/home/ameert/cut_pipe/'
pix_sz = 0.396

# End of settings

cursor = connect_to_mysql(dba,usr,pwd)

table_name = table_stem + 'full'

#make_big_table(table_name, filter, cursor)

#gal = {}
#gal.update(read_list(data_dir + sdss_filename, 'I,X,X,X,X,X,X,X,X,X,F,F,F,X,X,X,X,F,F,X,X,X,X,X,X,X,X,X,X,F,F,F,F,F,F,F,F,F,F,X,X', delimiter = ','))


#gal['filter'] = filter

#combine_small_tables(table_number, filter, cursor, fit_types)
#load_table_main_data(table_name, cursor, fit_types, filter)

####calc_dist_stuff(table_name, cursor) #THIS IS NOW DONE IN THE BIG TABLE SDSS_MAIN###


update_main_table(table_name, cursor, fit_types, pix_sz,filter)
