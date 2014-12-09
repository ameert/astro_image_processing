from mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys

dba = 'MB'
pwd = 'al130568'
usr = 'ameert'

stem = 'yang4'

cursor = mysql_connect(dba, usr, pwd)

cmd = """select a.galcount, a.groupID, a.brightest, a.most_massive,
a.L_group, a.Mstar_group,a.HaloMass_1, a.HaloMass_2, a.fEdge, a.ID1, a.ID2, a.group_counts, a.group_Z 
from yang.yang_groupsC as a order by a.galcount into outfile "/tmp/%s_1.txt";""" %(stem)
cursor.execute(cmd)

os.system('cp /tmp/%s_1.txt /scratch/MB/yang_full.txt' %stem)

