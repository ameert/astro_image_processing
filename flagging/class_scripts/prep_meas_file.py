import numpy as np
import scipy as sc
import pyfits as pf
import pylab as pl
import pickle
import os
import sys

from flag_defs import *
from mysql.mysql_class import *
#from gal_panel import *

model = sys.argv[2]
uname = 'alan'
cursor = mysql_connect('catalog','pymorph','pymorph','')
band = sys.argv[1]

cmd = """select x.galcount, z.Hrad_corr,z.BT, 
z.m_tot, -x.aa_{band} - x.kk_{band}*x.airmass_{band},
y.SexHrad, x.petroR50_{band}
from 
{band}_highn_{model} as z,
{band}_highn_fit as y,
CAST as x, DERT as s
where 
x.galcount = s.galcount and y.galcount = x.galcount and
x.galcount=z.galcount order by x.galcount;""".format(model = model, band = band)

data = cursor.get_data(cmd)

data = np.array([np.array(d) for d in data])

pos_dict = dict((a[1],a[0]) for a in enumerate(['galcount', 'hrad_corr', 'BT',
                                      'mag', 'zp', 'hrad_sex', 'petrorad']))

new_data = {'galcount': [int(a) for a in data[pos_dict['galcount']]],
            'tot_counts': 10.0**(-0.4*(data[pos_dict['mag']] - data[pos_dict['zp']]))}

new_data['r_tot']=data[pos_dict['hrad_corr']]
new_data['r_sex']=data[pos_dict['hrad_sex']]
new_data['r_petro']=data[pos_dict['petrorad']]
new_data['BT']=data[pos_dict['BT']]

outfile = open('full_highn_info_%s_%s.pickle' %(band,model), 'w')
pickle.dump(new_data, outfile)
outfile.close()
