import pylab as pl
import numpy as np
from mysql_class import *
from bin_stats import *
from MatplotRc import *

dba = 'catalog'
usr = 'ameert'
pwd = 'al130568'

cursor = mysql_connect(dba, usr, pwd)

size = get_fig_size()
size[0] *=1
size[1] *=1 
fig = pl.figure(figsize=size, frameon=True)
ticks = pub_plots(xmaj = 10,xmin=5,xstr= '%d',ymaj = 2,ymin = 0.5,ystr='%d')
pl.subplots_adjust(left = 0.2, right = 0.95, bottom = 0.35,                           top = 0.87, wspace = 0.15, hspace = 0.15) 

cmd = "select a.galcount, a.n, b.n, c.n, m.probaEll, m.probaS0, m.probaSab, m.probaScd, d.logMstar, z.Ngals from full_dr7_g_ser as a,full_dr7_r_ser as b,full_dr7_i_ser as c, M2010 as m, DERT as d, maxBCG_members.members as z where a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and a.galcount = m.galcount and z.galcount = a.galcount;"

data = cursor.get_data(cmd)

gals = {}
for d, dname in zip(data, ['galcount','n_g', 'n_r', 'n_i', 'PEll','PS0',
                           'PSab','PScd','logMstar', 'Ngals']):
    gals[dname] = np.array(d)

a = bin_stats(gals['Ngals'],gals['n_r'],
              np.arange(0,101.0,10.0), 0.5,7.9, weight = [1], 
              err_type = 'median')
a.plot_ebar('median', '68n', marker = 'o',color = 'g', ms = 4, 
            markerfacecolor = 'g',  ecolor = 'g', capsize = 5, 
            linestyle = '-', elinewidth = 2, barsabove=True, zorder = 10)

ax = fig.gca()
ax.set_aspect('auto')
ticks.set_plot(ax)
pl.xlabel('Richness')
pl.ylabel('n$_r$')
pl.xlim((0,70))
pl.ylim((0,6))

pl.savefig("./nr_richness.eps", format = 'eps')
pl.close(fig)


pl.hist(gals['Ngals'])
pl.savefig("./rich_hist.eps")




 
