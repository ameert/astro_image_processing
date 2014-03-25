import numpy as np
import pyfits as pf
import pickle
from flag_defs import new_finalflag_vals
from flag_configuration import autoflag_config

max_sep = 0.7 #70% of the Sex Hrad
model = 'serexp'
band = 'r'
#for folder_num in range(1,2684):
for folder_num in range(1,121):
    print 'count %d' %folder_num
    #infile = open('/home/ameert/to_classify/flagfiles/%s/%s/total_flag_%d.pickle' %(band,model,folder_num))
    infile = open('/home/ameert/to_classify/flagfiles/simulation/%s/total_flag_%d.pickle' %(model,folder_num))
    data = pickle.load(infile)
    infile.close()

    #infile = open('/home/ameert/to_classify/flagfiles/%s/%s/total_profile_%d.pickle' %(band,model,folder_num))
    infile = open('/home/ameert/to_classify/flagfiles/simulation/%s/total_profile_%d.pickle' %(model,folder_num))
    profile_data = pickle.load(infile)
    infile.close()

    profile_dict = dict(zip(profile_data['galcount'], zip(profile_data['chi_prof'], profile_data['bt_prof'], profile_data['im_ctr'])))

    
    
    data['im_ctr'] = [ profile_dict.get(a, (([-999.0],[-999.0]),([-999.0], [-999.0], [-999.0],[-999.0]), (-999.0, -999.0)))[2] for a in data['galcount']]
    data['chi_prof'] = [ profile_dict.get(a, (([-999.0],[-999.0]),([-999.0], [-999.0], [-999.0],[-999.0]), (-999.0, -999.0)))[0] for a in data['galcount']]
    data['bt_prof'] = [ profile_dict.get(a, (([-999.0],[-999.0]),([-999.0], [-999.0], [-999.0],[-999.0]), (-999.0, -999.0)))[1] for a in data['galcount']]

    #print data['im_ctr']
    #print zip(data['galcount'],data['chi_prof'])[2]
    #print data['bt_prof']

    #print profile_dict.get(8232)
    

    auto_flags = np.zeros_like(np.array(data['galcount'])).astype(int)

    # various metrics used to calculate flags
    fit_center_x = data['x_bulge']* data['BT']+ data['x_disk']*(1.0- data['BT'])
    fit_center_y = data['y_bulge']* data['BT']+ data['y_disk']*(1.0- data['BT'])

    imcenter_x = np.array([a[0] for a in data['im_ctr']])
    imcenter_y = np.array([a[1] for a in data['im_ctr']])

    separation = np.sqrt((fit_center_x-imcenter_x)**2+(fit_center_y-imcenter_y)**2)
    separation = separation*0.396/data['r_sex']

    new_chi = np.array([a[1][19] if len(a[1])>21 else -999 for a in data['chi_prof'] ])
    new_der = np.array([np.sum(a[1][1:19]-a[1][0:18]) if len(a[1])>21 else -999 for a in data['chi_prof'] ])
    
    ang1 = np.radians(data['pa_bulge'])
    ang2 = np.radians(data['pa_disk'])
    pa_diff = np.arccos(np.cos(ang1)*np.cos(ang2)+np.sin(ang1)*np.sin(ang2))
    pa_diff = np.abs(np.degrees(pa_diff))
    pa_diff = np.where(pa_diff>90.0, 180.0-pa_diff, pa_diff)

    cir_rad_bulge =  data['r_bulge']*np.sqrt(data['ba_bulge'])
    cir_rad_disk =  data['r_disk']*np.sqrt(data['ba_disk'])

    bulge_vs_sky = cir_rad_bulge/data['r_sex']
    disk_vs_sky = cir_rad_disk/data['r_sex']
    rad_rat = cir_rad_bulge/(1.678*cir_rad_disk)


    # set flags
    #high_chi = np.where(np.where(new_chi>12.0, 1,0)+np.where(new_der+new_chi>7,1,0)*np.where(new_chi>5,1,0)>0, 1,0)
    high_chi = np.where(new_chi>autoflag_config['chicut'], 1,0)
    center_probs = np.where(separation>autoflag_config['max_sep'], 1,0)
    posang_diff = np.where(data['ba_disk']<autoflag_config['posang_d']['ba_cut'],1,0) * \
                 np.where(data['ba_bulge']<autoflag_config['posang_d']['ba_cut'],1,0) * \
                 np.where(pa_diff>autoflag_config['posang_d']['pa_cut'], 1,0)    

    no_bulge = np.where(autoflag_config['bulge_cut'](data['BT'], data['m_bulge']), 1,0)
    no_disk = np.where(autoflag_config['disk_cut'](data['BT'], data['m_disk']), 1,0)  
    
    parallel_com_flag = parallel_com(autoflag_config['par_com'])*np.where(no_bulge==1, 0,1)*np.where(no_disk==1, 0,1)*np.where(data['n_bulge']<autoflag_config['disky_n'],1,0)
    
    disk_fitting_inner = check_inverted_disk(2.7)*np.where(no_disk==1, 0,1)*np.where(no_bulge==1, 0,1)
    disk_is_sky = np.where(disk_vs_sky>3.0, 1,0)* np.where(data['ba_disk']>0.6, 1,0)*np.where(no_disk==1, 0,1)
    disk_contamination = np.where(disk_vs_sky>3.0, 1,0)* np.where(data['ba_disk']<=0.6, 1,0)*np.where(no_disk==1, 0,1)
    high_e_disk = np.where(data['ba_disk']<0.4,1,0)*np.where(data['BT']>0.75,1,0)*np.where(no_disk==1, 0,1)
    disk_dominates_always = check_disk_dominates_always(0.95)*np.where(no_bulge==1, 0,1)

    posang_bulge = posang_diff*np.where(data['BT']<0.5, 1,0)*np.where(no_bulge==1, 0,1)
    bulge_fitting_outer = check_inverted_bulge(0.9)*np.where(no_bulge==1, 0,1)
    bulge_is_sky = np.where(bulge_vs_sky>4.0, 1,0)* np.where(data['ba_bulge']>0.6, 1,0)*np.where(no_bulge==1, 0,1)
    bulge_contamination = np.where(bulge_vs_sky>4.0, 1,0)* np.where(data['ba_bulge']<=0.6, 1,0)*np.where(no_bulge==1, 0,1)
    high_e_bulge = np.where(data['ba_bulge']<0.4,1,0)*np.where(data['BT']<0.25,1,0)*np.where(no_bulge==1, 0,1)
    bulge_is_disk_flag = np.where(rad_rat>1.5,1,0)*np.where(data['n_bulge']<2.0,1,0)*np.where(no_bulge==1, 0,1)
    bulge_low_n_flag = np.where(bulge_is_disk_flag,0,1)*np.where(data['n_bulge']<2.0,1,0)*np.where(no_bulge==1, 0,1)
    bulge_dominates_always = check_bulge_dominates_always(0.95)*np.where(no_disk==1, 0,1)

    flip_com_flag = np.where(bulge_is_disk_flag+bulge_fitting_outer+disk_fitting_inner >1, 1,0)| np.where(disk_fitting_inner+bulge_low_n_flag >1, 1,0)|np.where(bulge_is_disk_flag >=1, 1,0)|np.where(no_disk+bulge_low_n_flag >1, 1,0)
    
    auto_disk_total = np.where(disk_is_sky+disk_contamination+ disk_fitting_inner*np.where(bulge_is_disk_flag+bulge_fitting_outer+bulge_low_n_flag+ parallel_com_flag>0,0,1)+high_e_disk*posang_disk+parallel_com_flag>0,1,0)
    auto_bulge_total = np.where(bulge_fitting_outer*np.where(disk_fitting_inner+bulge_is_disk_flag>0,0,1)+bulge_is_sky+bulge_contamination+ high_e_bulge*posang_bulge+parallel_com_flag>0,1,0)
    bad_total_flag = np.where((np.where(disk_is_sky+disk_contamination+bulge_is_sky+bulge_contamination+center_probs>0, 1,0) + np.where(no_bulge+no_disk+disk_dominates_always+bulge_dominates_always>1,1,0))>0,1,0)+high_chi


    # if galfit failed, or some measurement is wrong in the pa
    galfit_fail = np.where(data['galfit_flag']==1,1,0) #| np.where((bulge_dominates_always+disk_dominates_always+no_bulge+no_disk)>1, 1,0)

    new_finalflag_dict = dict(new_finalflag_vals)

    print "folder num: %d" %folder_num
    
    #only log disk flags if disk is included
    if model in ['devexp', 'serexp']:
        auto_flags += posang_disk * 2**new_finalflag_dict['disk pa problem']
        auto_flags += disk_fitting_inner * 2**new_finalflag_dict['disk fitting inner']
        auto_flags += disk_is_sky * 2**new_finalflag_dict['disk is sky']
        auto_flags += disk_contamination * 2**new_finalflag_dict['disk contaminated']
        auto_flags += high_e_disk * 2**new_finalflag_dict['high e disk']
        auto_flags += auto_disk_total * 2**new_finalflag_dict['bad disk']
        auto_flags += disk_dominates_always * 2**new_finalflag_dict['disk dominates always']
        auto_flags += parallel_com_flag * 2**new_finalflag_dict['parallel components']
        auto_flags += flip_com_flag * 2**new_finalflag_dict['flip components']
    
    auto_flags += no_disk * 2**new_finalflag_dict['no disk likely']

    auto_flags += bulge_is_disk_flag * 2**new_finalflag_dict['bulge is disk']
    auto_flags += posang_bulge * 2**new_finalflag_dict['bulge pa problem']
    auto_flags += bulge_fitting_outer * 2**new_finalflag_dict['bulge fitting outer']
    auto_flags += bulge_is_sky * 2**new_finalflag_dict['bulge is sky']
    auto_flags += bulge_contamination * 2**new_finalflag_dict['bulge contaminated']
    auto_flags += no_bulge * 2**new_finalflag_dict['no bulge likely']
    auto_flags += high_e_bulge * 2**new_finalflag_dict['high e bulge']
    auto_flags += bulge_low_n_flag * 2**new_finalflag_dict['low n bulge']
    auto_flags += bulge_dominates_always * 2**new_finalflag_dict['bulge dominates always']
    
    auto_flags +=  auto_bulge_total * 2**new_finalflag_dict['bad bulge']
    
    auto_flags += center_probs * 2**new_finalflag_dict['centering']
    auto_flags += high_chi * 2**new_finalflag_dict['high chi^2']
    auto_flags += bad_total_flag * 2**new_finalflag_dict['Bad total fit']

    # if galfit failed, lets clear out all the flags...They are junk!
    auto_flags = np.where(galfit_fail==1, 0, auto_flags)
    auto_flags += galfit_fail * 2**new_finalflag_dict['galfit failure']
    
    #outfile = open('/home/ameert/to_classify/flagfiles/%s/%s/autoflags_%d_newtest.pickle' %(band, model,folder_num), 'w')
    outfile = open('/home/ameert/to_classify/flagfiles/simulation/%s/autoflags_%d_newtest.pickle' %(model,folder_num), 'w')
    pickle.dump({'galcount':data['galcount'],'autoflags':auto_flags},outfile)
    outfile.close()
    for a in zip(data['galcount'], auto_flags):
        print a[0], a[1]
