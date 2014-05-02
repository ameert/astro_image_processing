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

cmd = """select d.galcount, c.flag, d.Prob_pS,  d.Prob_n4, z.n_bulge from catalog.Flags_optimize as c, catalog.r_simard_fit as d, catalog.r_simard_ser as z where c.galcount = d.galcount and c.galcount = z.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by d.galcount;""".format(model = model, band = 'r')

data = cursor.get_data(cmd)

data = np.array([np.array(d) for d in data]).T

meert_flag = data[:,1].astype(int)
pS= data[:,2]
pn4= data[:,3]
sim_ser= data[:,4]

names=[ 'bulge', 'disk', '2com'] 
name_flags = [1, 2,32]
group_labels = names
fits_labels = names


meert_class = meert_flag_to_class(meert_flag)
simard_class = sim_prob_to_class(pS, pn4, sim_ser)
cov_mat =  cov(meert_class, simard_class, name_flags, name_flags)

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
pl.xlabel('S11')
pl.ylabel('This work')
pl.savefig('./%s_type_simard_mcc.eps' %(model))
