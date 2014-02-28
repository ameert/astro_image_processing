#OLD FLAGGING used in 2012
#



from flagfunc import *
import numpy as np
from mysql_class import *

def Get_FinalFlag(flagname):
        FlagDict = dict([('Total', 0),
                         ('BT', 1),
                         ('r_bulge', 2),
                         ('n_bulge', 3),
                         ('ba_bulge', 4),
			 ('phi_bulge', 5),
                         ('r_disk', 6),
			 ('ba_disk', 7),
			 ('phi_disk', 8),
			 ('neighbor_fit', 9)
                         ])	                 
        return FlagDict[flagname]

def set_flag_arr(final_flag, bad_tot, param_name):
    """sets the flag array for the three bands g,r,i depending on 
    the array passed in bad_tot"""
    for count, isbad in enumerate(bad_tot):
        if isbad ==1:
            try:
                final_flag[count] = SetFlag(final_flag[count], Get_FinalFlag(param_name))
            except badflag:
                pass
                                           
    return final_flag

def get_bad_band(gr_val, gi_val, ri_val):
    diff_array = np.array([gr_val, gi_val, ri_val])
    is_greater = np.where(diff_array >= trigger, 1,0)
    sorted_index = np.argsort(diff_array)[::-1]
    
    num_greater = np.sum(is_greater)
    
    if num_greater == 3:
        bad_band = [1,1,1]
    elif num_greater == 2:
        bad_band = [0,0,0]
        for band, check in zip([0,1,2], [np.array([1,1,0], dtype=int),
                                         np.array([1,0,1], dtype=int),
                                         np.array([0,1,1], dtype=int)]):
            
            if np.sum(is_greater*check)==2:
                bad_band[band] = 1
    else:
        bad_band = [0,0,0]
    return bad_band

            
trigger = 5.0
model = 'ser'
cursor = mysql_connect('catalog','pymorph','pymorph','')


gal_names = {'galcount':0, 'flag_g':1, 'flag_r':2, 'flag_i':3, 
'FitFlag_g':4, 'FitFlag_r':5, 'FitFlag_i':6, 
'Manual_flag':7, 'Manual_flag':8, 'Manual_flag':9, 
'total':10, 'total_gr':11, 'total_gi':12, 'total_ri':13,
'r_bulge_tot':14, 'r_bulge_gr':15, 'r_bulge_gi':16, 'r_bulge_ri':17,
'n_bulge_tot':18, 'n_bulge_gr':19, 'n_bulge_gi':20, 'n_bulge_ri':21,
'ba_bulge_tot':22, 'ba_bulge_gr':23, 'ba_bulge_gi':24, 'ba_bulge_ri':25,
'phi_bulge_tot':26, 'phi_bulge_gr':27, 'phi_bulge_gi':28, 'phi_bulge_ri':29,
'r_disk_tot':30, 'r_disk_gr':31, 'r_disk_gi':32, 'r_disk_ri':33,
'ba_disk_tot':34, 'ba_disk_gr':35, 'ba_disk_gi':36, 'ba_disk_ri':37,
'phi_disk_tot':38, 'phi_disk_gr':39, 'phi_disk_gi':40, 'phi_disk_ri':41,
'BT_tot':42, 'BT_gr':43, 'BT_gi':44, 'BT_ri':44
}

cmd = """select a.galcount, a.flag, b.flag, c.flag, 
a.FitFlag, b.FitFlag, c.FitFlag, 
a.Manual_flag, b.Manual_flag, c.Manual_flag, 
d.total, d.total_gr, d.total_gi, d.total_ri,
d.r_bulge_tot, d.r_bulge_gr, d.r_bulge_gi, d.r_bulge_ri,
d.n_bulge_tot, d.n_bulge_gr, d.n_bulge_gi, d.n_bulge_ri,
d.ba_bulge_tot, d.ba_bulge_gr, d.ba_bulge_gi, d.ba_bulge_ri,
d.pa_bulge_tot, d.pa_bulge_gr, d.pa_bulge_gi, d.pa_bulge_ri,
d.r_disk_tot, d.r_disk_gr, d.r_disk_gi, d.r_disk_ri,
d.ba_disk_tot, d.ba_disk_gr, d.ba_disk_gi, d.ba_disk_ri,
d.pa_disk_tot, d.pa_disk_gr, d.pa_disk_gi, d.pa_disk_ri,
d.BT_tot, d.BT_gr, d.BT_gi, d.BT_ri 
from g_band_{model} as a, r_band_{model} as b, i_band_{model} as c, classify.agree_{model} as d where a.galcount = b.galcount and b.galcount = c.galcount and b.galcount = d.galcount;""".format(model = model)

data = cursor.get_data(cmd)

galaxy = np.array(data, dtype = float).T

for gal in  galaxy:
    final_flag = [0, 0, 0]

    if gal[gal_names['total']] >= trigger: #if the total sigma is greater than the trigger
        bad_tot = get_bad_band(gal[gal_names['total_gr']],gal[gal_names['total_gi']], gal[gal_names['total_ri']]) 
        final_flag = set_flag_arr(final_flag, bad_tot, 'Total')

    for param in ['r_bulge', 'n_bulge', 'ba_bulge', 'phi_bulge', 
                  'r_disk', 'ba_disk', 'phi_disk', 'BT']:

        if gal[gal_names[param+'_tot']] >= trigger: #if the total sigma is greater than the trigger
            bad_tot = get_bad_band(gal[gal_names[param+'_gr']],gal[gal_names[param+'_gi']], gal[gal_names[param+'_ri']]) 
            final_flag = set_flag_arr(final_flag, bad_tot, param)    
          
    # now check for approach to any limits using fitflag
    for fitflag_name, param in zip(['BT_AT_LIMIT','N_AT_LIMIT', 'RE_AT_LIMIT',
                                    'RD_AT_LIMIT','EB_AT_LIMIT','ED_AT_LIMIT'], 
                                   ['BT', 'n_bulge', 'r_bulge', 'r_disk',
                                    'ba_bulge', 'ba_disk']):
        
        for count, fitflag in enumerate([int(gal[gal_names['FitFlag_g']]),int(gal[gal_names['FitFlag_r']]),int(gal[gal_names['FitFlag_i']])]):
            if isset(fitflag, Get_FitFlag(fitflag_name)):
                try:
                    final_flag[count] = SetFlag(final_flag[count], Get_FinalFlag(param)) 
                except badflag:
                    pass
    
    #print gal[gal_names['galcount']], final_flag  
    for band, flagval in zip(['g','r','i'], final_flag):
        cmd = 'update %s_band_%s set FinalFlag = %d where galcount = %d;' %(band, model, flagval, gal[gal_names['galcount']])
        cursor.execute(cmd)

