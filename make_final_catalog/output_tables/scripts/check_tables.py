#++++++++++++++++++++++++++
#
# TITLE: check_tables
#
# PURPOSE: This program compares two tables
#          (typically ours with Simard) to 
#          ensure that the tables are matched 
#          row by row
#
# INPUTS: 
#
# OUTPUTS: 
#
# PROGRAM CALLS:
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# WITH: Mariangela Bernardi
#       Department of Physics and Astronomy
#       University of Pennsylvania
#
# DATE: 
#
#-----------------------------------

import numpy as np
import pylab as pl
import scipy as sc

import os
import sys
import pylab as pl

a = open('table_1.txt')

us_data = {}

for line in a.readlines():
    line = line.split()
    if len(line)> 3:
        galcount = int(line[0])
        ra = float(line[1])
        dec = float(line[2])
        z = float(line[3])
        us_data[galcount] = [ra,dec,z]
        
a.close()

a = open('table_4.txt')
sim_data = {}

for line in a.readlines():
    line = line.split()
    if len(line)> 3:
        galcount = int(line[0])
        ra = float(line[1])
        dec = float(line[2])
        z = float(line[3])
        sim_data[galcount] = [ra,dec,z]
        
a.close()
  
us_keys = us_data.keys()
sim_keys = sim_data.keys()

good_keys = filter(lambda x: x in us_keys, sim_keys)

ra_us = []
dec_us = []
z_us = []

ra_sim = []
dec_sim = []
z_sim = []

for key in good_keys:
    ra_us.append(us_data[key][0])
    ra_sim.append(sim_data[key][0]) 
    dec_us.append(us_data[key][1])
    dec_sim.append(sim_data[key][1]) 
    z_us.append(us_data[key][2])
    z_sim.append(sim_data[key][2]) 
    
pl.scatter(ra_us, ra_sim)
pl.savefig('ra.eps')
pl.clf()

pl.scatter(dec_us, dec_sim)
pl.savefig('dec.eps')
pl.clf()

pl.scatter(z_us, z_sim)
pl.savefig('z.eps')
pl.clf()
