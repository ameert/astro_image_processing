import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
import matplotlib.cm as cm

#### Example of plotting using imshow               ####
#### For Charles Davis, Joseph Clampitt, Alan Meert ####
#### Jan 5 2015                                     ####

def make_neighbors(mu, nnum):
    """creates x, y coordinates for neighbor galaxies"""
    # radial distance
    r = poisson.rvs(mu, size=nnum)

    # angular position
    ang = np.random.uniform(low=0.0, high=2.0*np.pi, size=nnum)

    #convert to x, y
    x = r*np.cos(ang)
    y = r*np.sin(ang)
    
    return x,y

if __name__=="__main__":
    mu = 8.0 # Mpc; mean distance of the neighbors from the center
    nnum = 45 # number of neighbors
    binsize = 0.5 #Mpc 
    interpchoice = 'none' # interpolation for the neighbor image. try also 'gaussian' etc.

    #calculate bins
    nrange_x = np.arange(-15.0, 15.001, binsize) 
    nrange_y = nrange_x

    # make up a pair of galaxies.
    p1 = np.array((-3.5, -2.0))
    p2 = -1.0 * p1

    #get the neighbors
    nx, ny = make_neighbors(mu, nnum)

    #bin the neighbors
    neighbor_im, xedges, yedges = np.histogram2d(nx, ny, 
                                                 bins= (nrange_x, nrange_y)
                                                 )

    plt.scatter(0,0, s = 100, c='r', edgecolor='none')
    plt.scatter(p1[0], p1[1], s = 100, c='g', edgecolor='none')
    plt.scatter(p2[0], p2[1], s = 100, c='b', edgecolor='none')

    plt.imshow(neighbor_im, cmap = cm.YlGn, interpolation=interpchoice, 
               origin = 'lower', 
               extent = (xedges[0],xedges[-1],yedges[0],yedges[-1])
               )

    plt.xlabel('X Distance from center [Mpc]')
    plt.ylabel('Y Distance from center [Mpc]')
    plt.colorbar()
    plt.show()
