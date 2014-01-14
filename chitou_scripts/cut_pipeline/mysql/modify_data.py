#++++++++++++++++++++++++++
#
# TITLE: modify_data
#
# PURPOSE: this program modifies and combines
#          data from pymorph fits into a single
#          table.
#
# INPUTS: num_div: number of divisions of the fit table
#         
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
# DATE: 7 JAN 2011
#
#-----------------------------------

import MySQLdb as mysql
from numpy import *
from pylab import *
from scipy import interpolate
from cosmocal import *
import datetime

def connect_to_mysql(dba,usr,pwd):
    try:
        Conn = mysql.connect (host = "localhost",
                                     user = "%s" %usr,
                                     passwd = "%s" %pwd,
                                     db = "%s" %dba)
    except mysql.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit (1)
    cursor = Conn.cursor()

    return cursor

def make_big_table(table_name, filter, cursor):

    cmd = 'CREATE TABLE ' + table_name + ' '
    cmd += """(
    Name_%s                varchar(500),
    galcount               int,
    specobjid              bigint(8),
    marc_id                bigint(20),
    probaE                 float,
    probaEll               float,
    probaS0                float,
    probaSab               float,
    probaScd               float,
    ask_class              float,
    nyc_Id                 int(11),
    nyc_dist               float,
    nyc_A_%s               float,
    nyc_r0_%s              float,
    nyc_n_ser_%s           float,
    Date                   varchar(50),    
    Filter                 varchar(500),
    ra_                    float,          
    dec_                   float,         
    z                      float,                   
    dis_modu               float,          
    ang_di_dist_kpc_arcsec float,          
    MorphType              int(11),        
    fracdev_%s             float,              
    velo_disp              float,         
    velo_disp_err          float,          
    extinction_%s          float,
    k_corr_%s              float,
    zeropoint_pymorph      float,
    zeropoint_sdss_%s      float,
    Comments               varchar(1000),  
    Ie_Dev                 float,          
    Ie_DevExp              float,          
    Ie_Ser                 float,          
    Ie_SerExp              float,          
    Ie_err_Dev             float,          
    Ie_err_DevExp          float,          
    Ie_err_Ser             float,          
    Ie_err_SerExp          float,
    AbsMagBulge_Dev        float,          
    AbsMagBulge_DevExp     float,          
    AbsMagBulge_Ser        float,          
    AbsMagBulge_SerExp     float,          
    re_pix_Dev             float,          
    re_pix_DevExp          float,          
    re_pix_Ser             float,          
    re_pix_SerExp          float,          
    re_err_pix_Dev         float,          
    re_err_pix_DevExp      float,          
    re_err_pix_Ser         float,          
    re_err_pix_SerExp      float,          
    re_kpc_Dev             float,          
    re_kpc_DevExp          float,          
    re_kpc_Ser             float,          
    re_kpc_SerExp          float,          
    re_err_kpc_Dev         float,          
    re_err_kpc_DevExp      float,          
    re_err_kpc_Ser         float,          
    re_err_kpc_SerExp      float,          
    n_Dev                  float,          
    n_DevExp               float,          
    n_Ser                  float,          
    n_SerExp               float,          
    n_err_Dev              float,          
    n_err_DevExp           float,          
    n_err_Ser              float,          
    n_err_SerExp           float,          
    eb_Dev                 float,          
    eb_DevExp              float,          
    eb_Ser                 float,          
    eb_SerExp              float,                                        
    Id_Dev                 float,          
    Id_DevExp              float,          
    Id_Ser                 float,          
    Id_SerExp              float,         
    Id_err_Dev             float,          
    Id_err_DevExp          float,          
    Id_err_Ser             float,          
    Id_err_SerExp          float,         
    AbsMagDisk_Dev         float,          
    AbsMagDisk_DevExp      float,          
    AbsMagDisk_Ser         float,          
    AbsMagDisk_SerExp      float,         
    rd_pix_Dev             float,          
    rd_pix_DevExp          float,          
    rd_pix_Ser             float,          
    rd_pix_SerExp          float,          
    rd_err_pix_Dev         float,          
    rd_err_pix_DevExp      float,          
    rd_err_pix_Ser         float,          
    rd_err_pix_SerExp      float,          
    rd_kpc_Dev             float,          
    rd_kpc_DevExp          float,          
    rd_kpc_Ser             float,         
    rd_kpc_SerExp          float,          
    rd_err_kpc_Dev         float,          
    rd_err_kpc_DevExp      float,          
    rd_err_kpc_Ser         float,          
    rd_err_kpc_SerExp      float,         
    ed_Dev                 float,          
    ed_DevExp              float,          
    ed_Ser                 float,          
    ed_SerExp              float,          
    BT_Dev                 float,          
    BT_DevExp              float,          
    BT_Ser                 float,          
    BT_SerExp              float,
    BD_Dev                 float,
    BD_DevExp              float,
    BD_Ser                 float,          
    BD_SerExp              float,
    fit_Dev                float,
    fit_DevExp             float,
    fit_Ser                float,
    fit_SerExp             float,
    flag_Dev               float,
    flag_DevExp            float,
    flag_Ser               float,
    flag_SerExp            float,
    chi2nu_Dev             float, 
    chi2nu_DevExp          float, 
    chi2nu_Ser             float, 
    chi2nu_SerExp          float, 
    GalSky_Dev             float,          
    GalSky_DevExp          float,          
    GalSky_Ser             float,          
    GalSky_SerExp          float          
    )""" %(filter,filter,filter,filter,filter,filter,filter,filter)

    cursor.execute(cmd)
    
    return

