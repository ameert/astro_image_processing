import numpy as np 
import pyfits 
import os
from SDSS3_image_DN import frame_img

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

        """NOTE: we use petroR50_r for EVERYTHING to maintain consistent 
        cutout size, which makes color measurements easier"""
        for (galcount, run, rerun, camCol, field, rowc, 
             colc, petro_half_light, path_app) in zip(gal['galcount'], 
             gal['run'], gal['rerun'], gal['camCol'], gal['field'],
             gal['rowc_'+band_char] ,gal['colc_'+band_char],
             gal['petroR50_r'],gal['dir_end']):

             file_base = '%s/%08d_%s_' %(path_app, galcount, band_char)
             image_size = petro_half_light * cut_size * 2.0/pix_scale
            
             if image_size < min_size:
                 image_size = min_size

             nm  = 'frame-%s-%06d-%d-%04d.fits' %(band_char,run, camCol, field)
             if not os.path.isfile(data_path + nm+'.bz2'):
                 print data_path+nm
                 bad_gals.write('%d %d %d %d %d %s\n' %(galcount,run, rerun, camCol, field,  nm))
                 continue

             if not os.path.isfile(data_path+nm):
                 str = 'bzip2 -dk %s%s.bz2' %(data_path, nm)
                 os.system(str)

             try:
                 fpc_file = frame_img('%s%s' %(data_path, nm))
                 weight =fpc_file.weight_im(unit='DN')
                 data = fpc_file.DN(sky=True)
                 header = fpc_file.imhead                

                
                 # print shape(data)
                 row_low = np.round(rowc - .5 - .5*image_size)
                 row_high = np.round(rowc - .5 + .5*image_size)
                 col_low = np.round(colc - .5 - .5*image_size)
                 col_high = np.round(colc - .5 + .5*image_size)
                 # -.5 accounts for sdss convention of first pixel being at (.5,.5)

                 if row_low < 0.0:
                     row_low = 0.0
                     row_high = np.round(2*(rowc - .5))
                 if row_high > 1488.0:
                     row_high = 1488.0
                     row_low = np.round(1488.0 - 2*(1488.0 - rowc + .5))
                 if col_low < 0.0:
                     col_low = 0.0
                     col_high = np.round(2*(colc - .5))
                 if col_high > 2047.0:
                     col_high = 2047.0
                     col_low = np.round(2047.0 - 2*(2047.0 - colc + .5))
                
                 trim_data = data[row_low:row_high,col_low:col_high]
                 wz = weight[row_low:row_high,col_low:col_high]
                
                 # Lets generate the weight image while we are here
                 wf =  '%s%s/%sstamp_W.fits' %(out_path, band_char, file_base)
                 os.system('rm -f ' + wf) 
                 hdu = pyfits.PrimaryHDU(wz.astype(np.float32))
                 hdu.writeto(wf, clobber = 1)
                
                 # And update the header
                 header.update('MIN_SIZE', str(min_size), 'pixels')
                 header.update('EXPTIME', str(1.0), 'Exposure time (seconds)')
                 header.update('SOFTBIAS',str(0), 'software "bias" added to all DN')  
                 header.update('FIELD',str(field), 'Field sequence number within the run')  
                 #for del_char in ['RADECSYS', 'CTYPE1','CTYPE2','CUNIT1',
                 #                 'CUNIT2','CRPIX1','CRPIX2','CRVAL1','CRVAL2',
                 #                 'CD1_1','CD1_2','CD2_1','CD2_2']:
                 #    try:
                 #        del header[del_char]          
                 #    except:
                 #        pass
                
                 header.update('rowlow',str(row_low), 'Lowest row value included in cutout')            
                 header.update('rowhigh',str(row_high), 'Lowest row value included in cutout')            
                 header.update('collow',str(col_low), 'Lowest column value included in cutout')            
                 header.update('colhigh',str(col_high), 'Highest column value included in cutout')            

                 # Update the WCS info
                 header.update('CRPIX1',str(float(header['CRPIX1'])-row_low))            
                 header.update('CRPIX2',str(float(header['CRPIX2'])-col_low))            
                 
                 # Finally write the thing
                 ext = pyfits.PrimaryHDU(trim_data, header)
                 outfile = '%s%s/%sstamp.fits' %(out_path, band_char, file_base)
                 print 'writing %s' %outfile
                 ext.writeto(outfile, clobber = 1,output_verify = 'ignore' )
        
             except:
                 bad_gals.write('%d %s\n' %(galcount, nm))
            
        #remove fits file but leve zipped files to save space
        cmd = 'rm %s/*.fits' %data_path
        print "REMOVING FIT images to save space"
        print cmd
        os.system(cmd)
    
        bad_gals.close()
        
    return

