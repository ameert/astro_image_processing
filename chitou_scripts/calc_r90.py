import numpy as np
import scipy.interpolate as interp
from mysql_class import *

cursor = mysql_connect('catalog','pymorph','pymorph','')

nvals, rad_vals = np.loadtxt('n_r90.tbl', unpack = True)

tck = interp.splrep(nvals, rad_vals)

galcount, r50, ngal = cursor.get_data('select galcount, r50_r_arcsec, n from ser_hrad_90_est;')

r90 = interp.splev(ngal, tck)*r50

for cgal, cr90 in zip(galcount, r90):
    cursor.execute('update ser_hrad_90_est set r90_r_arcsec=%.2f where galcount = %d;' %(cr90, cgal))
