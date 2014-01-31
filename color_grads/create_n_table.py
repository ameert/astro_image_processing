from scipy.special import gammainc
from scipy.optimize import brentq
import numpy as np

nvals = np.arange(0.5, 8.01,0.1)

def to_min(x):
    return gammainc(2.0*n_curr, (1.9992*n_curr-0.3271)*x**(1.0/n_curr))-0.9


for n_curr in nvals:
    print n_curr, to_min(3.0)
    print brentq(to_min, 1.0, 50.0)
