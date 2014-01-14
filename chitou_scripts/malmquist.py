import numpy as np
import pylab as pl
import cosmocal as ccal
import scipy as sc
import scipy.interpolate as interp
import sys

z1_absmag = np.loadtxt('z1_absmag.txt', unpack = True)
all_absmag = np.loadtxt('all_absmag.txt', unpack = True)
z1_lumfunc = np.loadtxt('z1_lumfunc.txt', unpack = True)
all_lumfunc = np.loadtxt('all_lumfunc.txt', unpack = True)
z1_z = np.loadtxt('z1_z.txt', unpack = True)
all_z = np.loadtxt('all_z.txt', unpack = True)
z1_appmag = np.loadtxt('z1_appmag.txt', unpack = True)
all_appmag = np.loadtxt('all_appmag.txt', unpack = True)

z1_absmag_rev =np.array(z1_absmag[0])
z1_absmag_prop_rev =np.array(z1_absmag[1])
z_cum =  np.cumsum(z1_absmag_prop_rev/np.sum(z1_absmag_prop_rev))[7:]
z1_absmag_rev=z1_absmag_rev[7:]

z1_appmag_rev =np.array(z1_appmag[0])
z1_appmag_prop_rev =np.array(z1_appmag[1])
z_cum2 =  np.cumsum(z1_appmag_prop_rev/np.sum(z1_appmag_prop_rev))[7:-1]
z1_appmag_rev=z1_appmag_rev[7:-1]

tck = interp.splrep(z_cum,z1_absmag_rev)
tck2 = interp.splrep(z_cum2,z1_appmag_rev)

#x2 = np.linspace(0.0, 1.0, 101)
#y2 = interp.splev(x2, tck)
#pl.plot(z_cum,z1_absmag_rev, 'o', x2, y2)
#pl.show()

def plot_bar(binctr, val):
    bin_width = np.mean(binctr[1:]-binctr[0:-1])
    leftbin = binctr - 0.5*bin_width
    pl.bar(leftbin, val, width = bin_width, edgecolor = 'b',linewidth = 1, color = 'none')
    

#plot_bar(z1_appmag[0],z1_appmag[1]) 
#plot_bar(all_appmag[0],all_appmag[1]) 
#plot_bar(z1_absmag[0],z1_absmag[1]) 
#plot_bar(all_absmag[0],all_absmag[1]) 
#plot_bar(z1_z[0],z1_z[1]) 
#plot_bar(all_z[0],all_z[1]) 
    
z_bins = z1_z[0]
z_vals = z1_z[1]/np.sum(z1_z[1])

dist_vals = [ccal.cal(a, 70, 0.27, 0.73, 1.0) for a in z_bins]
dist_vals = np.array(dist_vals)
#zage_Gyr, DCMR_Mpc, dismod, kpc_DA * pixelscale

#print dist_vals[:,1]

gals = []
gals2 = []
tot_gals = 10000

for curz, prop, dismod in zip(z_bins, z_vals, dist_vals[:,2]):
    to_select = prop*tot_gals
    for count in range(0,to_select):
        ptmp = np.random.uniform()
        mag = interp.splev(ptmp, tck)
        gals.append(mag+dismod)
for curz, prop, dismod in zip(z_bins, z_vals, dist_vals[:,2]):
    to_select = prop*tot_gals
    for count in range(0,to_select):
        ptmp = np.random.uniform()
        mag = interp.splev(ptmp, tck2)
        gals2.append(mag)

#print gals
#print gals2

plot_bar(all_appmag[0],all_appmag[1]) 
pl.hist(gals, bins = all_appmag[0], histtype = 'step', color = 'g', normed = True)
pl.hist(gals2, bins = all_appmag[0], histtype = 'step', color = 'r', normed = True)

pl.show()

dist_vals = [ccal.cal(a, 70, 0.27, 0.73, 1.0) for a in np.arange(0.01, 0.101,0.01)]
print np.array(dist_vals)[:,2]
