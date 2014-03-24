import pylab as pl
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from cmp_functions import *
from MatplotRc import *
import matplotlib
import matplotlib.colors as col
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mysql_class import *

pp = PdfPages('fracdev_unch.pdf')

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)

cmd = """select 
a.devmag_r-a.extinction_r, 
a.expmag_r-a.extinction_r, 
a.fracdev_r, 
ifnull(-2.5*log10(a.fracdev_r*pow(10, -0.4*a.devmag_r) + (1.0*a.fracdev_r)*pow(10, -0.4*a.expmag_r))-a.extinction_r,-999), 
ifnull(b.m_tot-a.extinction_r,-999), 
ifnull(c.m_tot-a.extinction_r,-999), 
ifnull(-2.5*log10(a.fracdev_r*pow(10, -0.4*s.m_bulge) + (1.0*a.fracdev_r)*pow(10, -0.4*t.m_disk))-a.extinction_r,-999), 
ifnull(d.dismod+d.kcorr_r, -999), 
ifnull(s.m_tot-a.extinction_r,-999), 
ifnull(t.m_tot-a.extinction_r,-999), 
ifnull(u.m_tot-a.extinction_r,-999), 
ifnull(v.m_tot-a.extinction_r,-999), 
ifnull(w.m_tot-a.extinction_r,-999), 
ifnull(x.m_tot-a.extinction_r,-999)
from 
CAST as a, DERT as d,
r_band_dev as b, r_band_exp as c, r_band_ser as w, r_band_serexp as x,
r_rerun_dev as s, r_rerun_exp as t,r_rerun_ser as u,r_rerun_serexp as v,
full_dr7_neighborcount as z
where a.galcount = b.galcount and a.galcount = c.galcount and d.galcount = a.galcount and a.galcount = s.galcount and a.galcount = t.galcount and a.galcount = u.galcount and a.galcount = v.galcount and a.galcount = w.galcount and a.galcount = x.galcount and a.galcount = z.galcount and z.num_neigh_r = z.rerun_count;""" 

data= cursor.get_data(cmd)

gals = {}
datnam = ['devmag', 'expmag', 'fracdev', 'cmodel', 'dev_old', 'exp_old',
          'cmodel_us','abscorr',
          'dev_us','exp_us','ser_us', 'serexp_us','ser_old', 'serexp_old', 
          ]
for d,n in zip(data,datnam):
    gals[n]=np.array(d)

xlimsmag=(13.0,19.0)
xlimsabsmag=(-26.0,-21.0)
magbins = np.arange(13.0,19.0, 0.5)
absmagbins = np.arange(-26.0,-21.0, 0.5)
fracdevbins = np.arange

devplot = outlier_fig(figsize=(6.0,4.0))
devplot.setminval(10)
devplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
devplot.makeplot(gals['devmag'],gals['dev_us']-gals['devmag'], xlimsmag, (-0.8,0.3)) 
pl.xlabel('m$_{dev, SDSS}$')
pl.ylabel('$\Delta$m$_{dev}$(us-sdss)')
devplot.bin_it(magbins, -5, 5)
devplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

expplot = outlier_fig(figsize=(6.0,4.0))
expplot.setminval(10)
expplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
expplot.makeplot(gals['expmag'],gals['exp_us']-gals['expmag'], xlimsmag, (-0.5,0.5)) 
pl.xlabel('m$_{exp, SDSS}$' )
pl.ylabel('$\Delta$m$_{exp}$(us-sdss)' )
expplot.bin_it(magbins, -5, 5)
expplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

cplot = outlier_fig(figsize=(6.0,4.0))
cplot.setminval(10)
cplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
cplot.makeplot(gals['cmodel'],gals['dev_us']-gals['dev_old'], xlimsmag, (-0.5,0.5)) 
pl.xlabel('m$_{cmodel, SDSS}$' )
pl.ylabel('$\Delta$m$_{dev}$(us-old)' )
cplot.bin_it(magbins, -5, 5)
cplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

