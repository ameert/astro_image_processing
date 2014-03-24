import numpy as np
import pylab as  pl

#to run this script, you need a file with absmag and vmax columns


def lum_func(absmag, vmax, resolution, filename):
    fig = pl.figure(figsize = (3,2))            
    pl.subplots_adjust(bottom=0.23, left = 0.23)

    V_weight = 1.0/vmax
    
    bins = np.arange(-25.0, -15.999, resolution)
    
    mag_bins = np.digitize(absmag, bins)

    func_vals = np.array([np.sum(np.where(mag_bins==count,V_weight,0)) for count in range(1,len(bins))])/np.sum(V_weight)
    
    print func_vals
    print bins
    pl.bar(bins[:-1], np.log10(func_vals)+10.0, resolution, bottom=-10.0, color="g", edgecolor = 'none')

    pl.xlim(-16,-25)
    pl.ylim(-10.0,0)
    pl.xlabel('M$_{r}$')
    pl.ylabel('log(n)')
    
    ax = pl.gca()
    yloc = pl.MaxNLocator(6)
    ax.xaxis.set_major_locator(yloc)

    pl.savefig(filename)
    pl.close(fig)
    return


def absmag_dist(absmag, resolution, filename):
    vmax = np.ones_like(absmag)

    lum_func(absmag, vmax, resolution, filename)
    return


absmag, Vmax = np.loadtxt('test.txt', skiprows = 1, unpack = True)
lum_func(absmag, Vmax, 0.5, 'test_lum_func.eps')
absmag_dist(absmag, 0.5, 'test_absmag_dist.eps')
