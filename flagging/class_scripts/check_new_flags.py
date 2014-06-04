import os
from mysql.mysql_class import *
import numpy as np
import sys
import pylab as pl
import matplotlib.cm as cm
from covariance_functions import *
from flag_configuration_old import uflag_vals as old_uflag_dict
from flag_configuration import uflag_vals as uflag_dict

model = 'ser'
option = 1
endstem = 'band'

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

cmd = """select d.galcount,c.flag, d.flag from catalog.Flags_optimize as c,
catalog.Flags_catalog as d where d.galcount = c.galcount and 
c.band='{band}' and c.model = '{model}' and c.ftype = 'r' and
d.band='{band}' and d.model = '{model}' and d.ftype = 'r'
and d.galcount < 50*250 
order by d.galcount;""".format(model = model, band = 'r')

data = cursor.get_data(cmd)

data = np.array([np.array(d) for d in data]).T


galcount = data[:,0].astype(int)
old_flag = data[:,1].astype(int)
new_flag= data[:,2]

old_flagval = np.array([ 2**a[1] for a in old_uflag_dict], dtype=int)
new_flagval = np.array([ 2**a[1] for a in uflag_dict], dtype=int)

print old_flagval
print new_flagval

cov_mat =  cov(old_flag, new_flag, old_flagval, new_flagval)

np.set_printoptions(precision=3, suppress = True, linewidth = 150)
#print cov_mat

fig = pl.figure(figsize =(15,15))
ax = fig.add_subplot(111)
fig.subplots_adjust(left = 0.22, right = 0.97, bottom = 0.08, top = 0.8, 
                    wspace = 0.48, hspace = 0.48)  

disp_mat = make_disp_matrix(cov_mat, whitesec=None)
pl.imshow(disp_mat, interpolation = 'nearest', vmin = -1, vmax = 1, cmap = cm.jet)
print_nums(disp_mat, printsec=None)

#ax.xaxis.tick_top()
#ax.xaxis.set_label_position('top') 
#pl.xticks(np.arange(len(group_labels)), group_labels, fontsize = 8)
#pl.yticks(np.arange(len(group_labels)), group_labels, fontsize = 8)

pl.xticks(rotation=90)
pl.xlabel('old flags')
pl.ylabel('new flags')

pl.xticks(rotation=90)
pl.savefig('./%s_old_new.eps' %(model))

