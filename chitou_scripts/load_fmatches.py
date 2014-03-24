import pylab as pl
import numpy as np
from mysql_class import *
import sys

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)

if 0:
    infile = open('Yang_forFrancesco_RA_DEC.cat')

    for line in infile.readlines():
        if line[0] == '#':
            continue
        line = line.split()

        cmd = 'insert into fmatches (galid) values (%s);' %line[0]
        cursor.execute(cmd)
    infile.close()

if 1:
    infile = open('f_matches.txt')

    for line in infile.readlines():
        if line[0] == '#':
            continue
        line = line.split()

        cmd = 'update fmatches set galcount = %s, separation = %s where galid=%s;' %(line[1], line[2],line[0])

        cursor.execute(cmd)


    infile.close()


select a.galid, ifnull(c.ra_gal,-999), ifnull(c.dec_gal,-999), ifnull(c.redshift,-999),ifnull(c.Vmaxwti,-999),ifnull(c.Ga50,-999),ifnull(c.Gz50,-999), ifnull(f.m_tot - b.extinction_r - d.dismod - d.kcorr_r,-999), ifnull(log10(f.Hrad_corr*d.kpc_per_arcsec),-999), ifnull(f.m_tot - b.extinction_r - d.dismod - d.kcorr_r,-999), ifnull(log10(f.Hrad_corr*d.kpc_per_arcsec),-999) from ((((fmatches as a left join SSDR6 as c on a.galcount = c.galcount) left join  DERT as d on a.galcount = d.galcount) left join r_rerun_ser as f on f.galcount = a.galcount) left join r_rerun_serexp as g on f.galcount = g.galcount) left join CAST as b on a.galcount = b.galcount order by a.rowcount limit 10;

select count(*) from ((((fmatches as a left join SSDR6 as c on a.galcount = c.galcount) left join  DERT as d on a.galcount = d.galcount) left join r_rerun_ser as f on f.galcount = a.galcount) left join r_rerun_serexp as g on f.galcount = g.galcount) left join CAST as b on a.galcount = b.galcount where c.ra_gal is not null order by a.rowcount limit 10;

a.galid, ifnull(c.ra_gal,-999), ifnull(c.dec_gal,-999), ifnull(c.redshift,-999),ifnull(c.Vmaxwti,-999),ifnull(c.Ga50,-999),ifnull(c.Gz50,-999), ifnull(f.m_tot - b.extinction_r - d.dismod - d.kcorr_r,-999), ifnull(log10(f.Hrad_corr*d.kpc_per_arcsec),-999), ifnull(f.m_tot - b.extinction_r - d.dismod - d.kcorr_r,-999), ifnull(log10(f.Hrad_corr*d.kpc_per_arcsec),-999)
