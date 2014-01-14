#++++++++++++++++++++++++++
#
# TITLE: generate_params
#
# PURPOSE: this program will generate
#          the parameters for a galaxy
#          from the current distribtuion
#
# INPUTS:  uses the imported distribution
#
# OUTPUTS: the randomly selected values used
#          for generating the image
#
# PROGRAM CALLS: NONE really
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 20 FEB 2011
#
#-----------------------------------
import random as r
from scipy import interpolate
import sys
import numpy as n
import os 
from read_dists import read_dists

def generate_params(dist_path, dist_stem):
    """ usage:
    mag, bt, rd_kpc, inc, dang, re_kpc, ell, bang, ser_bulge, z, zp, kk, airmass = generate_params()

 
    INPUTS:  uses the imported distribution

    OUTPUTS: the randomly selected values used
    for generating the image
    mag, bt, rd_kpc, inc, dang, re_kpc, ell, bang, ser_bulge, z, zp, kk, airmass"""

    mag_dist, bt_dist, re_dist, rd_dist, eb_dist, n_bulge_dist,  z_dist, zp_dist, kk_dist, airmass_dist = read_dists(dist_path, dist_stem)


    selections = [] 
    for dist in [mag_dist, bt_dist, re_dist, rd_dist, eb_dist, n_bulge_dist, z_dist, zp_dist, kk_dist, airmass_dist]:

        number = r.random() #returns a number in [0,1)
        #tck = interpolate.splrep(dist[1], dist[0], s=0)
        #selections.append(interpolate.splev(number,tck,der=0))
        selections.append(n.interp(number,dist[1], dist[0]))


    
    mag = selections[0]
    bt = selections[1]
    re_kpc = selections[2]
    rd_kpc = selections[3]
    ell = selections[4]
    ser_bulge = selections[5]
    z = selections[6]
    zp = selections[7]
    kk = selections[8]
    airmass = selections[9]
    inc = r.uniform(0.0,n.pi/2.0)
    dang = r.uniform(0.0,n.pi)
    bang = r.uniform(0.0,n.pi)
    

    return mag, bt, rd_kpc, inc, dang, re_kpc, ell, bang, ser_bulge,z,zp,kk,airmass



