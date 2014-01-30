from image_info import *
import numpy as np
from mysql_class import *
import pyfits as pf
from util_funcs import *

def get_hrad(file_name, tot_counts, to_sum = [0]):
    inimage= pf.open(file_name)
    data = inimage[to_sum[0]].data
    for a in to_sum[1:]:
        data += inimage[a].data
    inimage.close()
    
    try:
        dat_info = image_info(data, mask = 'threshold')    
        hrad = dat_info.halflight(tot_counts)
    except MemoryError:
        hrad = (-999, -999)
    if np.isnan(hrad[0]):
        hrad = (-999, -999)
    print hrad[0], hrad[1]/tot_counts

    return hrad[0], hrad[1]/tot_counts

def get_tot_counts(cursor, table_name, id,  zp_name = 'zeropoint_sdss_r',
                   count_name = 'galcount'):
    cmd = "select Ie, Id, %s from %s where %s = %d;" %(zp_name, table_name, count_name, id)
    print cmd
    Ie, Id, zp = cursor.get_data(cmd)
    try:
        tot_mag, bt = mag_sum(np.abs(Id[0]), Ie[0])
        tot_counts = mag_to_counts( float(tot_mag), float(-zp[0]))/ 53.907456 
    except IndexError:
        tot_counts = np.nan

    return tot_counts

