from mysql_class import *
import os
import sys

from utilities import *
from faber_jackson import *
from kormendy import *
from fund_plane import *
from photo_fund_plane import *
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
for BT_max in np.arange(0, 1.01,0.25)[1:]:
    count +=1
    fig.add_subplot(2,2,count)

    cmd = 'select a.galcount, d.veldisp, d.veldispErr, abs(a.Ie)-a.dis_modu-a.magzp-d.aa_r -d.kk_r*d.airmass_r - b.kcorr_r, a.Ie_err, a.n, a.n_err, a.re_kpc, a.re_kpc_err, a.BT from full_dr7_r_serexp as a , DERT as b , M2010 as c , CAST as d where a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and c.ProbaEll > 0.75 and d.veldisp < 400.0 and abs(a.Ie) < 100 and d.veldisp > -1 and b.kcorr_r > -900 and a.BT > %f and a.BT <= %f order by a.galcount;' %(BT_max - 0.250, BT_max)  

    galcount, veldisp, veldispErr, Absmag, magErr, nser, nser_err, Rkpc, Rkpc_err, BT = cursor.get_data(cmd)

    galcount = np.array(galcount)
    veldisp = np.array(veldisp)
    veldispErr = np.array(veldispErr)
    Absmag = np.array(Absmag)
    magErr = np.array(magErr)
    nser = np.array(nser)
    nser_err = np.array(nser_err)
    Rkpc = np.array(Rkpc)
    Rkpc_err = np.array(Rkpc_err)
    BT = np.array(BT)

    Lgal, Lerr = absmag_to_LSun(Absmag,magErr, 'r')

    ax = photo_fund_plane(Rkpc, Rkpc_err, nser, nser_err, Lgal, Lerr, BT)
    pl.text(0.65, 0.92, '%2.1f < B/T <= %2.1f' %(BT_max-2.0, BT_max),fontsize = 10, transform = ax.transAxes )

pl.savefig('/home/ameert/pf_plane.eps')
