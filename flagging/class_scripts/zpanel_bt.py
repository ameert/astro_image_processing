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
              'add_param':' b.BT ',
              'normtype': 'xbin'}

names=[ plot_info[key]['label'] for key in plot_info.keys()] 
fig = pl.figure(figsize=(6,8))
pl.subplots_adjust(right = 0.92, top = 0.97, left =0.1, bottom=0.1,
                   hspace = 0.65, wspace = 0.95)

delta = 0.05
typebins = np.arange(0.0, 1.01, delta)
x_names= [str(int(a)) for a in typebins+0.5]


plot_count = 1
print "meert LG12" 
pl.subplot(5,2,plot_count)
flags_to_use = np.array([1,2,3,4,5,6])
galcount, autoflag, stype = get_vals('meert_lackner',sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1, ax2 =plot_props('B/T$_{%s}$' %sql_values['band'], props, 
                     typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names)
l = ax2.legend(loc=10, bbox_to_anchor=(1.5, 0.5), prop={'size':6})
pl.title('This Work (LG12 sample)', fontsize=8)
pl.xticks(fontsize=8)
pl.xlim(0.0,1.0)
ax1.yaxis.set_tick_params(labelsize=6)
ax2.yaxis.set_tick_params(labelsize=6)
plot_count +=1

print "meert full" 
pl.subplot(5,2,plot_count)
flags_to_use = np.array([1,2,3,4,5,6])
galcount, autoflag, stype = get_vals('meert',sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1, ax2 =plot_props('B/T$_{%s}$' %sql_values['band'], props, 
                     typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names)
pl.title('This Work (full sample)', fontsize=8)
pl.xticks(fontsize=8)
pl.xlim(0.0,1.0)
ax1.yaxis.set_tick_params(labelsize=6)
ax2.yaxis.set_tick_params(labelsize=6)
plot_count +=1


if band in 'gr':
    print "simard LG12" 
    pl.subplot(5,2,plot_count)
    flags_to_use = np.array([11,12,13,14])
    galcount, autoflag, stype = get_vals('simard_lackner',sql_values, cursor)
    props = get_flag_props(flags_to_use, autoflag, stype,typebins)
    props['datamask'] = np.where(np.array(props['total'])>0,True,False)
    props = flag_norm(flags_to_use, props, sql_values['normtype'])
    ax1, ax2 =plot_props('B/T$_{%s}$' %sql_values['band'], props, 
                         typebins, delta, flags_to_use,plot_info)
    #pl.xticks(typebins+0.5, x_names)
    l = ax2.legend(loc=10, bbox_to_anchor=(1.5, 0.5), prop={'size':6})
    pl.title('S11 (LG12 sample)', fontsize=8)
    pl.xticks(fontsize=8)
    pl.xlim(0.0,1.0)
    ax1.yaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)
    plot_count +=1

    print "simard full" 
    pl.subplot(5,2,plot_count)
    flags_to_use = np.array([11,12,13,14])
    galcount, autoflag, stype = get_vals('simard',sql_values, cursor)
    props = get_flag_props(flags_to_use, autoflag, stype,typebins)
    props['datamask'] = np.where(np.array(props['total'])>0,True,False)
    props = flag_norm(flags_to_use, props, sql_values['normtype'])
    ax1, ax2 =plot_props('B/T$_{%s}$' %sql_values['band'], props, 
                         typebins, delta, flags_to_use,plot_info)
    #pl.xticks(typebins+0.5, x_names)
    pl.title('S11 (full sample)', fontsize=8)
    pl.xticks(fontsize=8)
    pl.xlim(0.0,1.0)
    ax1.yaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)
    plot_count +=1

    if model in ['dev','ser','devexp']:
        print "mendel lg12"  
        pl.subplot(5,2,plot_count)
        flags_to_use = np.array([15,16,17,18])
        galcount, autoflag, stype = get_vals('mendel_lackner',sql_values, cursor)
        props = get_flag_props(flags_to_use, autoflag, stype,typebins)
        props['datamask'] = np.where(np.array(props['total'])>0,True,False)
        props = flag_norm(flags_to_use, props, sql_values['normtype'])
        ax1, ax2 =plot_props('B/T$_{%s}$' %sql_values['band'], props, 
                             typebins, delta, flags_to_use,plot_info)
        #pl.xticks(typebins+0.5, x_names)
        l = ax2.legend(loc=10, bbox_to_anchor=(1.5, 0.5), prop={'size':6})
        pl.title('Men14 (LG12 sample)', fontsize=8)
        pl.xticks(fontsize=8)
        pl.xlim(0.0,1.0)
        ax1.yaxis.set_tick_params(labelsize=6)
        ax2.yaxis.set_tick_params(labelsize=6)
        plot_count +=1

        print "mendel full" 
        pl.subplot(5,2,plot_count)
        flags_to_use = np.array([15,16,17,18])
        galcount, autoflag, stype = get_vals('mendel',sql_values, cursor)
        props = get_flag_props(flags_to_use, autoflag, stype,typebins)
        props['datamask'] = np.where(np.array(props['total'])>0,True,False)
        props = flag_norm(flags_to_use, props, sql_values['normtype'])
        ax1, ax2 =plot_props('B/T$_{%s}$' %sql_values['band'], props, 
                             typebins, delta, flags_to_use,plot_info)
        #pl.xticks(typebins+0.5, x_names)
        pl.title('Men14 (full sample)', fontsize=8)
        pl.xticks(fontsize=8)
        pl.xlim(0.0,1.0)
        ax1.yaxis.set_tick_params(labelsize=6)
        ax2.yaxis.set_tick_params(labelsize=6)
        plot_count +=1


if model in ['dev','ser','devexp']:
    print "lackner" 
    pl.subplot(5,2,plot_count)
    flags_to_use = np.array([7,8,9,10,11,12])
    galcount, autoflag, stype = get_vals('lackner',sql_values, cursor)
    props = get_flag_props(flags_to_use, autoflag, stype,typebins)
    props['datamask'] = np.where(np.array(props['total'])>0,True,False)
    props = flag_norm(flags_to_use, props, sql_values['normtype'])
    ax1, ax2 =plot_props('B/T$_{%s}$' %sql_values['band'], props, 
                         typebins, delta, flags_to_use,plot_info)
    #pl.xticks(typebins+0.5, x_names)
    l = ax2.legend(loc=10, bbox_to_anchor=(1.5, 0.5), prop={'size':6})
    pl.title('LG12 (LG12 sample)', fontsize=8)
    pl.xticks(fontsize=8)
    pl.xlim(0.0,1.0)
    ax1.yaxis.set_tick_params(labelsize=6)
    ax2.yaxis.set_tick_params(labelsize=6)
    plot_count +=1

#pl.show()
pl.savefig('./types_dist_BT_{band}_{model}.eps'.format(band=band, model=model), bbox_inches = 'tight')
