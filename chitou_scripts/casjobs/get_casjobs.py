from casjobs_new_query import *
from clean_cat import *

data_dir = '/home/ameert/new_cut_pipe/'
gal_cat = {'filename':'spectro_sample_raw.cat'}
out_file = 'spectro_sample.cat'


username = 'upenn_pymorph'
wsid = '396840617'
password = 'pymorph_upenn'

casjobs(gal_cat, data_dir, username, wsid, password)

clean_cat(gal_cat['filename'] ,out_file)
