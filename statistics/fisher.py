import numpy as np

def error_ellipse(cov_mat):
    """given the covariance matrix, this returns the error ellipse"""
    print (cov_mat[0,0]**2 +cov_mat[1,1]**2)/2.0
    print np.sqrt((cov_mat[0,0]**2 -cov_mat[1,1]**2)**2.0/4.0 +cov_mat[1,0]**2)

    a = np.sqrt((cov_mat[0,0]**2 +cov_mat[1,1]**2)/2.0 + np.sqrt(((cov_mat[0,0]**2 -cov_mat[1,1]**2)**2.0)/4.0 +cov_mat[1,0]**2))
    b = np.sqrt((cov_mat[0,0]**2 +cov_mat[1,1]**2)/2.0 - np.sqrt(((cov_mat[0,0]**2 -cov_mat[1,1]**2)**2.0)/4.0 +cov_mat[1,0]**2))

    theta = np.degrees(np.arctan(2.0*cov_mat[1,0]/(cov_mat[0,0]**2 -cov_mat[1,1]**2)/2.0))

    return a, b, theta
