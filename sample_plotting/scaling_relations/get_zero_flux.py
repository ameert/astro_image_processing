import os
import sys
import numpy as np
from scipy.integrate import simps

speed_of_light = -3.0 * 10.0*8 * 10.0**10 # in angstroms

for band in 'ugriz':
    data = np.loadtxt('%s.dat' %band, unpack = True)
    data[0] = speed_of_light/data[0]
    flux = simps(data[3], data[0])
    print band, ' ', flux
