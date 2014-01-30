#++++++++++++++++++++++++++
#
# TITLE: mysql_funcs
#
# PURPOSE: this program modifies and combines
#          data from pymorph fits into a single
#          table.
#
# INPUTS:          
#
# OUTPUTS: NONE, but does create a new fit table with new
#          columns calculated by us.
#
# PROGRAM CALLS: NONE...yet
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 25 MAY 2011
#
#-----------------------------------

from mysql_class import * 
import numpy as np
import pylab as pl
import datetime

def make_big_table(table_name, filter, cursor, max_galcount = 26153):

    cmd = 'CREATE TABLE ' + table_name + ' '
    cmd += """(
    galcount               int primary key,
    Name_%s                varchar(500) default -888,
    Date                   varchar(50) default -888,    
    Filter                 varchar(500) default -888,
    z                      float default -888,                   
    dis_modu               float default -888,          
    MorphType              int(11) default -888,        
    SexSky                 float default -888,
    mag_auto               float default -888,
    mag_err_auto           float default -888,
    sex_halflight_pix      float default -888,
    zeropoint_pymorph      float default -888,
    C                      float default -888, 
    C_err                  float default -888,
    A                      float default -888,
    A_err                  float default -888,
    S                      float default -888,
    S_err                  float default -888,
    G                      float default -888,
    M                      float default -888,
    Comments               varchar(1000) default -888,  
    Ie_Dev                 float default -888,          
    Ie_DevExp              float default -888,          
    Ie_Ser                 float default -888,          
    Ie_SerExp              float default -888,          
    Ie_err_Dev             float default -888,          
    Ie_err_DevExp          float default -888,          
    Ie_err_Ser             float default -888,          
    Ie_err_SerExp          float default -888,
    AbsMagBulge_Dev        float default -888,          
    AbsMagBulge_DevExp     float default -888,          
    AbsMagBulge_Ser        float default -888,          
    AbsMagBulge_SerExp     float default -888,          
    re_pix_Dev             float default -888,          
    re_pix_DevExp          float default -888,          
    re_pix_Ser             float default -888,          
    re_pix_SerExp          float default -888,          
    re_err_pix_Dev         float default -888,          
    re_err_pix_DevExp      float default -888,          
    re_err_pix_Ser         float default -888,          
    re_err_pix_SerExp      float default -888,          
    re_kpc_Dev             float default -888,          
    re_kpc_DevExp          float default -888,          
    re_kpc_Ser             float default -888,          
    re_kpc_SerExp          float default -888,          
    re_err_kpc_Dev         float default -888,          
    re_err_kpc_DevExp      float default -888,          
    re_err_kpc_Ser         float default -888,          
    re_err_kpc_SerExp      float default -888,          
    n_Dev                  float default -888,          
    n_DevExp               float default -888,          
    n_Ser                  float default -888,          
    n_SerExp               float default -888,          
    n_err_Dev              float default -888,          
    n_err_DevExp           float default -888,          
    n_err_Ser              float default -888,          
    n_err_SerExp           float default -888,          
    eb_Dev                 float default -888,          
    eb_DevExp              float default -888,          
    eb_Ser                 float default -888,          
    eb_SerExp              float default -888,
    eb_err_Dev             float default -888,          
    eb_err_DevExp          float default -888,          
    eb_err_Ser             float default -888,          
    eb_err_SerExp          float default -888,
    bboxy_Dev              float default -888,
    bboxy_DevExp           float default -888,
    bboxy_Ser              float default -888,
    bboxy_SerExp           float default -888,
    bboxy_err_Dev          float default -888,
    bboxy_err_DevExp       float default -888,
    bboxy_err_Ser          float default -888,
    bboxy_err_SerExp       float default -888,
    Id_Dev                 float default -888,          
    Id_DevExp              float default -888,          
    Id_Ser                 float default -888,          
    Id_SerExp              float default -888,         
    Id_err_Dev             float default -888,          
    Id_err_DevExp          float default -888,          
    Id_err_Ser             float default -888,          
    Id_err_SerExp          float default -888,         
    AbsMagDisk_Dev         float default -888,          
    AbsMagDisk_DevExp      float default -888,          
    AbsMagDisk_Ser         float default -888,          
    AbsMagDisk_SerExp      float default -888,         
    rd_pix_Dev             float default -888,          
    rd_pix_DevExp          float default -888,          
    rd_pix_Ser             float default -888,          
    rd_pix_SerExp          float default -888,          
    rd_err_pix_Dev         float default -888,          
    rd_err_pix_DevExp      float default -888,          
    rd_err_pix_Ser         float default -888,          
    rd_err_pix_SerExp      float default -888,          
    rd_kpc_Dev             float default -888,          
    rd_kpc_DevExp          float default -888,          
    rd_kpc_Ser             float default -888,         
    rd_kpc_SerExp          float default -888,          
    rd_err_kpc_Dev         float default -888,          
    rd_err_kpc_DevExp      float default -888,          
    rd_err_kpc_Ser         float default -888,          
    rd_err_kpc_SerExp      float default -888,         
    ed_Dev                 float default -888,          
    ed_DevExp              float default -888,          
    ed_Ser                 float default -888,          
    ed_SerExp              float default -888,          
    ed_err_Dev             float default -888,          
    ed_err_DevExp          float default -888,          
    ed_err_Ser             float default -888,          
    ed_err_SerExp          float default -888,          
    dboxy_Dev              float default -888,
    dboxy_DevExp           float default -888,
    dboxy_Ser              float default -888,
    dboxy_SerExp           float default -888,
    dboxy_err_Dev          float default -888,
    dboxy_err_DevExp       float default -888,
    dboxy_err_Ser          float default -888,
    dboxy_err_SerExp       float default -888,
    BT_Dev                 float default -888,          
    BT_DevExp              float default -888,          
    BT_Ser                 float default -888,          
    BT_SerExp              float default -888,
    BT_err_Dev             float default -888,          
    BT_err_DevExp          float default -888,          
    BT_err_Ser             float default -888,          
    BT_err_SerExp          float default -888,
    BD_Dev                 float default -888,
    BD_DevExp              float default -888,
    BD_Ser                 float default -888,          
    BD_SerExp              float default -888,
    BD_err_Dev             float default -888,          
    BD_err_DevExp          float default -888,          
    BD_err_Ser             float default -888,          
    BD_err_SerExp          float default -888,
    fit_Dev                float default -888,
    fit_DevExp             float default -888,
    fit_Ser                float default -888,
    fit_SerExp             float default -888,
    flag_Dev               float default -888,
    flag_DevExp            float default -888,
    flag_Ser               float default -888,
    flag_SerExp            float default -888,
    chi2nu_Dev             float default -888, 
    chi2nu_DevExp          float default -888, 
    chi2nu_Ser             float default -888, 
    chi2nu_SerExp          float default -888, 
    GalSky_Dev             float default -888,          
    GalSky_DevExp          float default -888,          
    GalSky_Ser             float default -888,          
    GalSky_SerExp          float default -888,
    bpa_Dev                float default -888,
    bpa_DevExp             float default -888,
    bpa_Ser                float default -888,
    bpa_SerExp             float default -888,
    dpa_Dev                float default -888,
    dpa_DevExp             float default -888,
    dpa_Ser                float default -888,
    dpa_SerExp             float default -888,
    bxc_Dev                float default -888,
    bxc_DevExp             float default -888,
    bxc_Ser                float default -888,
    bxc_SerExp             float default -888,
    byc_Dev                float default -888,
    byc_DevExp             float default -888,
    byc_Ser                float default -888,
    byc_SerExp             float default -888,
    dxc_Dev                float default -888,
    dxc_DevExp             float default -888,
    dxc_Ser                float default -888,
    dxc_SerExp             float default -888,
    dyc_Dev                float default -888,
    dyc_DevExp             float default -888,
    dyc_Ser                float default -888,
    dyc_SerExp             float default -888
    );""" %(filter)

    #print cmd
    cursor.execute(cmd)
    for count in range(0, max_galcount):
        cmd = "Insert Into %s (galcount) Values (%d);" %(table_name, count + 1)
        # print cmd
        cursor.execute(cmd)
        
    return

