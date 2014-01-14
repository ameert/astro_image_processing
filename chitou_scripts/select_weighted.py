from mysql_class import *
import numpy as np
import pylab as pl
import scipy.stats as stats
import scipy.interpolate as interp

model = 'serexp'

dba = 'simulations'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)

try:
    cmd = 'create table short_%s (galcount int primary key);' %model
    cursor.execute(cmd)
except:
    pass
try:
    cmd = 'create table tmp_1_%s like sample_%s ;' %(model, model)
    cursor.execute(cmd)
except:
    pass
try:
    cmd = 'create table tmp_2_%s like sample_%s ;' %(model, model)
    cursor.execute(cmd)
except:
    pass

try:
    cmd = 'truncate table tmp_2_%s;' %(model)
    cursor.execute(cmd)
    cmd = 'insert into tmp_2_%s select * from sample_%s;' %(model, model)
    cursor.execute(cmd)
except:
    pass

cmd = 'select b.galcount, b.z, a.V_max, b.petromag_r - b.extinction_r - f.kcorr_r - f.dismod, b.petromag_r - b.extinction_r, b.petroR50_r, b.petromag_r  from simard.simard_sample as a, catalog.CAST as b , catalog.DERT as f where f.galcount = b.galcount and  b.galcount = a.galcount and a.V_max > 0;'

galcount, z, V_max, absmag, petromag_r, halflight_rad,ucorr_mag = cursor.get_data(cmd)

z_dist, z_bins, z_patches  = pl.hist(z, range = (0.0, 0.3), bins = 30)
z_dist = np.array(z_dist)/float(len(galcount))
z_points = (z_bins[0:-1]+z_bins[1:])/2.0
z_spline = interp.splrep(z_points,z_dist)

absmag_dist, absmag_bins, absmag_patches  = pl.hist(absmag, range = (-25, -16), bins = 9)
absmag_dist = np.array(absmag_dist)/float(len(galcount))
absmag_points = (absmag_bins[0:-1]+absmag_bins[1:])/2.0
absmag_spline = interp.splrep(absmag_points,absmag_dist)

petro_dist, petro_bins, petro_patches  = pl.hist(petromag_r, range = (14.0, 18.0), bins = 8)
petro_dist = np.array(petro_dist)/float(len(galcount))
petro_points = (petro_bins[0:-1]+petro_bins[1:])/2.0
petro_spline = interp.splrep(petro_points,petro_dist)

hl_rad_dist, hl_rad_bins, hl_rad_patches  = pl.hist(halflight_rad, range = (0.0, 7.0), bins = 7)
hl_rad_dist = np.array(hl_rad_dist)/float(len(galcount))
hl_rad_points = (hl_rad_bins[0:-1]+hl_rad_bins[1:])/2.0
hl_rad_spline = interp.splrep(hl_rad_points,hl_rad_dist)


surf_bright = -2.5*np.log10(10**(-0.4*np.array(ucorr_mag))/(2*np.pi*np.array(halflight_rad)**2.0))
sb_dist, sb_bins, sb_patches  = pl.hist(surf_bright, range = (18.0, 24.0), bins = 12)
sb_dist = np.array(sb_dist)/float(len(galcount))
sb_points = (sb_bins[0:-1]+sb_bins[1:])/2.0
sb_spline = interp.splrep(sb_points,sb_dist)


frac = 67000

cmd = 'select b.galcount, b.z, a.V_max, b.petromag_r - b.extinction_r - f.kcorr_r - f.dismod, b.petromag_r - b.extinction_r, b.petroR50_r, b.petromag_r  from simard.simard_sample as a, catalog.CAST as b , catalog.DERT as f, simulations.sample_%s as z  where f.galcount = b.galcount and b.galcount = a.galcount and z.galcount = b.galcount and a.V_max > 0;' %model
galcount, z, V_max, absmag, petromag_r, halflight_rad,ucorr_mag = cursor.get_data(cmd)

cursor.execute('truncate table short_%s;' %model)

dists = [z_dist, absmag_dist, sb_dist, petro_dist, hl_rad_dist]  
bins = [z_bins, absmag_bins, sb_bins, petro_bins, hl_rad_bins]

for di, bi, ch in zip(dists, bins, ['b.z',  'b.petromag_r - b.extinction_r - f.kcorr_r - f.dismod', ' -2.5*log10(pow(10,-0.4*b.petromag_r)/(2*3.14159* pow(b.petroR50_r,2.0))) ']):# ,'b.petromag_r - b.extinction_r',  'b.petroR50_r'] ):
    frac = frac *.8

    di = di * frac

    for a in range(0, len(di)):
        cmd = 'insert into tmp_1_%s  select z.* from simard.simard_sample as a, catalog.CAST as b , catalog.DERT as f, simulations.tmp_2_%s as z  where f.galcount = b.galcount and b.galcount = a.galcount and z.galcount = b.galcount and a.V_max > 0 and %s >= %f and %s < %f order by rand() limit %d;' %(model,model, ch, bi[a], ch, bi[a+1], di[a])
        print cmd
        cursor.execute(cmd)

    cursor.execute('truncate table tmp_2_%s;' %model)
    cursor.execute('insert into tmp_2_%s select * from tmp_1_%s;' %(model, model))
    cursor.execute('truncate table tmp_1_%s;' %model)
    

    
    
