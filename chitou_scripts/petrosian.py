import numpy as np
import scipy as sc
import pylab as pl
import scipy.interpolate as interp

def calc_petroRad(rad, flux_rad, flux_inc, eta=0.2):
    """Calculates the petrorad for a given eta parameter using the standard 
petrosian quantity. Requires a set of radii, flux at that radius, and flux 
inside the radius. This is slightly different than the SDSS definition."""
    eta_rad = flux_inc/(np.pi*rad*rad*flux_rad)
    eta_interp = interp.InterpolatedUnivariateSpline(eta_rad, rad)

    return eta_interp(1.0/eta)

def get_petroflux(petrorad, rad, flux_inc, rad_mult = 2.0):
    """Calculates the petrosian flux using the number of petrosian radii
specified by the rad_mult parameter. It is usually 2 for petrorads"""
    flux_interp = interp.InterpolatedUnivariateSpline(rad, flux_inc)
    
    return flux_interp(rad_mult*petrorad)
    
def get_petrohalfrad(petroflux, rad, flux_inc):
    """Calculates the petro halflight radii"""
    rad_interp =interp.InterpolatedUnivariateSpline(flux_inc, rad) 
 
    return rad_interp(petroflux/2.0)


if __name__ =='__main__':
    from scipy.special import gammainc, gamma

    radii = np.array([0.1, 0.2, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 7.0, 8.0, 10.0, 15.0])
    Ie = 100.0
    Re = 1.0
    
    n_arr = np.arange(0.5, 10.01, 0.25)
    petro_arr = []
    petro_rad = []
    petro_halfrad = []
    for n_ser in n_arr:
        bn = 1.9992*n_ser - 0.3271
        x = bn*(radii/Re)**(1.0/n_ser)

        flux_included =  Ie*(Re**2.0)*2.0*np.pi*n_ser*np.exp(bn)/(bn**(2.0*n_ser)) * gammainc(2.0*n_ser, x)*gamma(2.0*n_ser)

        radial_flux = Ie*np.exp(-bn*((radii/Re)**(1.0/n_ser) -1))

        petroRad = calc_petroRad(radii, radial_flux, flux_included, eta=0.2)

        x = bn*(2.0*petroRad/Re)**(1.0/n_ser)

        petro_arr.append(gammainc(2.0*n_ser, x))
        petro_rad.append(petroRad)
        
        petroflux = get_petroflux(petroRad, radii, flux_included, rad_mult = 2.0)
        petro_halfrad.append(get_petrohalfrad(petroflux, radii, flux_included))

    pl.plot(n_arr, petro_arr)
    pl.title('Enclosed petrosian flux vs. n')
    pl.xlabel('n$_{ser}$')
    pl.ylabel('L$_{petro}$/L$_{ser}$')
    pl.ylim(0.0, 1.0)
    pl.savefig('petro_totflux.png')
    pl.clf()

    pl.plot(n_arr, petro_rad)
    pl.title('petrosian Radius vs. n')
    pl.xlabel('n$_{ser}$')
    pl.ylabel('R$_{petro}$')
    pl.savefig('petro_rad.png')
    pl.clf()

    pl.plot(n_arr, petro_halfrad)
    pl.title('petrosian R_hl vs. n')
    pl.xlabel('n$_{ser}$')
    pl.ylabel('R$_{1/2,\ petro}$')
    pl.ylim(0,2.0)
    pl.savefig('petro_halfrad.png')
    pl.clf()
