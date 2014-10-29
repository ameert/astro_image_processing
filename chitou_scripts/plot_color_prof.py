import numpy as np
import pylab as pl
import os
import sys
from scipy import interpolate
from scipy.special import gammainc, gamma
from mysql_class import *
from matplotlib.backends.backend_pdf import PdfPages

#start_mysql -e "select c.galcount, c.z, c.petroR50_r, c.PetroR90_r, d.kcorr_g,d.kcorr_r,g.MagHL_g,g.MagHL_r,g.grColor_hl, gr15_hl,gr3_hl, gr90_hl from CAST as c, DERT as d, COLOR_GRAD_ser as g, M2010 as m where c.galcount = g.galcount and c.galcount = d.galcount and c.galcount = m.galcount and m.ProbaEll+m.ProbaS0 >0.5 and g.gr3_hl<-0.55 order by RAND() limit 100;">gr3_steep_E.txt
#start_mysql -e "select c.galcount, c.z, c.petroR50_r, c.PetroR90_r, d.kcorr_g,d.kcorr_r,g.MagHL_g,g.MagHL_r,g.grColor_hl, gr15_hl,gr3_hl, gr90_hl from CAST as c, DERT as d, COLOR_GRAD_ser as g, M2010 as m where c.galcount = g.galcount and c.galcount = d.galcount and c.galcount = m.galcount and m.ProbaEll+m.ProbaS0 >0.5 and g.gr3_hl>-0.22 order by RAND() limit 100;">gr3_shallow_E.txt

cursor = mysql_connect('catalog','pymorph','pymorph','')

def bn(n):
    return 1.9992*n-0.3271

rad_lim = 4.5

files = ["gr3_steep_E.txt","gr3_shallow_E.txt"]
curr_file = files[int(sys.argv[1])]

galcount, z, petroR50, petroR90, kg, kr, MagHL_g,MagHL_r,grColor_hl, gr15_hl,gr3_hl, gr90_hl = np.loadtxt(curr_file, unpack = True, skiprows = 1)

galcount = galcount.astype(int)

for gal_tmp in galcount:
    folder = (gal_tmp)/250 +1

    filename = "%08d_ser_mag_colors.out" %(gal_tmp)

    if not os.path.isfile('./data/%s' %filename):
        os.system('scp ameert@folio.sas.upenn.edu:/data2/home/ameert/color_grads/data/%04d/%s ./data/' %(folder, filename))


