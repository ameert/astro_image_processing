#++++++++++++++++++++++++++
#
# TITLE: plot_sample.py
#
# PURPOSE: to plot basic distirbutions
#          of a sample, these include:
#          redshift(z), abs Mag, app mag, 
#          surface brightness, and halflight
#          radii.
#
# INPUTS: the galaxy data, the plot_stem
#
# OUTPUTS: the plots whose file names will 
#          start with "plot_stem"
#
# PROGRAM CALLS: numpy, pylab, MatplotRc
#                
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE:
#
#-----------------------------------
import numpy as np
import pylab as  pl
from MatplotRc import *
import time
#from plotting_funcs import *
def start_fig(sizech = (13,13)):
    matrc4X6()

    fig = pl.figure(figsize =sizech, frameon = True)

    fig.subplots_adjust(left = 0.25,  # the left side of the subplots of the figure
                        right = 0.97,    # the right side of the subplots of the figure
                        bottom = 0.3,   # the bottom of the subplots of the figure
                        top = 0.95,      # the top of the subplots of the figure
                        wspace = 0.48,   # the amount of width reserved for blank space between subplots
                        hspace = 0.48)   # the amount of height reserved for white space between subplots

    return fig

def plot_sample(z, absMag, appMag, rhl_arcsec, surf_bright, V_max,
                plot_stem = '', colors = ['k']):
    
    lsl = [2,1,1,1,2]
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
                         ymaj = 2, ymin = 1, ystr =  '% 02.1f')

    for curr_z, curr_weight, curr_color, cls, label  in zip(z, weights, colors, lsl, ['all','z1']): 
        n,bins,patches = pl.hist(curr_z, bins= 15*4, weights = curr_weight, range=(0,0.3), histtype = 'step', 
                color = curr_color, lw = cls, normed = True)

        fout = open('/home/ameert/Desktop/%s_z.txt' %label, 'w')
        fout.write('#bins, pdf\n')
        binctr= (bins[0:-1]+bins[1:])/2.0
        for a,b in zip(binctr, n):
            fout.write('%f %f\n' %(a,b))

    pl.xlabel('z')
    pl.ylabel('n(z)')
    pl.xlim((0, 0.325))
    pl.ylim((0,8.5))
    ax = pl.gca()
    plot_set.set_plot(ax)
    pl.savefig(plot_stem + 'z_dist.eps')#, bbox_inches = 'tight')
    pl.close(fig)
    
    # now do absmag distribution... 

    fig = start_fig(fig_size)            
    plot_set = pub_plots(xmaj = 0.1, xmin = 0.025, xstr = '%02.1f', 
                         ymaj = 2, ymin = 1, ystr =  '% 02.1f')

    for curr_absmag, curr_color, cls, label in zip(absMag,  colors,lsl, ['all','z1']): 
    
        n, bins, patches = pl.hist(curr_absmag, bins = 18*4, range=(-25,-16), log = True, color = curr_color, linestyle = 'solid', histtype = 'step', lw = cls, normed = True)
    
        fout = open('/home/ameert/Desktop/%s_absmag.txt' %label, 'w')
        fout.write('#bins, pdf\n')
        binctr= (bins[0:-1]+bins[1:])/2.0
        for a,b in zip(binctr, n):
            fout.write('%f %f\n' %(a,b))
        
    plot_set = pub_plots(xmaj = 2, xmin = 1, xstr = '%d', 
                         ymaj = 10, ymin = 5, ystr =  '% 02.1f')

    pl.xlim((-16,-25))
    #pl.ylim((10**-7.0,.1))
    pl.xlabel('M$_{r}$')
    pl.ylabel('log(n)')
    
    ax = pl.gca()
    plot_set.set_plot(ax)
    pl.yticks((1,1/10.,1/100.,1/1000.,1/10000.,1/100000.,1/1000000.,1/10000000.),(' 0.0', '','-2.0','','-4.0','','-6.0',''))#ax.set_yscale('log')
    pl.savefig(plot_stem+'absmag.eps')#, bbox_inches = 'tight')
    pl.close(fig)

    # now do luminosity distribution... 

    fig = start_fig(fig_size)            
    plot_set = pub_plots(xmaj = 0.1, xmin = 0.025, xstr = '%02.1f', 
                         ymaj = 2, ymin = 1, ystr = '% 02.1f')

    for curr_absmag,curr_V, curr_weight, curr_color, cls, label in zip(absMag, V_max, weights, colors,lsl, ['all','z1']): 
    
        V_weight = 1.0/curr_V
        n, bins, patches = pl.hist(curr_absmag, bins = 18, weights = V_weight/np.sum(V_weight), range=(-25,-16), log = True, color = curr_color, linestyle = 'solid', histtype = 'step', lw = cls, normed = True)

        fout = open('/home/ameert/Desktop/%s_lumfunc.txt' %label, 'w')
        fout.write('#bins, pdf\n')
        binctr= (bins[0:-1]+bins[1:])/2.0
        for a,b in zip(binctr, n):
            fout.write('%f %f\n' %(a,b))

    plot_set = pub_plots(xmaj = 2, xmin = 1, xstr = '%d', 
                         ymaj = 10, ymin = 5, ystr =  '% 02.1f')

    pl.xlim((-16,-25))
    #pl.ylim((10**-7.0,.1))
    pl.xlabel('M$_{r}$')
    pl.ylabel('log(n)')
    
    ax = pl.gca()
    plot_set.set_plot(ax)
    pl.yticks((1,1/10.,1/100.,1/1000.,1/10000.,1/100000.,1/1000000.,1/10000000.),(' 0.0', '','-2.0','','-4.0','','-6.0',''))#ax.set_yscale('log')
    pl.savefig(plot_stem+'lum_func.eps')#, bbox_inches = 'tight')
    pl.close(fig)

    # now do apparent mag distribution... 
    fig = start_fig(fig_size)            

    plot_set = pub_plots(xmaj = 1, xmin = 0.5, xstr = '%d', 
                         ymaj = 0.2, ymin = 0.1, ystr =  '% 02.1f')
    
    for curr_appmag, curr_weight, curr_color, cls, label in zip(appMag, weights, colors, lsl, ['all', 'z1']): 
        n, bins, patches = pl.hist(curr_appmag, weights = curr_weight, bins = 10*4, 
                                   range=(13,18), histtype = 'step', color = curr_color, lw = cls, normed = True)

        fout = open('/home/ameert/Desktop/%s_appmag.txt' %label, 'w')
        fout.write('#bins, pdf\n')
        binctr= (bins[0:-1]+bins[1:])/2.0
        for a,b in zip(binctr, n):
            fout.write('%f %f\n' %(a,b))

    pl.xlim((13.5,18.5))
    pl.ylim((0,0.8))
    pl.xlabel('m$_{r}$')
    pl.ylabel('n(m$_{r}$)')
    
    ax = pl.gca()
    plot_set.set_plot(ax)
    pl.savefig(plot_stem+'appmag_dist.eps')#, bbox_inches = 'tight')
    pl.close(fig)

    # now do radii distribution... 

    fig = start_fig(fig_size)            
    plot_set = pub_plots(xmaj = 2, xmin = 0.5, xstr = '%d', 
                         ymaj = 0.2, ymin = 0.05, ystr =  '% 02.1f')
    

    for curr_rhl, curr_weight, curr_color, cls in zip(rhl_arcsec, weights, colors, lsl): 
        n, bins, patches = pl.hist(curr_rhl, weights = curr_weight,bins = 20, 
                                   range=(0,10), histtype = 'step', color = curr_color, lw = cls, normed = True)

    pl.xlim((0,10.5))
    pl.ylim((0,.7))
    pl.xlabel('r$_{r, hl}$ [arcsec]')
    pl.ylabel('n(r$_{r, hl}$)')
    
    ax = pl.gca()
    plot_set.set_plot(ax)
    pl.savefig(plot_stem+'rad_dist.eps')#, bbox_inches = 'tight')
    pl.close(fig)

    # now do surface brightness distribution... 

    fig = start_fig(fig_size)            
    plot_set = pub_plots(xmaj = 2, xmin = 0.5, xstr = '%d', 
                         ymaj = 0.2, ymin = 0.05, ystr =  '% 02.1f')
    
    for curr_sb, curr_weight, curr_color, cls in zip(surf_bright, weights, colors,lsl): 
        n, bins, patches = pl.hist(curr_sb, weights = curr_weight,bins = 12, 
                                   range=(18,24), histtype = 'step', color = curr_color, lw = cls, normed = True)

    pl.xlim((18,24.5))
    pl.ylim((0,0.601))
    pl.xlabel('$\mu_{r, hl}$')
    pl.ylabel('n($\mu_{r, hl}$)')
    
    ax = pl.gca()
    plot_set.set_plot(ax)
    pl.savefig(plot_stem+'surfbright_dist.eps')#, bbox_inches = 'tight')
    pl.close(fig)


def get_flag_props(binvalx, binvaly, bins):

    binpos, xedge, yedge = np.histogram2d(binvalx, binvaly, bins=bins) 

    colsum = np.sum(binpos, axis=0)

    print binpos
    print colsum
    binpos = binpos /colsum
    print binpos

    return binpos

def plot_2d_sample(petromag_r, halflight_rad, plot_stem = './lackner_sample'):    
    mag_delta = 0.25
    magbins = np.arange(13.75, 18.01, mag_delta)
    
    rad_delta = 0.25
    radbins = np.arange(0.5, 6.01, rad_delta)
    
    props = get_flag_props(petromag_r, halflight_rad, [magbins, radbins])

    pl.imshow(props, extent = (magbins[0], magbins[-1], radbins[0], radbins[-1]), vmin = 0, interpolation = 'nearest', origin = 'lower', aspect = 'auto')
    xlim = pl.xlim()
    ylim = pl.ylim()
    pl.ylabel('M$_{petro}$')
    pl.xlabel('r$_{petro}$')
    pl.colorbar()
    #pl.plot([-25,-17],[-25,-17], 'r-')
    pl.xlim(xlim)
    pl.ylim(ylim)
    pl.savefig(plot_stem+'_rad_mag_dist.eps')
    return
