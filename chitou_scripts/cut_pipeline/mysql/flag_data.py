from calc_distance import *
import numpy as n
from mysql_connect import *


dba = 'sdss_sample'
usr = pwd = 'pymorph'

cursor = mysql_connect(dba, usr,pwd)

cmd = 'Select r.galcount, r.ra_, r.dec_, r.z, s.ra_dr4, s.dec_dr4, s.redshift, r.nyc_dist from sdss_main as r, dr4_data as s where r.galcount = s.gal_count;'

cursor.execute(cmd)

rows = cursor.fetchall()
rows = list(rows)

dr4_bad = 0
nyc_bad = 0
z_bad = 0

for row in rows:
    galcount = int(row[0])
    ra_py = float(row[1])
    dec_py = float(row[2])
    z_py = float(row[3])
    ra_dr4 = float(row[4])
    dec_dr4 = float(row[5])
    z_dr4 = float(row[6])
    nyc_dist = float(row[7])
    
    dis = n.degrees(calc_distance(n.radians(ra_py), n.radians(dec_py), n.radians(ra_dr4), n.radians(dec_dr4))) * 3600.0  #in arcseconds

    flag = 0
    if dis > 2.0:
        flag = flag | 1
        dr4_bad += 1
    if nyc_dist > 2.0:
        flag = flag | 2
        nyc_bad += 1
    if n.abs(z_py - z_dr4) > .01:
        flag = flag | 4
        z_bad += 1

    if flag != 0:
        cmd = 'UPDATE dr4_data SET match_flag = %d where gal_count = %d;' %(flag, galcount)
        print cmd
        print flag
        cursor.execute(cmd)


print dr4_bad, nyc_bad, z_bad
cursor.close()

