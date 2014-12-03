from mysql.mysql_class import *

band = 'i'

cursor = mysql_connect('catalog','pymorph','pymorph')

infile = open('poll_out_tab_deep_%s.txt' %band)
infile.readline()

for line in infile.readlines():
    line = line.strip()
    data = line.split()

    if int(data[2])==1:
        cmd = 'UPDATE CAST_neighbors_%s set is_masked_deep=1 where objid = %s;' %(band,data[1])
        print cmd
        cursor.execute(cmd)
infile.close()

cmd = 'update {band}_band_badfits as a, CAST_neighbors_{band} as b set a.is_polluted_deep = 0 where a.galcount = b.galcount;'.format(band=band)
cursor.execute(cmd)
cmd = 'update {band}_band_badfits as a, CAST_neighbors_{band} as b set a.is_polluted_deep = 1 where a.galcount = b.galcount and b.is_masked_deep=0 and b.is_polluter_deep=1;'.format(band=band)
cursor.execute(cmd)
