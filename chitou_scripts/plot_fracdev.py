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

pp = PdfPages('fracdev.pdf')

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)

cmd = 'select a.devmag_r-a.extinction_r, a.expmag_r-a.extinction_r, a.fracdev_r, ifnull(-2.5*log10(a.fracdev_r*pow(10, -0.4*a.devmag_r) + (1.0*a.fracdev_r)*pow(10, -0.4*a.expmag_r))-a.extinction_r,-999), b.m_tot-a.extinction_r, b.m_bulge-a.extinction_r, b.m_disk-a.extinction_r, b.BT, f.m_bulge - a.extinction_r,  g.m_disk - a.extinction_r, ifnull(d.dismod+d.kcorr_r, -999) from CAST as a, r_rerun_cmodel as b,r_rerun_dev as f,r_rerun_exp as g, DERT as d where a.galcount = b.galcount and a.galcount = f.galcount and a.galcount = g.galcount and a.galcount = d.galcount;' 

data= cursor.get_data(cmd)

gals = {}
datnam = ['devmag', 'expmag', 'fracdev', 'cmodel', 'cmodel_us', 'bulge_us', 'disk_us','BT', 'dev_us','exp_us','abscorr']
for d,n in zip(data,datnam):
    gals[n]=np.array(d)

xlimsmag=(13.0,19.0)
xlimsabsmag=(-26.0,-21.0)
magbins = np.arange(13.0,19.0, 0.5)
BT_bins = np.arange(0.0,1.01, 0.1)
absmagbins = np.arange(-26.0,-21.0, 0.5)
fracdevbins = np.arange

devplot = outlier_fig(figsize=(6.0,4.0))
devplot.setminval(10)
devplot.set_ticks(0.5, 0.1, '%02.1f', .1, 0.05,'%02.1f')
devplot.makeplot(gals['BT'],gals['bulge_us']-gals['dev_us'], (0.0,1.0), (-0.3,1.5)) 
pl.xlabel('BT$_{cmodel}$')
pl.ylabel('$\Delta$m$_{dev}$(cm-us)')
devplot.bin_it(BT_bins, -5, 5)
devplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

devplot = outlier_fig(figsize=(6.0,4.0))
devplot.setminval(10)
devplot.set_ticks(0.5, 0.1, '%02.1f', .1, 0.05,'%02.1f')
devplot.makeplot(gals['BT'],gals['disk_us']-gals['exp_us'], (0.0,1.0), (-0.3,1.5)) 
pl.xlabel('BT$_{cmodel}$')
pl.ylabel('$\Delta$m$_{exp}$(cm-us)')
devplot.bin_it(BT_bins, -5, 5)
devplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

devplot = outlier_fig(figsize=(6.0,4.0))
devplot.setminval(10)
devplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
devplot.makeplot(gals['devmag'],gals['bulge_us']-gals['dev_us'], xlimsmag, (-0.8,0.3)) 
pl.xlabel('m$_{dev, SDSS}$')
pl.ylabel('$\Delta$m$_{dev}$(cm-us)')
devplot.bin_it(magbins, -5, 5)
devplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

expplot = outlier_fig(figsize=(6.0,4.0))
expplot.setminval(10)
expplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
expplot.makeplot(gals['expmag'],gals['disk_us']-gals['exp_us'], xlimsmag, (-0.5,0.5)) 
pl.xlabel('m$_{exp, SDSS}$' )
pl.ylabel('$\Delta$m$_{exp}$(cm-us)' )
expplot.bin_it(magbins, -5, 5)
expplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()


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
cplot.makeplot(gals['cmodel'],gals['cmodel_us']-gals['cmodel'], xlimsmag, (-0.5,0.5)) 
pl.xlabel('m$_{cmodel, SDSS}$' )
pl.ylabel('$\Delta$m$_{cmodel}$(us-sdss)' )
cplot.bin_it(magbins, -5, 5)
cplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

cplot = outlier_fig(figsize=(6.0,4.0))
cplot.setminval(10)
cplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
cplot.makeplot(gals['cmodel'],gals['BT']-gals['fracdev'], xlimsmag, (-1.5,1.5)) 
pl.xlabel('m$_{cmodel, SDSS}$' )
pl.ylabel('$\Delta$m$_{fracdev}$(us-sdss)' )
cplot.bin_it(magbins, -5, 5)
cplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

eplot = outlier_fig(figsize=(6.0,4.0))
eplot.setminval(10)
eplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
eplot.makeplot(gals['cmodel'],gals['devmag']-gals['expmag'], xlimsmag, (-0.9,0.1)) 
pl.xlabel('m$_{cmodel, SDSS}$' )
pl.ylabel('$\Delta$m$_{dev-exp}$(sdss)' )
eplot.bin_it(magbins, -5, 5)
eplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

dplot = outlier_fig(figsize=(6.0,4.0))
dplot.setminval(10)
dplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
dplot.makeplot(gals['cmodel'],gals['dev_us']-gals['exp_us'], xlimsmag, (-0.9,0.1)) 
pl.xlabel('m$_{cmodel, SDSS}$' )
pl.ylabel('$\Delta$m$_{dev-exp}$(Pymorph)' )
dplot.bin_it(magbins, -5, 5)
dplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()










devplot = outlier_fig(figsize=(6.0,4.0))
devplot.setminval(10)
devplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
devplot.makeplot(gals['devmag']-gals['abscorr'],gals['dev_us']-gals['devmag'], xlimsabsmag, (-0.8,0.3)) 
pl.xlabel('M$_{dev, SDSS}$')
pl.ylabel('$\Delta$m$_{dev}$(us-sdss)')
devplot.bin_it(absmagbins, -5, 5)
devplot.add_bars('r')
pl.plot(pl.xlim(),(0,0), 'r--') 
pp.savefig()

expplot = outlier_fig(figsize=(6.0,4.0))
expplot.setminval(10)
expplot.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
expplot.makeplot(gals['expmag']-gals['abscorr'],gals['exp_us']-gals['expmag'], xlimsabsmag, (-0.5,0.5)) 
pl.xlabel('M$_{exp, SDSS}$' )
pl.ylabel('$\Delta$m$_{exp}$(us-sdss)' )
expplot.bin_it(absmagbins, -5, 5)
expplot.add_bars('r')
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