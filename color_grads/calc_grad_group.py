from mysql.mysql_class import *
import numpy as np
import pylab as pl
import sys
from matplotlib.backends.backend_pdf import PdfPages





class linefit():
    def __init__(self,x,y,yerr=None):
        self.x_mat = np.matrix([[1.0,val] for val in x])
        self.y_mat = np.matrix(y).T
        if yerr==None:
            self.c_mat = np.ones_like(y)/y.size
        else:
            self.c_mat = np.matrix(np.zeros((yerr.size, yerr.size)))
            for count, val in enumerate(yerr):
                self.c_mat[count, count] = val**2
                    
        self.b_err =(self.x_mat.T*(self.c_mat**(-1))*self.x_mat)**(-1) 
        self.b =  self.b_err*(self.x_mat.T*(self.c_mat**(-1))*self.y_mat)
        print self.b.T
        print self.b_err
        return

    def predict(self,xvals):
        a_calc = np.matrix([[1.0,val] for val in xvals])
        y_calc = self.b.T*a_calc.T
        return y_calc

bands = 'gr'
table_name = 'CAST'
dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'
lhost = ''
cursor = mysql_connect(dba, usr, pwd, '')

galtype = sys.argv[1]
magtype = sys.argv[2]
sky_cmd = {'pogson': 'select r.Galsky+5-c.extinction_g-d.kcorr_g, rs.Galsky+5-c.extinction_r-d.kcorr_r, c.extinction_r+d.kcorr_r-c.extinction_g-d.kcorr_g from r_band_ser as rs, g_band_ser as r, CAST as c, DERT as d where r.galcount = rs.galcount and rs.galcount = c.galcount and rs.galcount = d.galcount and rs.galcount = {gal};' ,
           'asinh': 'select -2.5/log(10)*log(pow(10.0, -0.4*r.Galsky-2)/2 + sqrt(pow(9.0e-11,2.0)+0.25*pow(10,-0.8*r.Galsky-4)))-c.extinction_g-d.kcorr_g, -2.5/log(10)*log(pow(10.0, -0.4*rs.Galsky-2)/2 + sqrt(pow(1.2e-10,2.0)+0.25*pow(10,-0.8*rs.Galsky-4)))-c.extinction_r-d.kcorr_r, c.extinction_r+d.kcorr_r-c.extinction_g-d.kcorr_g  from r_band_ser as rs, g_band_ser as r, CAST as c, DERT as d where rs.galcount = r.galcount and rs.galcount = c.galcount and rs.galcount = d.galcount and rs.galcount = {gal};'
           }

pp = PdfPages('grads_%s.pdf' %galtype)


path = '/home/ameert/Desktop/color_grad/data/9999' 
model = 'ser'

data = np.loadtxt('grads_%s.txt' %galtype, skiprows=1, unpack=True)

galcount = np.array(data[0], dtype = int)

for gc, dat in zip(galcount,np.array(data[1:]).transpose()):

    sky_g, sky_r, color_corr = cursor.get_data(sky_cmd[magtype].format(gal=gc))
    sky_g = sky_g[0]
    sky_r = sky_r[0]
    color_corr = color_corr[0]

    hrad_arcsec = dat[0]
    print gc, hrad_arcsec, sky_g, sky_r,sky_g-sky_r,color_corr
    outfile = '%s/%08d_mag_corr_%s.npz' %(path, gc, model)
    datafile = '%s/%08d_mag_corr_data.npz' %(path, gc)
    try:
    #if 1:
        profiles = np.load(outfile)
        data_profiles = np.load(datafile)
        hradlim = 3.0
        print gc, ' limit ', hrad_arcsec*hradlim, np.log10(hrad_arcsec*hradlim)
        print profiles.keys()
    
        rad_sky_cut_g = np.max(np.where(profiles['g']<sky_g))
        rad_sky_cut_r = np.max(np.where(profiles['r']<sky_r))

        print rad_sky_cut_g, rad_sky_cut_r
        
        print profiles['log_rad_arcsec'][rad_sky_cut_g],profiles['g'][rad_sky_cut_g]
        print profiles['log_rad_arcsec'][rad_sky_cut_r],profiles['r'][rad_sky_cut_r]
