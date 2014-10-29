import numpy as np
import numpy.random as rand
import scipy as sci
import pyfits as pf
import pylab as pl
import os
import sys
from scipy.stats.mstats import mquantiles
import matplotlib.cm as cm
import scipy.ndimage.filters as filters
import scipy.stats as stats
import scipy.interpolate as interp
from astro_image_processing.astro_utils.image_analysis import *
from astro_image_processing.statistics.bin_stats import *
import pickle

def BT_profs(bulge_prof, disk_prof, mask, weight, resid, hrad, 
            tot_light, smoothed = False, smooth_scale = 2.0):

    galprof = bulge_prof + disk_prof
    if smoothed:
        galprof = filters.gaussian_filter(galprof, smooth_scale)
        bulge_prof = filters.gaussian_filter(bulge_prof, smooth_scale)
        disk_prof = filters.gaussian_filter(disk_prof, smooth_scale)
    
    new_mask = np.where(galprof > np.max(galprof)/100.0, 1,0)
    galprof = image_info(galprof, mask = new_mask)# no mask needed since image is clean
    
    print 'stats'
    print galprof.x_ctr, galprof.y_ctr, galprof.ba, galprof.pa
    profile = image_info(bulge_prof, mask = mask, x_ctr = galprof.x_ctr, 
                         y_ctr = galprof.y_ctr, ell = galprof.ba, 
                         pa= galprof.pa )
    profile2 = image_info((bulge_prof+disk_prof), mask = mask, 
                          x_ctr = galprof.x_ctr, y_ctr = galprof.y_ctr, 
                          ell = galprof.ba, pa= galprof.pa )
    profile.profile()
    profile2.profile()
    
    cum_prof = np.array(profile.aperflux)/np.array(profile2.aperflux)
    cum_rad =  np.array(profile.rads)*0.396/hrad
    light_prof = np.array(profile2.aperflux)/tot_light

    cum_prof = np.extract(cum_rad > 0, cum_prof)
    light_prof = np.extract(cum_rad > 0, light_prof)
    cum_rad =  np.extract(cum_rad > 0, cum_rad)
    
    profile = image_info(bulge_prof/(bulge_prof+disk_prof), mask = mask, x_ctr = galprof.x_ctr, y_ctr = galprof.y_ctr, ell = galprof.ba, pa= galprof.pa )
    profile.profile()
    profs = np.array(profile.prof)
    profs = np.where(np.isnan(profile.prof),0, profile.prof)
    rads = np.array(profile.rads)*0.396/hrad

#    print rads
#    print profs

    profs = np.extract(rads > 0, profs)
    rads = np.extract(rads > 0, rads)

#    print rads
#    print profs

    x = np.arange(0.1, 6.0,0.1)
    s = interp.InterpolatedUnivariateSpline(rads,profs)
    bt_r = s(x)

    s = interp.InterpolatedUnivariateSpline(cum_rad,cum_prof)
    bt_in = s(x)
    
    s = interp.InterpolatedUnivariateSpline(cum_rad,light_prof)
    light_in = s(x)
        
    return x, bt_r, bt_in, light_in

def chi_profs(bulge_prof, disk_prof, mask, weight, resid, hrad, 
              smoothed = False, smooth_scale = 2.0):
    galprof = bulge_prof + disk_prof
    if smoothed:
        resid = filters.gaussian_filter(resid**2, smooth_scale)
        weight = filters.gaussian_filter(weight**2, smooth_scale)
    else:
        resid = resid**2
        weight = weight**2

        
    new_mask = np.where(galprof > np.max(galprof)/100.0, 1,0)    
    galprof = image_info(galprof, mask=new_mask)
    profile = image_info(resid/weight, mask = mask, x_ctr = galprof.x_ctr, y_ctr = galprof.y_ctr, ell = galprof.ba, pa= galprof.pa, zoom =-1 )
    profile.profile()

    rads = np.array(profile.rads)*0.396/hrad
    profs = np.array(profile.prof)
    cum_profs = np.array(profile.aperflux)/np.array(profile.included_pix)
    
    cum_profs = np.extract(rads>0, cum_profs)
    profs = np.extract(rads>0, profs)
    rads = np.extract(rads>0, rads)

    x = np.arange(0.1, 4.0,0.1)
    s = interp.InterpolatedUnivariateSpline(rads,cum_profs)
    ynew = s(x)
    
    return x, ynew 


