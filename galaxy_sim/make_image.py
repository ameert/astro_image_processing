#!/usr/bin/python

import sys
import os
import numpy as np
import scipy as sci
import pyfits as pf

from generate_images import *

def adjust_ang(ang):
    return ang

def do_psf(frame, obj,rowc,colc,band_char='r',run=745,camcol=2,field=518):  
    if band_char == 'u':
        band = 1
    elif band_char == 'g':
        band = 2
    elif band_char == 'r':
        band = 3
    elif band_char == 'i':
        band = 4
    elif band_char == 'z':
        band = 5
        
    nm  = '/home/ameert/bkrd_3/field_data/psField-%06d-%d-%04d.fit' %(run, camcol, field)
                
    cmd = '/home/ameert/software/readAtlasImages-v5_4_11/read_PSF  %s %d %f %f %d_%d_psf.fits' %(nm, band, rowc, colc, frame, obj)
    print cmd
    os.system(cmd)

    a = pf.open('%d_%d_psf.fits' %(frame,obj),'update' )
    # remove 1000 count soft-bias from images
    a[0].data = a[0].data - 1000
            
    a.close()

def main(field_info):
    band = field_info['band']
    indat = pf.open(field_info['infile'])

    data = indat[1].data
    header = indat[1].header

    print header

    indat.close()

    header_dict = {}
    count = 0


    count = 0
    gal_cnt = 0
    st_cnt = 0
    full_frame = im_obj(np.zeros((1489, 2048)))

    for obj in data:
        count+=1
        if obj['obj']== field_info['skipobj']:
            continue
        I_star = mag_to_counts(obj['PSFmag_%s' %band], obj['aa_%s' %band],
                               kk = obj['kk_%s' %band] , 
                               airmass = obj['airmass_%s' %band])
        I_dev = mag_to_counts(obj['devmag_%s' %band], obj['aa_%s' %band],
                              kk = obj['kk_%s' %band] , 
                              airmass = obj['airmass_%s' %band])
        I_exp = mag_to_counts(obj['expmag_%s' %band], obj['aa_%s' %band],
                              kk = obj['kk_%s' %band] , 
                              airmass = obj['airmass_%s' %band])
        inpsf = '%d_%d_psf.fits' %(field_info['frame'],count)

        print count , obj['rowc_%s' %band], obj['colc_%s' %band]
        print obj['PSFmag_%s' %band],obj['devmag_%s' %band],obj['expmag_%s' %band] 
        print obj['aa_%s' %band],obj['kk_%s' %band] , obj['airmass_%s' %band]
        print I_star, I_dev, I_exp
        print 'prob ', obj['probPSF']
        print obj['petroMag_%s' %band]

        I_star = 1.0
        I_dev = 1.0
        I_exp = 1.0
        do_psf(field_info['frame'], count,obj['rowc_%s' %band], obj['colc_%s' %band],band_char=band, run=obj['run'],camcol=obj['camCol'], field=obj['field'])

        if obj['PSFmag_%s' %band] < 0 or obj['devmag_%s' %band] < 0 or obj['expmag_%s' %band] < 0:
            continue    

        if  decide_obj(obj['probPSF']):
            print 'Star !!!'
            st_cnt +=1
            obim = point(I_star, obj['colc_%s' %band], obj['rowc_%s' %band])
            obim.make_image(inpsf)
            to_add = obim.convolved_image
        else:
            print 'Galaxy !!!'
            gal_cnt +=1

            print obj['expRad_%s' %band]
            obj['expPhi_%s' %band] = adjust_ang(obj['expPhi_%s' %band])
            obj['devPhi_%s' %band] = adjust_ang(obj['devPhi_%s' %band])
            print obj['expRad_%s' %band]
            try:
                obim = galaxy(I_dev,obj['devPhi_%s' %band], obj['devab_%s' %band], 
                              obj['devRad_%s' %band], I_exp, obj['expPhi_%s' %band],
                              obj['expab_%s' %band], obj['expRad_%s' %band], 
                              obj['fracdev_%s' %band], obj['colc_%s' %band], 
                              obj['rowc_%s' %band], inpsf)

                to_add = obim.new_gal.convolved_image
            except:
                to_add = np.zeros((1489, 2048))
        print 'adding image'
        full_frame.image += to_add


    full_frame.image =np.abs(full_frame.image) 
    if band == 'g':
        full_frame.image +=85.0
    elif band == 'r':
        full_frame.image +=130.0
    #full_frame.convolve_image('1_psf.fits')

    print "counts (star,gal) ", st_cnt, gal_cnt
    ext = pf.PrimaryHDU(full_frame.image)
    ext.writeto(field_info['outfile'], clobber = 1)

if __name__ == "__main__":
    choice = int(sys.argv[1])
	
    gal = {'galcount':[138529,142447,149162,558387,561842],
           'run':[2583,2662,2738,3325,3325],
           'rerun':[40,40,40,41,41],
           'camCol':[4,3,4,1,4],
           'field':[130,285,24,136,180]
           'skipobj':[[404, 419, 690, 963, 1244, 1665],
                      [130,210,290,1010],
                      [201,607,664,794],
                      [212,249],
                      [133,832]]      
}	

    field_info = {'galcount':gal['galcount'][choice], 'run':gal['run'][choice], 
                  'rerun':gal['rerun'][choice],'camcol':gal['rerun'][choice], 
                  'field':gal['filed'][choice], 
                  'infile':'./field_data/tsObj-%06d-%d-%d-%04d.fit' %(gal['run'][choice], gal['camCol'][choice], gal['rerun'][choice], gal['field'][choice]),
                  'outfile': 'flat_back_%d.fits' %gal['galcount'][choice]
                  'skipobj':gal['skipobj'][choice],
                  'frame':gal['frame'][choice],
                  'band':'r',
                  }

    main(field_info)
    os.system('rm %d_*psf.fits' %count)

