from mysql.mysql_class import *
bands = 'gri'
table_name = 'CAST'
dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'


galtype = sys.argv[1]

cursor = mysql_connect(dba, usr, pwd, '')


galcount = np.loadtxt('grads_%s.txt' %galtype, usecols=[0], skiprows=1, unpack=True)

galcount = galcount.astype(int)

for gal in galcount:

    cmd = 'select -2.5/log(10)*log(pow(10.0, -0.4*r.Galsky-2)/2 + sqrt(pow(9.0e-11,2.0)+0.25*pow(10,-0.8*r.Galsky-4))),-2.5/log(10)*log(pow(10.0, -0.4*rs.Galsky-2)/2 + sqrt(pow(1.2e-10,2.0)+0.25*pow(10,-0.8*rs.Galsky-4))),r.Galsky+5, rs.Galsky+5 from r_band_ser as rs, g_band_ser as r where r.galcount = rs.galcount and rs.galcount = %d;' %gal

    data =cursor.get_data(cmd)

    print gal, np.array(data).T[0]
