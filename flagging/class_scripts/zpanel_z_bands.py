from astro_image_processing.mysql import *
import numpy as np
import pylab as pl
import matplotlib
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
from zpanel_functions import *

cursor = mysql_connect('catalog','pymorph','pymorph','')

band = 'r'
model = 'serexp'
sql_values = {'band':band, 
              'model':model, 'galnumlim':10000000,
              'add_param':' r.z '.format(band=band),
              'normtype': 'xbin'}

#names=[ plot_info[key]['label'] for key in plot_info.keys()] 
matplotlib.rc('xtick', labelsize=8)
fig = pl.figure(figsize=(6,8))
pl.subplots_adjust(right = 0.92, top = 0.97, left =0.1, bottom=0.1,
                   hspace = 0.65, wspace = 0.95)


delta = 0.02
delta_lg12 = delta/5.0
typebins = np.arange(0.0, 0.305, delta)
typebins_lg12 = np.arange(0.0, 0.305, delta_lg12)


plot_count = 1

for band in 'gri':
    sql_values['band'] = band
    sql_values['add_param']=' r.z '.format(band=band)
    print '{band} band'.format(**sql_values)
    print "LG12" 
    pl.subplot(5,2,plot_count)
    flags_to_use = np.array([1,2,3,4,5,6])
    galcount, autoflag, stype = get_vals('meert_lackner',sql_values, cursor)
    props = get_flag_props(flags_to_use, autoflag, stype,typebins_lg12)
    props['datamask'] = np.where(np.array(props['total'])>0,True,False)
    props = flag_norm(flags_to_use, props, sql_values['normtype'])
    ax1, ax2 =plot_props('z', props, typebins_lg12, delta_lg12, flags_to_use,plot_info)
    #pl.xticks(typebins_lg12+0.5, x_names, fontsize = 8)
    pl.title('{model} {band}-band (LG12 sample)'.format(**sql_values), 
             fontsize=8)
    pl.xticks(fontsize=8)
    l = ax2.legend(loc=10, bbox_to_anchor=(1.5, 0.5), prop={'size':6})
    pl.xlim(0.0,0.055)
    ax1.yaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)
    plot_count+=1

    print "Full" 
    pl.subplot(5,2,plot_count)
    flags_to_use = np.array([1,2,3,4,5,6])
    galcount, autoflag, stype = get_vals('meert',sql_values, cursor)
    props = get_flag_props(flags_to_use, autoflag, stype,typebins)
    props['datamask'] = np.where(np.array(props['total'])>0,True,False)
    props = flag_norm(flags_to_use, props, sql_values['normtype'])
    ax1, ax2 =plot_props('z' , props, typebins, delta, flags_to_use,plot_info)
    #pl.xticks(typebins+0.5, x_names)
    pl.title('{model} {band}-band (full sample)'.format(**sql_values), 
             fontsize=8)
    pl.xticks(fontsize=8)
    #l = ax2.legend(loc=2, bbox_to_anchor=(1.01, 0.1), prop={'size':6})
    pl.xlim(0.0,0.3)
    ax1.yaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)
    plot_count +=1


pl.savefig('./types_dist_z_gri_{model}.eps'.format(model=model), 
           bbox_inches = 'tight')
#pl.show()
