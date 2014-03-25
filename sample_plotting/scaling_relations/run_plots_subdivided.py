from mysql_class import *
import os
import sys
from utilities import *
from faber_jackson import *
import pylab as pl

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

fig = pl.figure(figsize=(10,10), frameon = True)
fig.subplots_adjust(left = 0.12, 
                    right = 0.97,   
                    bottom = 0.08,  
                    top = 0.95,     
                    wspace = 0.3,  
                    hspace = 0.3)  
count = 0
for n_max in np.arange(0, 8.01,2.0)[1:]:
    count +=1
    fig.add_subplot(2,2,count)

    cmd = 'select a.galcount, d.veldisp, d.veldispErr, abs(a.Ie)-a.dis_modu-a.magzp-d.aa_r -d.kk_r*d.airmass_r - b.kcorr_r, a.Ie_err, a.n from full_dr7_r_ser as a , DERT as b , M2010 as c , CAST as d where a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and c.ProbaE > 0.75 and d.veldisp < 400.0 and abs(a.Ie) < 100 and d.veldisp > -1 and b.kcorr_r > -900 and a.n > %f and a.n <= %f order by a.galcount;' %(n_max - 2.0, n_max)

    galcount, veldisp, veldispErr, Absmag, magErr, nser = cursor.get_data(cmd)

    galcount = np.array(galcount)
    veldisp = np.array(veldisp)
    veldispErr = np.array(veldispErr)
    Absmag = np.array(Absmag)
    magErr = np.array(magErr)
    nser = np.array(nser)

    Lgal, Lerr = absmag_to_LSun(Absmag,magErr, 'r')

    faber_jackson(veldisp, veldispErr, Lgal, Lerr, nser)
    ax = pl.gca()
    pl.text(0.65, 0.92, '%2.1f < n <= %2.1f' %(n_max-2.0, n_max),fontsize = 10, transform = ax.transAxes )

pl.savefig('/home/ameert/faber_jackson.eps')