def load_table_main_data(table_name,table_data_name,cursor, curr_filter):

    today = str(datetime.datetime.today())
    today = today.split()[0]
    
    cmd = """Update %s as a, %s as b SET a.Name_%s = b.Name,a.Date = '%s',a.Filter = '%s',a.z = b.z, a.zeropoint_pymorph = 25.256,a.C = b.C,a.C_err = b.C_err,a.A = b.A,a.A_err = b.A_err,a.S = b.S,a.S_err = b.S_err,a.G = b.G,a.M = b.M,a.mag_auto = b.mag_auto,a.mag_err_auto = b.magerr_auto,a.sex_halflight_pix = b.HalfRadius where a.galcount = b.galcount;""" %(table_name,table_data_name,curr_filter, str(today),curr_filter)
    print cmd
    cursor.execute(cmd)
    

    return


def remove_nulls(table_stem, cursor, fit_types, filter):
    for model in fit_types:
        for name_col in all_cols:
            cmd = 'update ' + table_stem+model + ' set ' + name_col + ' = -888 where '+ name_col +" is null) ;"
            print cmd
            #cursor.execute(cmd)


def update_single_tables(cursor, filter = 'r', models =['dev','ser','devexp','serexp']):
    
    for model in models:
        cmd = "alter table %s_%s add column galcount int first;" %(filter, model)
        cursor.execute(cmd)

        cmd = "select Name from %s_%s;" %(filter, model)
        names, = cursor.get_data(cmd)

        for name in names:
            ind = int(name.split('_')[0])

            cmd = "Update %s_%s Set galcount = %d where Name = '%s';" %(filter, model, ind, name)
            print cmd
            cursor.execute(cmd)

    return

