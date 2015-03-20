import numpy as np
import pylab as pl
from statistics.bin_stats import *

from cmp_functions import *

#start_mysql -e "select b.r_bulge, b.ba_bulge, b.pa_bulge, b.r_disk, b.ba_disk, b.pa_disk, b.BT, b.m_tot, b.n_bulge, f.flag from DERT as d, CAST as c, Flags_optimize as f, r_band_serexp as b, M2010 as m  where m.galcount = c.galcount and  b.galcount = c.galcount and c.galcount = f.galcount and f.band='r' and f.model = 'serexp' and f.ftype = 'u' and c.galcount = d.galcount and f.flag&pow(2,19)=0;" > ba_plot_in.txt


r_bulge, ba_bulge, pa_bulge, r_disk, ba_disk, pa_disk, BT, m_tot, n_bulge, flag= np.loadtxt('ba_plot_in.txt', unpack=True, skiprows=1)

flag = np.array(flag, dtype=int)
def angdiff(theta1, theta2):
    theta1 = np.deg2rad(theta1)
    theta2 = np.deg2rad(theta2)
    vec1 = np.array([np.cos(theta1), np.sin(theta1)])
    vec2 = np.array([np.cos(theta2), np.sin(theta2)])
    dot = np.sum(vec1*vec2, axis = 0)
    diff = np.minimum(np.arccos(dot),np.arccos(-1.0*dot))
    return np.rad2deg(diff)

delta_pa =  angdiff(pa_bulge, pa_disk)
delta_ba = ba_bulge-ba_disk 

delta_pa = np.extract(flag&2**10>0, delta_pa)
delta_ba = np.extract(flag&2**10>0, delta_ba)
BT = np.extract(flag&2**10>0, BT)

delta_pa = np.extract(BT>0.6, delta_pa)
delta_ba = np.extract(BT>0.6, delta_ba)


oplot = outlier_fig()
oplot.set_ticks(0.4,0.01,"%0.1f",15.0,2.0,"%d")
oplot.makeplot(delta_ba,delta_pa, (-1.0, 1.0),(0.0, 90.0)) 

pl.show()
