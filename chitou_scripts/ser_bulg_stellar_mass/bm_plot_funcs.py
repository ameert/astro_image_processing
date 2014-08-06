import sys
import os
import numpy as np
import bin_stats as bs
import pylab as pl
from MatplotRc import *
from mysql_class import *

def extract_data():
    dba = 'catalog'
    usr = 'pymorph'
    pwd = 'pymorph'

    cursor = mysql_connect(dba, usr, pwd, '')

    data = cursor.get_data("""select 
    a.galcount, a.SDSSLOGMSTAR, a.ABSMAGTOT,  b.bt as bt_serexp, 
    b.m_bulge - c.extinction_r - d.kcorr_r - d.dismod as mbulge_serexp,  
    b.n_bulge as n_serexp, 
    IFNULL(b.r_bulge*d.kpc_per_arcsec*sqrt(b.ba_bulge),-999) as rbulge_serexp, 
    u.flag as f_serexp, 
    z.bt as bt_ser, 
    z.m_bulge - c.extinction_r - d.kcorr_r - d.dismod as mbulge_ser,  
    z.n_bulge as n_ser, 
    IFNULL(z.r_bulge*d.kpc_per_arcsec*sqrt(z.ba_bulge),-999) as rbulge_ser, 
    x.flag as f_ser,  
    -6.0*m.probaEll -3.0*m.probaS0+4.0*m.probaSab+8.0*m.probaScd as ttype 
    from 
    M2010 as m, Flags_optimize as u, Flags_optimize as x, SSDR6 as a, 
    CAST as c, DERT as d, r_band_serexp as b, r_band_ser as z 
    where 
    c.galcount = m.galcount and c.galcount = z.galcount and
    a.galcount = c.galcount and c.galcount = b.galcount and 
    c.galcount = d.galcount and c.galcount = u.galcount and 
    u.ftype = 'u' and u.band = 'r' and u.model = 'serexp' and u.flag>=0 and 
    c.galcount = x.galcount and x.ftype = 'u' and x.band = 'r' and 
    x.model = 'ser' and x.flag>=0 
    order by a.galcount """)

    colnames = ['galcount', 'SDSSLOGMSTAR', 'ABSMAGTOT',  'bt_serexp', 
                'mbulge_serexp', 'n_serexp', 'rbulge_serexp', 'f_serexp', 'bt_ser', 
                'mbulge_ser', 'n_ser', 'rbulge_ser', 'f_ser', 'ttype'] 

    data = dict([(a[0], np.array(a[1])) for a in zip(colnames, data)])

    isdisk = np.where(data['f_serexp']&2**4>0,1,0)
    isbulge  =np.where(data['f_serexp']&2**1>0,1,0)
    badserexp =np.where(data['f_serexp']&2**13>0,1,0)|np.where(data['f_serexp']&2**14>0,1,0)|np.where(data['f_serexp']&2**19>0,1,0)
    istwocom = np.where(data['f_serexp']&2**11>0,1,0)|np.where(data['f_serexp']&2**12>0,1,0)
    goodser =np.where(data['f_ser']&2**19==0,1,0)

    Mstar = 10**data['SDSSLOGMSTAR']
    data['mbulge_serexp'] = np.log10(Mstar * 10**(-0.4*(data['mbulge_serexp']- data['ABSMAGTOT'])))
    data['mbulge_ser'] = np.log10(Mstar * 10**(-0.4*(data['mbulge_ser']- data['ABSMAGTOT'])))

    sel_ser = (isdisk+isbulge)*goodser
    mbulge = data['mbulge_serexp']*istwocom +data['mbulge_ser']*sel_ser
    rbulge = data['rbulge_serexp']*istwocom +data['rbulge_ser']*sel_ser
    nbulge = data['n_serexp']*istwocom +data['n_ser']*sel_ser
    BT = data['bt_serexp']*istwocom +1.0*goodser*isbulge+0.01*goodser*isdisk
    ttype = data['ttype']
    galcount = data['galcount']

    log_Mstar_bulge = np.extract((istwocom|sel_ser)>0,mbulge)
    r_bulge = np.extract((istwocom|sel_ser)>0,rbulge)
    n_bulge = np.extract((istwocom|sel_ser)>0,nbulge)
    BT = np.extract((istwocom|sel_ser)>0,BT)
    ttype = np.extract((istwocom|sel_ser)>0,ttype)
    galcount = np.extract((istwocom|sel_ser)>0,galcount)
    sel_ser = np.extract((istwocom|sel_ser)>0,sel_ser) 

    return log_Mstar_bulge, r_bulge, n_bulge, BT, ttype, sel_ser, galcount




