import numpy as np
import pickle
import sys 
from mysql.mysql_class import *


def create_flag_pickle(folder_num, info_dict, print_info=False):
    cursor = info_dict['cursor']

    cmd = """select x.galcount, z.Hrad_corr,z.BT, 
z.m_tot, -x.aa_{band} - x.kk_{band}*x.airmass_{band},
y.SexHrad, y.num_targets, 
z.r_bulge, z.xctr_bulge, z.yctr_bulge, z.n_bulge, z.ba_bulge, z.pa_bulge,
z.xctr_bulge_err, z.yctr_bulge_err,
z.r_disk, z.xctr_disk, z.yctr_disk, z.ba_disk, z.pa_disk,
z.xctr_disk_err, z.yctr_disk_err, s.kpc_per_arcsec, z.m_bulge, 
z.m_disk, IF(z.flag&pow(2,15)>0,1,0), 
IF(bf.is_polluted=1, IF(bf.is_polluted_deep=1,1,IF(bf.is_fractured_deep=1,1,0)),0), 
IF(bf.is_fractured=1, 1, 0)
from 
{band}_band_{model} as z,{band}_band_fit as y,CAST as x, DERT as s,
{band}_band_badfits as bf 
where 
y.galcount = x.galcount and
x.galcount = s.galcount and 
x.galcount = z.galcount and
x.galcount = bf.galcount and  
x.galcount between {low} and {high} 
order by 
x.galcount;""".format(model = info_dict['model'], band = info_dict['band'], low = 250*(folder_num-1)+1, high = 250*folder_num)

    data = cursor.get_data(cmd)

    data = np.array([np.array(d) for d in data])

    pos_dict = dict((a[1],a[0]) for a in enumerate(['galcount', 'hrad_corr', 
                                      'BT', 'mag', 'zp', 'hrad_sex', 
                                      'num_targets','r_bulge','x_bulge', 
                                      'y_bulge', 
                                      'n_bulge', 'ba_bulge','pa_bulge',
                                      'x_bulge_err', 'y_bulge_err', 
                                      'r_disk','x_disk', 'y_disk',
                                      'ba_disk','pa_disk',
                                      'x_disk_err', 'y_disk_err', 
                                      'kpc_per_arcsec', 'm_bulge', 'm_disk', 
                                      'galfit_flag', 'polluted_flag', 
                                      'fractured_flag']))

    new_data = {'galcount': [int(a) for a in data[pos_dict['galcount']]],
                'tot_counts': 10.0**(-0.4*(data[pos_dict['mag']] - data[pos_dict['zp']]))}

    new_data['wfile']=['/media/SDSS2/fit_catalog/data/%s/%04d/%08d_%s_stamp_W.fits' %(info_dict['band'],folder_num, gc, info_dict['band']) for gc in new_data['galcount']]

    new_data['dfile']=['/media/SDSS2/fit_catalog/data/%s/%04d/%08d_%s_stamp.fits' %(info_dict['band'],folder_num, gc, info_dict['band']) for gc in new_data['galcount']]

    new_data['r_tot']=data[pos_dict['hrad_corr']]
    new_data['r_sex']=data[pos_dict['hrad_sex']]

    for key in [ 'BT', 'num_targets', 'r_bulge','x_bulge', 'y_bulge', 
            'ba_bulge','n_bulge', 'pa_bulge','x_bulge_err', 'y_bulge_err', 
            'r_disk','x_disk', 'y_disk','ba_disk','pa_disk',
            'x_disk_err', 'y_disk_err', 'kpc_per_arcsec', 'm_bulge', 'm_disk',
             'galfit_flag', 'polluted_flag', 'fractured_flag']:
        new_data[key]=data[pos_dict[key]]
    if print_info:
        print "writing:", '/home/ameert/to_classify/flagfiles/%s/%s/total_flag_%d.pickle' %(info_dict['band'],info_dict['model'],folder_num)
        print "gals:"
        print new_data['galcount']
    outfile = open('/home/ameert/to_classify/flagfiles/%s/%s/total_flag_%d.pickle' %(info_dict['band'],info_dict['model'],folder_num), 'w')
    pickle.dump(new_data, outfile)
    outfile.close()
    return

if __name__ == "__main__":

    folder_num = int(sys.argv[1])

    model = sys.argv[2]
    band = sys.argv[3]
    info_dict = {'dba':'catalog', 'usr':'pymorph', 'pwd':'pymorph', 'host':'',
                 'band':band, 'model':model}

    info_dict['cursor']=mysql_connect(info_dict['dba'],info_dict['usr'],info_dict['pwd'],info_dict['host'])
  
    create_flag_pickle(folder_num, info_dict, print_info=True)



