
def get_vals(binval): 
    cmd = """select a.galcount, x.flag, a.flag, %s from Flags_catalog as a,catalog.Flags_catalog as x, M2010 as b, CAST as c, DERT as d, r_sims_serexp as f   where x.galcount = c.true_galcount and  x.band = 'r' and x.model = 'serexp' and x.ftype = 'u' and a.flag >=0 and a.band = 'r' and a.model = 'serexp' and a.ftype = 'u' and a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and a.galcount = f.galcount and a.galcount > 20000 order by a.galcount limit 1000000;""" %binval

    galcount, flags_before, flags_after, binvals = cursor.get_data(cmd)
    galcount = np.array(galcount, dtype=int)
    autoflag_before = np.array(flags_before, dtype=int)
    autoflag_after = np.array(flags_after, dtype=int)
    binvals = np.array(binvals, dtype=float)
    
    return galcount, autoflag_before, binvals


cursor = mysql_connect('simulations','pymorph','pymorph','')

band = 'r'
model = 'serexp'

flags_to_use = [1,4,10,14,20]

plot_info = {1:{'color':'r', 'label':'bulges', 'ms':3},
             4:{'color':'b', 'label':'disks', 'ms':3},
             10:{'color':'g', 'label':'2com', 'ms':3},
             14:{'color':'y', 'label':'bad 2com', 'ms':3},
             20:{'color':'k', 'label':'bad', 'ms':3},
             'total': {'color':"#D0D0D0",'label':'total'}
             }

fig = pl.figure(figsize=(8,6))
pl.subplots_adjust(right = 0.85, left =0.1, hspace = 0.5, wspace = 0.75)


print "appmag" 
pl.subplot(3,2,1)

delta = 0.25
magbins = np.arange(13.25, 18.76, delta)
galcount, autoflag, mag = get_vals("f.m_tot")
props = get_flag_props(flags_to_use, autoflag, mag, magbins)
plot_props('m$_r$', props, magbins, delta, flags_to_use,plot_info)


print "apprad" 
pl.subplot(3,2,3)

delta = 0.5
radbins = np.arange(0.0, 8.0, delta)
galcount, autoflag, rad = get_vals("f.Hrad_corr")
props = get_flag_props(flags_to_use, autoflag, rad, radbins)
plot_props('r$_{hl, arcsec}$', props, radbins, delta, flags_to_use,plot_info)

print "z" 
pl.subplot(3,2,5)

delta = 0.025
zbins = np.arange(0.0, 0.3, delta)
galcount, autoflag, z = get_vals("c.z")
props = get_flag_props(flags_to_use, autoflag, z, zbins)
plot_props('z', props, zbins, delta, flags_to_use,plot_info)

print "absmag" 
pl.subplot(3,2,2)

delta = 0.5
magbins = np.arange(-25.0, -17.0, delta)
galcount, autoflag, mag = get_vals("f.m_tot-d.dismod-d.kcorr_r-c.extinction_r")
props = get_flag_props(flags_to_use, autoflag, mag, magbins)
plot_props('M$_r$', props, magbins, delta, flags_to_use,plot_info)


print "ABSrad" 
pl.subplot(3,2,4)

delta = 2.5
radbins = np.arange(0.0, 20.01, delta)
galcount, autoflag, rad = get_vals("f.Hrad_corr*d.kpc_per_arcsec")
props = get_flag_props(flags_to_use, autoflag, rad, radbins)
ax1, ax2 = plot_props('R$_{hl, kpc}$', props, radbins, delta, flags_to_use,plot_info)

l = ax2.legend(loc='center', bbox_to_anchor=(0.5, -1.05))


#pl.show()
pl.savefig('./dist_obs_simulation.eps')

