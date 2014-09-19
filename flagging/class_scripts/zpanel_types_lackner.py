from mysql_class import *
from flag_defs import *
import pylab as pl
import matplotlib.ticker as mticker
import scikits.bootstrap as bootstrap  


cursor = mysql_connect('catalog','pymorph','pymorph','')

band = 'r'
model = 'serexp'
choice = 'full'
flags_to_use = np.array([1,2,3,4,5,6])

plot_info = {1:{'color':'r', 'label':'bulges', 'ms':3},
             2:{'color':'b', 'label':'disks', 'ms':3},
             3:{'color':'g', 'label':'2com', 'ms':3},
             4:{'color':'y', 'label':'bad 2com', 'ms':3},
             5:{'color':'k', 'label':'bad', 'ms':3},
             6:{'color':'c', 'label':'2nh', 'ms':3},
             'total': {'color':"#D0D0D0",'label':'total'}
             }

names=[ plot_info[key]['label'] for key in plot_info.keys()] 
fig = pl.figure(figsize=(6,6))
pl.subplots_adjust(right = 0.95, left =0.1, hspace = 0.5, wspace = 0.75)

typebins = np.arange(-6.5, 12.51, 1.0)

print "meert" 
pl.subplot(1,1,1)

galcount, autoflag, stype = get_vals()

nair_typebins = typebins
nair_names= [str(a) for a in typebins]
props = get_flag_props(flags_to_use, autoflag, stype,nair_typebins)
print props['total']
props['datamask'] = np.where(np.array(props['total'])>0,True,False)
print props.keys()
print props
ax2 =plot_props('T', props, nair_typebins, flags_to_use,plot_info)
#pl.xticks(np.arange(len(nair_names))-3, nair_names, fontsize = 8)
pl.title('Meert types by TType')
#pl.xticks(rotation=90)
pl.xlim(-6,12.5)
l = ax2.legend(loc='center', bbox_to_anchor=(-1.5, 0.5))


#pl.show()
if choice =='nair_marc':
    pl.savefig('./types_dist_nair_marc.eps')
elif choice =='nair':
    pl.savefig('./types_dist_nair.eps')
elif choice =='full':
    pl.savefig('./types_dist_full.eps')

