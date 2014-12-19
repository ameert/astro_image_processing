import numpy as np
import pyfits as pf
import pickle
from astro_image_processing.mysql import *
from flag_configuration import autoflag_vals, autoflag_dict, autoflag_config


##############################################
# BEGIN Flag test functions
#############################################
def check_inverted_bulge(data, light_cut):
    result = []
    for a,b in zip(data['bt_prof'], data['BT']):
        result += [0]
        sel_bt_r = np.extract(a[3]<light_cut, a[1])-0.5
        transition = np.where(np.abs(sel_bt_r)< 0.01)
        if b<.7:
            if len(transition[0])>0:
                last_trans = np.max(transition)
                outer_val = np.sum(sel_bt_r[last_trans:])
                if outer_val > 0:
                    result[-1] = 1
                
    return np.array(result)

def  parallel_com(data, rms_cut):
    light_cut = 0.9
    result = []
    for a,b in zip(data['bt_prof'], data['BT']):
        result += [0]
        sel_bt_r = np.extract(a[3]<light_cut, a[1])
        bt_m = sel_bt_r - np.mean(sel_bt_r)
        bt_rms = np.sqrt(np.sum(bt_m*bt_m)/bt_m.size)
        if bt_rms < rms_cut:
            result[-1] = 1

    return np.array(result)


def check_bulge_dominates_always(data,light_cut):
    result = []
    for a in data['bt_prof']:
        result += [0]
        sel_bt_r = np.extract(a[3]<light_cut, a[1])-0.5
        transition = np.where(sel_bt_r< 0.0,1,0)
        if np.sum(transition)==0:
            result[-1] = 1
                
    return np.array(result)

def check_disk_dominates_always(data, light_cut):
    result = []
    for a in data['bt_prof']:
        result += [0]
        sel_bt_r = np.extract(a[3]<light_cut, a[1])-0.5
        transition = np.where(sel_bt_r> 0.0,1,0)
        if np.sum(transition)==0:
            result[-1] = 1
                
    return np.array(result)

def check_inverted_disk(data, rad_cut):
    result = []
    for c, a,b in zip(data['galcount'],data['bt_prof'], data['BT']):
        result += [0]
        if b< 0.75:
            sel_bt_r = np.extract(a[0]<rad_cut, a[1])-0.5
            transition = np.where(np.where(sel_bt_r[:-1]< 0,1,0)*np.where(sel_bt_r[1:]> 0,1,0)==1)[0]+1
            trans_to_disk =np.where(np.where(sel_bt_r[:-1]> 0,1,0)*np.where(sel_bt_r[1:]< 0,1,0)==1)[0]+1
            if len(transition)>0:
                first_trans = np.min(transition)
                if len(trans_to_disk) > 0:
                    to_disk_min = np.min(trans_to_disk)
                else:
                    to_disk_min = 999.0
                if first_trans< to_disk_min:
                    inner_val = np.sum(sel_bt_r[:first_trans])
                    if inner_val < 0:
                        result[-1] = 1

    return np.array(result)

##############################################
# END Flag test functions
#############################################

