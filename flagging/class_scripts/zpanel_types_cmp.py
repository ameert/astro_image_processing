from astro_image_processing.mysql import *
import numpy as np
import pylab as pl
import matplotlib
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
from zpanel_functions import *

cursor = mysql_connect('catalog','pymorph','pymorph','')

band = 'r'
model = 'devexp'
sql_values = {'band':band, 
              'model':model, 'galnumlim':10000000,
              'add_param':' -4.5775*m.probaEll -2.35723*m.probaS0+2.48028*m.probaSab+6.0815*m.probaScd',
              'normtype': 'xbin'}
    

names=[ plot_info[key]['label'] for key in plot_info.keys()] 
matplotlib.rc('xtick', labelsize=8)
fig = pl.figure(figsize=(6,8))
pl.subplots_adjust(right = 0.92, top = 0.97, left =0.1, bottom=0.1,
                   hspace = 0.65, wspace = 0.95)

delta = 1.0
typebins = np.arange(-6.5, 12.51, delta)
x_names= [str(int(a)) for a in typebins+0.5]
x_names = [ x_names[a] if a%2 ==0 else "" for a in range(len(x_names))] 


print "meert" 
pl.subplot(5,2,1)
flags_to_use = np.array([1,2,3,4,5,6])
galcount, autoflag, stype = get_vals('meert_lackner',sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1,ax2 =plot_props('T', props, typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('This Work (LG12 sample)', fontsize=8)
pl.xticks(rotation=90)
l = ax2.legend(loc=10, bbox_to_anchor=(1.5, 0.5), prop={'size':6})
pl.xlim(-6,7)
ax1.yaxis.set_tick_params(labelsize=6)
ax2.yaxis.set_tick_params(labelsize=6)

print "simard" 
pl.subplot(5,2,3)
flags_to_use = np.array([11,12,13,14])
galcount, autoflag, stype= get_vals('simard_lackner',sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1,ax2 =plot_props('T', props, typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('S11 (LG12 sample)', fontsize=8)
l = ax2.legend(loc=10, bbox_to_anchor=(1.5, 0.5), prop={'size':6})
#pl.xticks(rotation=90)
pl.xlim(-6,7)
ax1.yaxis.set_tick_params(labelsize=6)
ax2.yaxis.set_tick_params(labelsize=6)

print "mendel" 
pl.subplot(5,2,5)
flags_to_use = np.array([15,16,17,18])
galcount, autoflag, stype = get_vals('mendel_lackner',sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1,ax2 =plot_props('T', props, typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('Men14 (LG12 sample)', fontsize=8)
l = ax2.legend(loc=10, bbox_to_anchor=(1.5, 0.5), prop={'size':6})
#pl.xticks(rotation=90)
pl.xlim(-6,7)
ax1.yaxis.set_tick_params(labelsize=6)
ax2.yaxis.set_tick_params(labelsize=6)

print "lackner" 
pl.subplot(5,2,7)
flags_to_use = np.array([7,8,9,10,11,12])
galcount, autoflag, stype = get_vals('lackner',sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1,ax2 =plot_props('T', props, typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('LG12 (LG12 sample)', fontsize=8)
l = ax2.legend(loc=10, bbox_to_anchor=(1.5, 0.5), prop={'size':6})
#pl.xticks(rotation=90)
pl.xlim(-6,7)
ax1.yaxis.set_tick_params(labelsize=6)
ax2.yaxis.set_tick_params(labelsize=6)


print "meert" 
pl.subplot(5,2,2)
flags_to_use = np.array([1,2,3,4,5,6])
galcount, autoflag, stype = get_vals('meert',sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1,ax2 =plot_props('T', props, typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('This Work (full sample)', fontsize=8)
pl.xticks(rotation=90)
#l = ax2.legend(loc=2, bbox_to_anchor=(1.025, 0.00), prop={'size':6})
pl.xlim(-6,7)
ax1.yaxis.set_tick_params(labelsize=6)
ax2.yaxis.set_tick_params(labelsize=6)

print "simard" 
pl.subplot(5,2,4)
flags_to_use = np.array([11,12,13,14])
galcount, autoflag, stype = get_vals('simard',sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1,ax2 =plot_props('T', props, typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('S11 (full sample)', fontsize=8)
#l = ax2.legend(loc=2, bbox_to_anchor=(1.025, 0.00), prop={'size':6})
#pl.xticks(rotation=90)
pl.xlim(-6,7)
ax1.yaxis.set_tick_params(labelsize=6)
ax2.yaxis.set_tick_params(labelsize=6)

print "mendel" 
pl.subplot(5,2,6)
flags_to_use = np.array([15,16,17,18])
galcount, autoflag, stype = get_vals('mendel',sql_values, cursor)
props = get_flag_props(flags_to_use, autoflag, stype,typebins)
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
props = flag_norm(flags_to_use, props, sql_values['normtype'])
ax1,ax2 =plot_props('T', props, typebins, delta, flags_to_use,plot_info)
#pl.xticks(typebins+0.5, x_names, fontsize = 8)
pl.title('Men14 (full sample)', fontsize=8)
#l = ax2.legend(loc=2, bbox_to_anchor=(1.025, 0.00), prop={'size':6})
#pl.xticks(rotation=90)
pl.xlim(-6,7)
ax1.yaxis.set_tick_params(labelsize=6)
ax2.yaxis.set_tick_params(labelsize=6)


#print props.keys()
#print props[12]
#print props[10]
#print np.array(props[12])/np.array(props[10])

#pl.show()
pl.savefig('./types_dist_{band}_{model}.eps'.format(band=band, model = model) ,
           bbox_inches = 'tight')

