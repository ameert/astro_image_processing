import pylab as pl
import numpy as np
from mysql_class import *
from bin_stats import *
from MatplotRc import *
from matplotlib.font_manager import FontProperties

dba = 'catalog'
usr = 'ameert'
pwd = 'al130568'

cursor = mysql_connect(dba, usr, pwd)


size = get_fig_size()
size[0] *=2
size[1] *=6 

fig1 = pl.figure(num=1,figsize=size, frameon=True)
ticks = pub_plots(xmaj = 1,xmin=0.5,xstr= '%d',ymaj = 0.5,ymin = 0.25,ystr='%2.1f')
pl.subplots_adjust(left = 0.15, right = 0.9, bottom = 0.1,top = 0.92, wspace = 0.15, hspace = 0.4) 
fig2 = pl.figure(num=2,figsize=size, frameon=True)
ticks2 = pub_plots(xmaj = 1,xmin=0.5,xstr= '%d',ymaj = 0.1,ymin = 0.05,ystr='%2.1f')
pl.subplots_adjust(left = 0.15, right = 0.9, bottom = 0.1,top = 0.92, wspace = 0.15, hspace = 0.4)

gals = {}
delta_M = 0.5
save_stem = 'color'
prob_cut = 0.7

for add_con, pos, title in zip([' and d.groupID >0 and d.most_massive = 2  and d.group_counts > 1 ', ' and d.groupID >0 and d.most_massive = 1 and d.group_counts > 1 ',' and d.groupID>0  and d.group_counts > 1 '],[3,2,1],['satellites', 'centrals', 'all']):
    fig1.add_subplot(3,1,pos)
    fig2.add_subplot(3,1,pos)
    for mrange, color in zip(np.arange(11.0, 15.01, delta_M), ['k', 'b','c','g','y', 'm','#FFA500','r']):
        try:
            #cmd = "select a.galcount, a.n, b.n, c.n, m.probaE, m.probaEll, m.probaS0, m.probaSab, m.probaScd, d.brightest, d.most_massive, d.L_group, d.Mstar_group,d.HaloMass_1, d.HaloMass_2, f.Mstar_med_shift, a.re_kpc, b.re_kpc, c.re_kpc from full_dr7_g_ser as a,full_dr7_r_serexp as b,full_dr7_i_ser as c, M2010 as m, yang.yang_groupsC as d, JHU.JHU_masses as f where a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and a.galcount = m.galcount and a.galcount = f.galcount and b.z<0.09 and b.manual_flag = 0 and b.fitflag = 0 and m.probaE >=%f and  abs(d.group_Z - b.z) <= 0.01 and d.fedge>=0.6 %s and d.HaloMass_1 between %f and %f;" %(prob_cut, add_con, mrange, mrange+delta_M) 
            cmd = "select a.galcount, a.n, b.n, c.n, m.probaE, m.probaEll, m.probaS0, m.probaSab, m.probaScd, d.brightest, d.most_massive, d.L_group, d.Mstar_group,d.HaloMass_1, d.HaloMass_2, f.Mstar_med_shift, a.re_kpc, b.re_kpc, c.re_kpc from full_dr7_g_ser as a,full_dr7_r_serexp as b,full_dr7_i_ser as c, M2010 as m, CAST as z, DERT as y, magerr as x, yang.yang_groupsC as d, JHU.JHU_masses as f where a.galcount = z.galcount and a.galcount = x.galcount and a.galcount = y.galcount and a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and a.galcount = m.galcount and a.galcount = f.galcount and b.z<0.09 and b.manual_flag = 0 and b.fitflag = 0 and abs(d.group_Z - b.z) <= 0.01 and d.fedge>=0.6 %s and (d.HaloMass_1 between %f and %f) and (x.ModelMag_g -z.extinction_g - y.kcorr_g -x.ModelMag_i +z.extinction_i + y.kcorr_i)+0.0585*(x.ModelMag_i -z.extinction_i - y.kcorr_i - a.dis_modu+16.0)>0.78   ;" %(add_con, mrange, mrange+delta_M) #m.probaE >=0.8 and

            print cmd
            data = cursor.get_data(cmd)

        except IndexError:
            continue
    
        for d, dname in zip(data, ['galcount','n_g', 'n_r', 'n_i', 'PEarly', 
                                   'PEll','PS0',
                                   'PSab','PScd','brightest', 'most_massive', 
                                   'L_group','Mstar_group','HaloMass_1', 
                                   'HaloMass_2', 'logMstar', 
                                   're_g','re_r','re_i']):
            gals[dname] = np.array(d)
        print len(gals['galcount'])
        gals['PLate'] = gals['PSab']+gals['PScd']
        gals['P1'] = np.array([1])

        pl.figure(1)
        for ckey,ls in zip(['P1','PEll','PS0'],['-']):#,'--', ':']):
            a =bin_stats(gals['logMstar'],(gals['n_g']-gals['n_i']),
                np.arange(7.0,16.01,0.25), -4.0,4.0, weight = gals[ckey],    
                err_type = 'median')
            a.plot_ebar('median', '68n', marker = 'o',color = color, ms = 1, 
                        markerfacecolor = color,  ecolor = color, capsize = 5, 
                        linestyle = ls, elinewidth = 2, barsabove=True, 
                        zorder = 0, label='%.1f<M$_{halo}$<%.1f'%(mrange, mrange+delta_M))
            a.lay_bounds(color=color, sigma_choice = [68])
            for b1,b2,b3 in zip(a.bin_ctr,a.bin_median,a.bin_number):
                pl.plot(b1,b2,marker = 'o', color = color, 
                        ms = 1.5*np.log(float(b3)))

        pl.figure(2)
        for ckey,ls in zip(['P1','PEll','PS0'],['-']):#,'--', ':']):
            a = bin_stats(gals['logMstar'],
                (gals['re_g']-gals['re_i'])/gals['re_r'],
                np.arange(7.0,16.01,0.25), -10.0,10.0, weight = gals[ckey],    
                err_type = 'median')
            a.plot_ebar('median', '68n', marker = 'o',color = color, ms = 1, 
                        markerfacecolor = color,  ecolor = color, capsize = 5, 
                        linestyle = ls, elinewidth = 2, barsabove=True, 
                        zorder = 0, label='%.1f<M$_{halo}$<%.1f'%(mrange, mrange+delta_M))
            a.lay_bounds(color=color, sigma_choice = [68])
            for b1,b2,b3 in zip(a.bin_ctr,a.bin_median,a.bin_number):
                pl.plot(b1,b2,marker = 'o', color = color, 
                        ms = 1.5*np.log(float(b3)))

    pl.figure(1)
    for size in [10,100,1000,10000]:
        pl.plot(-100,-100,marker = 'o', color = 'r', 
                 ms = 1.5*np.log(float(size)), label = str(size))
    pl.title(title)
    ax = pl.gca()
    ax.set_aspect('auto')
    ticks.set_plot(ax)
    pl.xlabel('log(M$_{*}$)')
    pl.ylabel('(n$_g$ - n$_i$)')#/n$_r$')
    pl.xlim((9,12))
    pl.ylim((-1,0.5))
    pl.figure(2)

    for size in [10,100,1000,10000]:
        pl.plot(-100,-100,marker = 'o', color = 'r', 
                 ms = 1.5*np.log(float(size)), label = str(size))

    pl.title(title)
    ax = pl.gca()
    ax.set_aspect('auto')
    ticks2.set_plot(ax)
    pl.xlabel('log(M$_{*}$)')
    pl.ylabel('(r$_g$ - r$_i$)/r$_r$')
    pl.xlim((9,12))
    pl.ylim((-0.35,0.35))

