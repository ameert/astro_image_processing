#!/data2/home/ameert/python/bin/python2.5

from profile_to_arcsec_mag import *
from mysql.mysql_class import *
import sys 
import os
import numpy as np
from scipy import interpolate


bands = 'gr'
table_name = 'CAST'
dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'
lhost = ''

cursor = mysql_connect(dba, usr, pwd, lhost)

#folder_num = int(sys.argv[1])
galtype = sys.argv[1]
#inpath = '/home/ameert/color_grad/data/%04d' %folder_num
outpath = '/home/ameert/Desktop/color_grad/data/9999'


#cmd = """select a.galcount, a.aa_g, a.aa_r, a.aa_i, a.kk_g, a.kk_r, a.kk_i,a.airmass_g, a.airmass_r, a.airmass_i, a.extinction_g, a.extinction_r,a.extinction_i, d.kcorr_g, d.kcorr_r, d.kcorr_i from CAST as a, DERT as d where a.galcount = d.galcount  and a.galcount between %d and %d order by galcount;""" %((folder_num-1)*250, folder_num*250)

#data = cursor.get_data(cmd)
galcount = np.loadtxt('grads_%s.txt' %galtype, usecols=[0], skiprows=1, unpack=True)

galcount = galcount.astype(int)

#data = np.array(data).T

dat_keys = {'galcount':0, 'aa_g':1, 'aa_r':2, 'aa_i':3, 'kk_g':4, 'kk_r':5, 
            'kk_i':6,'airmass_g':7, 'airmass_r':8, 'airmass_i':9, 
            'extinction_g':10,'extinction_r':11,'extinction_i':12, 
            'kcorr_g':13, 'kcorr_r':14, 'kcorr_i':15}

profiles = {bands[0]:{}, bands[1]:{}, bands:[]}

for model in ['data','ser']:
    #for row in data:
    for gc in galcount:
        cmd = """select a.galcount, a.aa_g, a.aa_r, a.aa_i, a.kk_g, a.kk_r, a.kk_i,a.airmass_g, a.airmass_r, a.airmass_i, a.extinction_g, a.extinction_r,a.extinction_i, d.kcorr_g, d.kcorr_r, d.kcorr_i from CAST as a, DERT as d
    where a.galcount = d.galcount  and
    a.galcount = %d;""" %(gc)

        row = cursor.get_data(cmd)
        row = np.array(row).T[0,:]

        gc = int(row[dat_keys['galcount']])
    #    inpath = '/home/ameert/color_grad/%08d' %gc 
        inpath = '/home/ameert/Desktop/color_grad/data/9999' 

        try:
            for im_d in bands:
                for im_f in bands:
                    if im_d == im_f:
                        infile = '%s/%08d_%s_%s.npz' %(inpath,gc,im_d, model )
                    else:
                        infile = '%s/%08d_%s_%s_%s.npz' %(inpath,gc,im_d, im_f,model)

                    profiles[im_d][im_f] = profile_to_arcsec_mag(
                                                 row[dat_keys['aa_'+im_d]], 
                                                 row[dat_keys['kk_'+im_d]], 
                                                 row[dat_keys['airmass_'+im_d]], 
                                                 im_d, infile, 
                                    extinction = row[dat_keys['extinction_'+im_d]],
                                    kcorr = row[dat_keys['kcorr_'+im_d]])


            outfile = '%s/%08d_mag_corr_%s.npz' %(outpath,gc,model )

            profiles[bands] = [np.log10(profiles[bands[0]][bands[0]][0]),profiles[bands[0]][bands[1]][1]-profiles[bands[1]][bands[0]][1],np.sqrt(profiles[bands[0]][bands[1]][2]**2 + profiles[bands[1]][bands[0]][2]**2)]

            print "writing npz file"
            data_names = ['log_rad_arcsec', 
                          bands[0],bands[0]+'err', 
                          bands[1],bands[1]+'err', 
                          bands,bands+'_err']

            data = dict([a for a in zip(data_names, 
                           [ np.log10(profiles[bands[0]][bands[0]][0]),
                             profiles[bands[0]][bands[0]][1], 
                             profiles[bands[0]][bands[0]][2],
                             profiles[bands[1]][bands[1]][1], 
                             profiles[bands[1]][bands[1]][2],
                             profiles[bands][1], profiles[bands][2]])])
            np.savez(outfile, **data)

        except IOError:
            print IOError

