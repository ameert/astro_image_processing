import numpy as np
import scipy as sc
import pylab as pl
import scipy.interpolate as interp
import scipy.signal as sig
import scipy.integrate as integrate

def alan_boxsmooth(arr, smoothsize = 3):
    """Perform a boxcar smoothing on the given array,
    use odd number for window size"""
    out_arr = sig.convolve(arr, sig.boxcar(smoothsize)/smoothsize, mode='same')
    return out_arr

#def alan_convolve(ar1, ar2, pad = 0.0):
    
def calc_petroRad2(rad, flux_rad, flux_inc, eta=0.2, outfile = ''):
    """Calculates the petrorad for a given eta parameter using the standard 
petrosian quantity. Requires a set of radii, flux at that radius, and flux 
inside the radius. This is slightly different than the SDSS definition."""

    new_flux_inc = rad*flux_rad*2.0*np.pi
    new_flux_inc = np.concatenate((np.array([0,]),integrate.cumtrapz(new_flux_inc, rad))) + flux_inc[0]

#    for a in zip(new_flux_inc, flux_inc):
#        print a

#    print type(new_flux_inc)
#    print len(new_flux_inc)
#    print len(rad)
#    print len(flux_rad)
    eta_rad = new_flux_inc/(np.pi*rad*rad*flux_rad)
    #sort_eta_rad = np.argsort(eta_rad)
    #eta_rad = alan_boxsmooth(eta_rad, smoothsize = 5)
    #eta_interp = interp.InterpolatedUnivariateSpline(eta_rad[sort_eta_rad], rad[sort_eta_rad])

#    print eta_rad
    
    interp_limit = np.min(np.where(eta_rad>5.0))+2
    
    eta_interp = interp.InterpolatedUnivariateSpline(eta_rad[:interp_limit], rad[:interp_limit])
    rad_interp = interp.InterpolatedUnivariateSpline(rad[:interp_limit], eta_rad[:interp_limit])
    eta_smooth = interp.UnivariateSpline(eta_rad[:interp_limit], rad[:interp_limit])
    rad_smooth = interp.UnivariateSpline(rad[:interp_limit], eta_rad[:interp_limit])


    if outfile != '':
        pl.subplot(221)
        pl.plot(rad, eta_rad)
        pl.ylim(0,20)
        xlocs = np.arange(pl.xlim()[0],pl.xlim()[1], 0.01)
        pl.plot(xlocs, rad_interp(xlocs))
        pl.plot(xlocs, rad_smooth(xlocs))
        
        pl.subplot(222)
        pl.plot(eta_rad, rad)
        xlocs = np.arange(pl.xlim()[0],pl.xlim()[1], 0.01)
        pl.plot(xlocs, eta_interp(xlocs))
        pl.plot(xlocs, eta_smooth(xlocs))
        pl.ylim(np.min(xlocs), np.max(xlocs))
        pl.subplot(223)
        pl.plot(rad, flux_rad)
        pl.subplot(224)
        pl.plot(rad, flux_inc)
        pl.plot(rad, new_flux_inc)
        
        pl.savefig(outfile)
        pl.clf()
    return eta_smooth(1.0/eta)



