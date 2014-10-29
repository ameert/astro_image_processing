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

def plot_sample(z, absMag, appMag, rhl_arcsec, surf_bright, V_max,
                plot_stem = '', colors = ['k'], write_points=False, 
                line_styles=['-'], title=''):
    
    lsl = [0.5,0.5,0.5,0.5,0.5,0.5]
    if len(plot_stem)> 0 and plot_stem[-1]!='_':
        plot_stem += "_"

    # weight all gals equally
    weights = []
    for tmp_z in z:
        tmp = np.ones_like(tmp_z)
        tmp = tmp/np.sum(tmp)
        
        weights.append(tmp)

    # first plot z distribution
    fig_size = get_fig_size()
    #fig_size = (10,10)
    fig = start_fig(fig_size)            
    plot_set = pub_plots(xmaj = 0.1, xmin = 0.025, xstr = '%02.1f', 
                         ymaj = 0.01, ymin = 0.001, ystr =  '%03.2f')

    for curr_z, curr_weight, curr_color, cls, label, clstyle  in zip(z, weights, colors, lsl, ['all'],line_styles): 
        curr_color = 'k'
        n,bins,patches = pl.hist(curr_z, bins= 15*4, weights = curr_weight, range=(0.4,0.6), histtype = 'step', 
                color = curr_color, lw = cls)

        if write_points:
            fout = open('/home/ameert/Desktop/%s_z.txt' %label, 'w')
            fout.write('#bins, pdf\n')
            binctr= (bins[0:-1]+bins[1:])/2.0
            for a,b in zip(binctr, n):
                fout.write('%f %f\n' %(a,b))

    pl.title(title)
    pl.xlabel('z')
    pl.ylabel('n(z)')
    pl.xlim((0.4, 0.6))
    pl.ylim((0,0.05))
    ax = pl.gca()
    plot_set.set_plot(ax)
    pl.savefig(plot_stem + 'z_dist.eps')#, bbox_inches = 'tight')
    pl.close(fig)
    
    # now do absmag distribution... 

    fig = start_fig(fig_size)            
    plot_set = pub_plots(xmaj = 2, xmin = 0.5, xstr = '%d', 
                         ymaj = 2, ymin = 1, ystr =  '% 02.1f')

    for curr_absmag, curr_color, cls, label, clstyle in zip(absMag,  colors,lsl, ['g-band','r-band', 'i-band']*2,line_styles): 
    
        n, bins, patches = pl.hist(curr_absmag, bins = 18*4, range=(-30,-10), color = curr_color, linestyle = clstyle, histtype = 'step', lw = cls, weights = np.ones_like(curr_absmag)/curr_absmag.size )
    
        if write_points:
            fout = open('/home/ameert/Desktop/%s_absmag.txt' %label, 'w')
            fout.write('#bins, pdf\n')
            binctr= (bins[0:-1]+bins[1:])/2.0
            for a,b in zip(binctr, n):
                fout.write('%f %f\n' %(a,b))
        
    pl.title(title)
    pl.xlim((-13.5,-25.5))
    #pl.ylim((-6.0,0.0))
    pl.xlabel('M$_{petro}$')
    pl.ylabel('log(n)')
    
    ax = pl.gca()
    ax.set_yscale('log')
    plot_set.set_plot(ax)
    pl.yticks((1,1/10.,1/100.,1/1000.,1/10000.,1/100000.,1/1000000.,1/10000000.),(' 0.0', '','-2.0','','-4.0','','-6.0',''))#ax.set_yscale('log')
    pl.savefig(plot_stem+'absmag.eps')#, bbox_inches = 'tight')
    pl.close(fig)

    # now do luminosity distribution... 

    fig = start_fig(fig_size)            
    plot_set = pub_plots(xmaj = 2, xmin = 0.5, xstr = '%d', 
                         ymaj = 2, ymin = 1, ystr = '% 02.1f')

    for curr_absmag,curr_V, curr_weight, curr_color, cls, label, clstyle in zip(absMag, V_max, weights, colors,lsl, ['g-band','r-band', 'i-band']*2,line_styles): 
    
        V_weight = 1.0/curr_V
        n, bins, patches = pl.hist(curr_absmag, bins = 24, weights = V_weight/np.sum(V_weight), range=(-25,-13), color = curr_color, linestyle = clstyle, histtype = 'step', lw = cls)

        if write_points:
            fout = open('/home/ameert/Desktop/%s_lumfunc.txt' %label, 'w')
            fout.write('#bins, pdf\n')
            binctr= (bins[0:-1]+bins[1:])/2.0
            for a,b in zip(binctr, n):
                fout.write('%f %f\n' %(a,b))

    pl.title(title)
    pl.xlim((-13.5,-25.5))
    #pl.ylim((10**-7.0,.1))
    pl.xlabel('M$_{petro}$')
    pl.ylabel('log(n)')
    
    ax = pl.gca()
    ax.set_yscale('log')
    plot_set.set_plot(ax)
    pl.yticks((1,1/10.,1/100.,1/1000.,1/10000.,1/100000.,1/1000000.,1/10000000.),(' 0.0', '','-2.0','','-4.0','','-6.0',''))
    pl.savefig(plot_stem+'lum_func.eps')#, bbox_inches = 'tight')
    pl.close(fig)

    # now do apparent mag distribution... 
    fig = start_fig(fig_size)            

    plot_set = pub_plots(xmaj = 1, xmin = 0.5, xstr = '%d', 
                         ymaj = 0.05, ymin = 0.01, ystr =  '% 03.2f')
    
    for curr_appmag, curr_weight, curr_color, cls, label, clstyle in zip(appMag, weights, colors, lsl, ['g-band','r-band', 'i-band']*2, line_styles): 
        n, bins, patches = pl.hist(curr_appmag, weights = curr_weight, bins = 10*14, 
                                   range=(16,30), histtype = 'step', color = curr_color, lw = cls, linestyle=clstyle)

        if write_points:
            fout = open('/home/ameert/Desktop/%s_appmag.txt' %label, 'w')
            fout.write('#bins, pdf\n')
            binctr= (bins[0:-1]+bins[1:])/2.0
            for a,b in zip(binctr, n):
                fout.write('%f %f\n' %(a,b))

    pl.title(title)
    pl.xlabel('m$_{petro}$')
    pl.ylabel('n(m$_{petro}$)')
    
    ax = pl.gca()
    plot_set.set_plot(ax)
    pl.ylim((0,0.05))
    pl.xlim((17.0,27.0))
    pl.savefig(plot_stem+'appmag_dist.eps')#, bbox_inches = 'tight')
    pl.close(fig)

    # now do radii distribution... 

    fig = start_fig(fig_size)            
    plot_set = pub_plots(xmaj = 2, xmin = 0.5, xstr = '%d', 
                         ymaj = 0.1, ymin = 0.01, ystr =  '% 02.1f')
    

    for curr_rhl, curr_weight, curr_color, cls, clstyle in zip(rhl_arcsec, weights, colors, lsl, line_styles): 
        n, bins, patches = pl.hist(curr_rhl, weights = curr_weight,bins = 40, 
                                   range=(0,10), histtype = 'step', color = curr_color, lw = cls, linestyle=clstyle)

    pl.title(title)
    pl.xlim((0,8.5))
    pl.ylim((0,.15))
    pl.xlabel('r$_{hl}$ [arcsec]')
    pl.ylabel('n(r$_{hl}$)')
    
    ax = pl.gca()
    plot_set.set_plot(ax)
    pl.savefig(plot_stem+'rad_dist.eps')#, bbox_inches = 'tight')
    pl.close(fig)

    # now do surface brightness distribution... 

    fig = start_fig(fig_size)            
    plot_set = pub_plots(xmaj = 2, xmin = 0.5, xstr = '%d', 
                         ymaj = 0.02, ymin = 0.005, ystr =  '% 03.2f')
    
    for curr_sb, curr_weight, curr_color, cls, clstyle in zip(surf_bright, weights, colors,lsl, line_styles): 
        n, bins, patches = pl.hist(curr_sb, weights = curr_weight,bins = 48, 
                                   range=(18,24), histtype = 'step', color = curr_color, lw = cls, linestyle=clstyle)

    pl.title(title)
    pl.xlim((18,24.5))
    pl.ylim((0,0.1))
    pl.xlabel('$\mu_{hl}$')
    pl.ylabel('n($\mu_{hl}$)')
    
    ax = pl.gca()
    plot_set.set_plot(ax)
    pl.savefig(plot_stem+'surfbright_dist.eps')#, bbox_inches = 'tight')
    pl.close(fig)
    return

