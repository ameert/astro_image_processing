from astro_image_processing.mysql import *
import numpy as np
import pylab as pl
import matplotlib
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
from zpanel_functions import *

cursor = mysql_connect('catalog','pymorph','pymorph','')

sql_values = {# Set these params
              'band':'r', 
              'model':'serexp', 
              'normtype':'xbin',
              'galnumlim':10000000,
              #do not set this parameter! Set automatically!
              'add_param':'',
              }

sql_values['savename']='./ntypes_obs_{band}_{model}.eps'.format(**sql_values)
    
flags_to_use = [1,2,3,4,5,6]

fig = pl.figure(figsize=(8,6))
pl.subplots_adjust(right = 0.92, left =0.08, top=0.97, 
                   hspace = 0.5, wspace = 0.5, bottom=0.08)

print "nbulge" 
sql_values['add_param'] = ' b.n_bulge'.format(**sql_values)
sql_values['normtype'] = 'xbin'
pl.subplot(3,2,1)
delta = 0.25
magbins = np.arange(0.0, 8.01, delta)
galcount, autoflag, mag = get_vals('meert', sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, mag, magbins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1, ax2 = plot_props('n$_{{ {band}, bulge}}$'.format(**sql_values), props, magbins, delta, flags_to_use,plot_info)
ax2.set_ylim(plot_info.get('ylims',{}).get(sql_values['normtype'],{}).get('blah',(0.0,1.0)))

print "nbulge" 
pl.subplot(3,2,2)
sql_values['normtype'] = 'flagclass'
delta = 0.25
magbins = np.arange(0.0, 8.01, delta)
galcount, autoflag, mag = get_vals('meert', sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, mag, magbins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1, ax2 = plot_props('n$_{{ {band}, bulge}}$'.format(**sql_values), props, magbins, delta, flags_to_use,plot_info)
ax2.set_ylim(plot_info.get('ylims',{}).get(sql_values['normtype'],{}).get('blah',(0.0,1.0)))



l = ax2.legend(loc='center', bbox_to_anchor=(0.5, -1.05), fontsize='10')
#pl.show()
pl.savefig(sql_values['savename'])

