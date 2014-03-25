import os
from mysql_class import *
import numpy as np
import sys
import sys
from plotting_funcs import magsum
import pylab as pl
import matplotlib.cm as cm
import pickle

fitmodel = 'ser'

all_tables={}
all_tables['data']= {'ser':'catalog.full_dr7_r_ser', 
                     'devexp':'catalog.full_dr7_r_devexp', 
                     'serexp':'catalog.full_dr7_r_serexp'}

all_tables['sims']= {'fit':{'ser':'chip20_ser', 'devexp':'chip20_devexp',
                               'serexp':'chip20_serexp'}, 
                     'input':'sim_input'}

def get_data(cursor, xtab):
    cmd = "select a.re_kpc-15.0, a.n-2.5, a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-f.extinction_r-d.kcorr_r + 24, m.ProbaEll-.5, m.ProbaS0-.5, m.ProbaSab-.5, m.ProbaScd-.5 from %s as a,catalog.CAST as f , catalog.DERT as d, catalog.M2010 as m where f.galcount = a.galcount and f.galcount = d.galcount and f.galcount = m.galcount and a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-f.extinction_r < 17.77-38.2605 and a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r < 17.77 and f.z < 0.1 ;" %(xtab)
    
    data_vals = cursor.get_data(cmd) 

    names = ['re_kpc', 'n', 'Ie', 'Pell','PS0','PSab','PScd']
    data = {}

    for d, n in zip(data_vals,names):    
        data[n] = np.array(d, dtype = float)
    
    return data

def cov(data, mask):
    cov_mat = np.zeros((len(data), len(data)))
    for c1, d1 in enumerate(zip(data, mask)):
        for c2, d2 in enumerate(zip(data, mask)):
            cov_mat[c1,c2] = np.sum(d1[0]*d2[0]*d1[1]*d2[1])/(np.sum(d1[1]*d2[1])-1.0)
    return cov_mat

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

data = get_data(cursor, all_tables['data']['ser'])

arr_to_b = []
mask_to_b = []

names = ['re_kpc', 'n', 'Ie', 'Pell','PS0','PSab','PScd']
group_labels = ['r$_{hl}$','n$_{sersic}$','M$_{tot,\ abs}$','P$_{Ell}$',
                'P$_{S0}$','P$_{Sab}$','P$_{Scd}$']
#fits_labels = ['total mag','halflight rad arcsec','sersic index',
#               'sky counts', 
#               'bulge mag','r bulge arcsec', 'b vs a bulge', 
#               'pos ang bulge']

for name in names:
    hold = data[name]
    arr_to_b.append(hold)
    mask_to_b.append(np.where(np.abs(hold) > 100, 0, 1))
 
cov_mat =  cov(arr_to_b, mask_to_b)

np.set_printoptions(precision=3, suppress = True, linewidth = 150)
print cov_mat

correlation_mat = cov_mat.copy()
disp_mat = np.zeros_like(cov_mat)

for a in range(len(names)):
    for b in range(len(names)):
        correlation_mat[a,b] = cov_mat[a,b]/np.sqrt(cov_mat[a,a]*cov_mat[b,b])
        if b > a:
            disp_mat[a,b] = np.nan
        else:
            disp_mat[a,b] =  correlation_mat[a,b]
print correlation_mat

fig = pl.figure(figsize =(7,7))
ax = fig.add_subplot(111)
fig.subplots_adjust(left = 0.12, right = 0.97, bottom = 0.08, top = 0.87, 
                    wspace = 0.48, hspace = 0.48)  

pl.imshow(disp_mat, interpolation = 'nearest', vmin = -1, vmax = 1, cmap = cm.jet)
pl.colorbar()
for a in range(len(names)):
    for b in range(len(names)):
        if b > a:
            pl.text(b,a, '% 03.2f' %disp_mat[b,a], horizontalalignment='center',
                    verticalalignment='center', fontsize = 8)

ax.xaxis.tick_top()
pl.xticks(np.arange(len(group_labels)), group_labels)
pl.yticks(np.arange(len(group_labels)), group_labels)

pl.xticks(rotation=45)
#pl.suptitle("Correllation of errors for %s model fit with %s" %(inmodel, fitmodel))
pl.savefig('./%s_prob_data_correlation.eps' %(fitmodel))

#outfile = open('./%s_%s_correlation.txt' %(inmodel, fitmodel), 'w')
#outfile.write(str(correlation_mat))
#outfile.close()

#outfile = open('./%s_%s_correlation.pickle' %(inmodel, fitmodel), 'w')
#pickle.dump([correlation_mat, names, fits_labels], outfile)
#outfile.close()