def get_alldat(band, distance, table):
    cmd = 'select zgal, 1.0 as Vmax, PetroMag_{band} - extinction_{band} - dismod, petromag_{band} - extinction_{band}, 1.0 as petroR50_{band}, petromag_{band}  from catalog.corr_lum_func_{table} as b where kpc_per_arcsec*distance*60.0 between {dislow} and {dishigh};'.format(band=band, dislow=distance[0], dishigh=distance[1], table=table)

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


for distance in [(100,300),(300,500),(500,700),(700, 900)]:
    title = '%d$\leq distance \leq$ %d kpc' %(distance[0], distance[1])
    z = []
    absmag = []
    petromag = []
    halflight_rad =[]
    surf_bright = []
    V_max = []

    ztmp, vmaxtmp, petrotmp, hradtmp, abtmp, sbtmp  = get_alldat('g', distance, 'CMASS')
    z.append(ztmp)
    absmag.append(abtmp)
    petromag.append(petrotmp)
    halflight_rad.append(hradtmp)
    surf_bright.append(sbtmp)
    V_max.append(vmaxtmp)
    ztmp, vmaxtmp, petrotmp, hradtmp, abtmp, sbtmp  = get_alldat('r', distance, 'CMASS')
    z.append(ztmp)
    absmag.append(abtmp)
    petromag.append(petrotmp)
    halflight_rad.append(hradtmp)
    surf_bright.append(sbtmp)
    V_max.append(vmaxtmp)
    ztmp, vmaxtmp, petrotmp, hradtmp, abtmp, sbtmp  = get_alldat('i', distance, 'CMASS')
    z.append(ztmp)
    absmag.append(abtmp)
    petromag.append(petrotmp)
    halflight_rad.append(hradtmp)
    surf_bright.append(sbtmp)
    V_max.append(vmaxtmp)

    ztmp, vmaxtmp, petrotmp, hradtmp, abtmp, sbtmp  = get_alldat('g', distance, 'blanks')
    z.append(ztmp)
    absmag.append(abtmp)
    petromag.append(petrotmp)
    halflight_rad.append(hradtmp)
    surf_bright.append(sbtmp)
    V_max.append(vmaxtmp)
    ztmp, vmaxtmp, petrotmp, hradtmp, abtmp, sbtmp  = get_alldat('r', distance, 'blanks')
    z.append(ztmp)
    absmag.append(abtmp)
    petromag.append(petrotmp)
    halflight_rad.append(hradtmp)
    surf_bright.append(sbtmp)
    V_max.append(vmaxtmp)
    ztmp, vmaxtmp, petrotmp, hradtmp, abtmp, sbtmp  = get_alldat('i', distance, 'blanks')
    z.append(ztmp)
    absmag.append(abtmp)
    petromag.append(petrotmp)
    halflight_rad.append(hradtmp)
    surf_bright.append(sbtmp)
    V_max.append(vmaxtmp)

    print z, absmag, petromag, halflight_rad, surf_bright, V_max

    plot_sample(z, absmag, petromag, halflight_rad, surf_bright, V_max, plot_stem = './corr_lum_all_%s' %distance[0], colors = ['#00CC00','#FF0000','#000000','#66E066','#FF8080','#B2B2B2'], line_styles=['solid','solid','solid','solid','solid','solid'], title=title)
