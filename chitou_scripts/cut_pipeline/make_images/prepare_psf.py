from numpy import * 
import pyfits 
import os

def prepare_psf(gal, bands, data_path, out_path):
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

        if not os.path.isdir(out_path + band_char):
            os.mkdir(out_path+band_char)
            
        for count in range(len(gal['galcount'])):
            galcount_tmp = gal['galcount'][count]
            run_tmp      = gal['run'][count]
            rerun_tmp    = gal['rerun'][count]
            camCol_tmp   = gal['camCol'][count]
            field_tmp    = gal['field'][count]
            rowc_tmp     = gal['rowc_'+band_char][count]
            colc_tmp     = gal['colc_'+band_char][count]

            file_base = '%06d_%s_' %(galcount_tmp, band_char)
    
            nm  = 'psField-%06d-%d-%04d.fit' %(run_tmp, camCol_tmp, field_tmp)
            str = '/home/ameert/readAtlasImages-v5_4_11/read_PSF  %s%s %d %f %f %s%s/%spsf.fits' %(data_path,nm, band, rowc_tmp, colc_tmp, out_path, band_char, file_base)
            os.system(str)
    return

