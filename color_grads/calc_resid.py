#!/data2/home/ameert/python/bin/python2.5

import sys
import os
from mysql_class import *
import numpy as np

def measure_resid(dat_file, hrad):
    inrad = 3.0
    outrad = 6.0

    rad, data, data_err, prof, proferr = np.loadtxt(dat_file, skiprows = 1, unpack = True)

    resid = (data - prof)/np.sqrt(data_err**2 + proferr**2)

    inres = np.extract(rad <= inrad, resid)
    outres = np.extract( (rad>inrad)*(rad<=outrad), resid)

    return np.sum(inres), np.sum(inres**2),np.sum(outres), np.sum(outres**2)


folder_num = int(sys.argv[1])

dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'

save_dir = '/data2/home/ameert/color_grads/data/%04d' %folder_num

cursor = mysql_connect(dba, usr, pwd, 'shredder')

galcount, hrad = cursor.get_data("""select galcount, sqrt(eb)*re_pix from full_dr7_r_ser where galcount between %d and %d;""" %((folder_num-1)*250, folder_num*250))

for g1,h1 in zip(galcount, hrad):
    file_nm = "%s/%08d_r_ser.resid" %(save_dir, g1)
    if os.path.isfile(file_nm):
        out_data =  measure_resid(file_nm, h1)
        cmd = "update resid_ser set inres =%e, inressq = %e, outres =%e, outressq=%e where galcount = %d;" %(out_data[0],out_data[1],out_data[2],out_data[3],g1)
        print cmd
        cursor.execute(cmd)
