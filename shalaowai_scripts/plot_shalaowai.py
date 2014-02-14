#!/usr/bin/python

import pyfits as pf
import os
import sys
import copy
import traceback
from matplotlib import rc

from config import *

rc('text', usetex=True)
sys.path.append(alans_pipeline_dir)
sys.path.append(shalaowai_package_dir)

from get_gal import *
import astro_utils.user_params as params 
from astro_utils.surf_bright import *  
from astro_utils.surf_bright import *  
from astro_utils.sizes import *  
import mysql
from plot_1d_shalaowai import *
from flag_defs import *

def decompress_data(image, MIN, MAX, precision):
    """decompress array data from storage on a linear scale"""
    new_im = image.astype('float')
    scale_range = MAX-MIN

    new_im = (new_im*scale_range/precision) + MIN

    return new_im

def decompress(data, header):
    out_dat = {}
    out_dat['data'] = decompress_data(data, header['MINDAT'],header['MAXDAT'],
                               header[' SCALEDAT']) 
    
    out_dat['xctr']=header['IMCTR_X']
    out_dat['yctr']=header['IMCTR_Y']

    try:
        out_dat['xext']=(header['IMEXT_XL'],header['IMEXT_XH'])
        out_dat['yext']=(header['IMEXT_YL'],header['IMEXT_YH'])
    except KeyError:
        out_dat['xext']=(0,header['XSIZE_O'])
        out_dat['yext']=(0,header['YSIZE_O'])

    return out_dat



cursor = mysql.mysql_connect( dba, usr, pwd, lhost = host)

galcount = int(sys.argv[1])
try:
    models = [a for a in sys.argv[2:]]
except:
    models = ['ser']
band ='r'

folder_num = (galcount-1)/250 +1


source_dir =  source_dir.format(band=band)
data_dir = main_path + 'data_dir/'
plots_dir = main_path + 'plot_dir/'

copy_command = 'scp ameert@folio.sas.upenn.edu:"%s/{source_subdir}/{galstem1} %s/{source_subdir}/{galstem2}" %s' %(source_dir,source_dir, data_dir)

for model in models:
    save_name = plots_dir +'%06d_%s_%s.png' %(galcount,band,model)
    
    if not os.path.isfile(save_name):
        os.system(copy_command.format(source_subdir='%04d' %folder_num, galstem1='%08d_*.fits' %galcount, galstem2='%08d_*.npz' %galcount))
        break

plot_namestem = '%08d_%s_{model}.png' %(galcount, band)

#### Stuff to be printed on the plot ####
print_left = {
    8:['absmag','M$_{\mathrm{MODEL}}$', '%4.3f', models],
    9:['appmag','m$_{\mathrm{MODEL}}$', '%4.3f', models],
    10:['BT',  'B/T$_{\mathrm{MODEL}}$', '%3.2f', ['devexp','serexp']],
    11:['n',  'n$_{\mathrm{MODEL}}$', '%3.2f', ['ser','serexp']],
    12:['hrad_corr', 'r$_{\mathrm{hl, cir, MODEL}}$', '%3.2f', models],
    13:['re','r$_{\mathrm{bulge, MODEL}}$', '%3.2f', models],
    14:['rd','r$_{\mathrm{disk, MODEL}}$', '%3.2f', ['devexp','serexp']],
    15:['bpa','pa$_{\mathrm{bulge, MODEL}}$', '%3.2f', models],
    16:['dpa','pa$_{\mathrm{disk, MODEL}}$', '%3.2f', ['devexp','serexp']],
    17:['eb','ba$_{\mathrm{bulge, MODEL}}$', '%3.2f', models],
    18:['ed','ba$_{\mathrm{disk, MODEL}}$', '%3.2f', ['devexp','serexp']],
    #19:['GalSky', 'sky$_{MODEL}$', '%5.4f', models]       
    }

print_right = {
    1:['z','z', '%3.2f', models],
    2:['zoo_pE','P$_{zoo}$(Ell)','%3.2f', models],
    3:['zoo_pS','P$_{zoo}$(Spiral)','%3.2f', models],
    4:['m_pEL','P(Ell)','%3.2f', models],
    5:['m_pS0','P(S0)','%3.2f', models],
    6:['m_pSAB','P(Sab)','%3.2f', models],
    7:['m_pSCD','P(Scd)','%3.2f', models],
    8:['petro_absmag','M$_{\mathrm{Petro}}$', '%4.3f', models],
    9:['petro_mag','m$_{\mathrm{Petro}}$', '%4.3f', models],
    10:['petroR50', 'r$_{\mathrm{Petro}}$', '%3.2f', models],
    }
 
label_string = 'Note: The 1d data is calculated using background-subtracted data. The 2d data is shown with background included.' 
    
###### End of Stuff to be printed on the plot #####

gal_info = copy.deepcopy(g)

