import pylab as pl
import numpy as np
from MatplotRc import *

noba=False

if noba:
    psfrat, bflag, tcflag, btcflag = np.loadtxt('outpsf_noba_all.txt', skiprows=1, unpack=True)
else:
    psfrat, bflag, tcflag, btcflag = np.loadtxt('outpsf_all_BT.txt', skiprows=1, unpack=True)

psfrat = np.array(psfrat)
bflag=np.array(bflag, dtype =int)
tcflag=np.array(tcflag, dtype =int)
btcflag=np.array(btcflag, dtype =int)

fig = pl.figure(figsize=(3,2))
pl.subplot(1,1,1)
p1 = pub_plots(ymaj = 0.02, ymin = .002, ystr = '%0.2f',xmaj = 1, xmin = 0.1, xstr = '%d')
pstmp = np.array(list(np.extract(bflag>0.5, psfrat))+list(np.extract(tcflag>0.5, psfrat)))
pl.hist(pstmp, range = (0,10), bins = 100, histtype='step', weights = np.ones_like(pstmp)/pstmp.size, color='k')
pl.ylabel('N/N$_{tot}$')
pl.xlabel('r$_{bulge}$/seeing')
#pl.text(8.0, 0.8*pl.ylim()[1], "%%< 0.8HWHM:%f" %float(np.sum(np.where(psfrat<0.8,1,0)))/psfrat.size)
#pl.text(8.0, 0.7*pl.ylim()[1], "%%< HWHM:%f" %float(np.sum(np.where(psfrat<1.0,1,0)))/psfrat.size)

#pl.text(8.0, 0.8*pl.ylim()[1], "%%< 0.8HWHM:%f" %float(np.sum(np.where(psfrat<0.8,1,0)))/psfrat.size)
#pl.text(8.0, 0.7*pl.ylim()[1], "%f" %float(np.sum(np.where(psfrat<1.0,1,0)))/psfrat.size)
print float(np.sum(np.where(pstmp<0.8,1,0)))/pstmp.size
print float(np.sum(np.where(pstmp<1.0,1,0)))/pstmp.size
p1.set_plot(pl.gca())
pl.xlim(0,5)
ylims = pl.ylim()
pl.plot((0.8, 0.8), pl.ylim(), 'k:')
pl.plot((1.0, 1.0), pl.ylim(), 'k--')
pl.ylim(ylims)
if 0:
    pl.subplot(2,2,2)
    p2 = pub_plots(xmaj = 1, xmin = .1, xstr = '%d',ymaj = 1000, ymin = 100, ystr = '%d')
    pstmp = np.extract(bflag>0.5, psfrat)
    pl.hist(pstmp, range = (0,10), bins = 50, histtype='step')
    pl.title("bulges")
    #pl.text(8.0, 0.8*pl.ylim()[1], "%%< 0.8HWHM:%f" %float(np.sum(np.where(pstmp<0.8,1,0)))/pstmp.size)
    #pl.text(8.0, 0.7*pl.ylim()[1], "%%< HWHM:%f" %float(np.sum(np.where(pstmp<1.0,1,0)))/pstmp.size)
    print float(np.sum(np.where(pstmp<0.8,1,0)))/pstmp.size
    print float(np.sum(np.where(pstmp<1.0,1,0)))/pstmp.size
    #p2.set_plot(pl.gca())
    pl.plot((0.8, 0.8), pl.ylim(), 'k:')
    pl.plot((1.0, 1.0), pl.ylim(), 'k--')


    pl.subplot(2,2,3)
    p3 = pub_plots(xmaj = 1, xmin = .1, xstr = '%d',ymaj = 1000, ymin = 100, ystr = '%d')
    pstmp = np.extract(tcflag>0.5, psfrat)
    pl.hist(pstmp, range = (0,10), bins = 50, histtype='step')
    pl.title("2com")
    pl.plot((0.8, 0.8), pl.ylim(), 'k:')
    pl.plot((1.0, 1.0), pl.ylim(), 'k--')
    #pl.text(8.0, 0.8*pl.ylim()[1], "%%< 0.8HWHM:%f" %float(np.sum(np.where(pstmp<0.8,1,0)))/pstmp.size)
    #pl.text(8.0, 0.7*pl.ylim()[1], "%%< HWHM:%f" %float(np.sum(np.where(pstmp<1.0,1,0)))/pstmp.size)
    print float(np.sum(np.where(pstmp<0.8,1,0)))/pstmp.size
    print float(np.sum(np.where(pstmp<1.0,1,0)))/pstmp.size
    #p3.set_plot(pl.gca())

    pl.subplot(2,2,4)
    p4 = pub_plots(xmaj = 1, xmin = .1, xstr = '%d',ymaj = 100, ymin = 10, ystr = '%d')
    pstmp = np.extract(btcflag>0.5, psfrat)
    pl.hist(pstmp, range = (0,10), bins = 50, histtype='step')
    pl.title("Problem 2com")
    pl.plot((0.8, 0.8), pl.ylim(), 'k:')
    pl.plot((1.0, 1.0), pl.ylim(), 'k--')
    #pl.text(8.0, 0.8*pl.ylim()[1], "%%< 0.8HWHM:%f" %float(np.sum(np.where(pstmp<0.8,1,0)))/pstmp.size)
    #pl.text(8.0, 0.7*pl.ylim()[1], "%%< HWHM:%f" %float(np.sum(np.where(pstmp<1.0,1,0)))/pstmp.size)
    print float(np.sum(np.where(pstmp<0.8,1,0)))/pstmp.size
    print float(np.sum(np.where(pstmp<1.0,1,0)))/pstmp.size
    #p4.set_plot(pl.gca())

pl.subplots_adjust(wspace=0.25, hspace=0.35, left = .25, bottom=0.23)


if noba:
    pl.savefig('bulge_vs_psf_noba_all.eps')
else:
    pl.savefig('bulge_vs_psf_all.eps')
