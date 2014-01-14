import random
import pylab as pl
import numpy as np
import pyfits as pf
from images2gif import *
import scipy.signal as signal

class world_class():
    def __init__(self, N,M):
        self.data = np.zeros((N,M))
        self.dimensions = (N,M)
        self.perc_state = np.zeros((N,M))
        self.whois_neighbor() 
        return

    def whois_neighbor(self, connectivity = 8):
        if connectivity == 8:
            fil = np.array([1,1,1])
        elif connectivity == 4:
            fil = np.array([0,1,0])
        else:
            fil = np.array([0,0,0])
        self.neighbor_filter =fil
        return
    
    def percolate_row(self, row):
        if row < self.dimensions[1]:
            if row == 0:
            #initialize the row
                rowvals = self.data[:,row]
            else:
                rowvals = signal.convolve(self.perc_state[:,row-1], self.neighbor_filter, mode='same')
            rowvals = np.where(rowvals >0.5, 1,0)
        self.perc_state[:,row] = rowvals *self.data[:,row]
    
PERSON, EMPTY = 1.0, 0.0

def get_threshold():
    perc = raw_input("Please enter a thresold between 0-1.   ")
    perc = float(perc)
    return perc


def make_random_world(M, N):
    """Constructs a new random game world of size MxN."""
    perc = get_threshold()
    world = world_class(N,M)
    for j in range(N):
        for i in range(M):
            world.data[i, j] = percolation(perc)
    print world.data
    return world

def percolation(perc):
    randval = random.random()
    if randval > perc:
        return EMPTY
    else:
        return PERSON


def neighbors(world, x, y):
    M, N = world.dimensions
    nxmin = max(0, x-1)
    nxmax = min(M, x+1)
    nymin = max(0, y-1)
    nymax = min(N, y+1)
    r = []
    for nx in range(nxmin, nxmax+1):
        for ny in range(nymin, nymax+1):
            if nx != x or ny != y:
                r.append((nx, ny))
    return r


def print_world(world):
    """Prints out a string representation of a world."""
    #M, N = world['dimensions']
    #for j in range(N):
    #    for i in range(M):
    #        print world[i, j],
    #    print
    pl.imshow(world)

def make_world_option():
    m = int(raw_input("Please enter a m dimension.   "))
    n = int(raw_input("Please enter a n dimension.   "))

    raw_input("Press return to make a world")
    return make_random_world(m, n)

def show_neighbors_option(world):
    x = int(raw_input("Please enter an x coord.   "))
    y = int(raw_input("Please enter a y coord.   "))

    print neighbors(world, x, y)


def menu():
    print """
    Please pick your option:
    1) Percolation model for Small Pox
    2) Show world
    3) Instructions
    4) Show neighbors
    5) Exit
    """

    option = int(raw_input("Which option[1,2,3,4,5]? "))
    return option



if __name__ == '__main__':

    if 0:
        option = None
        while option != 5:
            if option == 1:
                world = make_world_option()
            elif option == 2:
                print_world(world)
            elif option == 4:
                show_neighbors_option(world)

            option = menu()

    images = []
    world = make_world_option()
    
    for row in range(world.data.shape[1]):
        world.percolate_row(row)
        im_tmp = world.data+world.perc_state
        im_tmp = np.where(im_tmp==0, 0.0, im_tmp)
        im_tmp = np.where(im_tmp==1, 0.5, im_tmp)
        im_tmp = np.where(im_tmp==2, 1.0, im_tmp)
 
        if 0:
            pl.figtext(0.5,0.9,'row %d' %row)
            pl.subplot(221)
            pl.imshow(world.data, interpolation = 'nearest')
            pl.colorbar()
            pl.subplot(222)
            pl.imshow(world.perc_state, interpolation = 'nearest')
            pl.colorbar()
            pl.subplot(223)
            pl.imshow(im_tmp, interpolation = 'nearest')
            pl.colorbar()
            
            pl.show()
        

        images.append(im_tmp)
        if np.sum(world.perc_state[:,row]) ==0:
            break

    writeGif('perc.gif',images, duration=0.1, dither=0)
         
