from mysql_class import *
import os
import itertools
import pyfits
import datetime
import sys

dba = 'catalog'
pwd = 'al130568'
usr = 'ameert'

stem = 'newt507'

cursor = mysql_connect(dba, usr, pwd)

cmd = """select f.galcount, f.ra_gal, f.dec_gal, f.z,
c.C, f.petroR50_r,f.petroR90_r, 
a.hrad_corr, b.hrad_corr,
a.ba_tot_corr, b.ba_tot_corr,
e.r20*0.396, e.r20e*0.396, e.r50*0.396, e.r50e*0.396,
e.r80*0.396, e.r80e*0.396, e.r90*0.396, e.r90e*0.396,
IFNULL(g.r20*sqrt(a.ba_bulge),-999), IFNULL(g.r50*sqrt(a.ba_bulge),-999),
IFNULL(g.r80*sqrt(a.ba_bulge),-999), IFNULL(g.r90*sqrt(a.ba_bulge),-999),
h.r20*0.396, h.r50*0.396,
h.r80*0.396, h.r90*0.396
from 
catalog.ser_conc_rads as g,
catalog.serexp_conc_rads as h,
catalog.agm_data as e,
catalog.r_band_ser as a,
catalog.r_band_fit as c,
catalog.r_band_serexp as b, 
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_optimize as u,
COLOR_GRAD_ser as z
where
f.galcount = g.galcount and
f.galcount = h.galcount and
f.galcount = e.galcount and
f.galcount = c.galcount and 
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
f.galcount = z.galcount and u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
order by f.galcount 
into outfile "/tmp/%s_1.txt";""" %(stem)

#cursor.execute(cmd)
#os.system('cp /tmp/%s_1.txt /scratch/concentration.txt' %(stem))




cmd = """select f.galcount, 
a.hrad_corr, b.hrad_corr,
a.ba_tot_corr, b.ba_tot_corr,
g.r20*0.396,g.r50*0.396,g.r80*0.396,g.r90*0.396,
h.r20*0.396, h.r50*0.396,h.r80*0.396, h.r90*0.396
from 
catalog.ser_conc_rads as g,
catalog.serexp_conc_rads as h,
catalog.agm_data as e,
catalog.r_band_ser as a,
catalog.r_band_fit as c,
catalog.r_band_serexp as b, 
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_optimize as u,
COLOR_GRAD_ser as z
where
f.galcount = g.galcount and
f.galcount = h.galcount and
f.galcount = e.galcount and
f.galcount = c.galcount and 
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
f.galcount = z.galcount and u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
order by f.galcount 
into outfile "/tmp/%s_2.txt";""" %(stem)

#cursor.execute(cmd)
#os.system('echo "#galcount, hrad_ser, hrad_serexp, ba_ser, ba_serexp, r20_ser, r50_ser, r80_ser, r90_ser,r20_serexp, r50_serexp, r80_serexp, r90_serexp" > /scratch/concentration_alans_code.txt' )
#os.system('cat /tmp/%s_2.txt >> /scratch/concentration_alans_code.txt' %(stem))

cmd = """select f.galcount, 
aser.r20*0.396, aser.r50*0.396, aser.r80*0.396, aser.r90*0.396,
aserexp.r20*0.396, aserexp.r50*0.396, aserexp.r80*0.396,  aserexp.r90*0.396
from 
catalog.agm_data_ser_no_psf as aser,
catalog.agm_data_serexp_no_psf as aserexp,
catalog.ser_conc_rads as g,
catalog.serexp_conc_rads as h,
catalog.agm_data as e,
catalog.r_band_ser as a,
catalog.r_band_fit as c,
catalog.r_band_serexp as b, 
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_optimize as u,
COLOR_GRAD_ser as z
where
f.galcount = aserexp.galcount and
f.galcount = aser.galcount and
f.galcount = g.galcount and
f.galcount = h.galcount and
f.galcount = e.galcount and
f.galcount = c.galcount and 
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
f.galcount = z.galcount and u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
order by f.galcount 
into outfile "/tmp/%s_3.txt";""" %(stem)

#cursor.execute(cmd)
#os.system('echo "#galcount, hrad_ser, hrad_serexp, ba_ser, ba_serexp, r20_ser, r50_ser, r80_ser, r90_ser,r20_serexp, r50_serexp, r80_serexp, r90_serexp" > /scratch/concentration_vinus_code.txt' )
#os.system('cat /tmp/%s_3.txt >> /scratch/concentration_vinus_code.txt' %(stem))


cmd = """select f.galcount, 
a.hrad_corr, b.hrad_corr,
a.ba_tot_corr, b.ba_tot_corr,
g.r20,g.r50,g.r80,g.r90,
h.r20, h.r50,h.r80, h.r90
from 
catalog.alan_1d_im_model_r_ser as g,
catalog.alan_1d_im_model_r_serexp as h,
catalog.agm_data as e,
catalog.r_band_ser as a,
catalog.r_band_fit as c,
catalog.r_band_serexp as b, 
catalog.CAST as f left join JHU.JHU_masses as j on f.galcount = j.galcount,
catalog.DERT as d, catalog.r_simard_fit as s,
catalog.M2010 as m, catalog.Flags_optimize as u,
COLOR_GRAD_ser as z
where
f.galcount = g.galcount and
f.galcount = h.galcount and
f.galcount = e.galcount and
f.galcount = c.galcount and 
f.galcount = a.galcount and f.galcount = b.galcount and 
f.galcount = d.galcount and f.galcount = s.galcount and
f.galcount = m.galcount and f.galcount = u.galcount and 
f.galcount = z.galcount and u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
order by f.galcount 
into outfile "/tmp/%s_4.txt";""" %(stem)

cursor.execute(cmd)
os.system('echo "#galcount, hrad_ser, hrad_serexp, ba_ser, ba_serexp, r20_ser, r50_ser, r80_ser, r90_ser,r20_serexp, r50_serexp, r80_serexp, r90_serexp" > /scratch/concentration_alans_code_interpolated.txt' )
os.system('cat /tmp/%s_4.txt >> /scratch/concentration_alans_code_interpolated.txt' %(stem))
