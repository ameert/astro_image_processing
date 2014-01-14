#++++++++++++++++++++++++++
#
# TITLE: plot_all 
#
# PURPOSE: allows us to view the
#          original data, the fit
#          and the residual in 1 and 2 d.
#
# INPUTS: NONE
#
# OUTPUTS: NONE??
#
# PROGRAM CALLS: NONE??
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 8 FEB 2011
#
# NOTE:  
#-----------------------------------

import random as r
from mysql_connect import *
from plot_2d_components import *
from sql_query import *
from plot_1d_fit import *
from galaxy_class import *
from galmorph_make_image import *
import sys
import time

   
two_d = 0

times = 9
old = 0
fixed = 0

seed = 36#5#3#36#5
r.seed(seed)

et = 53.907456
pix_sz = 0.396
dba = 'sdss_sample'
usr = 'pymorph'
pwd = 'pymorph'
models = ['Ser','Dev','SerExp','DevExp']
path_root = {'Ser':'/media/BACKUP/sdss_sample/fits/1_ser/',
             'Dev':'/media/BACKUP/sdss_sample/fits/1_dev/',
             'SerExp':'/media/BACKUP/sdss_sample/fits/1_serexp/',
             'DevExp':'/media/BACKUP/sdss_sample/fits/1_devexp/'}
             
path_main_data = '/home/ameert/sdss_sample/cutouts/r/'
save_path = '/home/ameert/profile_plotting/plots/'

cursor = mysql_connect(dba,usr,pwd)
f = open('fit_values.txt', 'w')
f.write( 'Inforamtion for examined fits\n')
f.write( 'Object Number\n')
f.write('(g$_{dev}$, g$_{ser}$, g$_{devexp}$, g$_{serexp}$, res$_{dev}$, res$_{ser}$, res$_{devexp}$, res$_{serexp}$, $\chi^2_{dev}$, $\chi^2_{ser}$, $\chi^2_{devexp}$, $\chi^2_{serexp}$, n$_{ser}$, n$_{serexp}$, BT$_{devexp}$, BT$_{serexp}$, re$_{dev}$, re$_{ser}$, re$_{devexp}$, re$_{serexp}$, re$_{devexp}$/rd$_{devexp}$, re$_{serexp}$/rd$_{serexp}$, sky$_{dev}$, sky$_{ser}$, sky$_{devexp}$, sky$_{serexp}$)' +'\n')

all_numbers = []

#cmd = 'select galcount from r_full where BT_DevExp < .4 and BT_DevExp > .2 and re_pix_DevExp/rd_pix_DevExp > .5 and fit_DevExp = 1  and fit_Ser = 1 and galcount <3000;'  
#cmd = 'select galcount from r_full where galcount = 2 or galcount = 4 or galcount = 135;'
cmd = 'select galcount from r_full where galcount < 4000;'
cursor.execute(cmd)
rows = cursor.fetchall()
rows = list(rows)
number_list = []
for row in rows:
    number_list.append(row[0])

