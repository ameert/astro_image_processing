import numpy as np

def sky_percent_diff(sky):
    sky = 100.0*(sky - 2.41154)/2.41154
    return sky

def magsum(mag1, mag2):
    mag1 = 10.0**( -.4*mag1)
    mag2 = 10.0**(-.4*mag2)

    mag_tot = mag1 + mag2
    bt = mag1/(mag1+mag2)
    mag_tot = -2.5 * np.log10(mag_tot)

    return mag_tot, bt

def measure_sn(r_pix, source_count, bkrd, gain, darkvar):
    #calculate the s/n inside the halflight raduis
    num_pix = np.pi*(r_pix**2)
    #half_flux = source_count/(2*np.sqrt(num_pix))
    half_flux = source_count/2.0
    back_flux = num_pix*bkrd
    sn = half_flux/(np.sqrt(num_pix)*np.sqrt((half_flux+back_flux)/gain + num_pix*darkvar))

    return sn

def mag_to_counts( mag, aa, kk = 0 , airmass = 0, exptime = 53.90456):
    return exptime * (10**(-.4*mag)) / (10**(0.4*(aa + kk*airmass)))

def get_data(cursor, outtab, inmodel, choice = 'sdss'):
    if choice == 'sdss':
        cmd = """select a.galcount,
a.re_pix*0.396*sqrt(a.eb),
c.re*sqrt(c.eb), (a.rd_pix*0.396 - c.rd)/c.rd + c.rd, c.rd, 
(a.hrad_pix_corr*0.396-c.hrad_pix_corr*0.396)/(c.hrad_pix_corr*0.396) + c.hrad_pix_corr*0.396, c.hrad_pix_corr*0.396, 
1.0,1.0, a.n, c.n, a.BT, c.BT, 
abs(a.Ie) -a.magzp+c.zeropoint_sdss_r, abs(c.Ie),
abs(a.Id) -a.magzp+c.zeropoint_sdss_r , abs(c.Id),
1.0,1.0,
a.galsky, a.sexsky, 130.0/53.907456, 0.396, c.zeropoint_sdss_r, 53.90456,
4.6, 1.0,  abs(a.Ie) -a.magzp+c.zeropoint_sdss_r- a.dis_modu,a.dis_modu,
a.re_pix_err*0.396, a.rd_pix_err*0.396, 
a.n_err, 0.01,
a.Ie_err, a.Id_err, a.galsky_err, a.eb, c.eb, a.bpa, c.bpa, abs(a.mag_auto) -a.magzp+c.zeropoint_sdss_r, (a.SexHalfRad*0.396-c.hrad_pix_corr*0.396)/(c.hrad_pix_corr*0.396) + c.hrad_pix_corr*0.396
 from %s as a, sim_input as c , catalog.CAST as b, catalog.Flags_optimize as z,
 catalog.Flags_optimize as x
 where a.galcount = c.simcount
and  c.galcount = b.galcount 
 and c.model = '%s' 
and c.galcount = z.galcount and z.band = 'r' and z.model='devexp' and z.ftype = 'u' and ( z.flag&pow(2,11)>0 or z.flag&pow(2,12)>0)
and c.galcount = x.galcount and x.band = 'r' and x.model='serexp' and x.ftype = 'u' and ( x.flag&pow(2,11)>0 or x.flag&pow(2,12)>0);""" %(outtab, inmodel) #and c.hrad_pix_corr*0.396/b.psfwidth_r > 0.5 /b.psfwidth_r #a.petro_psf_rad*0.396, c.petro_psf_rad
#abs(a.petro_psf_mag) -a.magzp+c.zeropoint_sdss_r , abs(c.petro_psf_mag),
#(a.re_pix*0.396 - c.re)/c.re + c.re,


    elif choice == 'pix05':
        cmd = """select a.galcount,(a.re_pix*2*0.396 - c.re)/c.re + c.re,
c.re, (a.rd_pix*2*0.396 - c.rd)/c.rd + c.rd, c.rd, 
(a.hrad_pix_corr*0.396*2-c.hrad_pix_corr*0.396)/(c.hrad_pix_corr*0.396) + c.hrad_pix_corr*0.396, c.hrad_pix_corr*0.396, 
a.petro_psf_rad*0.396, c.petro_psf_rad, a.n, c.n, a.BT, c.BT, 
abs(a.Ie)-2.5*log10(53.907465) -a.magzp+c.zeropoint_sdss_r, abs(c.Ie),
abs(a.Id)-2.5*log10(53.907465) -a.magzp+c.zeropoint_sdss_r , abs(c.Id),
abs(a.petro_psf_mag)-2.5*log10(53.907465) -a.magzp+c.zeropoint_sdss_r , 
abs(c.petro_psf_mag),
a.galsky, a.sexsky, 130.0/53.907456, 2*0.396, c.zeropoint_sdss_r, 53.90456,
4.6, 1.0,  abs(a.Ie) -a.magzp+c.zeropoint_sdss_r- a.dis_modu,
a.re_pix_err*0.396*2, a.rd_pix_err*0.396*2, 
a.n_err, 0.01,
a.Ie_err, a.Id_err, a.galsky_err
 from %s as a, sim_input as c where a.galcount = c.simcount  and c.model = '%s';
""" %(outtab, inmodel)
    elif choice == 'pix2':
        cmd = """select a.galcount,(a.re_pix*0.396/2 - c.re)/c.re + c.re,
c.re, (a.rd_pix*0.396/2 - c.rd)/c.rd + c.rd, c.rd, 
(a.hrad_pix_corr*0.396/2-c.hrad_pix_corr*0.396)/(c.hrad_pix_corr*0.396) + c.hrad_pix_corr*0.396, c.hrad_pix_corr*0.396, a.n, c.n, a.BT, c.BT, 
abs(a.Ie)-2.5*log10(53.907465) -a.magzp+c.zeropoint_sdss_r, abs(c.Ie),
abs(a.Id)-2.5*log10(53.907465) -a.magzp+c.zeropoint_sdss_r , abs(c.Id),
a.galsky, a.sexsky, 130.0/53.907456, 0.396/2, c.zeropoint_sdss_r, 53.90456,
4.6, 1.0,  abs(a.Ie) -a.magzp+c.zeropoint_sdss_r- a.dis_modu,
a.re_pix_err*0.396/2, a.rd_pix_err*0.396/2, 
a.n_err, 0.01,
a.Ie_err, a.Id_err, a.galsky_err, a.eb, c.eb
 from %s as a, sim_input as c where a.galcount = c.simcount  and c.model = '%s';
""" %(outtab, inmodel)
    elif choice == 'hst':
        zval = outtab.split('_')[1][1:]
        cmd = """select a.galcount,a.re_pix*0.03, 
c.re*c.kpc_per_arcsec/c.kpc_per_arcsec_%s, 
a.rd_pix*0.03, c.rd*c.kpc_per_arcsec/c.kpc_per_arcsec_%s, 
a.hrad_pix_corr*0.03, c.hrad_pix_corr*0.396*c.kpc_per_arcsec/(c.kpc_per_arcsec_10), a.n, c.n, a.BT, c.BT, 
abs(a.Ie), abs(c.Ie)-1.0*(%f)-1.0 - c.dismod + c.dismod_%s +c.z,
abs(a.Id), abs(c.Id)-1.0*(%f)-1.0 - c.dismod + c.dismod_%s +c.z,
a.galsky, a.sexsky, 17.1824096325044/2286.0, 0.03,24.84068, 2286.0, 1.0, 0.0,
abs(c.Ie) - c.dismod 
 from %s as a, sim_input as c where a.galcount = c.simcount  and c.model = '%s';
""" %(zval, zval, float(zval)/10.0, zval, float(zval)/10.0, zval, 
      outtab, inmodel) 
        
    print cmd
    data_list = cursor.get_data(cmd) 

    data_name = ['galcount', 're_out', 're_in','rd_out', 'rd_in', 
                 'hrad_out', 'hrad_in', 'prad_out', 'prad_in',
                 'n_out', 'n_in', 'BT_out', 'BT_in', 
                 'Ie_out','Ie_in','Id_out','Id_in', 
                 'pmag_out', 'pmag_in', 'galsky','sexsky','sky_in',
                 'pix_sz', 'magzp', 'exptime', 'gain', 'dvar', 'absmag','dismod',
                 're_err', 'rd_err', 'n_err','BT_err', 'Ie_err',
                 'Id_err', 'galsky_err', 'ba_out', 'ba_in', 'bpa_out','bpa_in',
                 'mag_auto', 'sexhrad']

    data = {}
