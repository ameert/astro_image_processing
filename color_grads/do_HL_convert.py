#!/data2/home/ameert/python/bin/python2.5

from profile_to_arcsec_mag import *
from mysql_class import *
import sys 
import os
import numpy as np
from scipy import interpolate

bands = 'gri'
table_name = 'CAST'
dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
model = 'ser'
cursor = mysql_connect(dba, usr, pwd, 'shredder')

folder_num = int(sys.argv[1])
path = '/home/ameert/color_grads/data/%04d' %folder_num

cmd = """select a.galcount, a.aa_g, a.aa_r, a.aa_i, a.kk_g, a.kk_r, a.kk_i,a.airmass_g, a.airmass_r, a.airmass_i, a.extinction_g, a.extinction_r,a.extinction_i, d.kcorr_g, d.kcorr_r, d.kcorr_i, x.r50_r_arcsec,x.r90_r_arcsec from CAST as a, DERT as d ,%s_hrad_90_est as x where a.galcount = x.galcount and  a.galcount = d.galcount  and a.galcount between %d and %d order by galcount;""" %(model,(folder_num-1)*250, folder_num*250)

data = cursor.get_data(cmd)

galcount = np.array(data[0], dtype = int)


profiles = {'g':{}, 'r':{}, 'i':{}, 'gr':[], 'gi':[], 'ri':[] }

for gc, dat in zip(galcount,np.array(data[1:]).transpose()):
    r50 = dat[-2]
    r90 = dat[-1]
    try:
        for im_d in [0,1,2]:
            for im_f in [0,1,2]:
                if im_d == im_f:
                    infile = '%s/%08d_%s_%s.out' %(path,gc,bands[im_d], model )
                    outfile = '%s/%08d_%s_%s_mag_corr.out' %(path,gc,bands[im_d], model )
                else:
                    infile = '%s/%08d_%s_%s_%s.out' %(path,gc,bands[im_d], bands[im_f], model)
                    outfile = '%s/%08d_%s_%s_mag_corr_%s.out' %(path,gc,bands[im_d], bands[im_f], models )

                profiles[bands[im_d]][bands[im_f]] = profile_to_arcsec_mag(dat[0+im_d], dat[3+im_d], dat[6+im_d], bands[im_d], infile, extinction = dat[9+im_d],kcorr = dat[12+im_d])

        for color in ['gr', 'gi', 'ri']:
            profiles[color] = [profiles[color[0]][color[0]][0],profiles[color[0]][color[1]][1]-profiles[color[1]][color[0]][1],np.sqrt(profiles[color[0]][color[1]][2]**2 + profiles[color[1]][color[0]][2]**2)]

        outfile = open('%s/%08d_%s_mag_colors.out' %(path,gc, model), 'w')
        outfile.write('# rad(arcsec), g, g_err, r, r_err, i, i_err, (g-r), (g-r)_err, (g-i), (g-i)_err, (r-i), (r-i)_err\n')

        for row in zip(profiles[color[0]][color[0]][0],profiles['g']['g'][1],profiles['g']['g'][2],profiles['r']['r'][1],profiles['r']['r'][2],profiles['i']['i'][1],profiles['i']['i'][2],profiles['gr'][1],profiles['gr'][2],profiles['gi'][1],profiles['gi'][2],profiles['ri'][1],profiles['ri'][2]):
            outfile.write(' '.join(['%.4e' %a for a in row])+'\n')

        outfile.close()

        rads = profiles[color[0]][color[0]][0]
        rad_interp = np.array([r50,1.5*r50, 2.5*r50, 3.0*r50, 4.0*r50, r90]) 
        rad_interp_str = [10, 15, 25, 30, 40, 90] 
        rad_vals = dict( [(a, [-999]*len(rad_interp)) for a in bands])
        for tb in bands:
            try:
                tck = interpolate.splrep(profiles[tb][tb][0],profiles[tb][tb][1],s=0)
                rad_vals[tb]= interpolate.splev(rad_interp,tck,der=0)
            except:
                pass
        for count, radname in enumerate(rad_interp_str):
            cmd = 'update %s_magHL_%srad set g_mag = %f, r_mag = %f, i_mag = %f where galcount = %d and HL_rad_10 = %d;' %(model, model, rad_vals['g'][count],rad_vals['r'][count],rad_vals['i'][count],gc, radname)

            cmd = cmd.replace('nan', '-999')
            cursor.execute(cmd)
    except IOError:
        pass
        

    
