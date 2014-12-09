import numpy as np
import pylab as  pl
from astro_image_processing.MatplotRc import *
import time
from astro_image_processing.mysql import *
import scipy.stats as stats
#from plotting_funcs import *

def start_fig(sizech = (13,13)):
    matrc4X6()

    fig = pl.figure(figsize =sizech, frameon = True)

    fig.subplots_adjust(left = 0.25,  # the left side of the subplots of the figure
                        right = 0.95,    # the right side of the subplots of the figure
                        bottom = 0.3,   # the bottom of the subplots of the figure
                        top = 0.85,      # the top of the subplots of the figure
                        wspace = 0.48,   # the amount of width reserved for blank space between subplots
                        hspace = 0.48)   # the amount of height reserved for white space between subplots

    return fig

def plot_appmag(appMag, weight, plot_stem = '', colors = ['k'], 
                write_points=False, line_styles=['-'], title=''):
    
    lsl = [0.5,0.5,0.5,0.5,0.5,0.5]
    if len(plot_stem)> 0 and plot_stem[-1]!='_':
        plot_stem += "_"

    # weight all gals equally
    weights = [ 1.0/a for a in V_max]
     
    fig_size = get_fig_size()
    fig = start_fig(fig_size)            
    plot_set = pub_plots(xmaj = 1, xmin = 0.5, xstr = '%d', 
                         ymaj = 0.05, ymin = 0.01, ystr =  '% 03.2f')
    
    for curr_appmag, curr_weight, curr_color, cls, label, clstyle in zip(appMag, weights, colors, lsl, ['g-band','r-band', 'i-band'], line_styles): 
        n, bins, patches = pl.hist(curr_appmag, weights = curr_weight, bins = 10*20, 
                                   range=(10,30), histtype = 'step', color = curr_color, lw = cls, linestyle=clstyle)

        if write_points:
            fout = open('/home/ameert/Desktop/%s_appmag.txt' %label, 'w')
            fout.write('#bins, pdf\n')
            binctr= (bins[0:-1]+bins[1:])/2.0
            for a,b in zip(binctr, n):
                fout.write('%f %f\n' %(a,b))

    pl.title(title)
    pl.xlabel('m$_{petro}$')
    pl.ylabel('n(m$_{petro}$)  [mpc$^{-2}$]')
    
    print min(n)
    ax = pl.gca()
    pl.ylim((-100,100))
    pl.xlim((10.0,30.0))
    pl.plot(pl.xlim(), [0,0], 'k--')
    pl.savefig(plot_stem+'appmag_dist.eps')#, bbox_inches = 'tight')
    pl.close(fig)
    print plot_stem+'appmag_dist.eps saved!!!!'
    return


def get_alldat(band, distance, table, typesearch = 'all'):
    if typesearch=='all':
        type_trim=''
    elif typesearch=='star':
        type_trim=' and type=6 '
    elif typesearch=='galaxy':
        type_trim=' and type=3 '

    cmd = 'select zgal, 1.0 as Vmax, PetroMag_{band} - extinction_{band} - dismod, petromag_{band} - extinction_{band}, 1.0 as petroR50_{band}, petromag_{band}  from catalog.corr_lum_func_{table} as b where kpc_per_arcsec*distance*60.0 between {dislow} and {dishigh} {type_trim};'.format(band=band, dislow=distance[0], dishigh=distance[1], table=table,type_trim=type_trim)

    print cmd
    z, V_max, absmag, petromag, halflight_rad,ucorr_mag = cursor.get_data(cmd)

    z1 = np.array(z, dtype=float)
    V_max1 = np.array(V_max, dtype=float)
    petromag_1 = np.array(petromag, dtype=float)
    halflight_rad1 = np.array(halflight_rad, dtype=float)
    absmag1 = np.array(absmag, dtype=float)
    ucorr_mag1 = np.array(ucorr_mag, dtype=float)

    surf_bright1 = -2.5*np.log10(10**(-0.4*ucorr_mag1)/(2*np.pi*halflight_rad1**2.0))
    
    return z1, V_max1, petromag_1, halflight_rad1, absmag1, surf_bright1

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)
colors = {'i':('#000000','#B2B2B2'),'r':('#FF0000','#FF8080'), 
          'g':('#00CC00','#66E066')}


for band in 'gri':
    for distance in [(a,a+200) for a in range(100,4000,200)]:
        title = '%d$\leq distance \leq$ %d kpc' %(distance[0], distance[1])
        z = []
        absmag = []
        petromag = []
        halflight_rad =[]
        surf_bright = []
        V_max = []

        #vol_corr = 4.0*np.pi/3.0*(distance[1]**2 - distance[0]**2)**1.5 / 1.0e9 #in mpc
        rcorr = 2.0/(3.0*5000)*(distance[1]**3 - distance[0]**3)/(distance[1]**2 - distance[0]**2)
        area_corr = np.pi*(distance[1]**2 - distance[0]**2) / (1.0e3)**2/rcorr # mpc
        print "distance, vol_corr"
        print distance, area_corr


        for choice in ['CMASS',]:#, 'CMASS_blanks']:
            for typesearch in ['all','galaxy','star']:
                ztmp1, vmaxtmp1, petrotmp1, hradtmp1, abtmp1, sbtmp1  = get_alldat(band, distance, choice,typesearch = typesearch)
                ztmp2, vmaxtmp2, petrotmp2, hradtmp2, abtmp2, sbtmp2  = get_alldat(band, distance, choice+"_blanks",typesearch = typesearch)
                z.append(np.concatenate((ztmp1, ztmp2)))
                absmag.append(np.concatenate((abtmp1, abtmp2)))
                petromag.append(np.concatenate((petrotmp1, petrotmp2)))
                halflight_rad.append(np.concatenate((hradtmp1, hradtmp2)))
                surf_bright.append(np.concatenate((sbtmp1, sbtmp2)))
                V_max.append(np.concatenate((np.ones_like(petrotmp1)*area_corr,np.ones_like(petrotmp2)*area_corr*-1.0)))
                #V_max.append(vmaxtmp)

        print z, absmag, petromag, halflight_rad, surf_bright, V_max

        plot_appmag(petromag, V_max, 
                    plot_stem = './plots/corr_lum_all_%sband_%s' %(band,distance[0]), 
                    colors = [colors['i'][0],colors['r'][0],colors['g'][0]], 
                    line_styles=['solid','solid','solid'], title=title)
