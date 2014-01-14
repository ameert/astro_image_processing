from mysql_class import *
import numpy as np
import scipy.stats as stats
import os

dba = 'simard'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)

cmd = 'select b.galcount, b.z, a.V_max, b.petromag_r - b.extinction_r - f.kcorr_r - f.dismod, b.petromag_r - b.extinction_r, b.petroR50_r, b.petromag_r  from simard_sample as a, catalog.CAST as b , catalog.DERT as f where f.galcount = b.galcount and  b.galcount = a.galcount and a.V_max > 0;'

galcount, z, V_max, absmag, petromag_r, halflight_rad,ucorr_mag = cursor.get_data(cmd)

galcount1 = np.array(galcount)
z1 = np.array(z)
V_max1 = np.array(V_max)
petromag_r1 = np.array(petromag_r)
halflight_rad1 = np.array(halflight_rad)
absmag1 = np.array(absmag)
ucorr_mag1 = np.array(ucorr_mag)

surf_bright1 = -2.5*np.log10(10**(-0.4*ucorr_mag1)/(2*np.pi*halflight_rad1**2.0))

counter =1

while 1:
    
    #os.system('python /home/ameert/python/alan_code/select_sample.py')
    cursor.execute("delete from simulations.sim_input where model = 'serexp';")
    cursor.execute("insert into simulations.sim_input (galcount, model) select galcount, 'serexp' from simulations.tmp_2_serexp order by rand() limit 10000;")

    cmd = "select b.galcount, b.z, a.V_max, b.petromag_r - b.extinction_r - f.kcorr_r - f.dismod, b.petromag_r - b.extinction_r, b.petroR50_r, b.petromag_r  from simard_sample as a, catalog.CAST as b, simulations.sim_input as c , catalog.DERT as f where f.galcount = b.galcount and  b.galcount = a.galcount and b.galcount = c.galcount and a.V_max > 0 and c.model = 'serexp';"
    #cmd = "select b.galcount, b.z, a.V_max, b.petromag_r - b.extinction_r - f.kcorr_r - f.dismod, b.petromag_r - b.extinction_r, b.petroR50_r, b.petromag_r  from simard_sample as a, catalog.CAST as b,  catalog.DERT as f where f.galcount = b.galcount and  b.galcount = a.galcount and a.V_max > 0 and a.galcount < 200000;"#order by rand() limit 10000;"

    galcount, z, V_max, absmag, petromag_r, halflight_rad,ucorr_mag = cursor.get_data(cmd)

    galcount3 = np.array(galcount)
    z3 = np.array(z)
    V_max3 = np.array(V_max)
    petromag_r3 = np.array(petromag_r)
    halflight_rad3 = np.array(halflight_rad)
    absmag3 = np.array(absmag)
    ucorr_mag3 = np.array(ucorr_mag)
    
    surf_bright3 = -2.5*np.log10(10**(-0.4*ucorr_mag3)/(2*np.pi*halflight_rad3**2.0))

    print '-----------------------------------------------------'
    print '                    trial: %d                        ' %counter
    print '-----------------------------------------------------'
    grades = np.zeros(5)
    k= stats.ks_2samp(absmag1, absmag3)
    print 'raw absmag ', k[1]
    if k[1]>.05:
        print "PASSED"
        grades[0] = 1
    else:
        print "FAILED"
    k= stats.ks_2samp(petromag_r1, petromag_r3)
    print 'appmag ',k[1]
    if k[1]>.05:
        print k[1]
        print "PASSED"
        grades[1] = 1
    else:
        print "FAILED"
    k = stats.ks_2samp(halflight_rad1, halflight_rad3)
    print 'rad ', k[1]
    if k[1]>.05:
        print k[1]
        print "PASSED"
        grades[2] = 1
    else:
        print "FAILED"
    k = stats.ks_2samp(surf_bright1, surf_bright3)
    print 'mu ',k[1]
    if k[1]>.05:
        print "PASSED"
        grades[3] = 1
    else:
        print "FAILED"
    k = stats.ks_2samp(z1, z3)
    print 'z ',k[1]
    if k[1]>.05:    
        print "PASSED"
        grades[4] = 1
    else:
        print "FAILED"
    
    if 0 not in grades:
        break
    counter +=1
