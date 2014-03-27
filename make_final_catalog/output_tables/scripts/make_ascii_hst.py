#++++++++++++++++++++++++++
#
# TITLE: make_ascii_hst
#
# PURPOSE: makes an ascii file of the
#          HST simulations
#
# INPUTS: 
#
# OUTPUTS: 
#
# PROGRAM CALLS:
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# WITH: Mariangela Bernardi
#       Department of Physics and Astronomy
#       University of Pennsylvania
#
# DATE:
#
#-----------------------------------

import numpy as np
import pylab as pl
import scipy as sc

from mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys

dba = 'simulations'
pwd = 'al130568'
usr = 'ameert'

stem = 'hstz9'

cursor = mysql_connect(dba, usr, pwd)

for model, count in zip(['ser','serexp'], [1,3]):
    cmd = """select a.simcount, b.probaEll, b.ProbaS0, b.ProbaSab, b.ProbaScd, 
-2.5*log10(pow(10, -0.4*a.Ie) + pow(10, -0.4*abs(a.Id)))-a.dismod+ a.z-1.0, 
-2.5*log10(pow(10, -0.4*c.Ie) + pow(10, -0.4*abs(c.Id)))-c.dis_modu+ a.z-1.0-c.magzp+a.zeropoint_sdss_r, 
-2.5*log10(pow(10, -0.4*d.Ie) + pow(10, -0.4*abs(d.Id)))-d.dis_modu +d.z,
-2.5*log10(pow(10, -0.4*e.Ie) + pow(10, -0.4*abs(e.Id)))-e.dis_modu+ e.z, 
-2.5*log10(pow(10, -0.4*f.Ie) + pow(10, -0.4*abs(f.Id)))-f.dis_modu+ f.z,
-2.5*log10(pow(10, -0.4*g.Ie) + pow(10, -0.4*abs(g.Id)))-g.dis_modu +g.z, 
-2.5*log10(pow(10, -0.4*h.Ie) + pow(10, -0.4*abs(h.Id)))-a.dismod+ a.z-1.0-h.magzp+a.zeropoint_sdss_r, 
-2.5*log10(pow(10, -0.4*j.Ie) + pow(10, -0.4*abs(j.Id)))-j.dis_modu+ j.z, 
-2.5*log10(pow(10, -0.4*k.Ie) + pow(10, -0.4*abs(k.Id)))-k.dis_modu+ k.z, 
-2.5*log10(pow(10, -0.4*m.Ie) + pow(10, -0.4*abs(m.Id)))-n.dis_modu+ m.z, 
-2.5*log10(pow(10, -0.4*n.Ie) + pow(10, -0.4*abs(n.Id)))-n.dis_modu+ n.z, 
ifnull(log10(a.hrad_pix_corr*0.396*a.kpc_per_arcsec),-999), 
ifnull(log10(c.hrad_pix_corr*c.re_kpc/c.re_pix), -999),
ifnull(log10(d.hrad_pix_corr*d.re_kpc/d.re_pix), -999), 
ifnull(log10(e.hrad_pix_corr*e.re_kpc/e.re_pix), -999), 
ifnull(log10(f.hrad_pix_corr*f.re_kpc/f.re_pix), -999),
ifnull(log10(g.hrad_pix_corr*g.re_kpc/g.re_pix), -999),
ifnull(log10(h.hrad_pix_corr*h.re_kpc/h.re_pix), -999),
ifnull(log10(j.hrad_pix_corr*j.re_kpc/j.re_pix), -999),
ifnull(log10(k.hrad_pix_corr*k.re_kpc/k.re_pix), -999),
ifnull(log10(m.hrad_pix_corr*m.re_kpc/m.re_pix), -999),
ifnull(log10(n.hrad_pix_corr*n.re_kpc/n.re_pix), -999)
from  sim_input as a, catalog.M2010 as b, psf_ser as c, psf_serexp as h,
hst_z10_ser as d,hst_z15_ser as e, hst_z17_ser as f, hst_z20_ser as g, 
hst_z10_serexp as j,hst_z15_serexp as k,hst_z17_serexp as m,hst_z20_serexp as n
where a.simcount = b.galcount and a.model = '%s' and a.simcount = c.galcount and a.simcount = d.galcount and a.simcount = e.galcount and a.simcount = f.galcount and a.simcount = g.galcount and a.simcount = h.galcount and a.simcount = j.galcount and a.simcount = k.galcount and a.simcount = m.galcount and a.simcount = n.galcount order by a.simcount  into outfile "/tmp/%s_%d.txt";""" %(model, stem,count) 

    cursor.execute(cmd)
    os.system('cp /tmp/%s_%d.txt /scratch/MB/hst_%s.txt' %(stem, count, model))
