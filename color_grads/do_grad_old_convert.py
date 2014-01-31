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

cursor = mysql_connect(dba, usr, pwd, 'shredder')

folder_num = int(sys.argv[1])
path = '/home/ameert/color_grads/data/%04d' %folder_num

cmd = """select a.galcount, a.aa_g, a.aa_r, a.aa_i, a.kk_g, a.kk_r, a.kk_i,
a.airmass_g, a.airmass_r, a.airmass_i, a.extinction_g, a.extinction_r, 
a.extinction_i, d.kcorr_g, d.kcorr_r, d.kcorr_i, a.petroR50_r, a.petroR90_r
from CAST as a, DERT as d 
where
a.galcount = d.galcount  and a.galcount between %d and %d;""" %((folder_num-1)*250, folder_num*250)

data = cursor.get_data(cmd)

galcount = np.array(data[0], dtype = int)


profiles = {'g':{}, 'r':{}, 'i':{}, 'gr':[], 'gi':[], 'ri':[] }

for gc, dat in zip(galcount,np.array(data[1:-1]).transpose()):
    r50 = dat[-2]
    r90 = dat[-1]
    try:
        for im_d in [0,1,2]:
            for im_f in [0,1,2]:
                if im_d == im_f:
                    infile = '%s/%08d_%s_ser.out' %(path,gc,bands[im_d] )
                    outfile = '%s/%08d_%s_ser_mag_corr.out' %(path,gc,bands[im_d] )
                else:
                    infile = '%s/%08d_%s_%s_ser.out' %(path,gc,bands[im_d], bands[im_f])
                    outfile = '%s/%08d_%s_%s_mag_corr_ser.out' %(path,gc,bands[im_d], bands[im_f] )

                profiles[bands[im_d]][bands[im_f]] = profile_to_arcsec_mag(dat[0+im_d], dat[3+im_d], dat[6+im_d], bands[im_d], infile, extinction = dat[9+im_d],kcorr = dat[12+im_d])

        for color in ['gr', 'gi', 'ri']:
            profiles[color] = [profiles[color[0]][color[0]][0],profiles[color[0]][color[1]][1]-profiles[color[1]][color[0]][1],np.sqrt(profiles[color[0]][color[1]][2]**2 + profiles[color[1]][color[0]][2]**2)]

        #outfile = open('%s/%08d_ser_mag_colors.out' %(path,gc), 'w')
        #outfile.write('# rad(arcsec), g, g_err, r, r_err, i, i_err, (g-r), (g-r)_err, (g-i), (g-i)_err, (r-i), (r-i)_err\n')

        #for row in zip(profiles[color[0]][color[0]][0],profiles['g']['g'][1],profiles['g']['g'][2],profiles['r']['r'][1],profiles['r']['r'][2],profiles['i']['i'][1],profiles['i']['i'][2],profiles['gr'][1],profiles['gr'][2],profiles['gi'][1],profiles['gi'][2],profiles['ri'][1],profiles['ri'][2]):
        #    outfile.write(' '.join(['%.4e' %a for a in row])+'\n')

        #outfile.close()

        rads = profiles[color[0]][color[0]][0]
        rad_vals = [-999]*30
        for tcount,tb in enumerate(bands):
            tck = interpolate.splrep(rads,profiles[tb][tb][1],s=0)
            rad_vals[tcount]= interpolate.splev(r50,tck,der=0)
        for tcount,tb in enumerate(['gr','gi','ri']):
            tck = interpolate.splrep(np.log10(rads),profiles[tb][1],s=0)
            rad_vals[tcount+3]= interpolate.splev(np.log10(r50),tck,der=1)
            rad_vals[tcount+6]= (profiles[tb][1][0] - interpolate.splev(np.log10(r50),tck,der=0))/np.log10(rads[0]/r50)
            rad_vals[tcount+9]= (profiles[tb][1][0] - interpolate.splev(np.log10(r50*4),tck,der=0))/np.log10(rads[0]/(4*r50))
            rad_vals[tcount+12]= (profiles[tb][1][0] - interpolate.splev(np.log10(r50*2),tck,der=0))/np.log10(rads[0]/(2*r50))
            rad_vals[tcount+15]= (profiles[tb][1][0] - interpolate.splev(np.log10(r50*0.5),tck,der=0))/np.log10(rads[0]/(0.5*r50))
            rad_vals[tcount+18]= (profiles[tb][1][0] - interpolate.splev(np.log10(r50*1.5),tck,der=0))/np.log10(rads[0]/(1.5*r50))
            rad_vals[tcount+21]= (profiles[tb][1][0] - interpolate.splev(np.log10(r50*2.5),tck,der=0))/np.log10(rads[0]/(2.5*r50))
            rad_vals[tcount+24]= (profiles[tb][1][0] - interpolate.splev(np.log10(r50*3),tck,der=0))/np.log10(rads[0]/(3*r50))
            rad_vals[tcount+27]= (profiles[tb][1][0] - interpolate.splev(np.log10(r90),tck,der=0))/np.log10(rads[0]/(r90))
            

        cmd = 'update ser_rad set MagHL_g = %f, MagHL_r = %f, MagHL_i = %f, grColor_hl = %f, giColor_hl = %f, riColor_hl = %f, grCenter_hl = %f, giCenter_hl = %f, riCenter_hl = %f, grOuter_hl = %f, giOuter_hl = %f, riOuter_hl = %f,grtwo_hl = %f, gitwo_hl = %f, ritwo_hl = %f, grhalf_hl = %f, gihalf_hl = %f, rihalf_hl = %f, gr15_hl = %f, gi15_hl = %f, ri15_hl = %f, gr25_hl = %f, gi25_hl = %f, ri25_hl = %f, gr3_hl = %f, gi3_hl = %f, ri3_hl = %f, gr90_hl = %f, gi90_hl = %f, ri90_hl = %f where galcount = %d;' %(rad_vals[0],rad_vals[1],rad_vals[2],rad_vals[3],rad_vals[4],rad_vals[5],rad_vals[6],rad_vals[7],rad_vals[8],rad_vals[9],rad_vals[10],rad_vals[11],rad_vals[12],rad_vals[13],rad_vals[14],rad_vals[15],rad_vals[16],rad_vals[17],rad_vals[18],rad_vals[19],rad_vals[20],rad_vals[21],rad_vals[22],rad_vals[23],rad_vals[24],rad_vals[25],rad_vals[26],rad_vals[27],rad_vals[28],rad_vals[29],gc)

        #print cmd
        cursor.execute(cmd)
    except IOError:
        pass
        

    