for count in range(times):
    while 1:
        number = r.choice([338,670,940,945,1184,2445,2599,3947,3997])#number_list)#r.randrange(1,4000)
        
        if number not in all_numbers: # and number not in [2112, 1918, 1949, 674, 1671,1184, 11,2073,2510, 2673]:
            all_numbers.append(number)
            break
    #number = 3309#813#3837
    if count > -1: #217
        try:
            print "count is: %d\n" %(count)
            print "galaxy is %d\n" %(number)
            time.sleep(5)
            d1_rad = []
            d1_flux = []
            d1_styles = []
            d1_labels = []
            d1_error = []
            d1_rad_resid = [] 
            d1_flux_resid = []
            d1_styles_resid = []
            d1_labels_resid = []
            d1_labels_resid = []

            for model_type in models:


                profile_data = {}
                profile_model = {}
                profile_nyc = {}

                cmd = sql_query(model_type, number,1)
                cursor.execute(cmd)
                rows_new = cursor.fetchall()
                rows_new = list(rows_new)
                #f.write(str(rows_new[0])+'\n')
                Name_r = str(rows_new[0][0])
                galcount = int(rows_new[0][1])
                n_model = float(rows_new[0][2])
                re_pix_model= float(rows_new[0][3])
                Ie_model= float(rows_new[0][4])
                eb_model= float(rows_new[0][5])
                rd_pix_model= float(rows_new[0][6])
                Id_model= float(rows_new[0][7])
                ed_model= float(rows_new[0][8])
                BT_model= float(rows_new[0][9])
                GalSky_model= float(rows_new[0][10])
                chi2nu_model= float(rows_new[0][11])
                fit_model= float(rows_new[0][12])
                probaE= float(rows_new[0][13])
                zeropoint_pymorph= float(rows_new[0][14])
                zeropoint_sdss_r= float(rows_new[0][15])
                kk_r= float(rows_new[0][16])
                airmass_r = float(rows_new[0][17])
                petroR50_r = float(rows_new[0][18]) # in pixels
                bpa_model = float(rows_new[0][19])+90.0
                dpa_model = float(rows_new[0][20])+90.0
                xctr_bulge = float(rows_new[0][21])
                yctr_bulge = float(rows_new[0][22])
                xctr_disk = float(rows_new[0][23])
                yctr_disk = float(rows_new[0][24])
                shift_sky = float(rows_new[0][25])
                print shift_sky
                if model_type == 'Ser':
                    n_sersic = n_model
                    re_ser = re_pix_model
                    chi_ser = chi2nu_model
                    galsky_ser = GalSky_model
                elif model_type == 'SerExp':
                    n_serexp = n_model
                    re_serexp = re_pix_model
                    rd_serexp = rd_pix_model
                    BT_serexp = BT_model
                    chi_serexp = chi2nu_model
                    galsky_serexp = GalSky_model
                elif model_type == 'Dev':
                    re_dev = re_pix_model
                    chi_dev = chi2nu_model
                    galsky_dev = GalSky_model
                elif model_type == 'DevExp':
                    re_devexp = re_pix_model
                    rd_devexp = rd_pix_model
                    BT_devexp = BT_model
                    galsky_devexp = GalSky_model


                print 'finding best fit'

                best_fit = galaxy(path_main_data, path_root[model_type], Name_r, number,model_type, Ie_model, re_pix_model, eb_model,bpa_model, n_model, Id_model, rd_pix_model, ed_model,dpa_model,BT_model, xctr_bulge, yctr_bulge, xctr_disk, yctr_disk, petroR50_r, zeropoint_sdss_r,  kk_r, airmass_r, GalSky_model)#zeropoint_pymorph
                print 'best fit initialized'
                best_fit.read_images()
                print 'images read'
                best_fit.make_sim_sum()
                print 'sums taken'
                best_fit.get_main_profiles()
                print 'profiles found'
                print "goodness = ", best_fit.calc_goodness()
                #f.write(str(number)+' '+ model_type +' '+
                #        str(best_fit.goodness)+ ' '+ str(fit_model) +'\n')
                if model_type == 'Ser':
                    good_ser = best_fit.goodness
                elif model_type == 'SerExp':
                    good_serexp = best_fit.goodness
                elif model_type == 'Dev':
                    good_dev = best_fit.goodness
                elif model_type == 'DevExp':
                    good_devexp = best_fit.goodness



                # Now shift galaxy profiles for plotting
                if model_type != 'DevExp':
                    shift_sky = shift_sky * et
                else:
                    shift_sky = 0
                best_fit.get_component_prof(shift_counts = shift_sky)        

                print best_fit.profile_sim_all['dat']
                if model_type in ['DevExp' ,'SerExp']:
                    print model_type
                    print best_fit.profile_bulge['dat']
                    print best_fit.profile_disk['dat']
                    print best_fit.profile_sim_all

                    
                # Now correct bulge and disk components to ensure the
                # shift doesn't make the profiles incorrect            
                
                #if model_type == "SerExp":
                #    max_len = len(best_fit.profile_sim_all['dat'])
                #    if len(best_fit.profile_bulge['dat']) > max_len:
                #        for keys in best_fit.profile_bulge.keys():
                #            best_fit.profile_bulge[keys]=best_fit.profile_bulge[keys][0:max_len + 1]
                #        if len(best_fit.profile_disk['dat']) > max_len:
                #            for keys in best_fit.profile_disk.keys():
                #                best_fit.profile_disk[keys]=best_fit.profile_disk[keys][0:max_len + 1]
                        
                #        for total, bulge, disk in zip(best_fit.profile_sim_all['dat'], best_fit.profile_bulge['dat'],best_fit.profile_disk['dat']):


                
                # nyc profile
                if model_type == 'Ser':
                    ## cmd = sql_query(model_type, number,3)
                    # #                     cursor.execute(cmd)
                    # #                     rows_nyu = cursor.fetchall()
                    # #                     rows_nyu = list(rows_nyu)
                    # #                     #f.write(str(rows_nyu[0])+'\n')
                    # #                     ny_n = float(rows_nyu[0][4])
                    # #                     ny_r = float(rows_nyu[0][3])
                    # #                     ny_a = float(rows_nyu[0][2])
                    
                    # #                     ny_tot = n.pi * ny_a * (ny_r **2) * gamma(2.0 * ny_n + 1)
                    # #                     ny_mag = 22.5 - 2.5 * n.log10(ny_tot) #mag per sq. arcsec
                    # #                     ny_Re = ((1.9992 * ny_n - 0.3271) ** ny_n ) * ny_r/pix_sz
                    # #                     ny_counts = mag_to_counts(ny_mag, -1.0 * zeropoint_sdss_r, kk_r, airmass_r)
                    
                    # #                     best_fit.sersic(ny_counts,ny_Re, ny_n)
                    # #                     best_fit.get_nyu_prof()
                    
                    # #                     nyc_resid =best_fit.nyu_resid 
                    # #                    nyc_res_rad = best_fit.nyu_res_rad

                    mod_resid = best_fit.fit_resid
                    mod_res_rad = best_fit.fit_res_rad

                # this builds the labels for the composite plot

                if model_type == 'DevExp':
                    d1_rad.append( best_fit.profile_pymodel['rad'])
                    d1_flux.append( best_fit.profile_pymodel['dat'])
                    d1_styles.append('b-')
                    d1_error.append( best_fit.profile_pymodel['daterr'])
                    d1_labels.append(model_type + ' fit')
                    d1_rad_resid.append(best_fit.fit_res_rad) 
                    d1_flux_resid.append(best_fit.fit_resid)
                    d1_styles_resid.append('b-')
                    d1_labels_resid.append(model_type + ' fit')

                else:
                    d1_rad.append(best_fit.profile_sim_all['rad'])
                    d1_flux.append(best_fit.profile_sim_all['dat'])
                    d1_error.append( best_fit.profile_sim_all['daterr'])
                    d1_labels.append(model_type + ' fit')
                    d1_labels_resid.append(model_type + ' fit')
                    d1_rad_resid.append(best_fit.fit_res_rad) 
                    d1_flux_resid.append(best_fit.fit_resid)
                    if model_type == 'Ser':
                        d1_styles.append('m-')
                        d1_styles_resid.append('m-')
                    elif model_type == 'Dev':
                        d1_styles.append('g-')
                        d1_styles_resid.append('g-')
                    elif model_type == 'SerExp':
                        d1_styles.append('r-')
                        d1_styles_resid.append('r-')

                    

                #print best_fit.profile_data['rad']
                #print best_fit.profile_data['dat']
                #print best_fit.profile_pymodel['rad']
                #print best_fit.profile_pymodel['dat']
                #print model_type + ' fit'
                #print model_type + ' fit'
                #print mod_res_rad 
                #print mod_resid

                #raw_input("Hit Enter")

                #if model_type == 'Ser':
                #    d1_rad.append(best_fit.profile_nyu_mag['rad'])
                #    d1_flux.append(best_fit.profile_nyu_mag['dat'])
                #    d1_styles.append('y-')
                #    d1_labels.append('nyu sersic fit')
                #    d1_rad_resid.append(nyc_res_rad) 
                #    d1_flux_resid.append(nyc_resid)
                #    d1_styles_resid.append('y-')
                #    d1_labels_resid.append('nyu sersic fit')

                if model_type == 'DevExp' or model_type == 'SerExp':

                    d1_rad.append(best_fit.profile_bulge['rad'])
                    d1_flux.append(best_fit.profile_bulge['dat'])
                    d1_error.append( best_fit.profile_bulge['daterr'])
                    d1_rad.append(best_fit.profile_disk['rad'])
                    d1_flux.append(best_fit.profile_disk['dat'])
                    d1_error.append( best_fit.profile_disk['daterr'])

                    if model_type == 'DevExp':
                        d1_styles.append('b--')
                        d1_labels.append('DevExp bulge')

                        d1_styles.append('b:')
                        d1_labels.append('DevExp disk')

                    else: 
                        d1_styles.append('r--')
                        d1_labels.append('SerExp bulge')

                        d1_styles.append('r:')
                        d1_labels.append('SerExp disk')

                if model_type == 'DevExp':
                    d1_rad.append(  best_fit.profile_data['rad'])
                    d1_flux.append( best_fit.profile_data['dat'])
                    d1_styles.append('k.')
                    d1_error.append( best_fit.profile_data['daterr'])
                    d1_labels.append('data')

                d1_max_rad = petroR50_r * 4.0 *0.396

                # Calculate a few other statistics
                if model_type == 'Dev':
                    res_dev = n.extract(best_fit.fit_res_rad < d1_max_rad, best_fit.fit_resid)
                    res_dev = n.sum(res_dev**2)
                elif model_type == 'Ser':
                    res_ser = n.extract(best_fit.fit_res_rad < d1_max_rad, best_fit.fit_resid)
                    res_ser = n.sum(res_ser**2)
                    pass
                elif model_type == 'DevExp':
                    res_devexp = n.extract(best_fit.fit_res_rad < d1_max_rad, best_fit.fit_resid)
                    res_devexp = n.sum(res_devexp**2)
                    pass
                elif model_type == 'SerExp':
                    res_serexp = n.extract(best_fit.fit_res_rad < d1_max_rad, best_fit.fit_resid)
                    res_serexp = n.sum(res_serexp**2)
                    
                


                # convert 2d plots to surf_brightness

                twod_data_mag = co_pix_to_mag_arc(best_fit.data_fits,-1.0 * zeropoint_sdss_r, kk_r,airmass_r)
                twod_model_mag = co_pix_to_mag_arc(best_fit.model_fits,-1.0 * zeropoint_sdss_r, kk_r,airmass_r)
                if model_type in ['DevExp', 'SerExp']:
                    twod_component_mag = co_pix_to_mag_arc(best_fit.bulge_im + best_fit.disk_im +  best_fit.sky_im ,-1.0 * zeropoint_sdss_r, kk_r,airmass_r)
                else:
                    twod_component_mag = co_pix_to_mag_arc(best_fit.bulge_im + best_fit.sky_im ,-1.0 * zeropoint_sdss_r, kk_r,airmass_r)

                twod_resid_mag = (twod_model_mag - twod_data_mag) 
                one_percent_sky = GalSky_model * 53.907456/100.0
                one_percent_sky = co_pix_to_mag_arc(one_percent_sky,-1.0 * zeropoint_sdss_r, kk_r,airmass_r)
                full_sky = GalSky_model * 53.907456
                full_sky = co_pix_to_mag_arc(full_sky,-1.0 * zeropoint_sdss_r, kk_r,airmass_r)
                #print 'sky ', full_sky
                #print GalSky_model*53.907456

                if model_type == 'SerExp':
                    twod_data_mag_serexp=twod_data_mag
                    twod_model_mag_serexp=twod_model_mag
                    twod_resid_mag_serexp =twod_resid_mag 
                    one_percent_sky_serexp = one_percent_sky
                    full_sky_serexp = full_sky

                
                if model_type == 'Ser':
                    pass
                    #junk = ' (n %4.3f,re %4.3f,nyu n %4.3f,nyu re %4.3f,R50 %4.3f)' %(n_model,re_pix_model*0.396, ny_n, ny_Re*pix_sz, petroR50_r)

                elif model_type == 'DevExp':
                    label_string = 'Note: The 1d data is calculated using background-subtracted data. The 2d data is shown with background included.' 
                    # junk = ' (n_dev %3.2f, n_ser %3.2f, re %3.2f, re_ser %3.2f, BT %3.2f, re/rd %3.2f, R50 %3.2f)' %( n_model,n_sersic,re_pix_model*0.396,re_pix_sersic * 0.396,BT_model,re_pix_model/rd_pix_model, petroR50_r)
                    junk1 = '(%4.3f, %4.3f, %4.3f, %4.3f,%4.3f, %4.3f, %4.3f, %4.3f,%4.3f, %4.3f, %4.3f, %4.3f, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f)' %(good_dev,good_ser, good_devexp,good_serexp,res_dev,res_ser,res_devexp,res_serexp, chi_dev,chi_ser, chi2nu_model,chi_serexp, n_sersic, n_serexp, BT_devexp, BT_serexp, re_dev*0.396,re_ser*0.396,re_devexp*0.396,re_serexp*0.396,re_devexp/rd_devexp, re_serexp/rd_serexp,galsky_dev,galsky_ser,galsky_devexp,galsky_serexp)
                    junk_names = '(g$_{dev}$, g$_{ser}$, g$_{devexp}$, g$_{serexp}$, res$_{dev}$, res$_{ser}$, res$_{devexp}$, res$_{serexp}$, $\chi^2_{dev}$, $\chi^2_{ser}$, $\chi^2_{devexp}$, $\chi^2_{serexp}$, n$_{ser}$, n$_{serexp}$, BT$_{devexp}$, BT$_{serexp}$, re$_{dev}$, re$_{ser}$, re$_{devexp}$, re$_{serexp}$, re$_{devexp}$/rd$_{devexp}$, re$_{serexp}$/rd$_{serexp}$, sky$_{dev}$, sky$_{ser}$, sky$_{devexp}$, sky$_{serexp}$)' 
                    f.write(str(number)+' '+ model_type +' '+junk1 +'\n')
                
                else:
                    pass
                    junk = '(%3.2f, %3.2f, %3.2f)' %( n_model,re_pix_model*0.396, petroR50_r)

                if two_d == 1:
                    print 'plotting'
                    plot_2d_components(save_path, number, model_type, '%06d %s ' %(number,model_type), twod_data_mag, twod_model_mag, twod_resid_mag, twod_component_mag, add_string = '$\chi^2$ = %4.3f' %(chi2nu_model))
                    print 'done plotting'
                elif two_d == 0 and model_type == 'DevExp':
                    print 'plotting'
                    plot_galaxy_fit('%s%06d_fits_1d_%s.png' %(save_path, number,model_type),twod_data_mag, twod_model_mag, twod_resid_mag,best_fit.mask_image, d1_rad, d1_flux, d1_error, d1_styles, d1_labels, d1_rad_resid, d1_flux_resid, d1_styles_resid, d1_labels_resid, d1_max_rad,one_percent_sky,full_sky, '%06d_r_%s' %(number,model_type), junk1, junk_names, label_string)
#                    plot_galaxy_fit('%s%06d_fits_1d_%s.png' %(save_path, number,'SerExp'),twod_data_mag_serexp, twod_model_mag_serexp, twod_resid_mag_serexp, best_fit.mask_image,d1_rad, d1_flux, d1_error, d1_styles, d1_labels, d1_rad_resid, d1_flux_resid, d1_styles_resid, d1_labels_resid, d1_max_rad,one_percent_sky_serexp,full_sky_serexp,'%06d_r_%s' %(number,'SerExp'), junk1, junk_names, label_string)

                    # print '\nrad\n',d1_rad,'\nflux\n', d1_flux,'\nstyle\n', d1_styles, '\nlabels\n', d1_labels, '\nrad_resid\n',d1_rad_resid,'\nflux_resid\n', d1_flux_resid,'\nstyles_resid\n', d1_styles_resid,'\nlabels_resid\n', d1_labels_resid
                    print 'done plotting'
        except:
            print "something bad happened!!!!\n\n"
        #    time.sleep(5)
            
f.close()
cursor.close()
