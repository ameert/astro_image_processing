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
    
    lsl = [2,2,2,2,2]
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

    for curr_z, curr_weight, curr_color, cls, label  in zip(z, weights, colors, lsl, ['all']): 
        curr_color = 'k'
        n,bins,patches = pl.hist(curr_z, bins= 15*4, weights = curr_weight, range=(0,0.3), histtype = 'step', 
                color = curr_color, lw = cls)

        fout = open('/home/ameert/Desktop/%s_z.txt' %label, 'w')
        fout.write('#bins, pdf\n')
        binctr= (bins[0:-1]+bins[1:])/2.0
        for a,b in zip(binctr, n):
            fout.write('%f %f\n' %(a,b))

    pl.xlabel('z')
    pl.ylabel('n(z)')
    pl.xlim((0, 0.325))
    pl.ylim((0,0.05))
    ax = pl.gca()
    plot_set.set_plot(ax)
    pl.savefig(plot_stem + 'z_dist.eps')#, bbox_inches = 'tight')
    pl.close(fig)
    
    # now do absmag distribution... 

    fig = start_fig(fig_size)            
    plot_set = pub_plots(xmaj = 2, xmin = 0.5, xstr = '%d', 
                         ymaj = 2, ymin = 1, ystr =  '% 02.1f')

    for curr_absmag, curr_color, cls, label in zip(absMag,  colors,lsl, ['g-band','r-band', 'i-band']): 
    
        n, bins, patches = pl.hist(curr_absmag, bins = 18*4, range=(-30,-10), color = curr_color, linestyle = 'solid', histtype = 'step', lw = cls, weights = np.ones_like(curr_absmag)/curr_absmag.size )
    
        fout = open('/home/ameert/Desktop/%s_absmag.txt' %label, 'w')
        fout.write('#bins, pdf\n')
        binctr= (bins[0:-1]+bins[1:])/2.0
        for a,b in zip(binctr, n):
            fout.write('%f %f\n' %(a,b))
        
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

    for curr_absmag,curr_V, curr_weight, curr_color, cls, label in zip(absMag, V_max, weights, colors,lsl, ['g-band','r-band', 'i-band']): 
    
        V_weight = 1.0/curr_V
        n, bins, patches = pl.hist(curr_absmag, bins = 24, weights = V_weight/np.sum(V_weight), range=(-25,-13), color = curr_color, linestyle = 'solid', histtype = 'step', lw = cls)

        fout = open('/home/ameert/Desktop/%s_lumfunc.txt' %label, 'w')
        fout.write('#bins, pdf\n')
        binctr= (bins[0:-1]+bins[1:])/2.0
        for a,b in zip(binctr, n):
            fout.write('%f %f\n' %(a,b))

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
                         ymaj = 0.2, ymin = 0.1, ystr =  '% 02.1f')
    
    for curr_appmag, curr_weight, curr_color, cls, label in zip(appMag, weights, colors, lsl, ['g-band','r-band', 'i-band']): 
        n, bins, patches = pl.hist(curr_appmag, weights = curr_weight, bins = 10*8, 
                                   range=(13,22), histtype = 'step', color = curr_color, lw = cls)

        fout = open('/home/ameert/Desktop/%s_appmag.txt' %label, 'w')
        fout.write('#bins, pdf\n')
        binctr= (bins[0:-1]+bins[1:])/2.0
        for a,b in zip(binctr, n):
            fout.write('%f %f\n' %(a,b))

    pl.xlim((14.0,19.5))
    pl.ylim((0,0.201))
    pl.xlabel('m$_{petro}$')
    pl.ylabel('n(m$_{petro}$)')
    
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
                                   range=(0,10), histtype = 'step', color = curr_color, lw = cls)

    pl.xlim((0,8.5))
    pl.ylim((0,.301))
    pl.xlabel('r$_{hl}$ [arcsec]')
    pl.ylabel('n(r$_{hl}$)')
    
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
                                   range=(18,24), histtype = 'step', color = curr_color, lw = cls)

    pl.xlim((18,24.5))
    pl.ylim((0,0.301))
    pl.xlabel('$\mu_{hl}$')
    pl.ylabel('n($\mu_{hl}$)')
    
    ax = pl.gca()
    plot_set.set_plot(ax)
    pl.savefig(plot_stem+'surfbright_dist.eps')#, bbox_inches = 'tight')
    pl.close(fig)




    

