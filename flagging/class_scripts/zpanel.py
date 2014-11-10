from astro_image_processing.mysql import *
import numpy as np
import pylab as pl
import matplotlib
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
from zpanel_functions import *

cursor = mysql_connect('catalog','pymorph','pymorph','')

sql_values = {# Set these params
              'band':'i', 
              'model':'serexp', 
              'normtype':'flagclass',
              'galnumlim':1000000,
              #do not set this parameter! Set automatically!
              'add_param':'',
              
              }


if sql_values['normtype'] == 'xbin':
    sql_values['savename']='./dist_obs_{band}_{model}.eps'.format(**sql_values)
elif sql_values['normtype'] == 'flagclass':
    sql_values['savename']='./dist_obs_class_per_{band}_{model}.eps'.format(**sql_values)
elif sql_values['normtype'] == 'total':
    sql_values['savename']='./dist_obs_total_per_{band}_{model}.eps'.format(**sql_values)
    
flags_to_use = [1,2,3,4,5,6]

fig = pl.figure(figsize=(8,6.5))
pl.subplots_adjust(right = 0.92, left =0.08, top=0.97, 
                   hspace = 0.5, wspace = 0.5, bottom=0.17)

print "appmag" 
sql_values['add_param'] = ' b.m_tot-r.extinction_{band}'.format(**sql_values)
pl.subplot(3,2,1)
delta = 0.25
magbins = np.arange(13.25, 20.01, delta)
galcount, autoflag, mag = get_vals('meert', sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, mag, magbins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1, ax2 = plot_props('m$_{{ {band}, tot}}$'.format(**sql_values), props, magbins, delta, flags_to_use,plot_info)
ax2.set_ylim(plot_info.get('ylims',{}).get(sql_values['normtype'],{}).get('mtot',(0.0,1.0)))
if sql_values['band']=='g':
    ax2.set_xlim((14.25,20.0))
    ax1.set_xlim((14.25,20.0))
if sql_values['band']=='r':
    ax2.set_xlim((13.0,18.0))
    ax1.set_xlim((13.0,18.0))
if sql_values['band']=='i':
    ax2.set_xlim((13.0,18.0))
    ax1.set_xlim((13.0,18.0))
ax1.tick_params(axis='y', labelsize=10)
ax2.tick_params(axis='y', labelsize=10)

print "apprad" 
sql_values['add_param'] = ' b.Hrad_corr'
pl.subplot(3,2,3)
delta = 0.5
radbins = np.arange(0.0, 10.0, delta)
galcount, autoflag, rad = get_vals('meert', sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, rad, radbins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1, ax2 = plot_props('r$_{hl, tot, arcsec}$', props, radbins, delta, flags_to_use,plot_info)
pl.xlim((0,8))
ax2.set_ylim(plot_info.get('ylims',{}).get(sql_values['normtype'],{}).get('rad',(0.0,1.0)))
ax1.tick_params(axis='y', labelsize=10)
ax2.tick_params(axis='y', labelsize=10)

print "ba" 
sql_values['add_param'] = ' b.ba_tot_corr'
pl.subplot(3,2,5)
delta = 0.05
radbins = np.arange(0.0, 1.01, delta)
galcount, autoflag, rad = get_vals('meert', sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, rad, radbins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1, ax2 = plot_props('b/a$_{tot}$', props, radbins, delta, flags_to_use,plot_info)
pl.xlim((0,1))
ax2.set_ylim(plot_info.get('ylims',{}).get(sql_values['normtype'],{}).get('ba',(0.0,1.0)))
ax1.tick_params(axis='y', labelsize=10)
ax2.tick_params(axis='y', labelsize=10)

print "absmag" 
sql_values['add_param'] = " b.m_tot-s.dismod-s.kcorr_{band}-r.extinction_{band}".format(**sql_values)
pl.subplot(3,2,2)

delta = 0.5
magbins = np.arange(-25.0, -17.0, delta)
galcount, autoflag, mag = get_vals('meert', sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, mag, magbins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1, ax2 = plot_props('M$_{{ {band}, tot}}$'.format(**sql_values), 
                      props, magbins, delta, flags_to_use,plot_info)
ax2.set_ylim(plot_info.get('ylims',{}).get(sql_values['normtype'],{}).get('absmtot',(0.0,1.0)))
ax1.tick_params(axis='y', labelsize=10)
ax2.tick_params(axis='y', labelsize=10)

print "ABSrad" 
sql_values['add_param'] = "b.Hrad_corr*s.kpc_per_arcsec"
pl.subplot(3,2,4)

delta = 0.5
radbins = np.arange(0, 15.1, delta)
galcount, autoflag, rad = get_vals('meert', sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, rad, radbins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1, ax2 = plot_props('R$_{hl, tot, kpc}$', 
                      props, radbins, delta, flags_to_use,plot_info)
pl.xlim((0,12))
ax2.set_ylim(plot_info.get('ylims',{}).get(sql_values['normtype'],{}).get('absrad',(0.0,1.0)))
ax1.tick_params(axis='y', labelsize=10)
ax2.tick_params(axis='y', labelsize=10)

print "nbulge" 
sql_values['add_param'] = "b.n_bulge"
pl.subplot(3,2,6)

delta = 0.4
radbins = np.arange(0, 8.01, delta)
galcount, autoflag, rad = get_vals('meert', sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, rad, radbins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1, ax2 = plot_props('n$_{bulge}$', 
                      props, radbins, delta, flags_to_use,plot_info)
pl.xlim((0,8))
ax2.set_ylim(plot_info.get('ylims',{}).get(sql_values['normtype'],{}).get('nbulge',(0.0,1.0)))
ax1.tick_params(axis='y', labelsize=10)
ax2.tick_params(axis='y', labelsize=10)

l = ax2.legend(loc='center', bbox_to_anchor=(-0.75, -0.6, 1.0, 0.1), fontsize='10', ncol = 3)
#l = ax2.legend(loc='center', bbox_to_anchor=(0.5, -1.05), fontsize='10')
#pl.show()
pl.savefig(sql_values['savename'])

