import os
from astro_image_processing.mysql import *
import numpy as np
import sys
import matplotlib.pyplot as plt 
import matplotlib.cm as cm
from sklearn.metrics import confusion_matrix
from covariance_functions import print_nums

model = 'serexp'
endstem = 'band'

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

for bands in [('g','r'), ('g','i'), ('r','i')]:
    cmd = """select f.galcount, 
IF(f.flag&pow(2,20), 4, IF(f.flag&POW(2,14),3, IF(f.flag&POW(2,1), 0, IF(f.flag&POW(2,4), 1, IF(f.flag&POW(2,10), IF(a.n_bulge>7.95, 5,2),-1))))), 
IF(g.flag&pow(2,20), 4, IF(g.flag&POW(2,14),3, IF(g.flag&POW(2,1), 0, IF(g.flag&POW(2,4), 1, IF(g.flag&POW(2,10), IF(b.n_bulge>7.95, 5,2),-1)))))
from catalog.Flags_catalog as f, catalog.Flags_catalog as g, 
{band1}_band_{model} as a, {band2}_band_{model} as b 
where 
a.galcount=b.galcount and a.galcount = f.galcount and 
f.galcount = g.galcount and  f.band='{band1}' and  g.band='{band2}'
 and f.model = '{model}' and f.ftype = 'u' and f.model=g.model 
and f.ftype = g.ftype order by g.galcount;""".format(model = model, band1 = bands[0], band2=bands[1])

    data = cursor.get_data(cmd)

    data = np.array([np.array(d) for d in data]).T

    flag1 = data[:,1].astype(int)
    flag2 = data[:,2].astype(int)

    names=[ 'bulges', 'disks',  '2com', 'bad 2com', 'bad', 'n8'] 
    name_flags = [0, 1, 2, 3, 4, 5]
    group_labels = names
    fits_labels = names

    con_mat =  confusion_matrix(flag1, flag2, name_flags).astype(float)/flag1.size

    print bands
    print con_mat
    print 'total ', np.sum(np.sum(con_mat))
    np.set_printoptions(precision=3, suppress = True, linewidth = 150)

    fig = plt.figure(figsize =(3,3))
    ax = fig.add_subplot(111)
    fig.subplots_adjust(left = 0.3, right = 0.97, bottom = 0.08, top = 0.7, 
                        wspace = 0.48, hspace = 0.48)  

    disp_mat = con_mat#make_disp_matrix(cov_mat, whitesec=None)
    plt.imshow(disp_mat, interpolation = 'nearest', cmap = cm.OrRd, 
              vmin=0.0)
    print_nums(disp_mat, printsec=None)

    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top') 
    plt.xticks(np.arange(len(group_labels)), group_labels, fontsize = 8)
    plt.yticks(np.arange(len(group_labels)), group_labels, fontsize = 8)

    plt.xticks(rotation=90)
    plt.ylabel('{band1}-band'.format(band1=bands[0], band2=bands[1]))
    plt.xlabel('{band2}-band'.format(band1=bands[0], band2=bands[1]))
    plt.tick_params( axis='x', which='both', bottom='off', top='off',   
    labeltop='on') 
    plt.tick_params( axis='y', which='both', right='off', left='off',   
    labelleft='on') 
    plt.savefig('./confusion_{band1}_{band2}.eps'.format(band1=bands[0],band2=bands[1]))
    
