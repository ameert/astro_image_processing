from mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys

dba = 'MB'
pwd = 'al130568'
usr = 'ameert'

stem = 'yang3'

cursor = mysql_connect(dba, usr, pwd)

if 1:
    for model, count in zip(['ser','serexp'], [1,3]):
        cmd = """select a.galcount, a.groupID, a.brightest, a.most_massive,
a.L_group, a.Mstar_group,a.HaloMass_1, a.HaloMass_2, a.fEdge, a.ID1, a.ID2, a.group_counts, a.group_Z 
from yang.yang_groupsC as a, old_%s_galcount as b where  a.galcount = b.galcount  order by a.galcount into outfile "/tmp/%s_%d.txt";""" %(model, stem, count)
        cursor.execute(cmd)

for count in [1,3]:
    os.system('cp /tmp/%s_%d.txt /scratch/MB/yang_%d.txt' %(stem, count, count))

