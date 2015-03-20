#!/data2/home/ameert/python/bin/python2.5

import pyfits as pf
from mysql_class import *
import numpy as np
import sys
from sersic_classes import *

start = int(sys.argv[1])
stop = int(sys.argv[2])

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
cursor = mysql_connect(dba, usr, pwd, 'shredder')

for model in model_list:
    galcount, = cursor.get_data("select simcount from sim_input_hst where simcount between %d and %d order by simcount;" %(start, stop))
                    
    for gc in galcount:
        print gc
        im = pf.open("/data2/home/ameert/hst_sims/sim_image/%08d_nopsf.fits" %(gc))
        new_gal =  im_obj(im[0].data)

        new_gal.convolve_image("/data2/home/ameert/hst_sims/%08d_psf.fits" %(gc))

        header = im[0].header

        ext = pf.PrimaryHDU(new_gal.convolved_image, header = header)

        ext.writeto("/data2/home/ameert/hst_sims/sim_image/%08d_flat.fits" %(gc), clobber =1)
        im.close()
        
