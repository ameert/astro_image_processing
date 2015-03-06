#!/data2/home/ameert/python/bin/python2.5

from regen_functions import *
import os
import sys

import numpy as np
import scipy as sc
import pyfits as pf
import pylab as pl
from gal_panel import *
import scipy.ndimage.filters as filters

this_dir = os.getcwd()

model = sys.argv[1]
folder_num = int(sys.argv[2])
band = 'r'

model = 'ser'
cursor = mysql_connect('pymorph','pymorph','pymorph9455','shredder')

cmd = """select x.galcount, z.Hrad_corr, z.BT, 
-2.5*log10(pow(10, -0.4*abs(z.Ie))+pow(10, -0.4*abs(z.Id))), z.zp,
z.SexHrad, z.num_targets, 
z.r_bulge, z.xctr_bulge, z.yctr_bulge, z.ba_bulge, 
z.xctr_bulge_err, z.yctr_bulge_err,
z.r_disk, z.xctr_disk, z.yctr_disk, z.ba_disk,
z.xctr_disk_err, z.yctr_disk_err 
from 
full_dr7_{band}_{model} as z,
CAST as x 
where 
z.galcount = x.galcount and
(z.galcount between ({fnum}-1)*250+1 and {fnum}*250 -1)
order by c.galcount;""".format(model = model, band = band)

data = cursor.get_data(cmd)

data = np.array([np.array(d) for d in data]).T

pos_dict = dict((a[1],a[0]) for a in enumerate(['galcount', 'hrad_corr', 'BT',
                                      'mag', 'zp', 'hrad_sex', 'num_targets',
                                      'r_bulge','x_bulge', 'y_bulge', 'ba_bulge',
                                      'x_bulge_err', 'y_bulge_err', 
                                      'r_disk','x_disk', 'y_disk','ba_disk',
                                      'x_disk_err', 'y_disk_err']))
              
for curr_gal in data:
    print curr_gal
    continue
    gc = int(curr_gal[pos_dict['galcount']])
    newflag = 0
    tot_counts = 10.0**(-0.4*(curr_gal[pos_dict['mag']] - curr_gal[pos_dict['zp']]))
    filepath = '/home/ameert/to_classify/data/r'
    
    ofile = '%s/O_r_%08d_r_stamp_%s.fits' %(filepath, gc, model)
    mfile = '%s/EM_r_%08d_r_stamp.fits' %(filepath, gc)
    wfile = '%s/%08d_r_stamp_W.fits' %(filepath, gc)
        
    if os.path.isfile(ofile):
        galim = pf.open(ofile)
        data = galim[1].data
        resid = galim[3].data
        galprof = galim[4].data# + galim[5].data
        bulgeprof = galim[4].data
        diskprof = np.zeros_like(bulgeprof)#galim[5].data
        galim.close()

        galim = pf.open(mfile)
        mask = np.where(galim[0].data<0.5, 1.0, 0.0)
        galim.close()

        galim = pf.open(wfile)
        weight = galim[0].data
        galim.close()

        fit_center_x =  (curr_gal[pos_dict['x_bulge']]* curr_gal[pos_dict['BT']]
            + curr_gal[pos_dict['x_disk']]*(1.0- curr_gal[pos_dict['BT']]))

        fit_center_y =  (curr_gal[pos_dict['y_bulge']]* curr_gal[pos_dict['BT']]
            + curr_gal[pos_dict['y_disk']]*(1.0- curr_gal[pos_dict['BT']]))
        
        im_center_y = galprof.shape[0]/2.0
        im_center_x = galprof.shape[1]/2.0
        
        separation = np.sqrt((fit_center_x-im_center_x)**2.0 + (fit_center_y-im_center_y)**2.0)
        if curr_gal[pos_dict['num_targets']]>1:
            max_sep = 2.0
        else:
            max_sep = 3.5

        if separation > max_sep:
            print 'galcount ', gc, ' centering is bad!!! ', separation 
            newflag +=2

        if curr_gal[pos_dict['r_bulge']] > 10.0*curr_gal[pos_dict['hrad_sex']]:
            if curr_gal[pos_dict['BT']]<0.05:
                print 'galcount ', gc, 'No bulge?!!! '
            else:
                if curr_gal[pos_dict['ba_bulge']]>0.5:
                    print 'galcount ', gc, ' bulge is sky?!!! ', curr_gal[pos_dict['hrad_sex']],curr_gal[pos_dict['r_bulge']]
                    newflag +=4
                else:
                    print 'galcount ', gc, ' edge on disk effect?!!! ', curr_gal[pos_dict['hrad_sex']],curr_gal[pos_dict['r_bulge']]
                    newflag +=8

        if curr_gal[pos_dict['r_disk']] > 10.0*curr_gal[pos_dict['hrad_sex']]:
            print 'galcount ', gc, ' disk is sky?!!! ', curr_gal[pos_dict['hrad_sex']],curr_gal[pos_dict['r_disk']]
            newflag +=4
        rads, cum_profs = chi_profs(bulgeprof.copy(), diskprof.copy(), mask.copy(), 
                                    weight.copy(), resid.copy(), curr_gal[pos_dict['hrad_corr']], 
                                    smoothed = True, smooth_scale = 2.0)
        new_cum_profs = filters.gaussian_filter(cum_profs, 5)

        #pl.plot(rads, cum_profs, 'b-')
        #pl.plot(rads, new_cum_profs, 'g-')
        #pl.show()
        chi_val = (rads[9], new_cum_profs[9])

        if chi_val[1] > 7.5:
            #print "galcount ", gc, ' bad chi?!!! ', chi_val[1]
            #newflag +=16
            pass
        if newflag > 0:
            newflag +=1

        cmd = "update catalog.Flags_optimize set flag = %d where galcount = %d and band = 'r' and model = '%s' and ftype = 't';" %(newflag, gc, model)
        print cmd
        cursor.execute(cmd)
