import os
from mysql_class import *
import sys
import numpy

cursor = mysql_connect('pymorph', 'pymorph','pymorph9455', 'shredder')

result_head = 'Name_1,ra_gal_2,dec_gal_3,z_4,MorphType_5,mag_auto_6,magerr_auto_7,SexHalfRad_8,num_targets_9,C_10,C_err_11,A_12,A_err_13,S_14,S_err_15,G_16,M_17,magzp_18,bulge_xctr_19,bulge_xctr_err_20,bulge_yctr_21,bulge_yctr_err_22,Ie_23,Ie_err_24,AvgIe_25,AvgIe_err_26,re_pix_27,re_pix_err_28,re_kpc_29,re_kpc_err_30,n_31,n_err_32,eb_33,eb_err_34,bpa_35,bpa_err_36,bboxy_37,bboxy_err_38,disk_xctr_39,disk_xctr_err_40,disk_yctr_41,disk_yctr_err_42,Id_43,Id_err_44,rd_pix_45,rd_pix_err_46,rd_kpc_47,rd_kpc_err_48,ed_49,ed_err_50,dpa_51,dpa_err_52,dboxy_53,dboxy_err_54,BD_55,BT_56,p_xctr_57,p_xctr_err_58,p_yctr_59,p_yctr_err_60,Ip_61,Ip_err_62,Pfwhm_63,Pfwhm_kpc_64,bar_xctr_65,bar_xctr_err_66,bar_yctr_67,bar_yctr_err_68,Ibar_69,Ibar_err_70,rbar_pix_71,rbar_pix_err_72,rbar_kpc_73,rbar_kpc_err_74,n_bar_75,n_bar_err_76,ebar_77,ebar_err_78,barpa_79,barpa_err_80,barboxy_81,barboxy_err_82,chi2nu_83,Goodness_84,run_85,SexSky_86,YetSky_87,GalSky_88,GalSky_err_89,dis_modu_90,distance_91,fit_92,FitFlag_93,flag_94,Manual_flag_95,Comments_96,Date_97,Version_98,Filter_99,Total_Run_100,rootname_101,Morphology_102,ObsID_103'

head_split = result_head.split(',')

cmd_base =  [ '_'.join(a.split('_')[0:-1]) for a in head_split]
cmd_base = 'select ' + ','.join(cmd_base) +' from '

for model in ['dev','ser','devexp','serexp']:
    for count in range(1,2684):
        data = cursor.get_data('%s full_dr7_r_%s where galcount > %d and galcount <= %d order by galcount;' %(cmd_base, model, (count-1)*250, count * 250))
        path = '/data2/home/ameert/catalog/r/fits/%s/%04d' %(model, count)
        os.rename('%s/result.csv' %path, '%s/result.original' %path)
        
        outfile = open('%s/result.csv' %path,'w')
        outfile.write(result_head + '\n')
        
        for galcount in range(len(data[0])):
            params = [ str(a[galcount]) for a in data]
            line = ','.join(params) + '\n'
            outfile.write(line)
        outfile.close()
            