def combine_small_tables(number_of_tables, filter, cursor,fit_types):
    
    for type in fit_types:
        cmd = 'CREATE TABLE ' + filter + '_' + type + ' LIKE ' + type + '1;'
        cursor.execute(cmd)

        for number in range(1,number_of_tables+1):
            cmd = 'INSERT INTO ' + filter + '_' + type + ' SELECT * FROM ' + type + str(number) + ';'
            cursor.execute(cmd)
        cmd = 'ALTER IGNORE TABLE ' + filter + '_' + type + ' ADD UNIQUE INDEX(Name_'+filter+',Morphology)'
        cursor.execute(cmd)
        
    return

def load_table_main_data(table_name,cursor, fit_types, curr_filter):

    ext_type = 'extinction_%s' %(curr_filter)
    zp_type = 'aa_%s' %(curr_filter)
    
    today = datetime.date.today()

    cmd = """INSERT INTO %s (Name_%s, galcount, specobjid, marc_id, probaE,probaEll,probaS0,
    probaSab,probaScd,ask_class,nyc_Id,nyc_dist,nyc_A_%s,nyc_r0_%s,nyc_n_ser_%s,
    Date,Filter,ra_,dec_,z,dis_modu,ang_di_dist_kpc_arcsec,MorphType,fracdev_%s,
    velo_disp,velo_disp_err,extinction_%s,k_corr_%s,zeropoint_pymorph,zeropoint_sdss_%s,Comments)
    SELECT Name_%s, galcount,specobjid,marc_id,probaE,probaEll,probaS0,probaSab,probaScd,
    ask_class,nyc_Id,nyc_dist,nyc_A_%s,nyc_r0_%s,nyc_ser_%s,'%s','%s',ra_,dec_,z,dis_modu,          
    ang_di_dist_kpc_arcsec,MorphType,fracdev_%s,velo_disp,velo_disp_err,extinction_%s,
    k_corr_%s, 25.256,zeropoint_sdss_%s,Comments FROM sdss_main;""" %(table_name,curr_filter, curr_filter, curr_filter,curr_filter, curr_filter, curr_filter, curr_filter, curr_filter, curr_filter, curr_filter, curr_filter,curr_filter,str(today),curr_filter, curr_filter, curr_filter, curr_filter, curr_filter)
    #cursor.execute(cmd)
    
    cmd = 'ALTER IGNORE TABLE ' + table_name + ' ADD UNIQUE INDEX(Name_'+curr_filter+')'
    #cursor.execute(cmd)
        
    for type in fit_types:
        cmd = """select Name, Ie, Ie_err, re_pix, re_err_pix,Id,Id_err, rd_pix, rd_err_pix, n,n_err,
        eb,ed,BT,BD,fit, flag, chi2nu, GalSky from """ + curr_filter + '_' + type +';'
        cursor.execute(cmd)
        print cmd
        rows = cursor.fetchall()
        rows = list(rows)
        count = 0
        for row in rows:
            cmd = 'update '+ table_name + ' set Ie_' + type + '=' + str(row[1]) + ', Ie_err_' + type + '=' + str(row[2]) + ', re_pix_' + type + '=' + str(row[3]) + ', re_err_pix_' + type + '=' + str(row[4]) + ',Id_' + type + '=' + str(row[5]) + ',Id_err_' + type + '=' + str(row[6]) + ', rd_pix_' + type + '=' + str(row[7]) + ', rd_err_pix_' + type + '=' + str(row[8]) + ', n_' + type + '=' + str(row[9]) + ',n_err_' + type + '=' + str(row[10]) + ',eb_' + type + '=' + str(row[11]) + ',ed_' + type + '=' + str(row[12]) + ',BT_' + type + '=' + str(row[13]) + ',BD_' + type + '=' + str(row[14]) + ', fit_' + type + '=' + str(row[15]) + ', flag_' + type + '=' + str(row[16]) + ', chi2nu_' + type + '=' + str(row[17]) + ', GalSky_' + type + '=' + str(row[18]) + " where Name_"+curr_filter+"='0" + str(row[0]) +"';"
            cursor.execute(cmd)
            print cmd
    return




