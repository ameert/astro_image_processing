import numpy as np 
import pyfits 
import os


def cut_images(gal, bands, data_stem, out_path, cut_size = 20.0, 
               pix_scale = 0.396, min_size = 80.0):
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

        data_path = data_stem + band_char + '/'

        if not os.path.isdir(out_path + band_char):
            os.mkdir(out_path+band_char)
            
        bad_gals = open(out_path + 'bad_gals_' + band_char+'.txt', 'a')

        for count in range(len(gal['galcount'])):
            galcount_tmp = gal['galcount'][count]
            run_tmp      = gal['run'][count]
            rerun_tmp    = gal['rerun'][count]
            camCol_tmp   = gal['camCol'][count]
            field_tmp    = gal['field'][count]
            rowc_tmp     = gal['rowc_'+band_char][count]
            colc_tmp     = gal['colc_'+band_char][count]
            # We want to cut everything to the same size
            petro_half_light = gal['petroR50_r'][count]
            gain_tmp    = gal['gain_'+band_char][count]
            noise_tmp   =  gal['darkvariance_'+band_char][count]
            path_app    =  gal['dir_end'][count]

            file_base = '%s/%08d_%s_' %(path_app, galcount_tmp, band_char)
            image_size = petro_half_light * cut_size * 2.0/pix_scale
            
            if image_size < min_size:
                image_size = min_size

            nm  = 'fpC-%06d-%s%d-%04d.fit.gz' %(run_tmp, band_char, camCol_tmp, field_tmp)
            if not os.path.isfile(data_path + nm):
                print data_path+nm
                bad_gals.write('%d %d %d %d %d %s\n' %(galcount_tmp,run_tmp, rerun_tmp, camCol_tmp, field_tmp,  nm))
                continue

            str = 'gunzip -f %s%s' %(data_path, nm)
            os.system(str)

            try:
                fpc_file = '%s%s' %(data_path, nm[0:-3])
                image = pyfits.open(fpc_file)
                data = image[0].data
                data = data - 1000.
                header = image[0].header
                image.close()

                # print shape(data)
                row_low = np.round(rowc_tmp - .5 - .5*image_size)
                row_high = np.round(rowc_tmp - .5 + .5*image_size)
                col_low = np.round(colc_tmp - .5 - .5*image_size)
                col_high = np.round(colc_tmp - .5 + .5*image_size)
                # -.5 accounts for sdss convention of first pixel being at (.5,.5)

                if row_low < 0.0:
                    row_low = 0.0
                    row_high = np.round(2*(rowc_tmp - .5))
                if row_high > 1488.0:
                    row_high = 1488.0
                    row_low = np.round(1488.0 - 2*(1488.0 - rowc_tmp + .5))
                if col_low < 0.0:
                    col_low = 0.0
                    col_high = np.round(2*(colc_tmp - .5))
                if col_high > 2047.0:
                    col_high = 2047.0
                    col_low = np.round(2047.0 - 2*(2047.0 - colc_tmp + .5))
                
                trim_data = data[row_low:row_high,col_low:col_high]
            
                # Lets generate the weight image while we are here
                exptime = float(header['EXPTIME'])
                wz = np.sqrt(trim_data / gain_tmp + noise_tmp) / exptime
                wf =  '%s%s/%sstamp_W.fits' %(out_path, band_char, file_base)
                os.system('rm -f ' + wf) 
                hdu = pyfits.PrimaryHDU(wz.astype(np.float32))
                hdu.writeto(wf, clobber = 1)

                # now normalize the image
                trim_data = trim_data/exptime

                # And update the header
                header.update('MIN_SIZE', min_size, 'pixels')
                header.update('EXPTIME', 1.0, 'Exposure time (seconds)')
                header.update('RDNOISE', noise_tmp, "approximated from dark varience")
                header.update('GAIN', gain_tmp, "approximated from gain")
                header.update('NCOMBINE', 1)
                header.update('SOFTBIAS',0, 'software "bias" added to all DN')  
                header.update('FIELD',field_tmp, 'Field sequence number within the run')  
                for del_char in ['RADECSYS', 'CTYPE1','CTYPE2','CUNIT1',
                                 'CUNIT2','CRPIX1','CRPIX2','CRVAL1','CRVAL2',
                                 'CD1_1','CD1_2','CD2_1','CD2_2']:
                    try:
                        del header[del_char]          
                    except:
                        pass
                
                # Finally write the thing
                ext = pyfits.PrimaryHDU(trim_data, header)
                outfile = '%s%s/%sstamp.fits' %(out_path, band_char, file_base)
                print 'writing %s' %outfile
                ext.writeto(outfile, clobber = 1,output_verify = 'ignore' )
        
            except:
                bad_gals.write('%d %s\n' %(galcount_tmp, nm))
            str = 'gzip %s%s' %(data_path,nm[0:-3])
            os.system(str)

        bad_gals.close()

    return

