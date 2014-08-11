import pyfits as p
from mysql_class import *
import numpy as np
import sys
import pylab as pl
import numpy.random as ran
from cosmolopy import distance
from cosmolopy import magnitudes

cosmo = {'omega_M_0':0.3, 'omega_lambda_0':0.7, 'omega_k_0':0.0, 'h':0.7}

def mag_sum(mag1, mag2):
    print mag1, mag2
    mag1 = 10.0**( -.4*mag1)
    mag2 = 10.0**(-.4*mag2)

    mag_tot = mag1 + mag2
    bt = mag1/(mag1+mag2)
    mag_tot = -2.5 * np.log10(mag_tot)

    return mag_tot, bt

def mag_to_counts( mag, aa, kk = 0 , airmass = 0):
    exptime = 53.907456 #in seconds, taken from SDSS website www.sdss.org/dr3/algorithms/fluxcal.html
    return exptime * (10**(-.4*mag)) / (10**(0.4*(aa + kk*airmass)))

def counts_to_mag( counts, aa, kk = 0 , airmass = 0):
    exptime = 53.907456 #in seconds, taken from SDSS website www.sdss.org/dr3/algorithms/fluxcal.html
    return -2.5 * np.log10(counts/exptime) + aa

model_list = ['ser']#,'devexp','serexp']
cursor = mysql_connect('andre_BCG','ameert','al130568')

if 0:
    cmd = 'DROP table andre_BCG.sim_input;'
    try:
        cursor.execute(cmd)
    except:
        pass
        
    cmd = """create table if not exists andre_BCG.sim_input (
simcount int primary key auto_increment, model varchar(8), 
galcount int, name varchar(30), kpc_per_arcsec float default -999, 
dismod float default -999 , zeropoint float default -999, 
z float default -999, kcorr float default -999,
m_tot float default -999,BT float default -999, 
n_bulge float default -999,r_bulge float default -999, 
m_bulge float default -999, ba_bulge float default -999,
pa_bulge float default -999,
r_disk float default -999,m_disk float default -999,
ba_disk float default -999,pa_disk float default -999);"""
    try:
        cursor.execute(cmd)
    except:
        pass
if 0: 
    for model in model_list:
        for redshift in np.arange(0.05, 0.30, 0.02):
            kpc_scale = distance.angular_diameter_distance(redshift, **cosmo)*1000.0*np.pi/(180.0*3600.0)
            dismod = magnitudes.distance_modulus(redshift, **cosmo)
            print "redshift:%.2f, scale:%.1f, DM:%.1f" %(redshift, kpc_scale, dismod)

            cmd = """insert into andre_BCG.sim_input (model, galcount, name, 
kpc_per_arcsec, dismod, zeropoint, z, BT, n_bulge, ba_bulge, 
pa_bulge, ba_disk, pa_disk) select 
'{model}', b.galcount, b.name,
{kpc_scale}, {dismod},  -1.0*c.aa_r-c.kk_r*c.airmass_r, {z}, 
b.BT, b.n, b.eb,b.bpa+90.0, 
b.ed, b.dpa+90.0 
from andre_BCG.CAST as c, andre_r_{model} as b, andre_BCG.DERT as d 
where 
d.galcount = b.galcount and b.galcount = c.galcount;""".format(model=model,
                                                               kpc_scale = kpc_scale, dismod = dismod, z=redshift)
            print cmd
            cursor.execute(cmd)            
            
if 0:
    for redshift in np.arange(0.05, 0.30, 0.02):
        cmd = """select avg(d.kcorr_r) from catalog.DERT as d, catalog.r_band_serexp as b, catalog.CAST as c, catalog.Flags_optimize as a where a.galcount = b.galcount and b.galcount = c.galcount and c.galcount = d.galcount and a.ftype = 'u' and a.model = 'serexp' and a.band = 'r' and (b.m_tot -c.extinction_r-d.dismod-d.kcorr_r between -24.25 and -23.75) and d.kcorr_r>-800 and (c.z between {low} and {high}) and  a.flag&1>0;""".format(low=redshift-0.02, high = redshift+0.02)
        val, = cursor.get_data(cmd)
        cmd = """Update andre_BCG.sim_input set kcorr={val} where z between {low} and {high};""".format(val=val[0],low=redshift-0.001, high = redshift+0.001)
        print cmd
        cursor.execute(cmd)

if 0:
    for model in model_list:
        cmd = """Update andre_BCG.sim_input as s, CAST as c, 
andre_r_{model} as b, DERT as d 
SET
s.m_bulge = b.Ie-25.256+s.zeropoint-d.kcorr_r + s.kcorr-d.dismod+s.dismod,
s.m_disk = abs(b.Id-25.256+s.zeropoint-d.kcorr_r + s.kcorr-d.dismod+s.dismod),
s.r_bulge = b.re_pix*0.396*d.kpc_per_arcsec/s.kpc_per_arcsec,
s.r_disk = b.rd_pix*0.396*d.kpc_per_arcsec/s.kpc_per_arcsec
where 
s.galcount=c.galcount and c.galcount=b.galcount and c.galcount=d.galcount and
model = {model};""".format(model = model)
        print cmd
        cursor.execute(cmd)

    cmd = """Update andre_BCG.sim_input set r_disk = -999, m_disk = 999 where model = 'ser';"""
    print cmd
    cursor.execute(cmd)

if 1:
    cmd = """Update andre_BCG.sim_input set m_tot = -2.5*log10(pow(10, -0.4*m_bulge)+pow(10,-0.4*m_disk));"""
    print cmd
    cursor.execute(cmd)