def add_bt_bd_err(cursor, models, table_stem):
    for model in models:
        cmd = 'alter table '+table_stem+model+' add column BT_err float default -888 after BT;'
        print cmd
        cursor.execute(cmd)
        cmd = 'alter table '+table_stem+model+' add column BD_err float default -888 after BD;'
        print cmd
        cursor.execute(cmd)

        if (model == 'dev') or (model == 'ser'):
            cmd = 'Update '+table_stem+model+' SET BT = 1, BD = -888, BT_err = 0, BD_err = -888;'
            print cmd
            cursor.execute(cmd)
        else:
            
            cmd = 'select galcount, BD, Ie_err, Id_err from '+table_stem+model+ ';'
            galcount, BD, Ie_err, Id_err = cursor.get_data(cmd)

            for curr_galcount, curr_bd, curr_ie_err, curr_id_err in zip(galcount, BD, Ie_err, Id_err):
                try:
                    BD_err = .921*curr_bd*np.sqrt(curr_ie_err**2.0 + curr_id_err**2.0)
                    BT_err = (1.0/(curr_bd + 1.0)**2) * BD_err
                    cmd = 'update '+table_stem+model+' SET BT_err = %f, BD_err = %f where galcount = %d;' %(BT_err, BD_err, curr_galcount)
                    print cmd
                    cursor.execute(cmd)
                except:
                    pass
    return
    
def combine_models(cursor, models,table_stem, table_name,  filter = 'r'):

    for model in models:
        cmd = 'Update '+table_name + ' as a, '+table_stem+model+ ' as b SET a.dis_modu=b.dis_modu, a.mag_auto = b.mag_auto, a.mag_err_auto = b.magerr_auto, a.sexsky = b.sexsky, a.Ie_%s=b.Ie,a.Ie_err_%s=b.Ie_err,a.AbsMagBulge_%s=b.Ie - b.dis_modu,a.re_pix_%s=b.re_pix,a.re_err_pix_%s=b.re_err_pix,a.re_kpc_%s=b.re_kpc, a.re_err_kpc_%s=b.re_err_kpc, a.n_%s=b.n, a.n_err_%s=b.n_err,a.eb_%s=b.eb, a.eb_err_%s=b.eb_err, a.bboxy_%s = b.bboxy, a.bboxy_err_%s = b.bboxy_err, a.Id_%s = b.Id, a.Id_err_%s = b.Id_err, a.AbsMagDisk_%s=b.Id-b.dis_modu, a.rd_pix_%s=b.rd_pix,a.rd_err_pix_%s = b.rd_err_pix, a.rd_kpc_%s=b.rd_kpc, a.rd_err_kpc_%s = b.rd_err_kpc, a.ed_%s=b.ed,a.ed_err_%s = b.ed_err, a.dboxy_%s = b.dboxy, a.dboxy_err_%s = b.dboxy_err, a.BT_%s=b.BT, a.BT_err_%s = b.BT_err, a.BD_%s = b.BD, a.BD_err_%s=b.BD_err, a.fit_%s=b.fit, a.flag_%s=b.flag, a.chi2nu_%s=b.chi2nu, a.GalSky_%s=b.GalSky, a.bpa_%s = -888, a.dpa_%s=-888, a.bxc_%s=-888, a.byc_%s=-888, a.dxc_%s=-888, a.dyc_%s = -888  where a.galcount = b.galcount and b.run = 1; ' %(model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model,model, model, model)

        print cmd
        cursor.execute(cmd)
    return

        
        
        
