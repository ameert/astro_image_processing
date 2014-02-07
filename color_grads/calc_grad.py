from mysql.mysql_class import *
import numpy as np
import pylab as pl
import sys
from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('grads.pdf')


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

cursor = mysql_connect(dba, usr, pwd, lhost)

folder_num = int(sys.argv[1])
path = '/home/ameert/color_grad/data/%04d' %folder_num
model = 'ser'

#cmd = """select a.galcount, x.r50_r_arcsec,x.r90_r_arcsec from CAST as a, 
#%s_hrad_90_est as x
#where a.galcount = x.galcount and a.galcount between %d and %d 
#order by galcount;""" %(model, (folder_num-1)*250, folder_num*250)

cmd = """select a.galcount, a.r_bulge*sqrt(a.ba_bulge), a.n_bulge,b.r_bulge*sqrt(b.ba_bulge), b.n_bulge, m.ProbaE, m.ProbaSab, m.ProbaScd from r_band_%s as a, g_band_%s as b, M2010 as m,Flags_optimize as c 
where a.galcount = m.galcount and a.galcount=b.galcount and a.galcount = c.galcount and c.band='r' and c.model='ser' and c.ftype='u' and c.flag&1>0 and m.ProbaE>0.75 and a.galcount between %d and %d order by a.galcount;""" %(model, model, (folder_num-1)*250, folder_num*250)

data = cursor.get_data(cmd)

galcount = np.array(data[0], dtype = int)

for gc, dat in zip(galcount,np.array(data[1:]).transpose()):
    hrad_arcsec = dat[0]
    if gc>9:
        break
    print gc, hrad_arcsec
    outfile = '%s/%08d_mag_corr_%s.npz' %(path, gc, model)
    try:
        profiles = np.load(outfile)
        hradlim = 3.0
        print gc, ' limit ', hrad_arcsec*hradlim, np.log10(hrad_arcsec*hradlim)
        print profiles.keys()
    
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

        pl.subplot(2,2,1)
        pl.errorbar(rads,gmag, yerr=gerr, linestyle = 'none', 
                    color = 'g', ecolor = 'g', marker = 'd',
                    label='g fitted data', markersize=4)
        pl.errorbar(bad_rad,bad_gmag, yerr=bad_gerr, linestyle = 'none', 
                    color = 'c', ecolor = 'c', marker = 'd',
                    label='g excluded data', markersize=4)
        pl.errorbar(rads,rmag, yerr=rerr, linestyle = 'none', 
                    color = 'r', ecolor = 'r', marker = 'd',
                    label='r fitted data', markersize=4)
        pl.errorbar(bad_rad,bad_rmag, yerr=bad_rerr, linestyle = 'none', 
                    color = 'm', ecolor = 'm', marker = 'd',
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

        pl.subplot(2,2,2)
        pl.errorbar(rads, color, yerr=cerr, linestyle = 'none', marker = 's',
                    label='fitted data', markersize=4)
        pl.errorbar(bad_rad, bad_color, yerr=bad_cerr, linestyle = 'none', 
                    marker = 's', label='excluded', markersize=4)

        for hrad_window in [(0.001,1.0,'fit 0-1: %.2f', 'r'),(1.0,2.0, 'fit 1-2: %.2f','g'),
                            (2.0,3.0, 'fit 2-3: %.2f','c'), (0.001, 3.0, 'fit 0-3: %.2f','m')]:
            print "window"
            print hrad_window
            
            to_use = np.where(profiles['log_rad_arcsec']<= np.log10(hrad_window[1]*hrad_arcsec),1,0)*np.where(profiles['log_rad_arcsec']> np.log10(hrad_window[0]*hrad_arcsec),1,0)
            print to_use
            to_use = np.where(to_use==1) #the elements to use for fitting
            print to_use
            tmp_fit = linefit(profiles['log_rad_arcsec'][to_use],
                              profiles[bands][to_use],
                              yerr=profiles[bands+'_err'][to_use])
            
            calc_rad = np.arange(np.log10(hrad_window[0]*hrad_arcsec), 
                                 np.log10(hrad_window[1]*hrad_arcsec), 0.01)

            calc_color = np.array(tmp_fit.predict(calc_rad))
            
            pl.plot(calc_rad, calc_color[0,:], color = hrad_window[3], 
                    label=hrad_window[2] %(tmp_fit.b[1]))
            
        pl.xlabel('log$_{10}$r (arcsec)')
        pl.ylabel('g-r')
        pl.legend(bbox_to_anchor=(-0.3, -0.4, 1., .102))
        pl.suptitle('color profile for galaxy %d, %.2f, %.2f, %.2f' %(gc, dat[-3], dat[-2], dat[-1]))
        pl.xlim(np.min(profiles['log_rad_arcsec']-0.2), np.log10(3.0*hrad_arcsec*hradlim))
        pl.subplots_adjust(wspace=0.4)
        #pl.show()
           
        pp.savefig()
        pl.close('all')
    except:
        pass
pp.close()
