def calc_distance(ra1, dec1, ra2, dec2):
    '''Calculate the circular angular distance of two points on a sphere.'''
    
    phi_s = dec1
    phi_f = dec2
    lambda_diff = ra1  - ra2
    
    cos = n.cos
    sin = n.sin
    
    num = (cos(phi_f) * sin(lambda_diff)) ** 2.0 + (cos(phi_s) * sin(phi_f) - sin(phi_s) * cos(phi_f) * cos(lambda_diff)) ** 2.0
    denom = sin(phi_s) * sin(phi_f) + cos(phi_s) * cos(phi_f) * cos(lambda_diff)
    
    return n.arctan2(n.sqrt(num), denom)

