from numpy import * 
import pyfits 
import os


def cut_images(gal, bands, data_path, out_path):
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
            petro_half_light = gal['petroR50_'+band_char][count]
    
            
            file_base = '%06d_%s_' %(galcount_tmp, band_char)
            image_size = petro_half_light * 8.0 * 2.0/.396

            nm  = 'fpC-%06d-%s%d-%04d.fit.gz' %(run_tmp, band_char, camCol_tmp, field_tmp)
            str = 'gunzip %s%s' %(data_path, nm)
            os.system(str)
        
            fpc_file = '%s%s' %(data_path, nm[0:-3])
            image = pyfits.open(fpc_file)
            data = image[0].data
            data = data - 1000.
            # print shape(data)
            row_low = round(rowc_tmp - .5 - .5*image_size)
            row_high = round(rowc_tmp - .5 + .5*image_size)
            col_low = round(colc_tmp - .5 - .5*image_size)
            col_high = round(colc_tmp - .5 + .5*image_size)
            # -.5 accounts for sdss convention of first pixel being at (.5,.5)

            if row_low < 0.0:
                row_low = 0.0
                row_high = round(2*(rowc_tmp - .5))
            if row_high > 1488.0:
                row_high = 1488.0
                row_low = round(1488.0 - 2*(1488.0 - rowc_tmp + .5))
            if col_low < 0.0:
                col_low = 0.0
                col_high = round(2*(colc_tmp - .5))
            if col_high > 2047.0:
                col_high = 2047.0
                col_low = round(2047.0 - 2*(2047.0 - colc_tmp + .5))
                
            ext = pyfits.PrimaryHDU(data[row_low:row_high,col_low:col_high])
            outfile = '%s%s/%sstamp.fits' %(out_path, band_char, file_base)
            os.system('rm '+outfile)
            ext.writeto(outfile)
        
            str = 'gzip %s%s' %(data_path,nm[0:-3])
            os.system(str)
    return

