from mysql_connect import *
import numpy as n
import pylab
from MatplotRc import *

matrc2X5()

usr = 'pymorph'
pwd = 'pymorph'
dba = 'sdss_sample'
name_stem = 'SerExp'
cursor = mysql_connect(dba,usr,pwd)

#cmd = 'select AbsMagBulge_SerExp, AbsMagDisk_SerExp, BT_SerExp, re_kpc_SerExp, rd_kpc_SerExp, eb_SerExp, zeropoint_sdss_r, z, kk_r, airmass_r from r_full where fit_SerExp = 1 and z > 0 and AbsMagBulge_SerExp > -50 and AbsMagDisk_SerExp > -50;'

cmd = 'select Ie_'+name_stem+'-zeropoint_pymorph+zeropoint_sdss_r, Id_'+name_stem+'-zeropoint_pymorph+zeropoint_sdss_r, BT_'+name_stem+', re_kpc_'+name_stem+', rd_kpc_'+name_stem+', eb_'+name_stem+', n_'+name_stem+',zeropoint_sdss_r, z, kk_r, airmass_r from r_full where fit_'+name_stem+' = 1 and z > 0;'

cursor.execute(cmd)
rows = cursor.fetchall()
rows = list(rows)

tot_mag = []
BT = []
re = []
rd = []
eb = []
n_bulge = []
zp = []
z  = []
kk = []
airmass  = []


for row in rows:
    tot_mag.append(-2.5 * n.log10(10**(-0.4*float(row[0])) + 10 ** (-0.4*float(row[1]))))
    BT.append(float(row[2]))
    re.append(float(row[3]))
    rd.append(float(row[4]))
    eb.append(float(row[5]))
    n_bulge.append(float(row[6]))
    zp.append(float(row[7]))
    z.append(float(row[8]))
    kk.append(float(row[9]))
    airmass.append(float(row[10]))
    
tot_mag = n.array(tot_mag)
BT = n.array(BT)
re = n.array(re)
rd = n.array(rd)
eb = n.array(eb)
n_bulge = n.array(n_bulge) 
zp = n.array(zp)
z  = n.array(z)
kk = n.array(kk)
airmass  = n.array(airmass)

pylab.suptitle('Distributions for ' + name_stem, fontsize = 18)
for var, name, pos in zip([tot_mag, BT, re, rd, eb, n_bulge, zp, z, kk, airmass],['tot_mag_obs', 'BT', 're_kpc', 'rd_kpc', 'eb', 'n_bulge', 'zp', 'z', 'kk', 'airmass'],[1,2,3,4,5,6,7,8,9,10]):
    pylab.subplot(5,2,pos)
    if name == 'rd_kpc' or name == 're_kpc':
        pdf,bins,patches = pylab.hist(var, bins = 100,cumulative = 1, normed = 1, range = (0,20))
    else:
        pdf,bins,patches = pylab.hist(var, bins = 100,cumulative = 1, normed = 1)
    pylab.title(name+' cdf')
    pylab.xlabel(name)
    pylab.ylabel('cdf')
    pylab.ylim(0,1)

    outfile = open(name_stem + '_' + name + '.txt', 'w')
    outfile.write(name+',cdf\n')
    outfile.write('%f,%3.1f\n' %(bins[0], 0.0))
    for count in range(1,len(bins)):
        outfile.write('%f,%f\n' %(bins[count],pdf[count -1]))
    outfile.close()
    
    

    
pylab.savefig(name_stem+'_cdf.png', format = 'png')