#    print len(data_list)
#    count = 0
    for a,b in zip(data_list, data_name):
#        print count
#        print b
        data[b] = np.array(a, dtype = float)
#        count+=1
#    raw_input()
    data['mtot_out']= magsum(data['Ie_out'],data['Id_out'])[0] 
    data['mtot_in']= magsum(data['Ie_in'],data['Id_in'])[0] 
    data['rerd_in'] = data['re_in']/data['rd_in']
    data['rerd_out'] = data['re_out']/data['rd_out']
    data['surf_bright_in'] = -2.5*np.log10(10**(-0.4*data['mtot_in'])/(2.0*np.pi*data['hrad_in']**2))
    data['surf_bright_out'] = -2.5*np.log10(10**(-0.4*data['mtot_out'])/(2.0*np.pi*data['hrad_out']**2))
    
    source_count = mag_to_counts( data['mtot_in'], -1.0*data['magzp'], 
                                  kk = 0,airmass=0,exptime=data['exptime'])

    data['sn_in'] = measure_sn(data['hrad_in']/data['pix_sz'], source_count, 
                               data['galsky']*data['exptime'],data['gain'],
                               data['dvar'])
    


    data['ba_frac_out'] = (1.0-data['ba_out'])/(1.0+data['ba_out'])
    data['ba_frac_in'] = (1.0-data['ba_in'])/(1.0+data['ba_in'])

    data['bpa_in'] = np.where(data['bpa_in']>180.0, data['bpa_in']-180.0, data['bpa_in'])
    data['bpa_in'] = np.where(data['bpa_in']<0.0, data['bpa_in']+180.0, data['bpa_in'])
    data['bpa_in'] = 90.0-data['bpa_in'] 


    data['sc_in'] = data['ba_frac_in']*np.cos(2.0*data['bpa_in'])
    data['ss_in'] = data['ba_frac_in']*np.sin(2.0*data['bpa_in'])
    data['sc_out'] = data['ba_frac_out']*np.cos(2.0*data['bpa_out'])
    data['ss_out'] = data['ba_frac_out']*np.sin(2.0*data['bpa_out'])


    return data
    

def get_savename(path, inmodel = 'ser', BT = 'devexp', color = 'nin', plot = 'scat', add = ''):
    return path + '/'+inmodel + '_'+add+BT+'_'+color + '_'+plot+'.eps'

