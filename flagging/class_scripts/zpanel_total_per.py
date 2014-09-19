
def get_vals(binval): 
#    cmd = """select a.galcount, a.flag, %s from Flags_catalog as a, M2010 as b, CAST as c, DERT as d, r_band_serexp as f, SSDR6 as z   where a.flag >=0 and a.band = 'r' and a.model = 'serexp' and a.ftype = 'u' and a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and a.galcount = f.galcount and a.galcount = z.galcount order by a.galcount limit 1000000;""" %binval

    cmd = """select a.galcount, IF(a.flag&pow(2,10)>0, IF(f.n_bulge>7.95, a.flag^(pow(2,10)+pow(2,27)),a.flag),a.flag) as flag , {binval} from Flags_catalog as a, M2010 as b, CAST as c, DERT as d, {band}_band_{model} as f where a.flag >=0 and a.band = '{band}' and a.model = '{model}' and a.ftype = 'u' and a.galcount = b.galcount and a.galcount = c.galcount and a.galcount = d.galcount and a.galcount = f.galcount order by a.galcount limit 1000000;""".format(binval=binval, model=model, band=band)

    print cmd
    galcount, flags, binvals = cursor.get_data(cmd)
    galcount = np.array(galcount, dtype=int)
    autoflag = np.array(flags, dtype=int)
    binvals = np.array(binvals, dtype=float)
    
    return galcount, autoflag, binvals

cursor = mysql_connect('catalog','pymorph','pymorph','')

band = 'r'
model = 'serexp'

flags_to_use = [1,4,10,27,14,20]

plot_info = {1:{'color':'r', 'label':'bulges', 'ms':3, 'marker':'o', 'ls':'-'},
             4:{'color':'b', 'label':'disks', 'ms':3, 'marker':'s', 'ls':'-'},
             10:{'color':'g', 'label':'2com', 'ms':3, 'marker':'d', 'ls':'-'},
             14:{'color':'y', 'label':'bad 2com', 'ms':3, 'marker':'o', 'ls':'--'},
             27:{'color':'c', 'label':'n8', 'ms':3, 'marker':'s', 'ls':'--'},
             20:{'color':'k', 'label':'bad', 'ms':3, 'marker':'d', 'ls':'--'},
             'total': {'color':"#D0D0D0",'label':'total'}
             }

fig = pl.figure(figsize=(8,6))
pl.subplots_adjust(right = 0.9, left =0.09, top=0.97, 
                   hspace = 0.5, wspace = 0.55, bottom=0.08)


print "appmag" 
pl.subplot(3,2,1)

delta = 0.25
magbins = np.arange(13.25, 18.01, delta)
#galcount, autoflag, mag = get_vals('c.petromag_r-c.extinction_r')
galcount, autoflag, mag = get_vals('f.m_tot-c.extinction_{band}'.format(band=band))
props = get_flag_props(flags_to_use, autoflag, mag, magbins)
plot_props('m$_{{ {band}, tot}}$'.format(band=band), props, 
           magbins, delta, flags_to_use,plot_info)


print "apprad" 
pl.subplot(3,2,3)

#delta = 0.1
delta = 0.5
#radbins = np.arange(-0.2, 1.51, delta)
radbins = np.arange(0.0, 10.0, delta)
#galcount, autoflag, rad = get_vals('c.petror50_r')
galcount, autoflag, rad = get_vals("f.Hrad_corr")
#rad = np.log10(rad)
props = get_flag_props(flags_to_use, autoflag, rad, radbins)
#plot_props('log$_{10}$r$_{hl, tot, arcsec}$', props, radbins, delta, flags_to_use,plot_info)
plot_props('r$_{hl, tot, arcsec}$', props, radbins, delta, flags_to_use,plot_info)
pl.xlim((0,8))

print "ba" 
pl.subplot(3,2,5)

delta = 0.05
radbins = np.arange(0.0, 1.01, delta)
#galcount, autoflag, rad = get_vals("c.petror50_r*d.kpc_per_arcsec")
galcount, autoflag, rad = get_vals("f.ba_tot_corr")
props = get_flag_props(flags_to_use, autoflag, rad, radbins)
ax1, ax2 = plot_props('b/a$_{tot}$', props, radbins, delta, flags_to_use,plot_info)

print "absmag" 
pl.subplot(3,2,2)

delta = 0.5
magbins = np.arange(-25.0, -17.0, delta)
#galcount, autoflag, mag = get_vals("c.petromag_r-d.dismod-d.kcorr_r-c.extinction_r")
galcount, autoflag, mag = get_vals("f.m_tot-d.dismod-d.kcorr_{band}-c.extinction_{band}".format(band=band))
props = get_flag_props(flags_to_use, autoflag, mag, magbins)
plot_props('M$_{{ {band}, tot}}$'.format(band=band), props, magbins, delta, flags_to_use,plot_info)


print "ABSrad" 
pl.subplot(3,2,4)

#delta = 0.1
#radbins = np.arange(-0.2, 1.51, delta)
delta = 0.5
radbins = np.arange(0, 15.1, delta)
#galcount, autoflag, rad = get_vals("c.petror50_r*d.kpc_per_arcsec")
galcount, autoflag, rad = get_vals("f.Hrad_corr*d.kpc_per_arcsec")
#rad = np.log10(rad)
props = get_flag_props(flags_to_use, autoflag, rad, radbins)
#ax1, ax2 = plot_props('log$_{10}$R$_{hl, tot, kpc}$', props, radbins, delta, flags_to_use,plot_info)
ax1, ax2 = plot_props('R$_{hl, tot, kpc}$', props, radbins, delta, flags_to_use,plot_info)
pl.xlim((0,12))
print "ABSrad" 

if 0:
    pl.subplot(3,2,7)

    delta = 0.5
    magbins = np.arange(-25.0, -17.0, delta)
    #galcount, autoflag, mag = get_vals("c.petromag_r-d.dismod-d.kcorr_r-c.extinction_r")
    galcount, autoflag, mag = get_vals("f.m_tot-d.dismod-d.kcorr_{band}-c.extinction_{band}".format(band=band))
    props = get_flag_props(flags_to_use, autoflag, mag, magbins)
    plot_inflag_prop('M$_{band}$'.format(band=band), props, magbins, delta, flags_to_use,plot_info)

    pl.subplot(3,2,6)

    delta = 2.5
    radbins = np.arange(0.0, 20.01, delta)
    #galcount, autoflag, rad = get_vals("c.petror50_r*d.kpc_per_arcsec")
    galcount, autoflag, rad = get_vals("f.Hrad_corr*d.kpc_per_arcsec")
    props = get_flag_props(flags_to_use, autoflag, rad, radbins)
    plot_inflag_prop('R$_{hl, kpc}$', props, radbins, delta, flags_to_use,plot_info)

#print "z" 
#pl.subplot(3,2,6)

#delta = 0.025
#zbins = np.arange(0.0, 0.3, delta)
#galcount, autoflag, z = get_vals("c.z")
#props = get_flag_props(flags_to_use, autoflag, z, zbins)
#plot_props('z', props, zbins, delta, flags_to_use,plot_info)


l = ax2.legend(loc='center', bbox_to_anchor=(0.5, -1.05), fontsize='10')


#pl.show()
pl.savefig('./dist_obs_total_per_%s_%s.eps' %(band,model))
#pl.savefig('./dist_obs_petro.eps')
#pl.savefig('./dist_obs_small_petro.eps')