###DO NOT USE THIS####
def calc_dist_stuff(table_name, cursor):

    z_k = [] #kcorrection z
    k_k = [] #kcorrection
    for l in open('k_corr_early.txt'):
        # this file has columns z k_g k_r
        v = l.split()
        z_k.append(v[0])
        k_k.append(v[2])
    SplineResult = interpolate.splrep(z_k, k_k, s=0, k=3)

    cmd = 'SELECT Name, z from ' + table_name + ';'
    cursor.execute(cmd)
    rows= cursor.fetchall()
    rows = list(rows)

    for row in rows:
        id = row[0]
        z = row[1]
        phy = cal(float(z))
        try:
            k_corr =  interpolate.splev(float(z), SplineResult, der=0)
            cmd = 'update '+table_name+ ' set k_corr = ' + str(k_corr) +',dis_modu='+ str(phy[0])+',ang_di_dist_kpc_arcsec=' + str(phy[1]) + " where Name = '" + str(row[0])+"';"
            cursor.execute(cmd)
        except:
            pass

    return





### OK USE THESE THOUGH ###

def update_main_table(table_name, cursor, fit_types, pix_sz, filter):

    for m in fit_types:
        cmd = 'select Name_' + filter + ', extinction_' + filter + ', k_corr_' + filter + ', zeropoint_sdss_' + filter + ', zeropoint_pymorph, dis_modu, ang_di_dist_kpc_arcsec, Ie_'+m+', re_pix_'+m+', re_err_pix_'+m+',Id_'+m+', rd_pix_'+m+', rd_err_pix_'+m+' from ' + table_name + ';'
        cursor.execute(cmd)
        rows = cursor.fetchall()
        rows = list(rows)

            

        for row in rows:
            try:
                re_kpc = row[8] * row[6] * pix_sz
                re_kpce = row[9] * row[6] * pix_sz
                rd_kpc = row[11] * row[6] * pix_sz
                rd_kpce = row[12] * row[6] * pix_sz
                zp = row[9]
                AbsMagBulge = row[7] - row[5] - row[2] - row[1] - row[4] + row[3] 
                AbsMagDisk = row[10] - row[5] - row[2] - row[1] - row[4] + row[3]
                cmd = 'update ' + table_name+' set AbsMagBulge_'+m+' = ' + str(AbsMagBulge) + ',AbsMagDisk_'+m+' = ' + str(AbsMagDisk) + ', re_kpc_'+m+' = ' + str(re_kpc) + ', re_err_kpc_'+m+' = ' + str(re_kpce) + ', rd_kpc_'+m+' = ' + str(rd_kpc) + ', rd_err_kpc_'+m+' = ' + str(rd_kpce) + " where Name_" + filter + " = '" + str(row[0])+"';"
                cursor.execute(cmd)
            except:
                pass

    return
