import os
from mysql.mysql_class import *
import numpy as np
import sys
import pylab as pl
import matplotlib.cm as cm
from covariance_functions import *

model = 'serexp'
option = 1
endstem = 'band'

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

cmd = """select d.galcount,c.flag, IF(d.ProfType=1, 1,0)+IF(d.ProfType=2, 2,0)+IF(d.ProfType=4, 3,0)+IF(d.ProfType=3, 4,0) from catalog.Flags_catalog as c, catalog.r_simard_fit as d where c.galcount = d.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by d.galcount;""".format(model = model, band = 'r')

data = cursor.get_data(cmd)

data = np.array([np.array(d) for d in data]).T

meert_flag = data[:,1].astype(int)
mendel_flag  = data[:,2].astype(int)

names=[ 'bulge', 'disk', '2com'] 
name_flags = [1, 2, 32]
group_labels = names
fits_labels = names


meert_class = meert_flag_to_class(meert_flag)
mendel_class = Men14_to_class(mendel_flag)
cov_mat =  cov(meert_class, mendel_class, name_flags, name_flags)

np.set_printoptions(precision=3, suppress = True, linewidth = 150)

fig = pl.figure(figsize =(3,3))
ax = fig.add_subplot(111)
fig.subplots_adjust(left = 0.22, right = 0.97, bottom = 0.08, top = 0.8, 
                    wspace = 0.48, hspace = 0.48)  

disp_mat = make_disp_matrix(cov_mat, whitesec=None)
pl.imshow(disp_mat, interpolation = 'nearest', vmin = -1, vmax = 1, cmap = cm.jet)
print_nums(disp_mat, printsec=None)

ax.xaxis.tick_top()
ax.xaxis.set_label_position('top') 
pl.xticks(np.arange(len(group_labels)), group_labels, fontsize = 8)
pl.yticks(np.arange(len(group_labels)), group_labels, fontsize = 8)

pl.xticks(rotation=90)
pl.xlabel('Men14')
pl.ylabel('This work')
pl.savefig('./%s_type_mendel_mcc.eps' %(model))
