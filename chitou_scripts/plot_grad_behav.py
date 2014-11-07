#create table test_grads (galcount int primary key, z float default -999, r_r float default -999, r_g float default -999, n_r float default -999, n_g float default -999, sky_1_g float default -999, sky_1_r float default -999, m_10_g float, m_10_r float, m_15_g float, m_15_r float, m_30_g float, m_30_r float, grad_10_gr float, grad_15_gr float, grad_30_gr float);
#insert into test_grads (galcount, z) select a.galcount, a.z from CAST as a, M2010 as m where a.galcount = m.galcount and m.probaE>0.5 and a.z between 0.13 and 0.16 order by RAND() limit 1000;
#insert into test_grads (galcount, z) select a.galcount, a.z from CAST as a, M2010 as m where a.galcount = m.galcount and m.probaE>0.5 and a.z between 0.03 and 0.06 order by RAND() limit 1000;
#update test_grads as a, r_band_ser as b set a.r_r=b.r_bulge*sqrt(b.ba_bulge), a.n_r=b.n_bulge, a.sky_1_r=-2.5/log(10)*log(pow(10.0, -0.4*b.Galsky-2)/2 + sqrt(pow(1.2e-10,2.0)+0.25*pow(10,-0.8*b.Galsky-4))) where a.galcount = b.galcount;
#update test_grads as a, g_band_ser as b set a.r_g=b.r_bulge*sqrt(b.ba_bulge), a.n_g=b.n_bulge, a.sky_1_g=-2.5/log(10)*log(pow(10.0, -0.4*b.Galsky-2)/2 + sqrt(pow(9.0e-11,2.0)+0.25*pow(10,-0.8*b.Galsky-4))) where a.galcount = b.galcount;
#update test_grads as a, ser_magHL_serrad as b set a.m_10_g=b.g_mag,a.m_10_r=b.r_mag where b.HL_rad_10=10 and a.galcount = b.galcount;
#update test_grads as a, ser_magHL_serrad as b set a.m_15_g=b.g_mag,a.m_15_r=b.r_mag where b.HL_rad_10=15 and a.galcount = b.galcount;
#update test_grads as a, ser_magHL_serrad as b set a.m_30_g=b.g_mag,a.m_30_r=b.r_mag where b.HL_rad_10=30 and a.galcount = b.galcount;
#update test_grads as a, ser_colorgrad_serrad as z set a.grad_10_gr=z.grCenter_hl,a.grad_15_gr=z.gr15_hl,a.grad_30_gr=z.gr3_hl where  a.galcount = z.galcount;


import pylab as pl
import numpy as np
from mysql_class import *

dba = 'catalog'
pwd = 'pymorph'
usr = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

lowz_data = cursor.get_data('select * from test_grads where z<0.1;')
highz_data = cursor.get_data('select * from test_grads where z>0.1;')

lowz_data = [np.array(a) for a in lowz_data]
highz_data = [np.array(a) for a in highz_data]

pl.subplot(2,2,1)
pl.scatter(lowz_data[7]-lowz_data[9],lowz_data[14], s=2, c = 'g', edgecolor = 'none') 
pl.scatter(lowz_data[7]-lowz_data[11],lowz_data[15], s=2, c = 'k', edgecolor = 'none') 
pl.scatter(lowz_data[7]-lowz_data[13],lowz_data[16], s=2, c = 'b', edgecolor = 'none') 

pl.scatter(highz_data[7]-highz_data[9],highz_data[14], s=2, c = 'c', edgecolor = 'none') 
pl.scatter(highz_data[7]-highz_data[11],highz_data[15], s=2, c = 'r', edgecolor = 'none') 
pl.scatter(highz_data[7]-highz_data[13],highz_data[16], s=2, c = 'm', edgecolor = 'none') 
pl.xlim(0,7)
pl.ylim(-0.5,0.0)

pl.subplot(2,2,2)
pl.scatter(lowz_data[2]/lowz_data[3],lowz_data[14], s=2, c = 'g', edgecolor = 'none') 
pl.scatter(lowz_data[2]/lowz_data[3],lowz_data[15], s=2, c = 'k', edgecolor = 'none') 
pl.scatter(lowz_data[2]/lowz_data[3],lowz_data[16], s=2, c = 'b', edgecolor = 'none') 

pl.scatter(highz_data[2]/highz_data[3],highz_data[14], s=2, c = 'c', edgecolor = 'none') 
pl.scatter(highz_data[2]/highz_data[3],highz_data[15], s=2, c = 'r', edgecolor = 'none') 
pl.scatter(highz_data[2]/highz_data[3],highz_data[16], s=2, c = 'm', edgecolor = 'none') 
pl.xlim(0.5,1.5)
pl.ylim(-0.5,0.0)

pl.subplot(2,2,3)
pl.scatter(lowz_data[4]/lowz_data[5],lowz_data[14], s=2, c = 'g', edgecolor = 'none') 
pl.scatter(lowz_data[4]/lowz_data[5],lowz_data[15], s=2, c = 'k', edgecolor = 'none') 
pl.scatter(lowz_data[4]/lowz_data[5],lowz_data[16], s=2, c = 'b', edgecolor = 'none') 

pl.scatter(highz_data[4]/highz_data[5],highz_data[14], s=2, c = 'c', edgecolor = 'none') 
pl.scatter(highz_data[4]/highz_data[5],highz_data[15], s=2, c = 'r', edgecolor = 'none') 
pl.scatter(highz_data[4]/highz_data[5],highz_data[16], s=2, c = 'm', edgecolor = 'none') 
pl.xlim(0.5,1.5)
pl.ylim(-0.5,0.0)

pl.show()
