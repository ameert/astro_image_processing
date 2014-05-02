import numpy as np
import pylab as pl
import matplotlib
import matplotlib.colors as col
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import sys
import os
from matplotlib.backends.backend_pdf import PdfPages

from mysql.mysql_class import *
from MatplotRc import *


cursor = mysql_connect('catalog','pymorph','pymorph','')

cmd = "select c.psfWidth_r, a.BT, a.m_tot, a.hrad_corr, a.r_bulge, a.ba_bulge, a.n_bulge, b.flag from CAST as c, r_band_serexp as a, Flags_optimize as b where a.galcount = b.galcount and a.galcount = c.galcount and b.band='r' and b.model = 'serexp' and b.ftype = 'u' and b.flag&pow(2,19)=0;"

psf_width,bt,mtot,hrad,r_bulge,ba_bulge,n_bulge,flag = cursor.get_data(cmd)






fig = figure(figsize=get_fig_size())

ticklabs = pub_plots(xmaj = 5, xmin = 1, xstr = '%03.2f', ymaj = 5, ymin = 1, ystr = '%d')