#        continue

        rads_to_use = np.where(profiles['log_rad_arcsec']< np.log10(hrad_arcsec*hradlim),1,0)+np.where(profiles['log_rad_arcsec']< np.log10(3.0*hradlim*hrad_arcsec),1,0)
        bad_rad = np.extract(rads_to_use== 1, profiles['log_rad_arcsec'])
        rads = np.extract(rads_to_use == 2, profiles['log_rad_arcsec'])
        
        gmag = np.extract(rads_to_use== 2, profiles['g'])
        gerr = np.extract(rads_to_use== 2, profiles['gerr'])
        bad_gmag = np.extract(rads_to_use== 1, profiles['g'])
        bad_gerr = np.extract(rads_to_use== 1, profiles['gerr'])

        rmag = np.extract(rads_to_use== 2, profiles['r'])
        rerr = np.extract(rads_to_use== 2, profiles['rerr'])
        bad_rmag = np.extract(rads_to_use== 1, profiles['r'])
        bad_rerr = np.extract(rads_to_use== 1, profiles['rerr'])

        data_rads_to_use = np.where(data_profiles['log_rad_arcsec']< np.log10(hrad_arcsec*hradlim),1,0)+np.where(data_profiles['log_rad_arcsec']< np.log10(3.0*hradlim*hrad_arcsec),1,0)
        data_bad_rad = np.extract(data_rads_to_use== 1, data_profiles['log_rad_arcsec'])
        data_rads = np.extract(data_rads_to_use == 2, data_profiles['log_rad_arcsec'])
        
        data_gmag = np.extract(data_rads_to_use== 2, data_profiles['g'])
        data_gerr = np.extract(data_rads_to_use== 2, data_profiles['gerr'])
        data_bad_gmag = np.extract(data_rads_to_use== 1, data_profiles['g'])
        data_bad_gerr = np.extract(data_rads_to_use== 1, data_profiles['gerr'])

        data_rmag = np.extract(data_rads_to_use== 2, data_profiles['r'])
        data_rerr = np.extract(data_rads_to_use== 2, data_profiles['rerr'])
        data_bad_rmag = np.extract(data_rads_to_use== 1, data_profiles['r'])
        data_bad_rerr = np.extract(data_rads_to_use== 1, data_profiles['rerr'])

        pl.subplot(2,2,1)
        pl.errorbar(rads,gmag, yerr=gerr, linestyle = '-', 
                    color = 'g', ecolor = 'g', marker = None,
                    label='g fitted %s'%model, markersize=4)
        pl.errorbar(bad_rad,bad_gmag, yerr=bad_gerr, linestyle = '-', 
                    color = 'c', ecolor = 'c', marker = None,
                    label='g excluded %s'%model, markersize=4)
        pl.errorbar(rads,rmag, yerr=rerr, linestyle = '-', 
                    color = 'r', ecolor = 'r', marker = None,
                    label='r fitted %s'%model, markersize=4)
        pl.errorbar(bad_rad,bad_rmag, yerr=bad_rerr, linestyle = '-', 
                    color = 'm', ecolor = 'm', marker = None,
                    label='r excluded %s'%model, markersize=4)

        print data_rads
        print data_gmag
        print  data_gerr
        pl.errorbar(data_rads,data_gmag, yerr=data_gerr, linestyle = '', 
                    color = 'g', ecolor = 'k', marker = 's',
                    label='g data', markersize=4)
        pl.errorbar(data_bad_rad,data_bad_gmag, yerr=data_bad_gerr, 
                    linestyle = '', 
                    color = 'c', ecolor = 'k', marker = 's',
                    label='g excluded data', markersize=4)
        pl.errorbar(data_rads,data_rmag, yerr=data_rerr, linestyle = '', 
                    color = 'r', ecolor = 'k', marker = 's',
                    label='r data', markersize=4)
        pl.errorbar(data_bad_rad,data_bad_rmag, yerr=data_bad_rerr, 
                    linestyle = '', 
                    color = 'm', ecolor = 'k', marker = 's',
                    label='r excluded data', markersize=4)
        pl.title('radial profiles')
        pl.xlim(np.min(profiles['log_rad_arcsec']-0.2), np.log10(3.0*hrad_arcsec*hradlim))
        pl.ylim(pl.ylim()[::-1])
        pl.legend(bbox_to_anchor=(-0.3, -0.3, 1., .102))
        pl.text(0.2, 0.4,'r$_r$:%2.2f"' %(dat[0]),horizontalalignment='center',
                verticalalignment='center',transform=pl.gca().transAxes)
        pl.text(0.2, 0.3,'r$_g$:%2.2f"' %(dat[2]),horizontalalignment='center',
                verticalalignment='center',transform=pl.gca().transAxes)
        pl.text(0.2, 0.2,'n$_r$:%2.2f' %(dat[1]),horizontalalignment='center',
                verticalalignment='center',transform=pl.gca().transAxes)
        pl.text(0.2, 0.1,'n$_g$:%2.2f' %(dat[3]),horizontalalignment='center',
                verticalalignment='center',transform=pl.gca().transAxes)

        color = np.extract(rads_to_use== 2, profiles[bands])
        cerr = np.extract(rads_to_use== 2, profiles[bands+'_err'])
        bad_color = np.extract(rads_to_use== 1, profiles[bands])
        bad_cerr = np.extract(rads_to_use== 1, profiles[bands+'_err'])

        data_color = np.extract(data_rads_to_use== 2, data_profiles[bands])
        data_cerr = np.extract(data_rads_to_use== 2, data_profiles[bands+'_err'])
        data_bad_color = np.extract(data_rads_to_use== 1, data_profiles[bands])
        data_bad_cerr = np.extract(data_rads_to_use== 1, data_profiles[bands+'_err'])
        for rad_pt in np.log10(np.arange(1.0,3.01,1.0)*hrad_arcsec):
            pl.plot((rad_pt,rad_pt),pl.ylim(), 'k:')

        pl.plot(pl.xlim(), [ sky_g]*2, 'g:')
        pl.plot(pl.xlim(), [sky_r]*2, 'r:')

        pl.subplot(2,2,2)
        pl.errorbar(rads, color, yerr=cerr, linestyle = 'none', marker = 's',
                    label='fitted %s' %model, markersize=2, 
                    markeredgecolor = 'none')
        pl.errorbar(bad_rad, bad_color, yerr=bad_cerr, linestyle = 'none', 
                    marker = 's', label='excluded %s' %model, markersize=2,
                    markeredgecolor = 'none')
        pl.errorbar(data_rads, data_color, yerr=data_cerr, 
                    linestyle = 'none', marker = 'o',
                    label='fitted data', markersize=2,
                    color = 'k', ecolor='k')
        pl.errorbar(data_bad_rad, data_bad_color, yerr=data_bad_cerr, 
                    linestyle = 'none', 
                    marker = 'o', label='excluded data', markersize=2,
                    color = 'k', ecolor='k')

    
        for hrad_window in [(0.001,1.0,'fit 0-1: %.2f', 'r'),(1.0,2.0, 'fit 1-2: %.2f','g'),
                            (2.0,3.0, 'fit 2-3: %.2f','c'), (0.001, 3.0, 'fit 0-3: %.2f','m')]:
            try:
                print "window"
                print hrad_window

                to_use = np.where(profiles['log_rad_arcsec']<= np.log10(hrad_window[1]*hrad_arcsec),1,0)*np.where(profiles['log_rad_arcsec']> np.log10(hrad_window[0]*hrad_arcsec),1,0)
                print to_use
                to_use = np.where(to_use==1) #the elements to use for fitting
                if len(to_use[0])<2:
                    continue
                print to_use
                tmp_fit = linefit(profiles['log_rad_arcsec'][to_use],
                                  profiles[bands][to_use],
                                  yerr=profiles[bands+'_err'][to_use])

                calc_rad = np.arange(np.log10(hrad_window[0]*hrad_arcsec), 
                                     np.log10(hrad_window[1]*hrad_arcsec), 0.01)

                calc_color = np.array(tmp_fit.predict(calc_rad))
                