cplot = outlier_fig(figsize=(6.0,4.0))
cplot.setminval(10)
cplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
cplot.makeplot(gals['cmodel'],gals['ser_us']-gals['ser_old'], xlimsmag, (-0.5,0.5)) 
pl.xlabel('m$_{cmodel, SDSS}$' )
pl.ylabel('$\Delta$m$_{ser}$(us-old)' )
cplot.bin_it(magbins, -5, 5)
cplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

cplot = outlier_fig(figsize=(6.0,4.0))
cplot.setminval(10)
cplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
cplot.makeplot(gals['cmodel'],gals['serexp_us']-gals['serexp_old'], xlimsmag, (-0.5,0.5)) 
pl.xlabel('m$_{cmodel, SDSS}$' )
pl.ylabel('$\Delta$m$_{serexp}$(us-old)' )
cplot.bin_it(magbins, -5, 5)
cplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

devplot = outlier_fig(figsize=(6.0,4.0))
devplot.setminval(10)
devplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
devplot.makeplot(gals['devmag']-gals['abscorr'],gals['dev_us']-gals['dev_old'], xlimsabsmag, (-0.5,0.5)) 
pl.xlabel('M$_{dev, SDSS}$')
pl.ylabel('$\Delta$m$_{dev}$(us-old)')
devplot.bin_it(absmagbins, -5, 5)
devplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

devplot = outlier_fig(figsize=(6.0,4.0))
devplot.setminval(10)
devplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
devplot.makeplot(gals['devmag']-gals['abscorr'],gals['ser_us']-gals['ser_old'], xlimsabsmag, (-0.5,0.5)) 
pl.xlabel('M$_{dev, SDSS}$')
pl.ylabel('$\Delta$m$_{ser}$(us-old)')
devplot.bin_it(absmagbins, -5, 5)
devplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

expplot = outlier_fig(figsize=(6.0,4.0))
expplot.setminval(10)
expplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
expplot.makeplot(gals['expmag']-gals['abscorr'],gals['exp_us']-gals['exp_old'], xlimsabsmag, (-0.5,0.5)) 
pl.xlabel('M$_{exp, SDSS}$' )
pl.ylabel('$\Delta$m$_{exp}$(us-old)' )
expplot.bin_it(absmagbins, -5, 5)
expplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

devplot = outlier_fig(figsize=(6.0,4.0))
devplot.setminval(10)
devplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
devplot.makeplot(gals['cmodel']-gals['abscorr'],gals['serexp_us']-gals['serexp_old'], xlimsabsmag, (-0.5,0.5)) 
pl.xlabel('M$_{dev, SDSS}$')
pl.ylabel('$\Delta$m$_{serexp}$(us-old)')
devplot.bin_it(absmagbins, -5, 5)
devplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

cplot = outlier_fig(figsize=(6.0,4.0))
cplot.setminval(10)
cplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
cplot.makeplot(gals['cmodel']-gals['abscorr'],gals['cmodel_us']-gals['cmodel'], xlimsabsmag, (-0.5,0.5)) 
pl.xlabel('M$_{cmodel, SDSS}$' )
pl.ylabel('$\Delta$m$_{cmodel}$(us-sdss)' )
cplot.bin_it(absmagbins, -5, 5)
cplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

eplot = outlier_fig(figsize=(6.0,4.0))
eplot.setminval(10)
eplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
eplot.makeplot(gals['cmodel']-gals['abscorr'],gals['devmag']-gals['expmag'], xlimsabsmag, (-0.9,0.1)) 
pl.xlabel('M$_{cmodel, SDSS}$' )
pl.ylabel('$\Delta$m$_{dev-exp}$(sdss)' )
eplot.bin_it(absmagbins, -5, 5)
eplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

dplot = outlier_fig(figsize=(6.0,4.0))
dplot.setminval(10)
dplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
dplot.makeplot(gals['cmodel']-gals['abscorr'],gals['dev_us']-gals['exp_us'], xlimsabsmag, (-0.9,0.1)) 
pl.xlabel('M$_{cmodel, SDSS}$' )
pl.ylabel('$\Delta$m$_{dev-exp}$(Pymorph)' )
dplot.bin_it(absmagbins, -5, 5)
dplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

pp.close()
