from mysql_class import *
import numpy as np
import pylab as pl
from MatplotRc import *
import ndimage
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import time

dba = 'simard'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)


cmd = 'select b.galcount, b.z, a.V_max from simard_sample as a, catalog.CAST as b where b.galcount = a.galcount and a.V_max > 0;'

galcount, z, V_max = cursor.get_data(cmd)

galcount = np.array(galcount)
z = np.array(z)
V_max = np.array(V_max)

weights = np.ones_like(galcount)/float(len(galcount))

pl.hist(z, bins= 80, weights = weights, range = (0,0.40), cumulative = True )
pl.plot((0,.4), (.05,.05))
pl.plot((0,.4), (.95,.95))

pl.show()
