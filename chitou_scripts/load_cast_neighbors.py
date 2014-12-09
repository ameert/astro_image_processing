from mysql.mysql_class import *

cursor = mysql_connect('catalog','pymorph','pymorph')

infile = open('/home/ameert/neighbor_info_i_upenn_pymorph.csv')
infile.readline()

cols=['galcount','distance','run','rerun','camcol','field','objid','ra_gal',
      'dec_gal','ModelMag_i','ModelMagerr_i','fracdev_i','petroMag_i',
      'petroMagErr_i','petroR90_i','petroR50_i','extinction_i','rowc_i',
      'colc_i','flags','flags_i','mode']

for line in infile.readlines():
    line = line.strip()
    data = line.split(',')

    datline = ','.join(data)
    cmd = 'insert ignore CAST_neighbors_i (%s) Values (%s);' %(','.join(cols),datline)
    #print cmd
    cursor.execute(cmd)
    #break
infile.close()