#                print calc_rad, calc_color, calc_color[0,:]
#                raw_input()
                pl.plot(calc_rad, calc_color[0,:], color = hrad_window[3], 
                        label=hrad_window[2] %(tmp_fit.b[1]))
            except:
                pass
        pl.xlabel('log$_{10}$r (arcsec)')
        pl.ylabel('g-r')
        pl.legend(bbox_to_anchor=(-0.3, -0.4, 1., .102))
        pl.suptitle('color profile for galaxy %d, %.2f, %.2f, %.2f' %(gc, dat[-3], dat[-2], dat[-1]))
        pl.xlim(np.min(profiles['log_rad_arcsec']-0.2), np.log10(3.0*hrad_arcsec*hradlim))
        pl.ylim((np.min(np.extract(rads_to_use>=1, profiles[bands]))-0.2,
                 np.max(np.extract(rads_to_use>=1, profiles[bands]))+0.2))

        for rad_pt in np.log10(np.arange(1.0,3.01,1.0)*hrad_arcsec):
            pl.plot((rad_pt,rad_pt),pl.ylim(), 'k:')
            
        pl.plot((profiles['log_rad_arcsec'][rad_sky_cut_g],
                 profiles['log_rad_arcsec'][rad_sky_cut_g]), pl.ylim(), 'g:')
        pl.plot((profiles['log_rad_arcsec'][rad_sky_cut_r],
                 profiles['log_rad_arcsec'][rad_sky_cut_r]), pl.ylim(), 'r:')
        #pl.plot(pl.xlim(),[sky_g-sky_r,sky_g-sky_r], 'm:')
        #pl.plot(pl.xlim(),[color_corr,color_corr], 'c:')
        pl.subplots_adjust(wspace=0.4)
        #pl.show()
           
        pp.savefig()
        pl.close('all')
    except:
        pl.close('all')      

    #break
pp.close()