def flag_profs(folder_num, data, model):
    new_data={'galcount':data['galcount'],
             'im_ctr': [],'chi_prof':[],'bt_prof':[]}
    print data.keys()
    for pos_count, curr_gal in enumerate(new_data['galcount']):
        print "curr gal ", curr_gal
        #if curr_gal < 88620:
        #    continue
        if os.path.isfile(data['dfile'][pos_count]):
            print "reading dfile ",data['dfile'][pos_count]
            galim = pf.open(data['dfile'][pos_count])
            galdata = galim[0].data
            galim.close()
            new_data['im_ctr'].append([galdata.shape[1]/2.0, galdata.shape[0]/2.0])
        else:
            new_data['im_ctr'].append([-999.0, -999.0])
            print "im not found!!!"
        if os.path.isfile(data['ofile'][pos_count]):
            try:
                try:
                    print pos_count
                    print data['ofile'][pos_count]
                    print len(galim)
                    galim = pf.open(data['ofile'][pos_count])

                    galdata = galim[1].data

                    resid = galim[3].data
                    if model in ['devexp','serexp']:
                        galprof = galim[4].data + galim[5].data
                        bulgeprof = galim[4].data
                        diskprof = galim[5].data #np.zeros_like(bulgeprof)
                    elif model in ['dev','ser']:
                        galprof = galim[4].data
                        bulgeprof = galim[4].data
                        diskprof = np.zeros_like(bulgeprof)

                    galim.close()

                    galim = pf.open(data['mfile'][pos_count])
                    mask = np.where(galim[0].data<0.5, 1.0, 0.0)
                    galim.close()

                    galim = pf.open(data['wfile'][pos_count])
                    weight = galim[0].data
                    galim.close()
                    #print 'resid'
                    #print resid
                    #print 'weight'
                    #print weight
                    #print 'chi'
                    #print resid/weight
                    #print np.max(resid/weight)
                    try:
                        rads, cum_profs = chi_profs(bulgeprof.copy(), diskprof.copy(), 
                                                    mask.copy(), weight.copy(), 
                                                    resid.copy(), data['r_tot'][pos_count],
                                                    smoothed = True, smooth_scale = 2.0)
                        print rads, cum_profs
                    except:
                        print "help chi_profs"
                        print "hrad ",data['r_tot'][pos_count]
                        rads = np.array([-999.0])
                        cum_profs = np.array([-999.0])

                    try:
                        bt_rads, bt_r, bt_in, light_in = BT_profs(bulgeprof.copy(), 
                                                                  diskprof.copy(), mask.copy(),
                                                                  weight.copy(), resid.copy(), 
                                                                  data['r_tot'][pos_count],
                                                                  data['tot_counts'][pos_count],
                                                                  smoothed = False, smooth_scale = 2.0)
                    except:
                        print "help bt_profs"
                        print "hrad ",data['r_tot'][pos_count]
                        print "tot_counts ",data['tot_counts'][pos_count]
                        bt_rads = np.array([-999.0])
                        bt_r = np.array([-999.0])
                        bt_in = np.array([-999.0])
                        light_in = np.array([-999.0])
                except IndexError:
                    rads = np.array([-999.0])
                    cum_profs = np.array([-999.0])
                    bt_rads = np.array([-999.0])
                    bt_r = np.array([-999.0])
                    bt_in = np.array([-999.0])
                    light_in = np.array([-999.0])
                    print "Index fits error!!!"
            except IOError:
                rads = np.array([-999.0])
                cum_profs = np.array([-999.0])
                bt_rads = np.array([-999.0])
                bt_r = np.array([-999.0])
                bt_in = np.array([-999.0])
                light_in = np.array([-999.0])
                print "IO fits error!!!"

        else:
            print "Ofile "+data['ofile'][pos_count]+" not found!!!!"
            rads = np.array([-999.0])
            cum_profs = np.array([-999.0])
            bt_rads = np.array([-999.0])
            bt_r = np.array([-999.0])
            bt_in = np.array([-999.0])
            light_in = np.array([-999.0])


        new_data['chi_prof'].append((rads,cum_profs))
        new_data['bt_prof'].append((bt_rads, bt_r, bt_in, light_in))



    outfile = open(data['outfile'], 'w')
    pickle.dump(new_data, outfile)
    outfile.close()
    return


