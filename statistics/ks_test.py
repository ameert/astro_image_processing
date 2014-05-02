import numpy as np
import scipy.stats as stats
import pylab as pl


def weighted_ECDF(values, weight, bins = 10, dat_range='NONE'):
    if dat_range == 'NONE':
        dat_range = np.array([np.min(values), np.max(values)])
    
    weight_norm = np.sum(weight)
    weighted_I = values*weight

    bin_ends = np.linspace(dat_range[0], dat_range[1], num = bins+1)
    
    wECDF = []
    for step in bin_ends:
        wECDF.append(np.sum(np.extract(values <= step, weight)))
    
    wECDF = np.array(wECDF)
    wECDF = wECDF/weight_norm

    return bin_ends, wECDF

def ks_weighted(val1, weight1, val2, weight2):
    bin_end1, ecdf1 = weighted_ECDF(val1, weight1, bins = 1000, dat_range=(-27,-13))
    bin_end2, ecdf2 = weighted_ECDF(val2, weight2, bins = 1000, dat_range=(-27,-13))
    pl.clf()
    pl.semilogy(bin_end1, ecdf1, 'k--')
    pl.semilogy(bin_end2, ecdf2, 'r:')
    pl.show()

    max_diff = np.max(np.abs(ecdf1-ecdf2))
    
    critical_val = 1.36*np.sqrt((float(len(val1))+float(len(val2)))/(float(len(val1))*float(len(val2))))

    print max_diff, critical_val
    print 4.0*max_diff**2.0 *((float(len(val1))+float(len(val2)))/(float(len(val1))*float(len(val2))))
    
    
    return
