from mysql.mysql_class import *

cursor = mysql_connect('catalog','pymorph','pymorph')

infile = open('/home/ameert/lackdr8.csv')
infile.readline()

#cols=['deVPhi_u','deVPhi_g','deVPhi_r','deVPhi_i','deVPhi_z','expPhi_u',
#      'expPhi_g','expPhi_r','expPhi_i','expPhi_z','expab_u','expab_g',
#      'expab_r','expab_i','expab_z',
#      'exprad_u','exprad_g','exprad_r','exprad_i','exprad_z',
#      'expmag_u','expmag_g','expmag_r','expmag_i','expmag_z']
#cols=["hrad_corr", "hrad_ba_corr"]

cols = ['specobjid', 'ra_dr8', 'ra_dr7','dec_dr8', 'dec_dr7',
        'z_dr8', 'z_dr7', 'zp_dr8','zp_dr7','zmagy']

#create table dr8zp (galcount int, specobjid bigint, ra_dr8 float, ra_dr7 float,dec_dr8 float, dec_dr7 float,z_dr8 float, z_dr7 float, zp_dr8 float,zp_dr7 float,zmagy float);

for line in infile.readlines():
    line = line.strip()
 #   data = line.split(',')

#    datline = ['='.join(a) for a in zip(cols, data[1:])]
#    datline = ','.join(datline)
#    cmd = 'UPDATE sim_input_hst set %s where simcount = %s;' %(datline,data[0])
#    cmd = 'UPDATE CAST set mode = %s where galcount = %s;' %(mode,galcount)
    cmd = 'insert into dr8zp values (%s);' %line
    #print cmd
    #break
    cursor.execute(cmd)
infile.close()
del cursor
