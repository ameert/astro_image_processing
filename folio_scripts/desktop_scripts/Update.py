from numpy import *
from pylab import *
from scipy import interpolate
from cosmocal import *
import MySQLdb as mysql

z_k = [] #kcorrection z
k_k = [] #kcorrection
for l in open('k-g.dat'):
 v = l.split()
 z_k.append(v[0])
 k_k.append(v[2])
SplineResult = interpolate.splrep(z_k, k_k, s=0, k=3)

dba = 'pymorph_data'
usr = 'pymorph'
pwd = 'pymorph'
try:
    Conn = mysql.connect (host = "localhost",
                                user = "%s" %usr,
                                passwd = "%s" %pwd,
                                db = "%s" %dba)
except mysql.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit (1)
cursor = Conn.cursor()
f = open('mysql', 'w')

i = 0
pix_sz = .05
m = '_Ser'# '_DevExp' '_Ser'
cmd = 'select Name, z,Ie'+m+', re_pix'+m+', re_err_pix'+m+',Id'+m+', rd_pix'+m+', rd_err_pix'+m+',extinction_r, zp_sdss_r from sab_all '
cursor.execute(cmd)
rows = cursor.fetchall()
rows = list(rows)
for row in rows:
    id = row[0]
    z = row[1]
    phy = cal(float(z))
    try:
        re_kpc = row[3] * phy[1] * pix_sz
        re_kpce = row[4] * phy[1] * pix_sz
        rd_kpc = row[6] * phy[1] * pix_sz
        rd_kpce = row[7] * phy[1] * pix_sz
        zp = row[9]
        AbsMagBulge = row[2] - phy[0] - interpolate.splev(float(z), SplineResult, der=0) - 25.256 - zp - row[8]
        AbsMagDisk = row[5] - phy[0] - interpolate.splev(float(z), SplineResult, der=0) - 25.256 - zp -row[8]
        cmd = 'update sab_all set AbsMagBulge'+m+' = ' + str(AbsMagBulge) + ',AbsMagDisk'+m+' = ' + str(AbsMagDisk) + ', re_kpc'+m+' = ' + str(re_kpc) + ', re_err_kpc'+m+' = ' + str(re_kpce) + ', rd_kpc'+m+' = ' + str(rd_kpc) + ', rd_err_kpc'+m+' = ' + str(rd_kpce) + ", zp_pymorph = 25.256 where Name = '" + str(row[0])+"';"
        cursor.execute(cmd)
    except:
        pass
##    f.writelines([str(cmd), '\n'])
##    i += 1
##    rows.remove(row)
##    if i % 50 == 0:
##     print i
##    break
## f.close()
