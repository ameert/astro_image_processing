import numpy as np
import sys
import os

infile = sys.argv[1]

try:
    models = [a for a in sys.argv[2:]]
except:
    models = ['ser']


gals = np.loadtxt(infile, usecols=[0], skiprows = 1)
gals = gals.astype(int)

for a in gals:
    cmd = 'python /home/ameert/public_html/cgi-bin/plot_shalaowai.py %d %s' %(a,' '.join(models))
    print cmd
    os.system(cmd)
             
                                                                 
