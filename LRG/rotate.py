import numpy as np
import numpy.linalg as LA

def to_sphere(point):
    """accepts a x,y,z, coordinate and returns the same point in spherical coords (r, theta, phi) i.e. (r, azimuthal angle, altitude angle) with phi=0 in the zhat direction and theta=0 in the xhat direction"""
    coord = (np.sqrt(np.sum(point**2)),
             np.arctan2(point[1],point[0]),
             np.pi/2.0 - np.arctan2(np.sqrt(point[0]**2 + point[1]**2),point[2])
             )
    
    return np.array(coord)
def to_cartesian(point):
    """accepts point in spherical coords (r, theta, phi) i.e. (r, azimuthal angle, altitude angle) with phi=0 in the zhat direction and theta=0 in the xhat direction and returns a x,y,z, coordinate"""
    coord = point[0]*np.array([np.cos(point[2])*np.cos(point[1]),
                                 np.cos(point[2])*np.sin(point[1]),
                                 np.sin(point[2])])
    
    
    return coord
            

def rotate(p1, p2, p3):
    """rotates coordinate axis so that p1 is at the pole of a new spherical coordinate system and p2 lies on phi (or azimuthal angle) = 0

inputs:
p1: vector in spherical coords (phi, theta, r) where phi is azimuthal angle (0 to 2 pi), theta is zenith angle or altitude (0 to pi), r is radius
p2: vector of same format 
p3: vector of same format

Output:
s1:vector in (r, theta, phi) with p1 on the z axis
s2:vector in (r,, theta, phi) with p2 on the phi-hat axis
s3:transformed vector of p3
"""

    p1_cc=to_cartesian(p1) 
    p2_cc=to_cartesian(p2) 
    p3_cc=to_cartesian(p3) 

    p1norm = p1_cc/LA.norm(p1_cc)
    p2norm = p2_cc/LA.norm(p2_cc)
    p3norm = p3_cc/LA.norm(p3_cc)
    
    zhat_new =  p1norm
    x_new = p2norm - np.dot(p2norm, p1norm) * p1norm
    xhat_new = x_new/LA.norm(x_new)
    
    yhat_new = np.cross(zhat_new, xhat_new)
    
    s1 = np.array(map(lambda x: np.dot(x, p1_cc), (xhat_new, yhat_new, zhat_new)))
    s2 = np.array(map(lambda x: np.dot(x, p2_cc), (xhat_new, yhat_new, zhat_new)))
    s3 = np.array(map(lambda x: np.dot(x, p3_cc), (xhat_new, yhat_new, zhat_new)))

    s1=to_sphere(s1) 
    s2=to_sphere(s2) 
    s3=to_sphere(s3)
    
    return s1, s2, s3


if __name__ == "__main__":

    sc = np.array([[1.0, 2.49946857, .59890624],
                   [1.0, 2.49601282, .59521662],
                   [1.0, 2.48552894, .59001915]])


    print "original"
    print sc[0]
    print sc[1]
    print sc[2]

    out = rotate(sc[0], sc[1], sc[2])
    print "rotated"
    print out[0]
    print out[1]
    print out[2]


    #plot the points
    import matplotlib.pyplot as plt
    ax = plt.subplot(111, polar=True)
    # theta is theta, but in degrees
    theta = np.array([out[0][1],out[1][1],out[2][1]])/np.pi * 180.0
    # r is the angle (from the pole of dec, in arcsec)
    r = np.pi/2.0-np.array([out[0][2],out[1][2],out[2][2]])
    print r
    r = r/np.pi * 180.0*3600.0
    print r

    print theta, r

    ax.scatter(theta, r, c=[-1,0.5,1], s=200)
    #ax.set_rmax(2.0)
    ax.grid(True)

    #ax.set_title("A line plot on a polar axis", va='bottom')
    plt.show()
