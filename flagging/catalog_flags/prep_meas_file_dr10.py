import numpy as np
import scipy as sc
import pyfits as pf
import pylab as pl
import pickle
import os
import sys

from astro_image_processing.mysql import *
from astro_image_processing.user_settings import mysql_params

model = sys.argv[1]
band = sys.argv[2]

cursor = mysql_connect(mysql_params['dba'],mysql_params['user'],
                       mysql_params['pwd'],mysql_params['host'])

cmd = """select x.galcount, z.Hrad_corr,z.BT, 
z.m_tot, -x.aa_{band} - x.kk_{band}*x.airmass_{band},
y.SexHrad, x.petroR50_{band},x.petroR50_r,
a.petroR50_r,a.petroR90_r,a.petroRad_r,2.0,3.0
from 
{band}_band_{model} as z,
{band}_band_fit as y,
CAST as x, DERT as s, CAST_dr10 as a
where 
x.galcount=a.galcount and 
x.galcount = s.galcount and y.galcount = x.galcount and
x.galcount=z.galcount order by x.galcount;""".format(model = model, band = band)

data = cursor.get_data(cmd)

data = np.array([np.array(d) for d in data])

pos_dict = dict((a[1],a[0]) for a in enumerate(['galcount', 'hrad_corr', 'BT',
                                      'mag', 'zp', 'hrad_sex', 'petrorad', 
                                      'petrorad_r', 
            'dr10_petrorad50_r', 'dr10_petrorad90_r', 'dr10_petroradtot_r', 'fiber2', 'fiber3']))

new_data = {'galcount': [int(a) for a in data[pos_dict['galcount']]],
            'tot_counts': 10.0**(-0.4*(data[pos_dict['mag']] - data[pos_dict['zp']]))}

new_data['r_tot']=data[pos_dict['hrad_corr']]
new_data['r_sex']=data[pos_dict['hrad_sex']]
new_data['r_petro']=data[pos_dict['petrorad']]
new_data['r_petro_r']=data[pos_dict['petrorad_r']]
new_data['BT']=data[pos_dict['BT']]



new_data['dr10_petro50']=data[pos_dict['dr10_petrorad50_r']]
new_data['dr10_petro90']=data[pos_dict['dr10_petrorad90_r']]
new_data['dr10_petrotot']=data[pos_dict['dr10_petroradtot_r']]
new_data['fiber2']=np.array(data[pos_dict['fiber2']], dtype=float)
new_data['fiber3']=np.array(data[pos_dict['fiber3']], dtype=float)




outfile = open('dr10_full_catalog_info_%s_%s.pickle' %(band,model), 'w')
pickle.dump(new_data, outfile)
outfile.close()
