import numpy as np
import pylab as pl
from mysql_class import *
import matplotlib
import matplotlib.cm as cm
import matplotlib.mlab as mlab
from matplotlib.patches import Ellipse
from test_hull import *
from MatplotRc import *

cursor = mysql_connect('simulations', 'pymorph','pymorph')

true_mag, true_magerr, true_rad, true_rad_err = cursor.get_data('select mag, mag_err, rad_pix*0.396, rad_pix_err*0.396 from  bootstrap_test where galcount = -1;')
fit_mag, fit_magerr, fit_rad, fit_rad_err = cursor.get_data('select mag, mag_err, rad_pix*0.396, rad_pix_err*0.396 from  bootstrap_test where galcount = 0;')

scat_mag, scat_magerr, scat_rad, scat_rad_err = cursor.get_data('select mag, mag_err, rad_pix*0.396, rad_pix_err*0.396 from  bootstrap_test where galcount > 0;')

scat_mag = np.array(scat_mag)
scat_magerr = np.array(scat_magerr)
scat_rad = np.array(scat_rad)
scat_rad_err = np.array(scat_rad_err)



def cov_mat(data1, data2, mean1 = None, mean2 = None):
    if mean1 == None:
        mean1 = np.mean(data1)
    if mean2 == None:
        mean2 = np.mean(data2)
    num_obj = data1.size

    cov_mat = np.matrix([[0., 0.],[0., 0.]])

    cov_mat[0,0] = np.sum((data1-mean1)**2)/num_obj
    cov_mat[1,1] = np.sum((data2-mean2)**2)/num_obj
    cov_mat[0,1] = np.sum((data1-mean1)*(data2-mean2))/num_obj
    cov_mat[1,0] = cov_mat[0,1]

    return cov_mat

def error_ellipse(cov_mat):
    print (cov_mat[0,0]**2 +cov_mat[1,1]**2)/2.0
    print np.sqrt((cov_mat[0,0]**2 -cov_mat[1,1]**2)**2.0/4.0 +cov_mat[1,0]**2)

    a = np.sqrt((cov_mat[0,0]**2 +cov_mat[1,1]**2)/2.0 + np.sqrt(((cov_mat[0,0]**2 -cov_mat[1,1]**2)**2.0)/4.0 +cov_mat[1,0]**2))
    b = np.sqrt((cov_mat[0,0]**2 +cov_mat[1,1]**2)/2.0 - np.sqrt(((cov_mat[0,0]**2 -cov_mat[1,1]**2)**2.0)/4.0 +cov_mat[1,0]**2))

    theta = np.degrees(np.arctan(2.0*cov_mat[1,0]/(cov_mat[0,0]**2 -cov_mat[1,1]**2)/2.0))

    return a, b, theta

                                
#cov_matrix = cov_mat(scat_mag, scat_rad)#, fit_mag[0],fit_rad[0])
#print cov_matrix
#print cov_matrix.I

#a,b,theta = error_ellipse(cov_matrix)

#ells = [Ellipse(xy=(fit_mag[0],fit_rad[0]), width=a, height=b, angle=theta)]
#ells = [Ellipse(xy=(fit_mag[0],fit_rad[0]), width=.1, height=.5, angle=theta)]

fig = pl.figure()
ticks = pub_plots(xmaj = 0.02, xmin = 0.01, xstr = '%03.2f', ymaj = .1, ymin = 0.05, ystr = '%03.2f')
ax = fig.add_subplot(111)#, aspect='equal')

#print (fit_mag[0],fit_rad[0])
#print a,b,theta

#for e in ells:
#    ax.add_artist(e)
#    e.set_clip_box(ax.bbox)
#    e.set_alpha(0.0)
#    e.set_facecolor((1.0,1.0,1.0))


#pl.errorbar(scat_mag, scat_rad, xerr=scat_magerr, yerr=scat_rad_err,marker ='s')


plot_data(scat_mag, scat_rad, 100, 1, 17.30, 17.40, 1000,4.5, 4.9, 1000)
#pl.scatter(scat_mag, scat_rad, marker ='s', c='m')
pl.scatter(true_mag, true_rad, marker = '+', s=30)
pl.scatter(fit_mag, fit_rad, marker = 's', s=8)
ax.set_xlim(17.40, 17.30)
ax.set_ylim(4.55, 4.85)
ticks.set_plot(ax)
pl.xlabel('mag')
pl.ylabel('rad (arcsec)')
pl.show()