def calc_petroRad(rad, flux_rad, flux_inc, eta=0.2, outfile = ''):
    """Calculates the petrorad for a given eta parameter using the standard 
petrosian quantity. Requires a set of radii, flux at that radius, and flux 
inside the radius. This is slightly different than the SDSS definition."""

    
    eta_rad = flux_inc/(np.pi*rad*rad*flux_rad)
    #sort_eta_rad = np.argsort(eta_rad)
    eta_rad = alan_boxsmooth(eta_rad, smoothsize = 5)
    #eta_interp = interp.InterpolatedUnivariateSpline(eta_rad[sort_eta_rad], rad[sort_eta_rad])

    
    interp_limit = np.min(np.where(eta_rad>5.0))+2
    
    eta_interp = interp.InterpolatedUnivariateSpline(eta_rad[:interp_limit], rad[:interp_limit])
    rad_interp = interp.InterpolatedUnivariateSpline(rad[:interp_limit], eta_rad[:interp_limit])
    eta_smooth = interp.UnivariateSpline(eta_rad[:interp_limit], rad[:interp_limit])
    rad_smooth = interp.UnivariateSpline(rad[:interp_limit], eta_rad[:interp_limit])


    if outfile != '':
        pl.subplot(221)
        pl.plot(rad, eta_rad)
        pl.ylim(0,20)
        xlocs = np.arange(pl.xlim()[0],pl.xlim()[1], 0.01)
        pl.plot(xlocs, rad_interp(xlocs))
        pl.plot(xlocs, rad_smooth(xlocs))
        
        pl.subplot(222)
        pl.plot(eta_rad, rad)
        xlocs = np.arange(pl.xlim()[0],pl.xlim()[1], 0.01)
        pl.plot(xlocs, eta_interp(xlocs))
        pl.plot(xlocs, eta_smooth(xlocs))
        pl.ylim(np.min(xlocs), np.max(xlocs))
        pl.subplot(223)
        pl.plot(rad, flux_rad)
        pl.subplot(224)
        pl.plot(rad, flux_inc)
        
        pl.savefig(outfile)
        pl.clf()
    return eta_smooth(1.0/eta)

def get_petroflux(petrorad, rad, flux_inc, rad_mult = 2.0):
    """Calculates the petrosian flux using the number of petrosian radii
specified by the rad_mult parameter. It is usually 2 for petrorads"""
    if petrorad*rad_mult>rad[-2]:
        outflux = np.max(flux_inc)
    else:
        flux_interp = interp.InterpolatedUnivariateSpline(rad, flux_inc)
        outflux = flux_interp(rad_mult*petrorad)
    return outflux
    
def get_petrohalfrad(petroflux, rad, flux_inc):
    """Calculates the petro halflight radii"""

    # we need to ensure that there are not any repeats in values...
    # so lets truncate after 90% of petrosian flux
    #rad = np.extract(flux_inc < 0.9*petroflux, rad)
    #flux_inc = np.extract(flux_inc < 0.9*petroflux, flux_inc)

    rad_interp =interp.InterpolatedUnivariateSpline(flux_inc, rad) 
 
    return rad_interp(0.5*petroflux)

