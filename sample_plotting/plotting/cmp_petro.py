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

    cmd = 'select a.modelmag_{band}, a.devRad_{band}, a.petroMag_{band}, petroR50_{band}, IF(d.p_ser <= 0.5, b.m_tot, c.m_tot),IF(d.p_ser <= 0.5, b.Hrad_corr*sqrt(b.ba_tot_corr),c.Hrad_corr*sqrt(c.ba_tot_corr) ) from CAST as a, {band}_band_ser as b, {band}_band_serexp as c, svm_probs as d where a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount;'.format(band = band)

    data = cursor.get_data(cmd)

    dat_names = ['Modelmag', 'sdss_devrad', 'Petromag', 'Petrorad', 'us_mag',
                 'us_rad']

    gal = {}
    for name, dat in zip(dat_names, data):
        gal[name] = np.array(dat, dtype=float)

    print "num gals ", len(gal['us_mag'])

    #do petromag
    print "petromag ", band
    pmag = outlier_fig()

    pmag.set_ticks(1, 0.5, '%d', .2, 0.05,'%02.1f')
    pmag.makeplot(gal['us_mag'],gal['us_mag']-gal['Petromag'], xlimsmag,
                    (-0.6,0.3)) 
    pl.xlabel('m$_{%s, Pymorph}$' %band)
    pl.ylabel('$\Delta$m$_{%s,Petro}$' %band)
    pmag.bin_it(magbins, -5, 5)
    pmag.add_bars('r')
    pmag.savefig('%s_petro_sdss_mag.eps' %band)
    

    #do modelmag
    print "modelmag ", band
    mmag = outlier_fig()

    mmag.set_ticks(1, 0.5, '%d', .2, 0.05,'%02.1f')
    mmag.makeplot(gal['us_mag'],gal['us_mag']-gal['Modelmag'], xlimsmag,
                    (-0.5,0.5)) 
    pl.xlabel('m$_{%s, Pymorph}$' %band)
    pl.ylabel('$\Delta$m$_{%s,Model}$' %band)
    mmag.bin_it(magbins, -5, 5)
    mmag.add_bars('r')
    mmag.savefig('%s_model_sdss_mag.eps' %band)
    
    #do rad
    print "petrorad ", band
    prad = outlier_fig()
    prad.set_ticks(2, 0.5,'%d', 20, 5, '%d')
    prad.makeplot(gal['us_rad'],100.0*(gal['us_rad']-gal['Petrorad'])/gal['us_rad'], (0.0,12.0), (-40.0,100.0))
    pl.xlabel('r$_{%s,Pymorph}$["]' %band)
    pl.ylabel('$\Delta$r$_{%s,Petro}$[%s]' %(band, '%'))
    prad.bin_it(radbins, -100, 100)
    prad.add_bars('r')
    prad.savefig('%s_petro_sdss_rad.eps' %band)

    #do rad vs mag
    print "petro radmag ", band
    radmag = outlier_fig()
    radmag.set_ticks(1, 0.25,'%d', 10, 5, '%d')
    radmag.makeplot(gal['us_mag'],100.0*(gal['us_rad']-gal['Petrorad'])/gal['us_mag'],xlimsmag, (-20.0,30.0))
    pl.xlabel('m$_{%s,Pymorph}$["]' %band)
    pl.ylabel('$\Delta$r$_{%s,Petro}$[%s]'  %(band, '%'))
    radmag.bin_it(magbins, -100, 100)
    radmag.add_bars('r')
    radmag.savefig('%s_petro_sdss_magrad.eps' %band)


