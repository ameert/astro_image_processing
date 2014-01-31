#!/data2/home/ameert/python/bin/python2.5


from profile_to_arcsec_mag import *
from mysql_class import *
import sys 
import os
import numpy as np
from scipy import interpolate

bands = 'gri'
table_name = 'CAST'
dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'
lhost = ''

cursor = mysql_connect(dba, usr, pwd, lhost)

folder_num = int(sys.argv[1])
path = '/home/ameert/color_grad/data/%04d' %folder_num
model = 'ser'

cmd = """select a.galcount, a.aa_g, a.aa_r, a.aa_i, a.kk_g, a.kk_r, a.kk_i,a.airmass_g, a.airmass_r, a.airmass_i, a.extinction_g, a.extinction_r,a.extinction_i, d.kcorr_g, d.kcorr_r, d.kcorr_i, x.r50_r_arcsec,x.r90_r_arcsec from CAST as a, DERT as d ,%s_hrad_90_est as x
where a.galcount = x.galcount and  a.galcount = d.galcount  and
a.galcount between %d and %d order by galcount;""" %(model, (folder_num-1)*250, folder_num*250)

data = cursor.get_data(cmd)

galcount = np.array(data[0], dtype = int)
profiles = {'g':{}, 'r':{}, 'i':{}, 'gr':[], 'gi':[], 'ri':[] }

for gc, dat in zip(galcount,np.array(data[1:]).transpose()):
    try:
        for im_d in [0,1,2]:
            for im_f in [0,1,2]:
                if im_d == im_f:
                    infile = '%s/%08d_%s_%s.npz' %(path,gc,bands[im_d], model )
                    outfile = '%s/%08d_%s_%s_mag_corr.npz' %(path,gc,bands[im_d],model )
                else:
                    infile = '%s/%08d_%s_%s_%s.npz' %(path,gc,bands[im_d], bands[im_f],model)
                    outfile = '%s/%08d_%s_%s_mag_corr_%s.npz' %(path,gc,bands[im_d], bands[im_f],model )

                profiles[bands[im_d]][bands[im_f]] = profile_to_arcsec_mag(dat[0+im_d], dat[3+im_d], dat[6+im_d], bands[im_d], infile, extinction = dat[9+im_d],kcorr = dat[12+im_d])

        for color in ['gr', 'gi', 'ri']:
            profiles[color] = [profiles[color[0]][color[0]][0],profiles[color[0]][color[1]][1]-profiles[color[1]][color[0]][1],np.sqrt(profiles[color[0]][color[1]][2]**2 + profiles[color[1]][color[0]][2]**2)]

        
        print "writing npz file"
        data_names = ['log_rad_arcsec', 
                      'g','gerr', 
                      'r','rerr', 
                      'i','ierr',
                      'gr', 'gr_err', 
                      'gi', 'gi_err', 
                      'ri', 'ri_err' ]
        data = dict([a for a in zip(data_names, 
                       [ np.log10(profiles[color[0]][color[0]][0]),
                       profiles['g']['g'][1], profiles['g']['g'][2],
                       profiles['r']['r'][1], profiles['r']['r'][2],
                       profiles['i']['i'][1], profiles['i']['i'][2],
                       profiles['gr'][1], profiles['gr'][2],
                       profiles['gi'][1], profiles['gi'][2],
                       profiles['ri'][1], profiles['ri'][2]])])
        np.savez(outfile, **data)

    except IOError:
        print IOError

