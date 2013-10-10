# the user-defined param values used by astro_utils


#SDSS asinh softening params
softb = {'u': 1.4e-10,'g': 9.0e-11,'r': 1.2e-10,'i': 1.8e-10,'z': 7.4e-10}

defaults = {'exptime':53.907456,#sec,(www.sdss.org/dr3/algorithms/fluxcal.html)
            'kk':0.0,
            'airmass':0.0,
            'band':'r',
            'magtype':'pogson',
            'pixsz':0.396 #arcsec/pixel, from SDSS
}
