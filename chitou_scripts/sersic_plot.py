import numpy as np
from scipy.special import gamma, gammainc
import pylab as pl

class sersic():
    def __init__(self, mtot, re, n):
        self.n = n
        self.re = re
        self.b = self.bn()

        self.Itot = 10.**(-0.4*mtot)
        self.Ie = self.Itot*self.b**(2.0*self.n)/(re**2.0*2*np.pi*self.n*np.exp(self.b)*gamma(2.0*self.n))
        
        return


    def bn(self):
        """sersic bn parameter"""
        return 1.9992*self.n-0.3271

    def profile(self, rads, mag=False):
        prof = self.Ie*np.exp(-self.b*((rads/self.re)**(1.0/self.n) - 1.0))
        if mag:
            prof = -2.5*np.log10(prof)
        return prof


    def m_inc(self, rads):
        x = self.b*(rads/self.re)**(1.0/self.n)
        Ir = gammainc(2.0*self.n, x)*self.Itot
        return -2.5*np.log10(Ir)

    

if __name__ == "__main__":
    ng=6.0
    nr=4.5
    
    mr=16.0
    mg=17.3

    rr=3.0
    rg=5.7

    gprof = sersic(mg, rg, ng)
    rprof = sersic(mr, rr, nr)
    
    rads = np.arange(0.2, 50.0, 0.01)
    
    g1=gprof.m_inc(rr)
    r1=rprof.m_inc(rr)

    print g1-r1
    pl.subplot(2,2,1)
    pl.plot(rads,gprof.profile(rads, mag=True), "g-")    
    pl.plot(rads,rprof.profile(rads, mag=True), "r-")    
    pl.ylim(30, 18)

    pl.subplot(2,2,2)
    pl.plot(rads,gprof.profile(rads, mag=True)-rprof.profile(rads, mag=True))
    #pl.ylim(30, 18)

    pl.subplot(2,2,3)
    pl.plot(rads,((g1-r1)-(gprof.profile(rads, mag=True)-rprof.profile(rads, mag=True)))/np.log10(rr/rads))
    pl.ylim(-1.0, 1.0)

    pl.show()
