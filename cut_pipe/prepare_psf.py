from numpy import *
import numpy as np 
import pyfits as pf
import os
import astro_image_processing.user_settings as user_settings

def prepare_psf(gal, bands, data_stem, out_path):
    for band_char in bands:
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

        data_path = data_stem + 'psField/'

        if not os.path.isdir(out_path + band_char):
            os.mkdir(out_path+band_char)
        
        for a in gal['dir_end']:
            if not os.path.isdir(out_path + band_char+'/'+a):
                os.mkdir(out_path+band_char+'/'+a)
            

        for count in range(len(gal['galcount'])):
            galcount_tmp = gal['galcount'][count]
            run_tmp      = gal['run'][count]
            rerun_tmp    = gal['rerun'][count]
            camCol_tmp   = gal['camCol'][count]
            field_tmp    = gal['field'][count]
            rowc_tmp     = gal['rowc_'+band_char][count]
            colc_tmp     = gal['colc_'+band_char][count]
            path_app     = gal['dir_end'][count]

            file_base = '%08d_%s_' %(galcount_tmp, band_char)
    
            nm  = 'psField-%06d-%d-%04d.fit' %(run_tmp, camCol_tmp, field_tmp)
            if not os.path.isfile(data_path+nm):
                if os.path.isfile(data_path+nm+'.gz'):
                    print 'gunzip -f -k '+data_path+nm+'.gz'
                    os.system('gunzip -f -k '+data_path+nm+'.gz')
                
            str = '%s  %s%s %d %f %f %s%s/%s/%spsf.fits' %(user_settings.readatlas_readPSF_path, data_path,nm, band, rowc_tmp, colc_tmp, out_path, band_char, path_app, file_base)
            os.system(str)

            a = pf.open('%s%s/%s/%spsf.fits' %(out_path, band_char, path_app, file_base),'update' )
            # remove 1000 count soft-bias from images and normalize
            a[0].data = a[0].data - 1000
            a[0].data = a[0].data/np.sum(a[0].data)
            
            a.close()

    raw_input()
    # remove unpacked fits files but leave zipped files to save space
    cmd = 'rm %s/*.fit' %data_path
    print "REMOVING FIT images to save space"
    print cmd
    os.system(cmd)
    return

