import pyfits
import numpy as np
import pylab
from scipy import interpolate
from MatplotRc import *
from mysql_class import *

cursor = mysql_connect('pymorph','pymorph','pymorph9455','shredder')
cmd = 'Select galcount from r_full order by rand() limit 10;'

galaxies, = cursor.get_data(cmd)

print galaxies

#galaxies = [46,109,120,252,267,347,375]

for curr_gal in galaxies:
    image = pyfits.open('/data2/home/ameert/sdss_sample/serexp/O_%08d_r_stamp.fits' %(curr_gal)) 

    bulge = image[4].data
    disk = image[5].data

    im_size = np.shape(bulge)
    im_rad = im_size[0]/2
    
    rad = np.arange(2,im_rad, 2)
    bt = []
    for rr in rad:
        b_p=bulge[im_rad - rr: im_rad + rr,im_rad - rr: im_rad + rr]
        d_p=disk[im_rad - rr: im_rad + rr,im_rad - rr: im_rad + rr]

        bt.append(b_p.sum()/(d_p.sum()+b_p.sum()))
        print bt

    SplineResult = interpolate.splrep(rad, bt, s=0, k=3)

    bt_der_1 = interpolate.splev(rad, SplineResult, der=1)
    bt_der_2 = interpolate.splev(rad, SplineResult, der=2)
    
    print rad
    print bt

    
    fig = pylab.figure(figsize = (12.0, 4.0))
    matrc4()
    pylab.subplots_adjust(left = 0.06,  # the left side of the subplots of the figure
                          right = 0.97,    # the right side of the subplots of the figure
                          bottom = 0.12,   # the bottom of the subplots of the figure
                          top = 0.87,      # the top of the subplots of the figure
                          wspace = 0.3,   # the amount of width reserved for blank space between subplots
                          hspace = 0.3)   # the amount of height reserved for white space between subplots

    pylab.suptitle('BT as a function of radius for galaxy %d' %(curr_gal))

    fig.add_subplot(1,3,1)
    pylab.title('BT')
    pylab.plot(rad*.395, bt)
    pylab.xlabel('radius in arcsec')
    pylab.ylabel('BT')

    fig.add_subplot(1,3,2)
    pylab.title('BT first derivative')
    pylab.plot(rad*.395, bt_der_1)
    pylab.xlabel('radius in arcsec')
    pylab.ylabel('BT derivative')

    fig.add_subplot(1,3,3)
    pylab.title('BT second derivative')
    pylab.plot(rad*.395, bt_der_2)
    pylab.xlabel('radius in arcsec')
    pylab.ylabel('BT derivative')


    pylab.savefig('im_%06d.png' %(curr_gal), format = 'png')
    pylab.clf()
    image.close()
