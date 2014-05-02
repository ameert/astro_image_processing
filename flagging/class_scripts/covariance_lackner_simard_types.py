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

cmd = """select d.galcount, If(l12.model='dvc',1,0)+If(l12.model='exp',2,0)+If(l12.model='ser',3,0)+If(l12.model='nb1',4,0)+If(l12.model='nb4',5,0), f.n_bulge, d.Prob_pS,  d.Prob_n4, z.n_bulge from catalog.Flags_optimize as c, catalog.r_simard_fit as d, catalog.r_simard_ser as z, catalog.r_lackner_fit as l12, catalog.r_lackner_ser as f where d.galcount = f.galcount and l12.galcount = c.galcount and c.galcount = d.galcount and c.galcount = z.galcount and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' order by d.galcount;""".format(model = model, band = 'r')

data = cursor.get_data(cmd)

data = np.array([np.array(d) for d in data]).T

lmodel = data[:,1].astype(int)
lser = data[:,2]
pS= data[:,3]
pn4= data[:,4]
sim_ser= data[:,5]

names=[ 'bulge', 'disk', '2com'] 
name_flags = [1, 2, 32]
group_labels = names
fits_labels = names

lack_class = lg12_to_class(lmodel, lser)
simard_class = sim_prob_to_class(pS, pn4, sim_ser)
cov_mat =  cov(lack_class, simard_class, name_flags, name_flags)

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
pl.ylabel('LG12')
pl.savefig('./lackner_type_simard_mcc.eps')
