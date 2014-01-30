from mysql_class import * 
import numpy as np
import sys

table_name = 'simard_sample'

cursor = mysql_connect('pymorph', 'pymorph','pymorph9455', 'shredder')


#cursor.execute('create table simard_sample (galcount int primary key );')

col1 = ['objid','z','SpecClass','arcsec_per_kpc','V_max', 'f_test_ser', 'f_test_devexp']
col2 = ['bigint default -99','float default -99','int default -99','float default -99','float default -99','float default -99','float default -99']

if 0:
    for cola, colb in zip(col1, col2):
        cmd = 'alter table simard_sample add column '+cola+' '+colb+';'
        print cmd
        cursor.execute(cmd)


    for count in range(1, 26154):
        cmd = 'insert into simard_sample (galcount) values (%d);' %count
        cursor.execute(cmd)


        cmd = 'update serexp as a, simard_sample as b set b.objid = a.objid, b.z = a.z,b.SpecClass=a.SpecClass,b.arcsec_per_kpc=a.arcsec_per_kpc,b.V_max=a.V_max, b.f_test_ser=a.f_test_ser, b.f_test_devexp=a.f_test_devexp where b.galcount = a.galcount;'
        cursor.execute(cmd)


old_col_names = ['mag_r_tot','mag_r_tot_err','BT_r','BT_r_err','re_kpc','re_kpc_err','eb','eb_err','rd_kpc','rd_kpc_err','n','n_err']

new_col_names = ['Ie', 'Ie_err', 'Id', 'Id_err', 'BT', 'BT_err', 're_kpc', 're_err_kpc', 'eb', 'eb_err', 'rd_kpc', 'rd_err_kpc', 'n', 'n_err']
 

models = ['ser','devexp','serexp']

for curr_col in new_col_names:
    for model in models:
        cmd = 'alter table simard_sample add column ' + curr_col + '_'+ model +' float default -888;'
        print cmd
        #cursor.execute(cmd)


for model in models:
    cmd = 'select objid, ' + ','.join(old_col_names) +' from '+ model + ' where galcount < 27000 and galcount > 0;'
    print cmd

    objid ,mag_tot, mag_tot_err, bt, bt_err, re, re_err, eb, eb_err, rd, rd_err, n, n_err = cursor.get_data(cmd)


    mag_tot = np.array(mag_tot)
    mag_tot_err = np.array(mag_tot_err)
    bt = np.array(bt)
    bt_err = np.array(bt_err)
    
    Ie = mag_tot -2.5*np.log10(bt)
    Id = mag_tot -2.5*np.log10(1.0-bt)

    Ie_err = np.sqrt( (mag_tot_err)**2.0 + (2.5/np.log(10))**2.0 *(bt_err/bt)**2.0)
    Id_err = np.sqrt( (mag_tot_err)**2.0 + (2.5/np.log(10))**2.0 *(bt_err/(1.0-bt))**2.0)

    low_bt = np.where(bt <= 0.00000001)

    for points in low_bt:
        Ie[points] = 999.0
        Ie_err[points] = 999.0

    high_bt = np.where(bt >= 0.9999999)

    for points in high_bt:
        Id[points] = 999.0
        Id_err[points] = 999.0

    for curr_objid, curr_ie, curr_ie_err, curr_id, curr_id_err, curr_bt, curr_bt_err, curr_re, curr_re_err, curr_eb, curr_eb_err, curr_rd, curr_rd_err, curr_n, curr_n_err in zip(objid, Ie, Ie_err, Id, Id_err, bt, bt_err, re, re_err, eb, eb_err, rd, rd_err, n, n_err):
        cmd = 'update '+ table_name + ' SET Ie_'+model+'='+str(curr_ie)+ ',Ie_err_'+model+'='+str(curr_ie_err)+ ',Id_'+model+'='+str(curr_id)+ ',Id_err_'+model+'='+str(curr_id_err)+ ',BT_'+model+'='+str(curr_bt)+ ',BT_err_'+model+'='+str(curr_bt_err)+ ',re_kpc_'+model+'='+str(curr_re)+ ',re_err_kpc_'+model+'='+str(curr_re_err)+ ',eb_'+model+'='+str(curr_eb)+ ',eb_err_'+model+'='+str(curr_eb_err)+ ',rd_kpc_'+model+'='+str(curr_rd)+ ',rd_err_kpc_'+model+'='+str(curr_rd_err)+ ',n_'+model+'='+str(curr_n)+ ',n_err_'+model+'='+str(curr_n_err)+ ' where objid = ' + str(curr_objid) + ';'

        #print cmd
        cursor.execute(cmd)
