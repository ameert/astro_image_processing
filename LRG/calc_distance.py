import numpy as np

def calc_distance(ra1, dec1, ra2, dec2):
    '''Calculate the circular angular distance of two points on a sphere.'''
    lambda_diff = ra1  - ra2
    cos1 = np.cos(dec1)
    cos2 = np.cos(dec2)
    sin1 = np.sin(dec1)
    sin2 = np.sin(dec2)
    
    num = (cos2 * np.sin(lambda_diff)) ** 2.0 + (cos1 * sin2 - sin1 * cos2 * np.cos(lambda_diff)) ** 2.0
    denom = sin1 * sin2 + cos1 * cos2 * np.cos(lambda_diff)
    
    return np.arctan2(np.sqrt(num), denom)

