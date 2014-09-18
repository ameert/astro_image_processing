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

model = 'serexp'
band = 'r'
uname = 'alan'
cursor = mysql_connect('catalog','pymorph','pymorph','')

cmd = """select x.galcount, z.Hrad_corr,z.BT, 
z.m_tot-x.extinction_{band},  
z.r_bulge*sqrt(z.ba_bulge), z.n_bulge, 
z.r_disk*sqrt(z.ba_disk),
s.kpc_per_arcsec, z.m_bulge-x.extinction_{band}, 
z.m_disk-x.extinction_{band}, c.flag, s.dismod,
x.petromag_g - x.extinction_g, x.petromag_r - x.extinction_r, 
x.petromag_i - x.extinction_i, -4.5775*m.probaEll -2.35723*m.probaS0+2.48028*m.probaSab+6.0815*m.probaScd, s.kcorr_g, s.kcorr_r, s.kcorr_i
from 
{band}_band_{model} as z,{band}_band_fit as y,CAST as x, DERT as s,
M2010 as m, Flags_catalog as c 
where 
y.galcount = x.galcount and
x.galcount = s.galcount and 
x.galcount = z.galcount and 
x.galcount = m.galcount and
x.galcount = c.galcount and
c.band = '{band}' and c.model = '{model}' and
c.ftype = 'u' 
order by 
x.galcount;""".format(model = model, band = band)

# , r_lackner_fit as a 
# x.galcount = a.galcount and


data = cursor.get_data(cmd)

data = [np.array(d) for d in data]

pos_dict = dict([(a[0],a[1]) for a in zip(['galcount', 'hrad_corr', 'BT',
                                      'mag', 'r_bulge','n_bulge',
                                      'r_disk', 'kpc_per_arcsec', 
                                      'm_bulge', 'm_disk', 
                                      'flag','dismod', 'petrog','petror',
                                      'petroi', 'ttype', 'kg', 'kr', 'ki'
                                           ], data)])

outfile = open('./color_file.npz', 'w')
np.savez(outfile, **pos_dict)
outfile.close()
