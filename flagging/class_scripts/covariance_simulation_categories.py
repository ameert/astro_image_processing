import os
from mysql_class import *
import numpy as np
import sys
import pylab as pl
import matplotlib.cm as cm
from flag_defs import *

def get_score(true_val, test_val):
    TP = np.max([.0001,float(np.sum(test_val*true_val))])
    TN = np.max([.0001,float(np.sum(np.where(test_val==0, 1,0) * np.where(true_val==0, 1,0)))])
    FP = np.max([.0001,float(np.sum(test_val * np.where(true_val==0, 1,0)) )])
    FN = np.max([.0001,float(np.sum(np.where(test_val==0, 1,0) * true_val))])

    
    mcc = TP * TN - FP *FN
    mcc = mcc/np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    precision = (TP)/(FP+TP)
    recall = (TP)/(FN+TP)
    TNR = TN/(TN+FP)
    accuracy = (TP+TN)/(TP+TN+FP+FN)
    f1 = 2.0*precision*recall/(precision+recall)
    #mcc=f1
    print "tp: %d, tn: %d, fp: %d, fn:%d, mcc:%f" %(TP,TN,FP,FN, mcc)
    return mcc



model = 'serexp'
option = 1
endstem = 'band'

def cov(data, data2, mask):
    cov_mat = np.zeros((len(data), len(data)))
    for c1, d1 in enumerate(zip(data, mask)):
        for c2, d2 in enumerate(zip(data2, mask)):
            #if c1 in [5,13]:
            #    if c2 in [5,13]:
                    print c1, c2
                    cov_mat[c1,c2] = get_score(d1[0], d2[0])
            #np.sum(d1[0]*d2[0]*d1[1]*d2[1])/(np.sum(d1[1]*d2[1])-1.0)
    return cov_mat

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

cmd = """select d.galcount,c.flag, d.flag from catalog.Flags_optimize as c, simulations.Flags_optimize as d, simulations.CAST as x where x.galcount = d.galcount and x.true_galcount = c.galcount and x.galcount >20000 and c.band='{band}' and c.model = '{model}' and c.ftype = 'u' and d.band='{band}' and d.model = '{model}' and d.ftype = 'u' order by d.galcount;""".format(model = model, band = 'r')

data = cursor.get_data(cmd)

data = np.array([np.array(d) for d in data]).T

flag = data[:,-2].astype(int)
flag2 = data[:,-1].astype(int)

names=[ a[0].replace('\t','') for a in category_flag ] 
group_labels = names
fits_labels = names

arr_to_b = []
arr_to_b2 = []
mask_to_b = []

for flagval in [ 2**a[1] for a in category_flag]:
    print flagval
    hold =  np.where((flag & flagval)>0, 1,0)#*np.where(flag & (2**6)>0, 0,1)
    arr_to_b.append(hold)
    hold2 =  np.where((flag2 & flagval)>0, 1,0)#*np.where(flag & (2**6)>0, 0,1)
    arr_to_b2.append(hold2)
    print hold, hold2
    #mask_to_b.append(np.where(np.abs(hold) > 100, 0, 1)) 
    mask_to_b.append(np.ones_like(hold))


for temp in zip(arr_to_b,arr_to_b2):
    print temp


cov_mat =  cov(arr_to_b, arr_to_b2, mask_to_b)

np.set_printoptions(precision=3, suppress = True, linewidth = 150)
#print cov_mat

correlation_mat = cov_mat.copy()
disp_mat = np.zeros_like(cov_mat)

for a in range(len(names)):
    for b in range(len(names)):
        correlation_mat[a,b] = cov_mat[a,b]#/np.sqrt(cov_mat[a,a]*cov_mat[b,b])
        if 0:#b > a:
            disp_mat[a,b] = np.nan
        else:
            disp_mat[a,b] =  correlation_mat[a,b]
#print correlation_mat

fig = pl.figure(figsize =(14,14))
ax = fig.add_subplot(111)
fig.subplots_adjust(left = 0.22, right = 0.97, bottom = 0.08, top = 0.8, 
                    wspace = 0.48, hspace = 0.48)  

if option ==1:
    pl.imshow(disp_mat, interpolation = 'nearest', vmin = -1, vmax = 1, cmap = cm.jet)
    pl.colorbar()
    for a in range(len(names)):
        for b in range(len(names)):
            if b > -10:#a:
                #pl.text(b,a, '% 03.2f' %disp_mat[b,a], horizontalalignment='center',
                pl.text(b,a, '% 03.2f' %disp_mat[a,b], horizontalalignment='center',
                        verticalalignment='center', fontsize = 8)

    ax.xaxis.tick_top()
    pl.xticks(np.arange(len(group_labels)), group_labels, fontsize = 8)
    pl.yticks(np.arange(len(group_labels)), group_labels, fontsize = 8)

elif option == 2:
    pass

pl.xticks(rotation=90)
#pl.suptitle("Correllation of errors for %s model fit with %s" %(inmodel, fitmodel))
#pl.savefig('./%s_correlation_%s_final.eps' %(model, endstem))
pl.savefig('./%s_uflag_simulation.eps' %(model))

#outfile = open('./%s_correlation_%s_final.txt' %(model, endstem), 'w')
#outfile.write(str(correlation_mat))
#outfile.close()

#outfile = open('./%s_correlation_final.pickle' %model, 'w')
#pickle.dump([correlation_mat, names, fits_labels], outfile)
#outfile.close()