def plot_figs(log_Mstar_bulge,n_bulge, BT,  r_bulge_cir, plotstart, 
              fig, nrow_plots, ncol_plots, title=''):
    xmaj = 1.0
    xstr = "%d"
    xmin = 0.25
   
    ax = fig.add_subplot(nrow_plots,ncol_plots,plotstart)
    data_holder = pub_plots(xmaj, xmin, xstr, 2.0, 0.5, '%d')
    ndata = bs.bin_stats(log_Mstar_bulge, n_bulge, np.arange(9,12,.5), 0.0, 8.0)
    ndata.plot_ebar('median', 'med95ci', ecolor='r', linestyle = 'none', ms=3, marker='o')
    ndata.lay_bounds(sigma_choice = [68,95])
    pl.ylim(0.0, 9.0)
    pl.xlim(9.0, 12.0)
    pl.xlabel('$log(M_{star})$')
    pl.ylabel('n$_{r}$')
    pl.title(title)
    pl.text(0.9, 0.1,str(np.sum(ndata.bin_number)), horizontalalignment='right',
         verticalalignment='center',transform=ax.transAxes)
    data_holder.set_plot(ax)

    ax = fig.add_subplot(nrow_plots,ncol_plots,plotstart+1)
    data_holder = pub_plots(xmaj, xmin, xstr, 0.2, 0.05, '%0.1f')
    ndata = bs.bin_stats(log_Mstar_bulge, BT, np.arange(9,12,.5), 0.0, 8.0)
    ndata.plot_ebar('median', 'med95ci', ecolor='r', linestyle = 'none', ms=3, marker='o')
    ndata.lay_bounds(sigma_choice = [68,95])
    pl.ylim(0.0, 1.0)
    pl.xlim(9.0, 12.0)
    pl.xlabel('$log(M_{star})$')
    pl.ylabel('BT')
    pl.title(title)
    pl.text(0.9, 0.1,str(np.sum(ndata.bin_number)), horizontalalignment='right',
         verticalalignment='center',transform=ax.transAxes)
    data_holder.set_plot(ax)

    ax = fig.add_subplot(nrow_plots,ncol_plots,plotstart+2)
    data_holder = pub_plots(xmaj, xmin, xstr, 0.5, 0.1, '%0.1f')
    
    ndata = bs.bin_stats(log_Mstar_bulge, r_bulge_cir, np.arange(9,12,.5), 0.0, 100.0)
    ndata.to_log(1)
    #raw_input()
    ndata.plot_ebar('median', 'med95ci', ecolor='r', linestyle = 'none', ms=3, marker='o')
    ndata.lay_bounds(sigma_choice = [68,95])
    ax = pl.gca()
    #ax.set_yscale('log')
    #pl.ylim(0.5, 20.0)
    pl.ylim(-1, 2.0)
    pl.xlim(9.0, 12.0)
    pl.xlabel('$log(M_{star})$')
    pl.ylabel('logR$_{cir}$ [kpc]')
    pl.title(title)
    pl.text(0.9, 0.1,str(np.sum(ndata.bin_number)), horizontalalignment='right',
         verticalalignment='center',transform=ax.transAxes)
    data_holder.set_plot(ax)

    return

def get_data(selection, array_list):
    new_arr_list = []
    for a  in array_list:
        new_arr_list.append(np.where(selection==1, a, np.nan))
    return new_arr_list

