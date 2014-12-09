from astro_image_processing.mysql import *
import os
import itertools
import pyfits
import datetime
import sys

dba = 'catalog'
pwd = 'pymorph'
usr = 'pymorph'

stem = 'newt503'

cursor = mysql_connect(dba, usr, pwd)

cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
c.C, f.petroR50_r,f.petro90_r, a.hrad_tot_corr, b.hrad_tot_corr
from 
catalog.r_band_ser as a,
catalog.r_band_fit as c,
catalog.r_band_serexp as b, 
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_optimize as u,
COLOR_GRAD_ser as z
where
f.galcount = c.galcount and 
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
f.galcount = z.galcount and u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
order by f.galcount 
into outfile "/tmp/%s_1.txt";""" %(stem)

cursor.execute(cmd)


os.system('cp /tmp/%s_1.txt ./galtable.txt' %(stem))

