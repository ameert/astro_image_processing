from modify_data import *
from read_list import *

# These are things I set
dba = 'pymorph_data'
usr = 'pymorph'
pwd = 'pymorph'

table_number = 6
filter = 'r'
table_stem = filter + '_'
fit_types = ['Dev','DevExp','Ser', 'SerExp']
sdss_filename = 'matched_samples.txt'
data_dir = '/home/ameert/sdss_sample/'
pix_sz = 0.396

# End of settings

cursor = connect_to_mysql(dba,usr,pwd)

table_name = 'sdss_sample' #table_stem + 'full'

gal = {}
#gal.update(read_list(data_dir + sdss_filename, 'I,X,X,X,X,X,X,X,X,X,F,F,F,A,X,X,X,F,F,X,X,X,F,F,F,F,F,X,X,X,X,X,X,F,F,F,F,F,X,X,X,X,X,X,X,X,X,X', delimiter = ','))
gal.update(read_list(data_dir + sdss_filename, 'I,I', column_names = ['gal_count', 'sdss_count']))

gal['filter'] = filter
print gal.keys()

for count,dr4_count in zip(gal['gal_count'], gal['sdss_count']):
    cmd = 'update '+ table_name+ ' SET dr4_index = ' +str(dr4_count) + " where gal_count =" +str(count)  +";"
    if count == 1:
        print cmd
    #cursor.execute(cmd)
cursor.close()