pl.figure(1)
handles, labels = ax.get_legend_handles_labels()
legend_font_props = FontProperties()
legend_font_props.set_size('small')
l1 = pl.legend(handles[0:-4:1],labels[0:-4:1], bbox_to_anchor=(0, 0,1, 1), 
          bbox_transform=pl.gcf().transFigure, prop = {'size':6})
l2 = pl.legend(handles[-4::1],labels[-4::1], bbox_to_anchor=(0, .8,.2, .2), 
          bbox_transform=pl.gcf().transFigure, prop = {'size':10}, numpoints = 1)
pl.gca().add_artist(l1)
pl.savefig("./ndiff_yang_%s.eps" %save_stem, format = 'eps')
pl.close(1)

pl.figure(2)
handles, labels = ax.get_legend_handles_labels()
legend_font_props = FontProperties()
legend_font_props.set_size('small')
l1 = pl.legend(handles[0:-4:1],labels[0:-4:1], bbox_to_anchor=(0, 0,1, 1), 
          bbox_transform=pl.gcf().transFigure, prop = {'size':6})
l2 = pl.legend(handles[-4::1],labels[-4::1], bbox_to_anchor=(0, .8,.2, .2), 
          bbox_transform=pl.gcf().transFigure, prop = {'size':10}, numpoints = 1)
pl.gca().add_artist(l1)
pl.savefig("./rdiff_yang_%s.eps" %save_stem, format = 'eps')
pl.close(2)





 
