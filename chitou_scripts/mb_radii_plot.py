import numpy as np
import matplotlib.pyplot as plt

from astro_image_processing.user_settings import mysql_params
from astro_image_processing.statistics import bin_stats
from astro_image_processing.mysql import *

cursor = mysql_connect(mysql_params['dba'],mysql_params['user'],mysql_params['pwd'])

 
class data(object):
    """contains radii data for plotting"""
    def __init__(self, tablea, tableb, hrad, r20, r50, r80, r90, scale):
        self.tablea = tablea
        self.tableb = tableb
        self.hrad = hrad
        self.r20 = r20
        self.r50 = r50
        self.r80 = r80
        self.r90 = r90
        self.scale = scale
        self.plotdat = {}
        self.zbins = np.arange(0.05,0.23, 0.02)
        self.mbins = np.arange(9.0,12.5, 0.4)
        self.plot_colors = ['Black','Blue','Cyan','OliveDrab',
                            'Green','Chocolate','Orange', 'Tomato',
                            'Red', 'Orchid', 'Magenta']
        return

    def fetch(self):
        cmd =  """select f.galcount, f.z,f.petroR50_r,f.petroR90_r,
IFNULL(log10(f.veldisp), -999), IF(m.probaEll<=0, 0, m.probaEll), IF(m.probaS0<=0, 0, m.probaS0), IF((m.probaSab+m.probaScd)<=0, 0, m.probaSab+m.probaScd), 
j.logMs,{scale},
{hrad}, {r20}, {r50}, {r80}, {r90}
from 
catalog.{tablea} as a,
catalog.{tableb} as b, 
catalog.r_band_fit as c,
catalog.CAST as f left join 
catalog.Mariangela_masses as j on f.galcount = j.galcount,
catalog.DERT as d,
catalog.M2010 as m, 
catalog.Flags_optimize as u
where
f.galcount = a.galcount and
f.galcount = b.galcount and
f.galcount = c.galcount and
f.galcount = d.galcount and 
f.galcount = m.galcount and 
f.galcount = u.galcount and 
u.ftype = 'u' and u.band='r' and u.model = 'serexp' 
order by f.galcount;""".format(**self.__dict__)

        data = cursor.get_data(cmd)
        varnames = ['galcount', 'z','petroR50_r','petroR90_r',
                    'logvd', 'pEll', 'pS0', 'pL', 'logmstar','scale',
                    'hrad', 'r20', 'r50', 'r80', 'r90']

        for a in zip(varnames, data):
            self.plotdat[a[0]]=np.array(a[1], dtype=float)   
        
        for a in ['hrad', 'r20', 'r50', 'r80', 'r90','petroR50_r','petroR90_r']:
            self.plotdat[a]*=self.plotdat['scale']   
        
        return

    def plot(self, radlist):
        """makes a plot of the radius data"""
        fig = plt.figure(figsize=(8,6))
        for zlims in zip(self.zbins[:-1], self.zbins[1:], self.plot_colors):
            print zlims
            zmask = np.where(self.plotdat['z']>=zlims[0],1.0,0.0)*np.where(self.plotdat['z']<=zlims[1],1.0,0.0)
            zmask = zmask*self.plotdat['pEll']
            print "gals ", np.sum(zmask)

            self.plotz(zmask,zlims[2], radlist) 
        return fig
    
    def plotz(self, zmask, color, radlist):
        for rad, linestyle in zip(radlist, ['-',':','--', '--']):
            a = bin_stats.bin_stats(self.plotdat['logmstar'],self.plotdat[rad], self.mbins, 0.0, 200.0, weight = zmask)
            a.to_log(1)
            a.plot_ebar('median', 'med95ci', color=color, linestyle = linestyle)
        return

if __name__ == "__main__": 
    from matplotlib.backends.backend_pdf import PdfPages
    pp = PdfPages('alans_test.pdf')
    if 0:
        a = data('r_band_ser','ser_conc_rads','a.hrad_corr','b.r20*0.396','b.r50*0.396','b.r80*0.396','b.r90*0.396', 'd.kpc_per_arcsec')
        a.fetch()
        fig = a.plot(['hrad', 'r50', 'petroR50_r'])#, 'r20', 'r80'])
        plt.title('alans code (chitou)')
        plt.ylim(0.0, 2.0)
        plt.xlim(10.0, 12.5)
        plt.xlabel('logM(star)')
        plt.ylabel('logR')
        pp.savefig()
        a = data('r_band_ser','alan_code_old','a.hrad_corr','b.r20Ser','b.r50Ser','b.r80Ser','b.r90Ser', 'd.kpc_per_arcsec')
        a.fetch()
        fig = a.plot(['hrad', 'r50', 'petroR50_r'])#, 'r20', 'r80'])
        plt.title('alans code old')
        plt.ylim(0.0, 2.0)
        plt.xlim(10.0, 12.5)
        plt.xlabel('logM(star)')
        plt.ylabel('logR')
        pp.savefig()
        a = data('r_band_ser','concent_all','a.hrad_corr','b.r20Ser','b.r50Ser','b.r80Ser','b.r90Ser', 'd.kpc_per_arcsec')
        a.fetch()
        fig = a.plot(['hrad', 'r50', 'petroR50_r'])#, 'r20', 'r80'])
        plt.title('concent_all')
        plt.ylim(0.0, 2.0)
        plt.xlim(10.0, 12.5)
        plt.xlabel('logM(star)')
        plt.ylabel('logR')
        pp.savefig()
        a = data('r_band_ser','alan_code_new','a.hrad_corr','b.r20Ser','b.r50Ser','b.r80Ser','b.r90Ser', 'd.kpc_per_arcsec')
        a.fetch()
        fig = a.plot(['hrad', 'r50', 'petroR50_r'])#, 'r20', 'r80'])
        plt.title('alans code (txt)')
        plt.ylim(0.0, 2.0)
        plt.xlim(10.0, 12.5)
        plt.xlabel('logM(star)')
        plt.ylabel('logR')
        pp.savefig()
        a = data('r_band_ser','agm_data_ser_no_psf','a.hrad_corr','b.r20*0.396','b.r50*0.396','b.r80*0.396','b.r90*0.396', 'd.kpc_per_arcsec')
        a.fetch()
        fig = a.plot(['hrad', 'r50', 'petroR50_r'])#, 'r20', 'r80'])
        plt.title('vinus code')
        plt.ylim(0.0, 2.0)
        plt.xlim(10.0, 12.5)
        plt.xlabel('logM(star)')
        plt.ylabel('logR')
        pp.savefig()

    a = data('r_band_ser','alan_1d_im_model_r_ser','a.hrad_corr','b.r20','b.r50','b.r80','b.r90', 'd.kpc_per_arcsec')
    a.fetch()
    fig = a.plot(['hrad', 'r50', 'petroR50_r'])#, 'r20', 'r80'])
    plt.title('alan again code')
    plt.ylim(0.0, 2.0)
    plt.xlim(10.0, 12.5)
    plt.xlabel('logM(star)')
    plt.ylabel('logR')
    pp.savefig()

    a = data('r_band_ser','alan_1d_im_model_r_ser','a.hrad_corr','b.r20','b.r50','b.r80','b.r90', 'd.kpc_per_arcsec')
    a.fetch()
    fig = a.plot(['r20', 'r50', 'r80'])
    plt.title('alan again code 20,50,80')
    plt.ylim(0.0, 2.0)
    plt.xlim(10.0, 12.5)
    plt.xlabel('logM(star)')
    plt.ylabel('logR')
    pp.savefig()

    pp.close()
