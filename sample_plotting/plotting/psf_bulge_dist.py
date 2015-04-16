import numpy as np
import pylab as pl
import matplotlib
import matplotlib.colors as col
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import sys
import os
from matplotlib.backends.backend_pdf import PdfPages

from astro_image_processing.mysql import *
from astro_image_processing.MatplotRc import *

band = 'g'

cursor = mysql_connect('catalog','pymorph','pymorph','')

cmd = "select c.psfWidth_{band}, a.BT, a.m_tot, a.hrad_corr, a.r_bulge, a.ba_bulge, a.n_bulge, b.flag from CAST as c, {band}_band_serexp as a, Flags_catalog as b where a.galcount = b.galcount and a.galcount = c.galcount and b.band='{band}' and b.model = 'serexp' and b.ftype = 'u' and b.flag&pow(2,19)=0;".format(band=band)

psf_width,bt,mtot,hrad,r_bulge,ba_bulge,n_bulge,flag = cursor.get_data(cmd)



fig = pl.figure(figsize=get_fig_size())

ticklabs = pub_plots(xmaj = 5, xmin = 1, xstr = '%03.2f', ymaj = 5, ymin = 1, ystr = '%d')





