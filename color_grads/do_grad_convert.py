#!/data2/home/ameert/python/bin/python2.5


"""create table %s_colorgrad_%srad (galcount int primary key, centerrad_arcsec float default -999,
grCenter float default -999,  giCenter float default -999,  riCenter float default -999,
gr05_hl float default -999,  gi05_hl float default -999,  ri05_hl float default -999,
gr10_hl float default -999,  gi10_hl float default -999,  ri10_hl float default -999,
gr15_hl float default -999,  gi15_hl float default -999,  ri15_hl float default -999,
gr20_hl float default -999,  gi20_hl float default -999,  ri20_hl float default -999,
gr25_hl float default -999,  gi25_hl float default -999,  ri25_hl float default -999,
gr30_hl float default -999,  gi30_hl float default -999,  ri30_hl float default -999,
gr40_hl float default -999,  gi40_hl float default -999,  ri40_hl float default -999,
gr90_hl float default -999,  gi90_hl float default -999,  ri90_hl float default -999);
"""

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
model = 'serexp'

cmd = """select a.galcount, a.aa_g, a.aa_r, a.aa_i, a.kk_g, a.kk_r, a.kk_i,a.airmass_g, a.airmass_r, a.airmass_i, a.extinction_g, a.extinction_r,a.extinction_i, d.kcorr_g, d.kcorr_r, d.kcorr_i, x.r50_r_arcsec,x.r90_r_arcsec from CAST as a, DERT as d ,%s_hrad_90_est as x
where a.galcount = x.galcount and  a.galcount = d.galcount  and
a.galcount between %d and %d order by galcount;""" %(model, (folder_num-1)*250, folder_num*250)

data = cursor.get_data(cmd)

galcount = np.array(data[0], dtype = int)
#print galcount
#print data
profiles = {'g':{}, 'r':{}, 'i':{}, 'gr':[], 'gi':[], 'ri':[] }

for gc, dat in zip(galcount,np.array(data[1:]).transpose()):
    #print dat
    r50 = dat[-2]
    r90 = dat[-1]
    try:
        for im_d in [0,1,2]:
            for im_f in [0,1,2]:
                if im_d == im_f:
                    infile = '%s/%08d_%s_%s.out' %(path,gc,bands[im_d], model )
                    outfile = '%s/%08d_%s_%s_mag_corr.out' %(path,gc,bands[im_d],model )
                else:
                    infile = '%s/%08d_%s_%s_%s.out' %(path,gc,bands[im_d], bands[im_f],model)
                    outfile = '%s/%08d_%s_%s_mag_corr_%s.out' %(path,gc,bands[im_d], bands[im_f],model )

                profiles[bands[im_d]][bands[im_f]] = profile_to_arcsec_mag(dat[0+im_d], dat[3+im_d], dat[6+im_d], bands[im_d], infile, extinction = dat[9+im_d],kcorr = dat[12+im_d])

        for color in ['gr', 'gi', 'ri']:
            profiles[color] = [profiles[color[0]][color[0]][0],profiles[color[0]][color[1]][1]-profiles[color[1]][color[0]][1],np.sqrt(profiles[color[0]][color[1]][2]**2 + profiles[color[1]][color[0]][2]**2)]

        #outfile = open('%s/%08d_%s_mag_colors.out' %(path,gc, model), 'w')
        #outfile.write('# rad(arcsec), g, g_err, r, r_err, i, i_err, (g-r), (g-r)_err, (g-i), (g-i)_err, (r-i), (r-i)_err\n')

        #for row in zip(profiles[color[0]][color[0]][0],profiles['g']['g'][1],profiles['g']['g'][2],profiles['r']['r'][1],profiles['r']['r'][2],profiles['i']['i'][1],profiles['i']['i'][2],profiles['gr'][1],profiles['gr'][2],profiles['gi'][1],profiles['gi'][2],profiles['ri'][1],profiles['ri'][2]):
        #    outfile.write(' '.join(['%.4e' %a for a in row])+'\n')

        #outfile.close()

        rads = profiles[color[0]][color[0]][0]
        innerrad = rads[0]
        rads_to_eval = np.array([innerrad, 0.5*r50, 1.0*r50, 1.5*r50, 2.0*r50,
                                 2.5*r50, 3.0*r50, 4.0*r50, r90])
        rad_vals = np.array([-999.0]*3*(rads_to_eval.size))

        for tcount,tb in enumerate(['gr','gi','ri']):
            try:
                tck = interpolate.splrep(np.log10(rads),profiles[tb][1],s=0)
                rad_vals[tcount]= interpolate.splev(np.log10(r50),tck,der=1)
                
                grad_vals =interpolate.splev(np.log10(rads_to_eval),tck,der=0)
                grad_vals = np.where(rads_to_eval<rads[0], -888, grad_vals)
            
            
                rad_vals[tcount::3] = grad_vals
            except:
                #print "skipping gc:%d band:%s" %(gc, tb)
                pass
        cmd = """update %s_colorgrad_%srad set centerrad_arcsec = %f,
        grCenter = %f,  giCenter = %f,  riCenter = %f,
        gr05_hl = %f,  gi05_hl = %f,  ri05_hl = %f,
        gr10_hl = %f,  gi10_hl = %f,  ri10_hl = %f,
        gr15_hl = %f,  gi15_hl = %f,  ri15_hl = %f,
        gr20_hl = %f,  gi20_hl = %f,  ri20_hl = %f,
        gr25_hl = %f,  gi25_hl = %f,  ri25_hl = %f,
        gr30_hl = %f,  gi30_hl = %f,  ri30_hl = %f,
        gr40_hl = %f,  gi40_hl = %f,  ri40_hl = %f,
        gr90_hl = %f,  gi90_hl = %f,  ri90_hl = %f
        where galcount = %d;""" %(model, model, innerrad,
        rad_vals[0],rad_vals[1],rad_vals[2],
        rad_vals[3],rad_vals[4],rad_vals[5],
        rad_vals[6],rad_vals[7],rad_vals[8],
        rad_vals[9],rad_vals[10],rad_vals[11],
        rad_vals[12],rad_vals[13],rad_vals[14],
        rad_vals[15],rad_vals[16],rad_vals[17],
        rad_vals[18],rad_vals[19],rad_vals[20],
        rad_vals[21],rad_vals[22],rad_vals[23],
        rad_vals[24],rad_vals[25],rad_vals[26],
        gc)

        cmd = cmd.replace('nan', '-999.0')
        #print gc
        #print r50, r90
        #print cmd
        cursor.execute(cmd)
    except IOError:
        print IOError
        

    
