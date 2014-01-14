#!/usr/bin/python

#This program just plots the Kelvin-ev relationship
#so that I can remember it easier


import numpy as np
import pylab

ev_to_k = 1.1604505*(10.0**4)

ev =np.array( [0.001,0.01,0.1,0.5, 1.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0, 2000.0, 5000.0, 10000.0])

k = ev * ev_to_k

pylab.loglog(ev, k)
pylab.grid(b=1)
pylab.title("eV vs. K")
pylab.xlabel('eV')
pylab.ylabel('Kelvins')
pylab.show()

