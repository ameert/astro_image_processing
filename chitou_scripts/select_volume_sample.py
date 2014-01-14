from mysql_class import *
import numpy as np
import scipy.stats as stats
import os

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)

cmd = "select a.re_kpc-15.0, a.n-2.5, a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-f.extinction_r-d.kcorr_r + 24, m.ProbaEll-.5, m.ProbaS0-.5, m.ProbaSab-.5, m.ProbaScd-.5 from catalog.full_dr7_r_ser as a,catalog.CAST as f , catalog.DERT as d, catalog.M2010 as m where f.galcount = a.galcount and f.galcount = d.galcount and f.galcount = m.galcount and a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-f.extinction_r < 17.77-38.2605 and a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r < 17.77 and f.z < 0.1 ;" 
    
data_vals = cursor.get_data(cmd) 

names = ['re_kpc', 'n', 'Ie', 'Pell','PS0','PSab','PScd']
data = {}

for d, n in zip(data_vals,names):    
    data[n] = np.array(d, dtype = float)

cmd = "select a.re_kpc-15.0, a.n-2.5, a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-f.extinction_r-d.kcorr_r + 24, m.ProbaEll-.5, m.ProbaS0-.5, m.ProbaSab-.5, m.ProbaScd-.5 from catalog.full_dr7_r_ser as a,catalog.CAST as f , catalog.DERT as d, catalog.M2010 as m where f.galcount = a.galcount and f.galcount = d.galcount and f.galcount = m.galcount and a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-a.dis_modu-f.extinction_r < 17.77-38.2605 and a.Ie-a.magzp-f.aa_r-f.kk_r*f.airmass_r-f.extinction_r < 17.77 and f.z < 0.1 and a.n<8 ;" 
    
data_vals = cursor.get_data(cmd) 

names = ['re_kpc', 'n', 'Ie', 'Pell','PS0','PSab','PScd']
data1 = {}

for d, n in zip(data_vals,names):    
    data1[n] = np.array(d, dtype = float)


print '-----------------------------------------------------'
print '                    trial: 1                        ' 
print '-----------------------------------------------------'
grades = np.zeros(7)
k= stats.ks_2samp(data['Ie'],data1['Ie'])
print 'raw absmag ', k[1]
if k[1]>.05:
    print "PASSED"
    grades[0] = 1
else:
    print "FAILED"
k= stats.ks_2samp(data['n'],data1['n'])
print 'sersic index ',k[1]
if k[1]>.05:
    print k[1]
    print "PASSED"
    grades[1] = 1
else:
    print "FAILED"
k = stats.ks_2samp(data['re_kpc'],data1['re_kpc'])
print 'rad ', k[1]
if k[1]>.05:
    print k[1]
    print "PASSED"
    grades[2] = 1
else:
    print "FAILED"
k = stats.ks_2samp(data['Pell'],data1['Pell'])
print 'P(Ell) ',k[1]
if k[1]>.05:
    print "PASSED"
    grades[3] = 1
else:
    print "FAILED"
k = stats.ks_2samp(data['PS0'],data1['PS0'])
print 'P(S0) ',k[1]
if k[1]>.05:
    print "PASSED"
    grades[3] = 1
else:
    print "FAILED"
k = stats.ks_2samp(data['PSab'],data1['PSab'])
print 'P(Sab) ',k[1]
if k[1]>.05:
    print "PASSED"
    grades[3] = 1
else:
    print "FAILED"
k = stats.ks_2samp(data['PScd'],data1['PScd'])
print 'P(Scd) ',k[1]
if k[1]>.05:
    print "PASSED"
    grades[3] = 1
else:
    print "FAILED"
