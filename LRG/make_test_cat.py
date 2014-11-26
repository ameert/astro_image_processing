import numpy as np
import pyfits as pf
import random
import math
from scipy import integrate

numObjs=100
dzp = .065
dzs = .0125

dir = '/home/clampitt/filaments/spatial_cats/'

patches = np.arange(0, 33, 1)

ras = []
decs = []
zs = []

print('Aggregating pairs with appropriate R_pair...')
for patch in patches:
    print('Patch number %d' % (patch))
    lensfile = 'pair-cat-nov4_LRG_Rmax24.0_rlos6.0_p%d.fit' % (patch)
    hdu = pf.open(dir + lensfile)
    data = hdu[1].data
    indices=[]
    for i in range(len(data)):
        if (data[i]['R_pair'] <= 10.0 and data[i]['R_pair'] >= 6.0):
            indices.append(i)
    for i in indices:
        ras = np.hstack((ras, data[i].field('ra_mid')))
        decs = np.hstack((decs, data[i].field('dec_mid')))
        zs = np.hstack((zs, data[i].field('z')))
    hdu.close()
        
print('Aggregation complete.  %d objects aggregated.' % (len(ras)))
print('Selecting objects...')

out = np.zeros((numObjs, 7))

for i in range(numObjs):
    rand = random.randrange(0, len(ras))
    out[i, 0] = i
    out[i, 1] = ras[rand]
    out[i, 2] = decs[rand]
    out[i, 3] = zs[rand]

print('Calculating thetas...')

Dh = 3000 #h^-1 MPC
for i in range(numObjs):
    Dc = integrate.quad(lambda z: 1 / math.sqrt((.3 * (1 + z)**3) + .7), 0, out[i, 3])
    Da = Dh * Dc[0] / (1 + out[i, 3])
    theta = 15. / Da
    theta = theta * (180./math.pi) * (1./60.)
    out[i, 4] = theta
    out[i, 5] = dzp
    out[i, 6] = dzs

np.savetxt('test_file_%d_objs.txt' % (numObjs), out)


print('File written.')

'''
class myObj:
    def __init__(self, ra, dec, z, oid):
        self.ra = ra
        self.dec = dec
        self.z = z
        self.objID = oid

    def toArray(self):
        return np.array(self.oid, self.ra, self.dec, self.z)


objects = np.empty(numObjs, dtype=object)

for i in range(numObjs):
    rand = random.randrange(0, len(ras))
    objects[i] = myObj(ras[rand], decs[rand], zs[rand], i)

for i in objects:
'''
