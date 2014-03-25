import os
import sys
import numpy as np

h7 = 1.01428571429 # 70 km/s/Mpc * h7 = 71 km/s/Mpc

parsec_to_meters = 3.08568025 * 10**16 # meters/parsec
L_sun = 3.839 * 10**26 # watts

#from get_zero_flux.py
#bandwidth = { 'u':22761660.6275 , 'g': 57315744.8071, 'r': 38235449.1222, 
#              'i':  21237685.6674, 'z':  2959254.28494} 
            # in hz from integrating the response function in each filter
   
absmag_sun = { 'u':6.80 , 'g': 5.45, 'r': 4.76, 
              'i':  4.58, 'z':  4.51} 
            # see Blanton et al. 2003, ApJ, 592, 819
            # http://mips.as.arizona.edu/~cnaw/sun.html
def absmag_to_LSun(AbsMag, magErr, band = 'r'):
    lgal = -0.4*(AbsMag - absmag_sun[band])
    lgal = 10.0**lgal # in solar luminosities
    return lgal, magErr





    #lum = 10**(-0.4*AbsMag)
    #surf_area = 4.0*np.pi * (10.0*parsec_to_meters)**2.0
    
    #lum = 3631.0 * 10**(-23) * lum * surf_area # watts/Hz
    #lum = lum * bandwidth[band] # in watts

    #lum = lum /L_sun

    #return lum
