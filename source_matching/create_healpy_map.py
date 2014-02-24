
# Python imports
import numpy as np
import healpy as hp
import itertools

# internal module imports
from source_match.util import *


def get_crossmatch(formatch, backmatch):
    """the crossmatches should have the nearest neighbor matches be equivalet in either direction, so we test this"""
    matches = []
    reverse = False
    if len(formatch.keys())<len(backmatch.keys()):
        prime_cat = formatch
        second_cat = backmatch
    else:
        prime_cat = backmatch
        second_cat = formatch
        reverse = True

    for key in prime_cat.keys():
        if second_cat.get(prime_cat[key][0], (-999,-999))[0] == key:
            matches.append([key, prime_cat[key][0],prime_cat[key][1]])
    
    if reverse:
        matches = [[a[1], a[0],a[2]] for a in matches] 
    
    return matches

class catalog():
    def __init__(self, galcount, ra,dec, NSIDE=256):
        self.galcount = np.array(galcount, dtype = int)
        self.dec = np.radians(np.array(dec, dtype=float))
        self.ra = np.radians(np.array(ra, dtype=float))
        self.set_NSIDE(NSIDE)

        return

    def set_NSIDE(self, NSIDE):
        self.NSIDE = NSIDE
        return


    def ra_dec_2_pix(self):
        """takes ra/dec in degrees, transforms to the correct coordinates and radians for healpy"""

        ra_rad = 2.0*np.pi - self.ra
        dec_rad = np.pi/2.0 - self.dec
        
        self.pix = hp.ang2pix(self.NSIDE, dec_rad, ra_rad)
        return self.pix
 
    def set_pixel_list(self):
        """creates a list of all pixels and their neighbors for quicker matching"""
        self.pix_and_neigh = set(set(list(self.pix)).union(set(list(hp.get_all_neighbours(self.NSIDE, self.pix).flatten()))))
        return self.pix_and_neigh

    def reorder_gals(self):
        pixnum_args = np.argsort(self.pix) 
    
        self.pix = self.pix[pixnum_args]
        self.galcount = self.galcount[pixnum_args]
        self.ra = self.ra[pixnum_args]
        self.dec = self.dec[pixnum_args]
        return 

    def get_pix_info(self):
        self.pix_info = {}
        for pixel in list(set(self.pix)):
            self.pix_info[pixel] = self.get_pixelgals(pixel)
        return 

    def get_pixelgals(self, pixel):
        return np.where(self.pix==pixel)[0]
     
    def map_sample(self):
        print "2 pix"
        self.ra_dec_2_pix()
        self.set_pixel_list()
        print "reorder gals"
        self.reorder_gals()
        print "pix_info"
        self.get_pix_info()
        
        return 
    
    def pix_pos(self, index):
        """returns the endpoints of the pixel info"""
        return self.pix_info.get(index, [-1,-1])
    
    def forward_match(self, catalog2, maxsep):
        """matches self to external catalog in the "LEFT JOIN" sense. ie looks for closest object in catalog2 to each galaxy in self. catalog2 should be of same class as self and already be mapped to pixels with the same number of nsides"""
        if self.NSIDE != catalog2.NSIDE:
            raise MatchError("NSIDES dont agree!!")
        matches = {}
        
        maxsep = np.radians(maxsep/3600.0) #convert arcsec to radians
        neighbor_pix = hp.get_all_neighbours(self.NSIDE, self.pix).T
        for count, a in enumerate(self.pix):    
            if a in catalog2.pix_and_neigh:
                pix_to_check = np.append(neighbor_pix[count][:],[a])
                gallist = [catalog2.pix_info.get(b,[]) for b in pix_to_check]

                chain = itertools.chain.from_iterable(gallist)                
                dec_array2 = np.array([catalog2.dec[tmp] for tmp in chain])
                chain = itertools.chain.from_iterable(gallist)                
                ra_array2 = np.array([catalog2.ra[tmp] for tmp in chain])
                chain = itertools.chain.from_iterable(gallist)                
                galcount2 = np.array([catalog2.galcount[tmp] for tmp in chain])


                dis = self.calc_distance(self.ra[count], self.dec[count], ra_array2,dec_array2)  #in radians
                try:
                    sorted_dis = np.argsort(dis)[0]
                    best_gal = galcount2[sorted_dis]
                    dis = dis[sorted_dis]
                    dis = np.degrees(dis)*3600.0 #back to arcsec
                except ValueError:
                    dis = np.inf
            else:
                dis = np.inf

            if dis >maxsep:
                best_gal = -999
                dis = -999
                
            matches[self.galcount[count]] = (best_gal, dis)

        return matches

    def calc_distance(self, ra1, dec1, ra2, dec2):
        '''Calculate the circular angular distance of two points on a sphere.'''
        lambda_diff = ra1  - ra2
        cos1 = np.cos(dec1)
        cos2 = np.cos(dec2)
        sin1 = np.sin(dec1)
        sin2 = np.sin(dec2)

        num = (cos2 * np.sin(lambda_diff)) ** 2.0 + (cos1 * sin2 - sin1 * cos2 * np.cos(lambda_diff)) ** 2.0
        denom = sin1 * sin2 + cos1 * cos2 * np.cos(lambda_diff)
    
        return np.arctan2(np.sqrt(num), denom)

