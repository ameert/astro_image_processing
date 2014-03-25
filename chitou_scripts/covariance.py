import os
from mysql_class import *
import numpy as np
import sys
import sys
from plotting_funcs import magsum
import pylab as pl
import matplotlib.cm as cm
import pickle

try:
    inmodel = sys.argv[1]
except:
    inmodel = 'ser'
try:
    fitmodel = sys.argv[2]
except:
    fitmodel = 'ser'
try:
    option =  int(sys.argv[3])
except:
    option = 1

all_tables={}
all_tables['data']= {'ser':'catalog.full_dr7_r_ser', 
                     'devexp':'catalog.full_dr7_r_devexp', 
                     'serexp':'catalog.full_dr7_r_serexp'}

all_tables['sims']= {'fit':{'ser':'chip20_ser', 'devexp':'chip20_devexp',
                               'serexp':'chip20_serexp'}, 
                     'input':'sim_input'}

def get_data(cursor, xtab, intab, model):
    cmd = "select a.n, b.n, a.BT, b.BT,  abs(a.Ie) -a.magzp +b.zeropoint_sdss_r, abs(b.Ie), abs(a.Id) -a.magzp +b.zeropoint_sdss_r, abs(b.Id), a.re_pix*0.396, b.re, a.rd_pix*0.396, b.rd, a.eb, b.eb, a.ed, b.ed, 90.0-a.bpa, b.bpa, 90.0-a.dpa, b.dpa, a.hrad_pix_corr*0.396, b.hrad_pix_corr*0.396, a.galsky, 130.0/53.904756 from %s as a, %s as b where a.galcount = b.simcount and b.model = '%s';" %(xtab, intab, model)
    
    data_vals = cursor.get_data(cmd) 

    names = ['n', 'n_in', 'BT', 'BT_in', 'Ie', 'Ie_in', 'Id', 'Id_in', 
             're', 're_in', 'rd', 'rd_in', 'eb', 'eb_in', 'ed', 'ed_in', 
             'bpa', 'bpa_in', 'dpa', 'dpa_in', 'rhl', 'rhl_in', 'sky','sky_in']
    data = {}

    for d, n in zip(data_vals,names):    
        data[n] = np.array(d, dtype = float)

    data['Itot'] = magsum(data['Ie'], data['Id'])[0]
    data['Itot_in'] = magsum(data['Ie_in'], data['Id_in'])[0]
    
    return data

def cov(data, mask):
    cov_mat = np.zeros((len(data), len(data)))
    for c1, d1 in enumerate(zip(data, mask)):
        for c2, d2 in enumerate(zip(data, mask)):
            cov_mat[c1,c2] = np.sum(d1[0]*d2[0]*d1[1]*d2[1])/(np.sum(d1[1]*d2[1])-1.0)
    return cov_mat

dba = 'simulations'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

data = get_data(cursor, all_tables['sims']['fit'][fitmodel], 
                all_tables['sims']['input'], inmodel)

arr_to_b = []
mask_to_b = []
if (inmodel == 'ser') or (fitmodel == 'ser'):
    if fitmodel == inmodel:
        names=['Itot', 'rhl','n', 'sky', 'Ie', 're', 'eb', 'bpa']
        group_labels = ['m$_{tot}$','r$_{hl}$','n$_{sersic}$','sky$_{counts}$', 
                        'm$_{bulge}$','r$_{bulge}$', '(b/a)$_{bulge}$', 
                        '$\\phi_{bulge}$']
        fits_labels = ['total mag','halflight rad arcsec','sersic index',
                       'sky counts', 
                       'bulge mag','r bulge arcsec', 'b vs a bulge', 
                        'pos ang bulge']
    else:
        names=['Itot', 'rhl','sky']
        group_labels = ['m$_{tot}$', 'r$_{hl}$','sky']
        fits_labels = ['total mag','halflight rad arcsec','sky counts'] 
        
else:
    names=['Itot', 'rhl','n', 'BT', 'sky', 'Ie', 're', 'eb', 'bpa', 
           'Id', 'rd', 'ed', 'dpa']
    group_labels = ['m$_{tot}$', 'r$_{hl}$','n$_{sersic}$', 
                    'B/T', 'sky$_{counts}$', 
                    'm$_{bulge}$',  'r$_{bulge}$', '(b/a)$_{bulge}$', 
                    '$\\phi_{bulge}$',  'm$_{disk}$','r$_{disk}$',
                    '(b/a)$_{disk}$','$\\phi_{disk}$']

    fits_labels = ['total mag','halflight rad arcsec','sersic index',
                   '', 'sky counts', 
                   'bulge mag','r bulge arcsec', 'b vs a bulge','pos ang bulge',
                   'disk mag','r disk arcsec', 'b vs a disk', 'pos ang disk']
for name in names:
    hold = data[name]-data[name+'_in']
    arr_to_b.append(hold)
    mask_to_b.append(np.where(np.abs(hold) > 100, 0, 1)) 
    #mask_to_b.append(np.ones_like(hold))
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

if option ==1:
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

elif option == 2:
    pass

pl.xticks(rotation=45)
#pl.suptitle("Correllation of errors for %s model fit with %s" %(inmodel, fitmodel))
pl.savefig('./%s_%s_correlation.eps' %(inmodel, fitmodel))

outfile = open('./%s_%s_correlation.txt' %(inmodel, fitmodel), 'w')
outfile.write(str(correlation_mat))
outfile.close()

outfile = open('./%s_%s_correlation.pickle' %(inmodel, fitmodel), 'w')
pickle.dump([correlation_mat, names, fits_labels], outfile)
outfile.close()
