import MySQLdb as mysql
from numpy import *
from scipy import interpolate
from cosmocal import *
import datetime
from read_list import *

def make_big_table(table_name, filter, cursor):

    cmd = 'CREATE TABLE ' + table_name + ' '
    cmd += """ (
    Name_g                varchar(500),
    Name_r                varchar(500),
    Name_i                varchar(500),
    galcount               int,
    specobjid              bigint(8),
    ra_                    float,          
    dec_                   float,         
    z                      float,                   
    dis_modu               float,          
    ang_di_dist_kpc_arcsec float,          
    MorphType              int(11),        
    marc_id                bigint(20),
    probaE                 float,
    probaEll               float,
    probaS0                float,
    probaSab               float,
    probaScd               float,
    ask_class              float,
    nyc_Id                 int(11),
    nyc_dist               float,
    nyc_A_g                float,
    nyc_A_r                float,
    nyc_A_i                float,
    nyc_r0_g               float,
    nyc_r0_r               float,
    nyc_r0_i               float,
    nyc_n_ser_g            float,
    nyc_n_ser_r            float,
    nyc_n_ser_i            float,
    velo_disp              float,         
    velo_disp_err          float,
    fracdev_g              float,              
    fracdev_r              float,              
    fracdev_i              float,              
    extinction_g           float,
    extinction_r           float,
    extinction_i           float,
    k_corr_g               float,
    k_corr_r               float,
    k_corr_i               float,
    zeropoint_sdss_g       float,
    zeropoint_sdss_r       float,
    zeropoint_sdss_i       float,
    Comments               varchar(1000)  
    )""" %(filter)

    cursor.execute(cmd)
    
    return

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


def load_table_main_data(table_name, gal, cursor, curr_filter):
    for count in gal['galcount']:
        cmd = "INSERT INTO %s (Name_r,galcount) VALUES ('%06d_%s_stamp', %d);" %(table_name,count,curr_filter,count)
        #cursor.execute(cmd)

    cmd = 'ALTER IGNORE TABLE ' + table_name + ' ADD UNIQUE INDEX(galcount)'
    #cursor.execute(cmd)

    
    for count in range(len(gal['galcount'])):
        name = '%06d_%s_stamp' %(gal['galcount'][count], curr_filter)
        z = gal['redshift'][count]
        
        cmd = 'update '+ table_name+ " set ra_ = " + str(gal['ra'][count]) + ',dec_ = ' + str(gal['dec'][count]) + ',z = ' + str(z) + ',velo_disp =' + str(gal['veldisp'][count]) + ',velo_disp_err = ' + str(gal['veldispErr'][count])+ ' ,specobjid = '+ str(gal['specobjid'][count]) +  " where galcount = '" + str(gal['galcount'][count]) +"';"
        cursor.execute(cmd)


    return


def calc_dist_stuff(table_name, cursor):

    z_k = [] #kcorrection z
    k_k = [] #kcorrection
    for l in open('k_corr_early.txt'):
        # this file has columns z k_g k_r
        v = l.split()
        z_k.append(v[0])
        k_k.append(v[1])
    SplineResult = interpolate.splrep(z_k, k_k, s=0, k=3)

    cmd = 'SELECT galcount, z from ' + table_name + ';'
    cursor.execute(cmd)
    rows= cursor.fetchall()
    rows = list(rows)

    for row in rows:
        id = row[0]
        z = row[1]
        phy = cal(float(z))
        try:
            k_corr =  interpolate.splev(float(z), SplineResult, der=0)
            cmd = 'update '+table_name+ ' set k_corr_g = ' + str(k_corr) + " where galcount = " + str(row[0])+";"
            cursor.execute(cmd)
            print cmd
        except:
            pass

    return

usr = 'pymorph'
pwd = 'pymorph'
dba = 'sdss_sample'

table_name = 'sdss_main'
filter = 'r'
filename = 'sdss_list_out_ex_ameert.csv'
cursor = connect_to_mysql(dba,usr,pwd)

#make_big_table(table_name, filter, cursor)

gal = {}
gal.update(read_list(filename, 'I,X,X,X,X,X,X,X,X,X,F,F,F,A,X,X,X,F,F,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,F,F', delimiter = ','))

print gal.keys()

#load_table_main_data(table_name, gal, cursor, filter)
calc_dist_stuff(table_name, cursor)


cursor.close()