def run_auto_flags(model, band, folder_num, print_flags=False):
    """Runs the autoflags and produces autoflag picklefile that can be loaded
to a mysql database"""
    
    infile = open('/home/ameert/to_classify/flagfiles/%s/%s/total_flag_%d.pickle' %(band,model,folder_num))
    data = pickle.load(infile)
    infile.close()

    infile = open('/home/ameert/to_classify/flagfiles/%s/%s/total_profile_%d.pickle' %(band,model,folder_num))
    profile_data = pickle.load(infile)
    infile.close()

    profile_dict = dict(zip(profile_data['galcount'], zip(profile_data['chi_prof'], profile_data['bt_prof'], profile_data['im_ctr'])))

    data['im_ctr'] = [ profile_dict.get(a, (([-999.0],[-999.0]),([-999.0], [-999.0], [-999.0],[-999.0]), (-999.0, -999.0)))[2] for a in data['galcount']]
    data['chi_prof'] = [ profile_dict.get(a, (([-999.0],[-999.0]),([-999.0], [-999.0], [-999.0],[-999.0]), (-999.0, -999.0)))[0] for a in data['galcount']]
    data['bt_prof'] = [ profile_dict.get(a, (([-999.0],[-999.0]),([-999.0], [-999.0], [-999.0],[-999.0]), (-999.0, -999.0)))[1] for a in data['galcount']]

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
    #high_chi = np.where(np.where(new_chi>autoflag_config['chicut'], 1,0)+np.where(new_der+new_chi>7,1,0)*np.where(new_chi>5,1,0)>0, 1,0)
    high_chi = np.where(new_chi>autoflag_config['chicut'], 1,0)
    center_probs = np.where(separation>autoflag_config['max_sep'], 1,0)
    posang_diff = np.where(data['ba_disk']<autoflag_config['posang_d']['ba_cut'],1,0) * \
                 np.where(data['ba_bulge']<autoflag_config['posang_d']['ba_cut'],1,0) * \
                 np.where(pa_diff>autoflag_config['posang_d']['pa_cut'], 1,0)    

    no_bulge = np.where(autoflag_config['bulge_cut'][band](data['BT'], data['m_bulge']), 1,0)
    no_disk = np.where(autoflag_config['disk_cut'][band](data['BT'], data['m_disk']), 1,0)  

    parallel_com_flag = parallel_com(data, autoflag_config['par_com'])*np.where(no_bulge==1, 0,1)*np.where(no_disk==1, 0,1)*np.where(data['n_bulge']<autoflag_config['disky_n'],1,0)

    posang_disk = posang_diff*np.where(data['BT']>=0.5, 1,0)*np.where(no_disk==1, 0,1)

    disk_fitting_inner = check_inverted_disk(data,autoflag_config['disk_rad_cut'])*np.where(no_disk==1, 0,1)*np.where(no_bulge==1, 0,1)

    disk_is_sky = np.where(disk_vs_sky>autoflag_config['disk_sky_cut'], 1,0)* np.where(data['ba_disk']>autoflag_config['disk_sky_ba'], 1,0)*np.where(no_disk==1, 0,1)
    disk_contamination = np.where(disk_vs_sky>autoflag_config['disk_sky_cut'], 1,0)* np.where(data['ba_disk']<=autoflag_config['disk_sky_ba'], 1,0)*np.where(no_disk==1, 0,1)
    high_e_disk = np.where(data['ba_disk']<autoflag_config['disk_ba_cut'],1,0)*np.where(data['BT']>autoflag_config['disk_ba_BT'],1,0)*np.where(no_disk==1, 0,1)
    disk_dominates_always = check_disk_dominates_always(data, autoflag_config['disk_dom_light'])*np.where(no_bulge==1, 0,1)

    posang_bulge = posang_diff*np.where(data['BT']<0.5, 1,0)*np.where(no_bulge==1, 0,1)        
    bulge_fitting_outer = check_inverted_bulge(data, autoflag_config['bulge_light_cut'])*np.where(no_bulge==1, 0,1)
    bulge_is_sky = np.where(bulge_vs_sky>autoflag_config['bulge_sky_cut'], 1,0)* np.where(data['ba_bulge']>autoflag_config['bulge_sky_ba'], 1,0)*np.where(no_bulge==1, 0,1)
    bulge_contamination = np.where(bulge_vs_sky>autoflag_config['bulge_sky_cut'], 1,0)* np.where(data['ba_bulge']<=autoflag_config['bulge_sky_ba'], 1,0)*np.where(no_bulge==1, 0,1)
    high_e_bulge = np.where(data['ba_bulge']<autoflag_config['bulge_ba_cut'],1,0)*np.where(data['BT']<autoflag_config['bulge_ba_BT'],1,0)*np.where(no_bulge==1, 0,1)
    bulge_is_disk_flag = np.where(rad_rat>autoflag_config['bulge_disk_rat'],1,0)*np.where(data['n_bulge']<autoflag_config['disky_n'],1,0)*np.where(no_bulge==1, 0,1)
    bulge_low_n_flag = np.where(bulge_is_disk_flag,0,1)*np.where(data['n_bulge']<autoflag_config['disky_n'],1,0)*np.where(no_bulge==1, 0,1)
    bulge_dominates_always = check_bulge_dominates_always(data,autoflag_config['bulge_dom_light'])*np.where(no_disk==1, 0,1)

    flip_com_flag = np.where(bulge_is_disk_flag+bulge_fitting_outer+disk_fitting_inner >1, 1,0)| np.where(disk_fitting_inner+bulge_low_n_flag >1, 1,0)|np.where(bulge_is_disk_flag >=1, 1,0)|np.where(no_disk+bulge_low_n_flag >1, 1,0)

    tiny_bulge = np.where(data['r_bulge']*np.sqrt(data['ba_bulge'])/0.396>0,1,0)* np.where(data['r_bulge']*np.sqrt(data['ba_bulge'])/0.396<=0.5,1,0)

    auto_disk_total = np.where(disk_is_sky+disk_contamination+ disk_fitting_inner*np.where(bulge_is_disk_flag+bulge_fitting_outer+bulge_low_n_flag+ parallel_com_flag>0,0,1)+high_e_disk*posang_disk+parallel_com_flag>0,1,0)
    auto_bulge_total = np.where(bulge_fitting_outer*np.where(disk_fitting_inner+bulge_is_disk_flag>0,0,1)+bulge_is_sky+bulge_contamination+ high_e_bulge*posang_bulge+parallel_com_flag>0,1,0)
    bad_total_flag = np.where((np.where(disk_is_sky+disk_contamination+bulge_is_sky+bulge_contamination+center_probs>0, 1,0) + np.where(no_bulge+no_disk+disk_dominates_always+bulge_dominates_always>1,1,0))>0,1,0)+high_chi

    # if galfit failed, or some measurement is wrong in the pa
    galfit_fail = np.where(data['galfit_flag']==1,1,0) #| np.where((bulge_dominates_always+disk_dominates_always+no_bulge+no_disk)>1, 1,0)

    # only log disk flags if disk is included
    if model in ['devexp', 'serexp']:
        auto_flags += posang_disk * 2**autoflag_dict['disk pa problem']
        auto_flags += disk_fitting_inner * 2**autoflag_dict['disk fitting inner']
        auto_flags += disk_is_sky * 2**autoflag_dict['disk is sky']
        auto_flags += disk_contamination * 2**autoflag_dict['disk contaminated']
        auto_flags += high_e_disk * 2**autoflag_dict['high e disk']
        auto_flags += auto_disk_total * 2**autoflag_dict['bad disk']
        auto_flags += disk_dominates_always * 2**autoflag_dict['disk dominates always']
        auto_flags += parallel_com_flag * 2**autoflag_dict['parallel components']
        auto_flags += flip_com_flag * 2**autoflag_dict['flip components']

    auto_flags += no_disk * 2**autoflag_dict['no disk likely']
    auto_flags += bulge_is_disk_flag * 2**autoflag_dict['bulge is disk']
    auto_flags += posang_bulge * 2**autoflag_dict['bulge pa problem']
    auto_flags += bulge_fitting_outer * 2**autoflag_dict['bulge fitting outer']
    auto_flags += bulge_is_sky * 2**autoflag_dict['bulge is sky']
    auto_flags += bulge_contamination * 2**autoflag_dict['bulge contaminated']
    auto_flags += no_bulge * 2**autoflag_dict['no bulge likely']
    auto_flags += high_e_bulge * 2**autoflag_dict['high e bulge']
    auto_flags += bulge_low_n_flag * 2**autoflag_dict['low n bulge']
    auto_flags += bulge_dominates_always * 2**autoflag_dict['bulge dominates always']

    auto_flags +=  auto_bulge_total * 2**autoflag_dict['bad bulge']

    auto_flags += center_probs * 2**autoflag_dict['centering']
    auto_flags += high_chi * 2**autoflag_dict['high chi^2']
    auto_flags += bad_total_flag * 2**autoflag_dict['Bad total fit']
    auto_flags += data['polluted_flag'] * 2**autoflag_dict['polluted']
    auto_flags += data['fractured_flag'] * 2**autoflag_dict['fractured']
    auto_flags += tiny_bulge * 2**autoflag_dict['tinybulge']



    # if galfit failed, lets clear out all the flags...They are junk!
    auto_flags = np.where(galfit_fail==1, 0, auto_flags)
    auto_flags += galfit_fail * 2**autoflag_dict['galfit failure']

    outfile = open('/home/ameert/to_classify/flagfiles/%s/%s/autoflags_%d.pickle' %(band, model,folder_num), 'w')
    pickle.dump({'galcount':data['galcount'],'autoflags':auto_flags},outfile)
    outfile.close()
    if print_flags:
        print "autoflags"
        for a in zip(data['galcount'], auto_flags):
            print a[0], a[1]
    return


def load_autoflag(folder_num, info_dict, print_info = False):
    cursor = info_dict['cursor']

    if print_info:
        print 'loading folder %d' %folder_num
        print '/home/ameert/to_classify/flagfiles/%s/%s/autoflags_%d.pickle' %(info_dict['band'],info_dict['model'],folder_num)
    infile = open('/home/ameert/to_classify/flagfiles/%s/%s/autoflags_%d.pickle' %(info_dict['band'],info_dict['model'],folder_num))
    data = pickle.load(infile)
    infile.close()

    for galcount,flagval in zip(data['galcount'], data['autoflags']):
        cmd = """update {table} set flag = {finalval} where galcount = {galcount} and band = '{band}' and model = '{model}' and ftype = '{autoflag_ftype}';""".format(table = info_dict['table'], finalval = flagval, band=info_dict['band'], model=info_dict['model'], galcount = galcount, autoflag_ftype=info_dict['autoflag_ftype'])
        if print_info:
            print cmd
        cursor.execute(cmd)

    return