if __name__ =='__main__':
    from scipy.special import gammainc, gamma

    def mag_to_counts( mag, aa, kk = 0 , airmass = 0):
        exptime = 53.907456 #in seconds, taken from SDSS website www.sdss.org/dr3/algorithms/fluxcal.html
        return exptime * (10**(-.4*mag)) / (10**(0.4*(aa + kk*airmass)))


    def meas_profs(fileend, Ltot):
        n_arr = []
        petro_arr = []
        petro_rad = []
        petro_halfrad = []
        pixsz = 0.396 #arcsec per pix

        for count, n in enumerate(np.arange(0.5, 10.01, 0.5)):
            radii, flux, flux_err, flux_inc = np.loadtxt('%08d%s' %(count, fileend), unpack = True)

            flux = np.extract(radii>0, flux)
            flux_err = np.extract(radii>0, flux_err)
            flux_inc = np.extract(radii>0, flux_inc)
            radii = np.extract(radii>0, radii)
            print radii, flux, flux_err, flux_inc
            #pl.plot(radii, flux)
            #pl.show(block=True)

            #raw_input()
            radii = radii*pixsz
            flux = flux/(pixsz**2)
            petroRad = calc_petroRad(radii.copy(), flux.copy(), flux_inc.copy(), eta=0.2)
            petroflux = get_petroflux(petroRad.copy(), radii.copy(), flux_inc.copy(), rad_mult = 2.0)
            
            n_arr.append(n)
            petro_arr.append(petroflux/Ltot)
            petro_rad.append(petroRad)
            petro_halfrad.append(get_petrohalfrad(petroflux, radii, flux_inc))
        return n_arr, petro_arr ,petro_rad ,petro_halfrad         

    def create_ana_data(Itot):
        radii = np.arange(0.05, 15.0, 0.1)

        Re = 2.0
    
        n_arr = np.arange(0.5, 10.01, 0.5)
        petro_arr = []
        petro_rad = []
        petro_halfrad = []
        for n_ser in n_arr:
            
            bn = 1.9992*n_ser - 0.3271
            x = bn*(radii/Re)**(1.0/n_ser)

            Ie = Itot * (bn**(2.0*n_ser))/ ((Re**2.0)*2.0*np.pi*n_ser*np.exp(bn)*gamma(2.0*n_ser))

            flux_included =  Itot * gammainc(2.0*n_ser, x)

            radial_flux = Ie*np.exp(-bn*((radii/Re)**(1.0/n_ser) -1))

            petroRad = calc_petroRad(radii, radial_flux, flux_included, eta=0.2)

            x = bn*(2.0*petroRad/Re)**(1.0/n_ser)

            petro_arr.append(gammainc(2.0*n_ser, x))
            petro_rad.append(petroRad)

            petroflux = get_petroflux(petroRad, radii, flux_included, rad_mult = 2.0)
            petro_halfrad.append(get_petrohalfrad(petroflux, radii, flux_included))
        return n_arr, petro_arr ,petro_rad ,petro_halfrad 

    mtot = 17.0
    zeropoint= 24.0
    Itot = mag_to_counts(mtot, -1.0*zeropoint)

    n_arr, petro_arr, petro_rad, petro_halfrad = create_ana_data(Itot)

    n_im, petro_im, prad_im, phrad_im = meas_profs('_nosample_profile.txt', Itot)
    n_im2, petro_im2, prad_im2, phrad_im2 = meas_profs('_psfsample_profile.txt', Itot)
    n_im3, petro_im3, prad_im3, phrad_im3 = meas_profs('_noise_profile.txt', Itot)

    print n_im, petro_im, prad_im, phrad_im

    suff = 'image'

    pl.plot(n_arr, petro_arr, 'b-', label='analytic')
    pl.plot(n_im, petro_im, 'r--', label='clean')
    pl.plot(n_im2, petro_im2, 'm--', label='psf')
    pl.plot(n_im3, petro_im3, 'g--', label = 'noise+psf')
    pl.legend(loc=3)
    pl.title('Enclosed petrosian flux vs. n')
    pl.xlabel('n$_{ser}$')
    pl.ylabel('L$_{petro}$/L$_{ser}$')
    pl.ylim(0.0, 1.1)
    pl.savefig('petro_totflux_%s.png' %suff)
    pl.clf()

    pl.plot(n_arr, petro_rad, 'b-', label='analytic')
    pl.plot(n_im, prad_im, 'r--', label='clean')
    pl.plot(n_im2, prad_im2, 'm--', label='psf')
    pl.plot(n_im3, prad_im3, 'g--', label = 'noise+psf')
    pl.legend()
    pl.title('petrosian Radius vs. n')
    pl.xlabel('n$_{ser}$')
    pl.ylabel('R$_{petro}$')
    pl.ylim(0.0, 6.0)
    pl.savefig('petro_rad_%s.png' %suff)
    pl.clf()

    pl.plot(n_arr, petro_halfrad, 'b-', label='analytic')
    pl.plot(n_im, phrad_im, 'r--', label='clean')
    pl.plot(n_im2, phrad_im2, 'm--', label='psf')
    pl.plot(n_im3, phrad_im3, 'g--', label = 'noise+psf')
    pl.legend()
    pl.title('petrosian R_hl vs. n')
    pl.xlabel('n$_{ser}$')
    pl.ylabel('R$_{1/2,\ petro}$')
    pl.ylim(0,3.0)
    pl.savefig('petro_halfrad_%s.png' %suff)
    pl.clf()
