import pylab as pl
from mysql_class import *
import numpy as np

cursor = mysql_connect('catalog', 'pymorph', 'pymorph', '')

cmd = 'select a.galcount, a.inres, a.inressq, a.outres, a.outressq, b.Hrad_corr,b.m_tot, b.m_tot - c.extinction_r-d.dismod  from resid_ser as a, r_band_ser as b, CAST as c, DERT as d where a.galcount = b.galcount and b.galcount = c.galcount and c.galcount = d.galcount and a.inres between -300 and 300 and a.outres between -300 and 300;'

galcount, inres, inressq, outres, outressq, hrad, mag, absmag = cursor.get_data(cmd)

inres = np.array(inres)
inressq = np.array(inressq)
outres = np.array(outres)
outressq = np.array(outressq)

def get_stat(arr):
    mean = np.mean(arr)
    std = np.std(arr)
    count = np.sum(np.where((np.abs(arr-mean)/std)>3, 1,0))
    print mean, std, count, len(arr)

    return mean, std

mean, std = get_stat(inres)

fig = pl.figure()
fig.add_subplot(2,2,1)
pl.hist(inres, bins = 1000, range = (mean-5*std, mean + 5*std), histtype = 'step', normed = True)
yval = pl.ylim()
pl.plot([mean-3*std,mean-3*std], yval, 'k:')
pl.plot([mean+3*std,mean+3*std], yval, 'k:')

fig.add_subplot(2,2,2)
bad_mag = np.extract((np.abs(inres-mean)/std)>3, mag)
pl.hist(bad_mag, bins = 1000, range = (12, 18), histtype = 'step', normed = True)
pl.ylim((0,.5))

fig.add_subplot(2,2,3)
pl.hist(absmag, bins = 1000, range = (-25, -18), histtype = 'step', normed = True)

fig.add_subplot(2,2,4)
bad_absmag = np.extract((np.abs(inres-mean)/std)>3, absmag)
pl.hist(bad_absmag, bins = 1000, range = (-25, -18), histtype = 'step', normed = True)


pl.savefig('inres.eps')
pl.clf()

mean, std = get_stat(outres)
fig = pl.figure()
fig.add_subplot(2,2,1)
pl.hist(outres, bins = 1000, range = (mean-5*std, mean + 5*std), histtype = 'step', normed = True)
yval = pl.ylim()
pl.plot([mean-3*std,mean-3*std], yval, 'k:')
pl.plot([mean+3*std,mean+3*std], yval, 'k:')

fig.add_subplot(2,2,2)
bad_mag = np.extract((np.abs(outres-mean)/std)>3, mag)
pl.hist(bad_mag, bins = 1000, range = (12, 18), histtype = 'step', normed = True)
pl.ylim((0,.5))

fig.add_subplot(2,2,3)
pl.hist(absmag, bins = 1000, range = (-25, -18), histtype = 'step', normed = True)

fig.add_subplot(2,2,4)
bad_absmag = np.extract((np.abs(outres-mean)/std)>3, absmag)
pl.hist(bad_absmag, bins = 1000, range = (-25, -18), histtype = 'step', normed = True)

pl.savefig('outres.eps')
pl.clf()
    
