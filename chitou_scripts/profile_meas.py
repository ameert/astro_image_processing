import numpy as np
from scipy.special import gammainc
from scipy.optimize import newton
import matplotlib.pyplot as plt
from astro_image_processing.mysql import *
from scipy.interpolate import splev, splrep

cursor = mysql_connect('catalog', 'pymorph', 'pymorph', autocommit=False)

def bn(n):
    return 1.9992*n-0.3271

nsers = np.arange(0.5, 8.01, 0.1)
vals = {'0.2':[],'0.5':[],'0.8':[],'0.9':[], 'nsers':nsers}
            

for light in ['0.2', '0.5','0.8', '0.9']:
    print light
    for nser in nsers:
        answer = newton(lambda x: gammainc(2.0*nser, x)-float(light), bn(nser))

        vals[light].append((answer/bn(nser))**nser)


    plt.plot(nsers,vals[light], label = light)

plt.legend()

plt.show()



galcount, hrad, nser =  cursor.get_data('Select galcount, r_bulge, n_bulge from r_band_ser where r_bulge>0 order by galcount ;')

galcount = np.array(galcount, dtype=int)
hrad = np.array(hrad)
nser = np.array(nser)

outrads = {}

for light in ['0.2', '0.5','0.8', '0.9']:
    tck = splrep(vals['nsers'], vals[light])
    outrads[light] = splev(nser, tck)*hrad

outfile = open('concen_rads.txt', 'w')

for a in zip(galcount, outrads['0.2'], outrads['0.5'], outrads['0.8'], outrads['0.9']):
    outfile.write('%d %f %f %f %f\n' %a)

outfile.close()