pp = PdfPages(curr_file.split('.')[0]+'.pdf')
count = 0
for gal_tmp,z_tmp, petroR50_tmp, r90_tmp in zip(galcount,z, petroR50, petroR90):
    print count
    count+=1
    filename = "%08d_ser_mag_colors.out" %(gal_tmp)

    rad, g,g_err, r, r_err, i, i_err, gr_color, gr_err , gi_color, gi_err , ri_color, ri_err = np.loadtxt('./data/'+filename, unpack = True)

    ng, rg, nr,rr,ni,ri, gsky, rsky, isky, eg, er, ei, kg, kr, ki, bag, bar, bai, pg, pr, pi, magg, magrr, magi  = cursor.get_data("""select a.n_bulge, a.r_bulge*sqrt(a.ba_bulge),
b.n_bulge, b.r_bulge*sqrt(b.ba_bulge),
c.n_bulge, c.r_bulge*sqrt(c.ba_bulge), 
-2.5/log(10)*log(pow(10.0, -0.4*a.Galsky-2)/2 + sqrt(pow(9.0e-11,2.0)+0.25*pow(10,-0.8*a.Galsky-4))),
-2.5/log(10)*log(pow(10.0, -0.4*b.Galsky-2)/2 + sqrt(pow(1.2e-10,2.0)+0.25*pow(10,-0.8*b.Galsky-4))),
-2.5/log(10)*log(pow(10.0, -0.4*c.Galsky-2)/2 + sqrt(pow(1.8e-10,2.0)+0.25*pow(10,-0.8*c.Galsky-4))),
x.extinction_g, x.extinction_r, x.extinction_i, 
d.kcorr_g, d.kcorr_r, d.kcorr_i,
a.ba_bulge,b.ba_bulge,c.ba_bulge, 
a.pa_bulge,b.pa_bulge,c.pa_bulge 
a.m_bulge,b.m_bulge,c.m_bulge 
from 
CAST as x, r_band_ser as b, g_band_ser as a, i_band_ser as c, DERT as d 
where 
a.galcount = b.galcount and a.galcount = c.galcount and 
a.galcount = d.galcount and 
a.galcount = x.galcount and a.galcount = %d;""" %gal_tmp)

    g = g+eg[0]+kg[0]
    r = r+er[0]+kr[0]
    i = i+ei[0]+ki[0]

    rads = [1.0*petroR50_tmp,2.0*petroR50_tmp,3.0*petroR50_tmp,4.0*petroR50_tmp,r90_tmp] 
    vcol = ['k:']*4 + ['c:'] 

    vert_plot = zip(rads, vcol)

    fig = pl.figure(figsize=(12,10))
    pl.suptitle('%06d z=%0.2f r =%1.2f' %(gal_tmp,z_tmp, petroR50_tmp))
    pl.subplot(2,2,1)
    pl.errorbar(rad,g, ecolor='g', color='g',label='g-band')
    pl.errorbar(rad,r, ecolor='m',color='m',label='r-band')
    pl.errorbar(rad,i, ecolor='r',color='r',label='i-band')

    pl.title('Mag')
    pl.xlabel('Radius (arcsec)')
    pl.ylabel('Surface Brightness (magnitude)')
    pl.ylim(26,19)
    pl.plot(pl.xlim(), [gsky,gsky], 'g--')
    pl.plot(pl.xlim(), [rsky,rsky], 'm--')
    pl.plot(pl.xlim(), [isky,isky], 'r--')
    [pl.plot([a[0],a[0]], pl.ylim(), a[1] ) for a in vert_plot]


    pl.legend()
    pl.xlim(0,rad_lim*petroR50_tmp)

    pl.subplot(2,2,2)
    pl.errorbar(rad,gr_color, ecolor='g',color = 'g',label='g-r color')
    pl.errorbar(rad,gi_color, ecolor='m',color = 'm',label='g-i color')
    pl.errorbar(rad,ri_color, ecolor='r',color = 'r',label='r-i color')


    pl.title('Colors')
    pl.xlabel('Radius (arcsec)')
    pl.ylabel('Color')
    #pl.ylim(-1,1)
    pl.legend()
    pl.xlim(0,rad_lim*petroR50_tmp)
    [pl.plot([a[0],a[0]], pl.ylim(), a[1] ) for a in vert_plot]



    tck_gr = interpolate.splrep(np.log10(rad),gr_color,s=0)
    tck_gi = interpolate.splrep(np.log10(rad),gi_color,s=0)
    tck_ri = interpolate.splrep(np.log10(rad),ri_color,s=0)
    rad_vals= np.arange(rad[0], rad_lim*petroR50_tmp, 0.01)[1:]

    pl.subplot(2,2,3)
    
    pl.errorbar(rad_vals,(gr_color[0]- interpolate.splev(np.log10(rad_vals),tck_gr,der=0))/np.log10(rad[0]/rad_vals), ecolor='g',color = 'g',label='g-r color')
    pl.errorbar(rad_vals,(gi_color[0]- interpolate.splev(np.log10(rad_vals),tck_gi,der=0))/np.log10(rad[0]/rad_vals), ecolor='m',color = 'm',label='g-i color')
    pl.errorbar(rad_vals,(ri_color[0]- interpolate.splev(np.log10(rad_vals),tck_ri,der=0))/np.log10(rad[0]/rad_vals), ecolor='r',color = 'r',label='g-r color')

    tt = bn(ng[0])*((rad[0]/rg[0])**(1.0/ng[0]) - (rad_vals/rg[0])**(1.0/ng[0])) -bn(nr[0])*((rad[0]/rr[0])**(1.0/nr[0]) - (rad_vals/rr[0])**(1.0/nr[0]))
    grad = 2.5*np.log10(np.exp(1))*tt/np.log10(rad[0]/rad_vals)
    pl.plot(rad_vals, 2.5*np.log10(np.exp(1))*tt/np.log10(rad[0]/rad_vals), 'g--')

    tt = bn(ng[0])*((rad[0]/rg[0])**(1.0/ng[0]) - (rad_vals/rg[0])**(1.0/ng[0])) -bn(ni[0])*((rad[0]/ri[0])**(1.0/ni[0]) - (rad_vals/ri[0])**(1.0/ni[0]))
    pl.plot(rad_vals, 2.5*np.log10(np.exp(1))*tt/np.log10(rad[0]/rad_vals), 'm--')

    tt = bn(nr[0])*((rad[0]/rr[0])**(1.0/nr[0]) - (rad_vals/rr[0])**(1.0/nr[0])) -bn(ni[0])*((rad[0]/ri[0])**(1.0/ni[0]) - (rad_vals/ri[0])**(1.0/ni[0]))
    pl.plot(rad_vals, 2.5*np.log10(np.exp(1))*tt/np.log10(rad[0]/rad_vals), 'r--')


    print bag[0], bar[0], bai[0]
    print pg[0], pr[0], pi[0]


    pl.title('Color grad')
    pl.xlabel('Radius (arcsec)')
    pl.ylabel('grad')
    pl.ylim(-1,1)
    pl.legend()
    pl.xlim(0,rad_lim*petroR50_tmp)
    [pl.plot([a[0],a[0]], pl.ylim(), a[1] ) for a in vert_plot]

    pl.figtext(0.75, 0.35, "n_g=%2.1f" %ng[0])
    pl.figtext(0.75, 0.32, "r_g=%2.1f" %rg[0])
    pl.figtext(0.75, 0.29, "n_r=%2.1f" %nr[0])
    pl.figtext(0.75, 0.26, "r_r=%2.1f" %rr[0])
    pl.figtext(0.75, 0.23, "n_i=%2.1f" %ni[0])
    pl.figtext(0.75, 0.20, "r_i=%2.1f" %ri[0])
    #pp.savefig()
    #fig.close()
    pl.show()
pp.close()