for model in models:
    save_name = plots_dir +'%06d_%s_%s.png' %(galcount,band,model)
    
    if not os.path.isfile(save_name):
        gal_info = get_gal(cursor, model, galcount, gal_info, band = 'r')
        gal_info['model_types'][model]=model
        gal_info['band'][model]=band
        gal_info['Name'][model]= 'r_%08d_r_stamp' %galcount

        # load images
        two_d_ims = {}

        infile = pf.open('%s/%08d_r_input.fits' %(data_dir, galcount))
        two_d_ims['data_wide'] = decompress(infile[1].data, infile[1].header)
        two_d_ims['data'] = decompress(infile[2].data, infile[2].header)
        infile.close()

        infile = pf.open('%s/%08d_r_model_%s.fits' %(data_dir,galcount,model))
        two_d_ims['model'] = decompress(infile[1].data, infile[1].header)
        two_d_ims['resid'] = decompress(infile[2].data, infile[2].header)
        infile.close()

        for key in ['data_wide','data','model']:
            two_d_ims[key]['data'], err = co_pix_to_mag_arc(two_d_ims[key]['data'], 
               np.ones_like(two_d_ims[key]['data']), 
               gal_info['sdss_zeropoint'][model], kk = gal_info['kk'][model], 
               airmass = gal_info['airmass'][model], band = band, exptime=1.0)
            print 'extent %s ' %key, two_d_ims[key]['xext'], two_d_ims[key]['yext']
        two_d_ims['resid']['data'] = (two_d_ims['model']['data'] - two_d_ims['data']['data']) 
        
        new_extent = np.array([np.array(two_d_ims['data']['xext'], dtype=float)-two_d_ims['data']['xctr'], np.array(two_d_ims['data']['yext'], dtype=float)-two_d_ims['data']['yctr']])
        new_extent = new_extent.flatten()
        print 'new extent', new_extent

        full_sky = gal_info['GalSky'][model]
        one_percent_sky = gal_info['GalSky'][model]+ 5.0


        data_1d = np.load(data_dir+'%08d_%s_%s_all_profs_joined.npz' %(galcount, band, model))
#        print data_1d.keys()
#        print data_1d['rad'],data_1d['rad'].shape
#        print data_1d['data'],data_1d['data'].shape
#        sys.exit()
        
        d1_data = {}
        d1_data['rad'] = pixels_to_size(data_1d['rad'])
        d1_data['data'],err = co_pix_to_mag_arc(data_1d['data'], np.ones_like(data_1d['data']), gal_info['sdss_zeropoint'][model], kk = gal_info['kk'][model], airmass = gal_info['airmass'][model], band = band, exptime=1.0)
        d1_data['total'],err = co_pix_to_mag_arc(data_1d['model'], np.ones_like(data_1d['model']), gal_info['sdss_zeropoint'][model], kk = gal_info['kk'][model], airmass = gal_info['airmass'][model], band = band, exptime=1.0)
        if model in ['devexp', 'serexp']:
            d1_data['bulge'],err = co_pix_to_mag_arc(data_1d['bulge'], np.ones_like(data_1d['bulge']), gal_info['sdss_zeropoint'][model], kk = gal_info['kk'][model], airmass = gal_info['airmass'][model], band = band, exptime=1.0)
            d1_data['disk'],err = co_pix_to_mag_arc(data_1d['disk'], np.ones_like(data_1d['disk']), gal_info['sdss_zeropoint'][model], kk = gal_info['kk'][model], airmass = gal_info['airmass'][model], band = band, exptime=1.0)
        d1_data['resid']= d1_data['total']-d1_data['data']
        d1_data['bt_rad'] = data_1d['bt_hrad']*gal_info['hrad_corr'][model]
        d1_data['bt_at_rad'] = data_1d['bt_at_hrad']
        d1_data['bt_cum'] = data_1d['bt_cum']
        d1_data['light_cum'] = data_1d['light_cum']
        

        # set the largest radii to which the 1D profile will be plotted
        #d1_max_rad = gal_info['petroR50'][model] * 6.0
        d1_max_rad = gal_info['hrad_corr'][model] * 6.0

        #### add values to stuff printed on the left side of the plot ##### 
        add_info_left =[]
        try:
            for key in print_left.keys():
                if model in print_left[key][3]:
                    ts = print_left[key][2] %(gal_info[print_left[key][0]][model])
                    add_info_left.append(print_left[key][1].replace('MODEL', model) + ' = '+ ts)
        except Exception, inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to printed directly
            print "something bad happened!!!!\n\n"
            traceback.print_exc()
            print key
            print print_left[key][2]
            print gal_info[print_left[key][0]][model]

        for count in range(0,1):
            add_info_left.append('')
        
        add_info_left.append(r'\underline{FLAGS}')
        
        ff = gal_info['flags'][model]
        if  ff >= 0:
            for curr_flag in category_flag:#([('no fitflags', -1)]+new_finalflag_vals):
                if check_flags(ff, curr_flag[1]):
                    add_info_left.append(curr_flag[0].replace('\t','')) 
        else:
            add_info_left.append('NOT CLASSIFIED')

        #### add values to stuff printed on the right side of the plot ##### 
        add_info_right =[]
        try:
            for key in print_right.keys():
                if model in print_right[key][3]:
                    ts = print_right[key][2] %(gal_info[print_right[key][0]][model])
                    add_info_right.append(print_right[key][1].replace('MODEL', model) + ' = '+ ts)
        except Exception, inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to printed directly
            print "something bad happened!!!!\n\n"
            traceback.print_exc()
            print key
            print print_right[key][2]
            print gal_info[print_right[key][0]][model]

        print 'plotting'

        try:
            plot_galaxy_fit(save_name, two_d_ims['data_wide'], two_d_ims['data'], two_d_ims['model'],two_d_ims['resid'], d1_data, d1_max_rad,gal_info['hrad_corr'][model],one_percent_sky,full_sky, model, title ='%06d_%s_%s' %(gal_info['galcount'][model],band,model), add_info_left =add_info_left,add_info_right = add_info_right, label_string = label_string)
            print "Plotting complete!!!"
        except Exception, inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to printed directly
            print "something bad happened!!!!\n\n"
            traceback.print_exc()
            print "Plotting failed!!!"
    
    else:
        print "plot %s already exists!!!\nSkipping!!!!!" %save_name
