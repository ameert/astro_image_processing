from mysql.mysql_class import *

def get_data(cursor, table1, table2, add_tables = '', conditions = '', flags=False, flagmodel = 'serexp'):
    cmd = """select a.galcount, 
a.m_tot-c.extinction_r, a.Hrad_corr, a.ba_tot_corr, a.BT,
a.m_bulge-c.extinction_r , a.r_bulge, a.n_bulge, a.ba_bulge, a.pa_bulge, 
a.m_disk-c.extinction_r , a.r_disk, a.ba_disk, a.pa_disk, a.galsky,
b.m_tot-c.extinction_r , b.Hrad_corr, b.ba_tot_corr, b.BT,
b.m_bulge-c.extinction_r , b.r_bulge, b.n_bulge, b.ba_bulge, b.pa_bulge, 
b.m_disk-c.extinction_r , b.r_disk, b.ba_disk, b.pa_disk,b.galsky, 
d.kcorr_r + d.dismod, d.kpc_per_arcsec, c.z, d.vmax,
c.PetroMag_r-c.extinction_r, c.PetroR50_r
from %s as a, %s as b, CAST as c, DERT as d %s,  
Flags_optimize as x
where a.galcount = b.galcount and a.galcount = c.galcount and 
a.galcount = x.galcount  and x.band = 'r' and x.ftype = 'u' and 
x.model = '%s' and
d.galcount = c.galcount 
""" %(table1, table2,add_tables, flagmodel)
    if flags:
        cmd += """ and ( x.flag&pow(2,19)=0 ) 
"""
    cmd += """ %s  ;"""  %conditions  
    # x.flag&pow(2,14)=0 and x.flag&pow(2,10)>0 and
    # and  a.r_bulge*sqrt(a.ba_bulge)>0.396
    print cmd
    data_list = cursor.get_data(cmd) 

    data_name = ['galcount',  'mtot_1', 'hrad_1', 'batot_1', 
                 'BT_1', 'mbulge_1', 'rbulge_1', 'nbulge_1', 'babulge_1', 
                 'pabulge_1', 'mdisk_1', 'rdisk_1', 'badisk_1', 
                 'padisk_1', 'sky_1','mtot_2', 'hrad_2', 'batot_2', 
                 'BT_2', 'mbulge_2', 'rbulge_2', 'nbulge_2', 'babulge_2', 
                 'pabulge_2', 'mdisk_2', 'rdisk_2', 'badisk_2','padisk_2', 
                 'sky_2', 'magcorr','kpc_per_arcsec','z', 'vmax',
                 'petromag_1', 'petrorad_1']

    data = {}
    for a,b in zip(data_list, data_name):
        data[b] = np.array(a, dtype = float)

    data['surf_bright_1'] = -2.5*np.log10(10**(-0.4*data['mtot_1'])/(2.0*np.pi*data['hrad_1']**2))
    data['surf_bright_2'] = -2.5*np.log10(10**(-0.4*data['mtot_2'])/(2.0*np.pi*data['hrad_2']**2))
    
    data['mtot_abs_1'] = data['mtot_1'] - data['magcorr']
    data['mtot_abs_2'] = data['mtot_2'] - data['magcorr']
    

    data['petromag_2'] = data['petromag_1']
    data['petrorad_2'] = data['petrorad_1']

    data['petromag_abs_1'] = data['petromag_1'] - data['magcorr']
    data['petromag_abs_2'] = data['petromag_2'] - data['magcorr']
    
    data['n_1'] = data['nbulge_1']
    data['n_2'] = data['nbulge_2']

    
    data['rbulge_1'] = data['rbulge_1']*np.sqrt(data['babulge_1'])
    data['rbulge_2'] = data['rbulge_2']*np.sqrt(data['babulge_2'])
   
    #source_count = mag_to_counts( data['mtot_in'], -1.0*data['magzp'], 
    #                              kk = 0,airmass=0,exptime=data['exptime'])

    #data['sn_in'] = measure_sn(data['hrad_in']/data['pix_sz'], source_count, 
    #                           data['galsky']*data['exptime'],data['gain'],
    #                           data['dvar'])
    
    return data
    
