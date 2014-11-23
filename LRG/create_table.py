from astro_image_processing import mysql
import pyfits as pf
import numpy as np
from scipy import integrate

dir = '/home/clampitt/filaments/spatial_cats/'
patches = np.arange(0, 33, 1)

for patch in patches:
    print('Patch number %d' % (patch))
    lensfile = 'pair-cat-nov4_LRG_Rmax24.0_rlos6.0_p%d.fit' % (patch)
    hdu = pf.open(dir + lensfile)
    data = hdu[1].data
    indices=[]
    for i in data:
        print i
        break
    print hdu[1].header
    hdu.close()
    break
