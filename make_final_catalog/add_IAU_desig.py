from mysql.mysql_class import *
import numpy as np

cursor = mysql_connect('catalog','pymorph','pymorph')

cmd= 'select galcount, ra_gal, dec_gal from CAST;'

galcount, ra_gal, dec_gal = cursor.get_data(cmd) 

galcount = np.array(galcount, dtype=int)
ra_gal = np.array(ra_gal)
dec_gal = np.array(dec_gal)

def ra_str(ra):
    hour_deg = 360.0/24.0
    min_deg = hour_deg/60.0
    sec_deg = min_deg/60.0
    hours = np.floor(ra/hour_deg).astype(int)
    ra -= hours*hour_deg
    minutes = np.floor(ra/min_deg).astype(int)
    ra -= minutes*min_deg
    seconds = np.trunc(ra/sec_deg *100.0)/100.0
    
    ra_str = ['%02d%02d%05.2f' %(int(a[0]),int(a[1]),a[2]) for a in 
              zip(hours,minutes,seconds)]

    return ra_str

def dec_str(dec):
    min_deg = 1.0/60.0
    sec_deg = min_deg/60.0

    sign = np.where(dec<0,'-','+')
    dec = np.abs(dec)
    deg = np.trunc(dec).astype(int)
    dec -= deg
    minutes = np.floor(dec/min_deg).astype(int)
    dec -= minutes*min_deg
    seconds = np.trunc(dec/sec_deg *10.0)/10.0
    
    dec_str = ['%s%02d%02d%04.1f' %(a[0],int(a[1]),int(a[2]),a[3]) for a in 
              zip(sign,deg,minutes,seconds)]

    return dec_str

ra_name = ra_str(ra_gal)
dec_name = dec_str(dec_gal)

IAU_name = ['SDSS J'+a[0]+a[1] for a in zip(ra_name, dec_name)]

cmd = "update CAST set SDSS_IAU='{name}' where galcount = {galcount};"

for gal,nm in zip(galcount, IAU_name):
    #print cmd.format(galcount=gal, name=nm)
    cursor.execute(cmd.format(galcount=gal, name=nm))
