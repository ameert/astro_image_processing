import pyfits as pf
import numpy as np
import sys
import numpy.random as ran
from cosmolopy import distance
from cosmolopy import magnitudes
from astro_image_processing.astro_utils.magnitudes import magsum
from astro_image_processing.mysql.mysql_class import *
from astro_image_processing import user_settings
dba = 'andre_BCG'

all_info={
'cosmo':{'omega_M_0':0.3, 'omega_lambda_0':0.7, 'omega_k_0':0.0, 'h':0.7},
'model_list':['ser','devexp','serexp'],
'cursor':mysql_connect(dba,
                       user_settings.mysql_params['user'],
                       user_settings.mysql_params['pwd'],
                       user_settings.mysql_params['host']),
'out_table':'sim_input_test',
'in_table':'andre_r_{model}',
'dba':dba,
'z_range':{'start':0.05, 'stop':0.3, 'scale':0.02},
'in_zeropoint':25.256,
'in_pixscale':0.396,
}

cmd = 'DROP table {dba}.{out_table};'.format(**all_info)

try:
    print cmd
#cursor.execute(cmd)
except:
    pass
        
cmd = """create table if not exists {dba}.{out_table} (
simcount int primary key auto_increment, model varchar(8), 
galcount int, name varchar(30), kpc_per_arcsec float default -999, 
dismod float default -999 , zeropoint float default -999, 
z float default -999, kcorr float default -999,
m_tot float default -999,BT float default -999, 
n_bulge float default -999,r_bulge float default -999, 
m_bulge float default -999, ba_bulge float default -999,
pa_bulge float default -999,
r_disk float default -999,m_disk float default -999,
ba_disk float default -999,pa_disk float default -999);""".format(**all_info)

try:
    print cmd
    cursor.execute(cmd)
except:
    pass

for model in all_info['model_list']:
    for redshift in np.arange(all_info['z_range']['start'], all_info['z_range']['stop'], all_info['z_range']['scale']):
        kpc_scale = distance.angular_diameter_distance(redshift, **all_info['cosmo'])*1000.0*np.pi/(180.0*3600.0) #kpc_per_arcsec
        dismod = magnitudes.distance_modulus(redshift, **all_info['cosmo'])
        print "redshift:%.2f, scale:%.1f, DM:%.1f" %(redshift, kpc_scale, dismod)
        cmd = """insert into {dba}.{out_table} (model, galcount, name, 
kpc_per_arcsec, dismod, zeropoint, z, BT, n_bulge, ba_bulge, 
pa_bulge, ba_disk, pa_disk) select 
'{model}', b.galcount, b.name,
{kpc_scale}, {dismod},  -1.0*c.aa_r-c.kk_r*c.airmass_r, {z}, 
b.BT, b.n, b.eb,b.bpa+90.0, 
b.ed, b.dpa+90.0 
from {dba}.CAST as c, {dba}.{in_table} as b, {dba}.DERT as d 
where 
d.galcount = b.galcount and b.galcount = c.galcount;""".format(model=model,
                                                               kpc_scale = kpc_scale, dismod = dismod, z=redshift, **all_info).format(model=model)
        print cmd
        cursor.execute(cmd)            
        
        cmd = """select avg(d.kcorr_r) from catalog.DERT as d, catalog.r_band_serexp as b, catalog.CAST as c, catalog.Flags_optimize as a where a.galcount = b.galcount and b.galcount = c.galcount and c.galcount = d.galcount and a.ftype = 'u' and a.model = 'serexp' and a.band = 'r' and (b.m_tot -c.extinction_r-d.dismod-d.kcorr_r between -24.25 and -23.75) and d.kcorr_r>-800 and (c.z between {low} and {high}) and  a.flag&1>0;""".format(low=redshift-0.02, high = redshift+0.02)
        print cmd
        val, = cursor.get_data(cmd)
        cmd = """Update {dba}.{out_table} set kcorr={val} where z between {low} and {high};""".format(val=val[0],low=redshift-0.001, high = redshift+0.001, **all_info)
        print cmd
        cursor.execute(cmd)
    
    cmd = """Update {dba}.{out_table} as s, CAST as c, 
{in_table} as b, DERT as d 
SET
s.m_bulge = b.Ie-{in_zeropoint}+s.zeropoint-d.kcorr_r + s.kcorr-d.dismod+s.dismod,
s.m_disk = abs(b.Id-{in_zeropoint}+s.zeropoint-d.kcorr_r + s.kcorr-d.dismod+s.dismod),
s.r_bulge = b.re_pix*{in_pixscale}*d.kpc_per_arcsec/s.kpc_per_arcsec,
s.r_disk = b.rd_pix*{in_pixscale}*d.kpc_per_arcsec/s.kpc_per_arcsec
where 
s.galcount=c.galcount and c.galcount=b.galcount and c.galcount=d.galcount and
model = {model};""".format(model = model, **all_info).format(model=model)
    print cmd
    cursor.execute(cmd)
cmd = """Update {dba}.{out_table} set r_disk = -999, m_disk = 999 where model in ('ser', 'dev');""".format(model = model, **all_info).format(model=model)
print cmd
cursor.execute(cmd)
    
cmd = """Update {dba}.{out_table} set m_tot = -2.5*log10(pow(10, -0.4*m_bulge)+pow(10,-0.4*m_disk));""".format(model = model, **all_info).format(model=model)
print cmd
cursor.execute(cmd)

