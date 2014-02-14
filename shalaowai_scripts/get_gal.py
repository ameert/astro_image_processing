import numpy as np

#from astro_utils.user_params import *

g = {'band':{}, 'save_path':{},'path_main_data':{},'model_types':{},    
      'path_root':{},  'weight_image':{},
    'mask_image':{},   'sim_mask_image':{}, 'file_name':{},    'galcount':{},
    'Name':{},    'm_pEL':{},    'm_pS0':{},    'm_pSAB':{},    'm_pSCD':{},
    'zoo_pE':{},    'zoo_pS':{},    'sdss_zeropoint':{},    'kk':{},
    'airmass':{},    'chi2nu':{},    'petroR50':{},    'hrad_corr':{},
    'n':{},    're':{},    'Ie':{},    'eb':{},    'rd':{},    'Id':{},
    'ed':{},    'BT':{},    'GalSky':{},    'bpa':{},    'dpa':{},
    'xctr_bulge':{},    'yctr_bulge':{},    'xctr_disk':{},    'yctr_disk':{},
    'shift_sky':{},    'absmag':{}, 'appmag':{},    'abscorr':{},    
     'imctr':{},    'z':{}, 'ba_tot_corr':{},'petro_mag':{},'petro_absmag':{},
     'flags':{}
    }

def get_gal(cursor, model, galcount, gal_info, band = 'r'):
    cmd = """select a.galcount,
        b.probaEll, b.probaS0, b.probaSab, b.probaScd,
        c.p_el_debiased, c.p_cs_debiased,
        -1.0*c.aa_{band}, c.kk_{band}, c.airmass_{band},
        a.chi2nu,
        c.petroR50_{band}, a.Hrad_corr,
        abs(a.m_bulge), abs(a.m_disk),
        a.r_bulge, a.r_disk, a.n_bulge, a.BT, 
        a.ba_tot_corr, a.ba_bulge, a.ba_disk, 
        a.pa_bulge, a.pa_disk, a.GalSky,
        a.xctr_bulge,a.yctr_bulge,a.xctr_disk,a.yctr_disk, 
        f.dismod+f.kcorr_{band}, c.z, abs(a.m_tot), c.petromag_{band},
        z.flag
        from  {band}_band_%s as a, Flags_optimize as z,
        M2010 as b, CAST as c, DERT as f
        where  a.galcount = %d and a.galcount = b.galcount
        and a.galcount = f.galcount
        and a.galcount = c.galcount and a.galcount = z.galcount and
        z.band = '{band}' and z.model = '%s' and z.ftype = 'u'
        ;""" %(model, galcount, model)

    cmd = cmd.replace('{band}', band)

    tmp_info = cursor.get_data(cmd)
    
    for tmp_ind, tmp_val in zip( ['galcount','m_pEL','m_pS0','m_pSAB',
                                  'm_pSCD','zoo_pE','zoo_pS',
                                  'sdss_zeropoint','kk','airmass','chi2nu',
                                  'petroR50','hrad_corr',
                                  'Ie','Id','re','rd','n','BT', 'ba_tot_corr',
                                  'eb','ed','bpa','dpa','GalSky',    
                                  'xctr_bulge','yctr_bulge',
                                  'xctr_disk','yctr_disk', 'abscorr', 'z',
                                  'appmag', 'petro_mag', 'flags'],
                                 tmp_info):

        gal_info[tmp_ind][model] = tmp_val[0]

    gal_info['absmag'][model] = gal_info['appmag'][model] - gal_info['abscorr'][model]
    gal_info['petro_absmag'][model] = gal_info['petro_mag'][model] - gal_info['abscorr'][model]

    gal_info['imctr'][model] = [gal_info['xctr_bulge'][model]*gal_info['BT'][model] + gal_info['xctr_disk'][model]*(1.0-gal_info['BT'][model]),gal_info['yctr_bulge'][model]*gal_info['BT'][model] + gal_info['yctr_disk'][model]*(1.0-gal_info['BT'][model])]
    
    return gal_info
