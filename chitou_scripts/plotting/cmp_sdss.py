from mysql_class import *
import numpy as np
import pylab as pl
from cmp_functions import *
from MatplotRc import *
import matplotlib
import matplotlib.colors as col
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages

for band in 'r':
    if band == 'i':
        xlimsmag = (13.0,19.0)
    elif band == 'r':
        xlimsmag = (13.0,19.0)
    elif band == 'g':
        xlimsmag = (14.0,20.0)

    magbins = np.arange(xlimsmag[0],xlimsmag[1], 0.5)
    radbins = np.arange(0.0,12.0, 1.0)

    cursor = mysql_connect('catalog','pymorph','pymorph','')

    cmd = 'select a.devmag_{band}, a.devRad_{band}, a.petroMag_{band}, petroR50_{band}, b.m_bulge, b.r_bulge from CAST as a, {band}_band_dev as b where a.galcount = b.galcount and a.fracdev_{band} =1.0;'.format(band = band)

    data = cursor.get_data(cmd)

    dat_names = ['sdss_devmag', 'sdss_devrad', 'Petromag', 'Petrorad', 'us_devmag',
                 'us_devrad']

    gal = {}
    for name, dat in zip(dat_names, data):
        gal[name] = np.array(dat, dtype=float)

    print "num gals ", len(gal['sdss_devmag'])

    #do devmag
    devmag = outlier_fig()

    devmag.set_ticks(2, 0.5, '%d', .1, 0.05,'%02.1f')
    devmag.makeplot(gal['us_devmag'],gal['us_devmag']-gal['sdss_devmag'], xlimsmag,
                    (-0.25,0.15)) 
    pl.xlabel('m$_{%s,dev, Pymorph}$' %band)
    pl.ylabel('$\Delta$m$_{%s,dev}$' %band)
    devmag.bin_it(magbins, -5, 5)
    devmag.add_bars('r')
    devmag.savefig('%s_dev_sdss_mag.eps' %band)

    #do devrad
    devrad = outlier_fig()
    devrad.set_ticks(2, 0.5,'%d', 10, 5, '%d')
    devrad.makeplot(gal['us_devrad'],100.0*(gal['us_devrad']-gal['sdss_devrad'])/gal['us_devrad'], (0.0,12.0), (-10.0,30.0))
    pl.xlabel('r$_{%s,dev, Pymorph}$["]' %band)
    pl.ylabel('$\Delta$r$_{%s,dev}$[%s]' %(band, '%'))
    devrad.bin_it(radbins, -100, 100)
    devrad.add_bars('r')
    devrad.savefig('%s_dev_sdss_rad.eps' %band)

    #do devrad vs mag
    devradmag = outlier_fig()
    devradmag.set_ticks(1, 0.25,'%d', 10, 5, '%d')
    devradmag.makeplot(gal['us_devmag'],100.0*(gal['us_devrad']-gal['sdss_devrad'])/gal['us_devmag'],xlimsmag, (-10.0,30.0))
    pl.xlabel('m$_{%s,dev, Pymorph}$["]' %band)
    pl.ylabel('$\Delta$r$_{%s,dev}$[%s]'  %(band, '%'))
    devradmag.bin_it(magbins, -100, 100)
    devradmag.add_bars('r')
    devradmag.savefig('%s_dev_sdss_magrad.eps' %band)


