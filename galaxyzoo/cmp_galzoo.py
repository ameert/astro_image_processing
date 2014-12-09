from astro_image_processing.mysql import *
import numpy as np
import pylab as pl

def flag_sep(flag):
    counts = np.array([np.sum(np.where(flag&2**1>0,1,0)),
                      np.sum(np.where(flag&2**4>0,1,0)),
                      np.sum(np.where(flag&2**10>0,1,0)),
                      np.sum(np.where(flag&2**14>0,1,0)),
                      np.sum(np.where(flag&2**19>0,1,0)),0], dtype=float)
    return counts/flag.size
    
def fix_BT(BT, flag):
    newBT = np.where(flag&2**1>0, 1.0,BT)
    newBT = np.where(flag&2**4>0, 0.0,newBT)
    newBT = np.where(flag&2**19>0, -0.1,newBT)
    weights = np.where(flag&2**1>0,1,0.00001)+np.where(flag&2**4>0,1,0.00001)+np.where(flag&2**10>0,1,0.00001)
    return newBT, weights/newBT.size

def fix_zspec(zspec, flag):
    newzspec = np.where(flag&2**19>0, -0.1,zspec)
    weights = np.where(flag&2**1>0,1,0.00001)+np.where(flag&2**4>0,1,0.00001)+np.where(flag&2**10>0,1,0.00001)
    return newzspec, weights/newzspec.size

def fix_r(r, flag):
    newr = np.where(flag&2**4>0, -1.0,r)
    newr = np.where(flag&2**19>0, -2.0,newr)
    weights = np.where(flag&2**1>0,1,0.00001)+np.where(flag&2**4>0,1,0.00001)+np.where(flag&2**10>0,1,0.00001)
    return newr, weights/newr.size

def fix_ba(ba, flag):
    newba = np.where(flag&2**4>0, -0.1,ba)
    newba = np.where(flag&2**19>0, -0.2,newba)
    weights = np.where(flag&2**1>0,1,0.00001)+np.where(flag&2**4>0,1,0.00001)+np.where(flag&2**10>0,1,0.00001)
    return newba, weights/newba.size

def fix_n(n, flag):
    newr = np.where(flag&2**13>0, 1.0,n)
    newr = np.where(flag&2**4>0, -0.5,newr)
    newr = np.where(flag&2**19>0, -1,newr)
    weights = np.where(flag&2**1>0,1,0.00001)+np.where(flag&2**4>0,1,0.00001)+np.where(flag&2**10>0,1,0.00001)
    return newr, weights/newr.size

def panel_plot(BT, flags, r_bulge, n_bulge,ba_bulge,ba_disk, ref_BT,ref_flag, ref_rb, ref_nb, ref_ba,ref_badisk, zspec, ref_zspec):
    fig = pl.figure(figsize=(8,5))
    pl.subplot(2,3,1)
    typebins = np.array([0,1,2,3,4,5])

    print flag_sep(flags)
    pl.step(typebins, flag_sep(flags), color = 'k', ls=':', lw=2, label = 'w/ bars',where='post')
    pl.step(typebins, flag_sep(ref_flag), color = 'k', ls='-',lw=2, label='w/o bar',where='post')
        
    x_names = ['bulges','disks','2com','prob 2com','bad']
    pl.xticks(typebins[:-1]+0.5, x_names, fontsize = 10)
    pl.xticks(rotation=45)
    pl.title('Galaxy class')
    pl.xlim((0, 5))


    pl.subplot(2,3,2)
    new_bt, weights = fix_BT(BT, flags)
    new_ref_bt, ref_weights = fix_BT(ref_BT, ref_flag)
    pl.hist(new_bt, range=(-0.1,1.0), bins = 22, histtype='step',lw=2,
            color = 'k', linestyle='dotted', label = 'w/ bars', weights = weights)
    pl.hist(new_ref_bt, range=(-0.1,1.0), bins = 22, lw=2,
            histtype='step',color = 'k', linestyle='solid',label='w/o bar',
            weights=ref_weights)
    pl.title('B/T')
    pl.xlim((0,1))
    pl.ylim((0,0.5))
    pl.xlabel('B/T')
    pl.ylabel('N/N$_{tot}$')

    pl.subplot(2,3,3)
    new_r, weights = fix_r(r_bulge, flags)
    new_ref_r, ref_weights = fix_r(ref_rb, ref_flag)
    pl.hist(new_r, range=(-2,10.0), bins = 24, histtype='step',lw=2,
            color = 'k', linestyle='dotted', label = 'w/ bars', weights = weights)
    pl.hist(new_ref_r, range=(-2,10), bins = 24, lw=2,
            histtype='step',color = 'k', linestyle='solid',label='w/o bar',
            weights=ref_weights)
    pl.title('bulge r')
    pl.xlim((0,6))
    pl.ylim((0,0.25))
    pl.xlabel('r$_{bulge}$ [arcsec]')
    pl.ylabel('N/N$_{tot}$')

    pl.subplot(2,3,4)
    new_n, weights = fix_n(n_bulge, flags)
    new_ref_n, ref_weights = fix_n(ref_nb, ref_flag)
    pl.hist(new_n, range=(-2,8.01), bins = 20, histtype='step',lw=2,
            color = 'k', linestyle='dotted', label = 'w/ bars', weights = weights)
    pl.hist(new_ref_n, range=(-2,8.01), bins = 20, lw=2,
            histtype='step',color = 'k', linestyle='solid',label='w/o bar',
            weights=ref_weights)
    pl.title('bulge n')
    pl.xlim((0,8))
    pl.ylim((0,0.15))
    pl.xlabel('n$_{bulge}$')
    pl.ylabel('N/N$_{tot}$')

    pl.subplot(2,3,5)
    new_ba, weights = fix_ba(ba_bulge, flags)
    new_ref_ba, ref_weights = fix_ba(ref_ba, ref_flag)
    pl.hist(new_ba, range=(-0.2,1.0), bins = 24, lw=2,
            histtype='step',color = 'k', linestyle='dotted', label = 'w/ bars', weights = weights)
    pl.hist(new_ref_ba, range=(-0.2,1.0), bins = 24, lw=2,
            histtype='step',color = 'k', linestyle='solid',label='w/o bar',
            weights=ref_weights)
    pl.title('bulge b/a')
    pl.xlim((0,1))
    pl.ylim((0,0.1))
    pl.xlabel('b/a$_{bulge}$')
    pl.ylabel('N/N$_{tot}$')

    l = pl.gca().legend(loc='center', 
                        bbox_to_anchor=(2.0, 0.5), fontsize='12')

    pl.subplots_adjust(left=0.09, hspace=0.65, wspace = 0.45, bottom=0.11,
                       right=0.97, top=0.92, )
    return

def zpanel_plot(BT, flags, r_bulge, n_bulge,ba_bulge,ba_disk, ref_BT,ref_flag, ref_rb, ref_nb, ref_ba,ref_badisk, zspec, ref_zspec):
    fig = pl.figure(figsize=(8,3))
    pl.subplot(1,2,1)
    new_zspec, weights = fix_zspec(zspec, flags)
    new_ref_zspec, ref_weights = fix_zspec(ref_zspec, ref_flag)

    pl.hist(new_zspec, range=(0.0,0.2), bins = 10, lw=2,
            histtype='step',color = 'r', linestyle='solid', label = 'w/ bars', weights = weights)
    pl.hist(new_ref_zspec, range=(0.0,0.2), bins = 10, lw=2,
            histtype='step',color = 'k', linestyle='solid', 
            label = 'w/o bar', weights =ref_weights)
    pl.title('z dist')
    pl.xlim((0,0.2))
    pl.ylim((0,0.2))
    pl.xlabel('z')
    pl.ylabel('N/N$_{tot}$')
    pl.subplots_adjust(left=0.09, hspace=0.65, wspace = 0.45, bottom=0.11,
                       right=0.97, top=0.92, )
    l = pl.gca().legend(loc='center', 
                        bbox_to_anchor=(2.0, 0.5), fontsize='12')

    print np.sum(new_zspec*weights)/np.sum(weights)
    print np.sum(new_ref_zspec*ref_weights)/np.sum(ref_weights)

    return


def do_panel(condition, refcondition, figtitle, cursor, band='r'):
    cmd = "select a.BT, f.flag, a.r_bulge,  a.n_bulge, a.ba_bulge, a.ba_disk, c.z from CAST as c, Flags_catalog as f, {band}_band_serexp as a, gz2_flags as z where a.galcount = c.galcount and a.galcount = f.galcount and a.galcount = z.galcount and f.band='{band}' and f.model='serexp' and f.ftype ='u' and {condition};"
#a.r_bulge,
    BT, flags, r_bulge, n_bulge,ba_bulge,ba_disk, zspec =cursor.get_data(cmd.format(condition=condition, band=band))
    ref_BT,ref_flag, ref_rb, ref_nb, ref_ba,ref_badisk, ref_zspec = cursor.get_data(cmd.format(condition=refcondition, band=band))
    BT = np.array(BT)
    flags = np.array(flags, dtype=int)
    r_bulge = np.array(r_bulge)
    n_bulge= np.array(n_bulge)
    ba_bulge= np.array(ba_bulge)
    ba_disk= np.array(ba_disk)
    zspec = np.array(zspec)

    ref_BT = np.array(ref_BT)
    ref_flag = np.array(ref_flag, dtype=int)
    ref_rb = np.array(ref_rb)
    ref_nb= np.array(ref_nb)
    ref_ba= np.array(ref_ba)
    ref_badisk= np.array(ref_badisk)
    ref_zspec = np.array(ref_zspec)


    panel_plot(BT, flags, r_bulge, n_bulge,ba_bulge,ba_disk, 
               ref_BT,ref_flag, ref_rb, ref_nb, ref_ba,ref_badisk, 
               zspec, ref_zspec)
    pl.figtext(0.5, 0.95, figtitle)
    print figtitle+' ',BT.size, ' objects' 
    pl.savefig('bar_params_serexp_%s.eps' %band)
    #pl.savefig('bar_z_serexp.eps')
    return


# now start the program

if __name__ == "__main__":
    cursor = mysql_connect('catalog','pymorph','pymorph')
    band = 'i'
    if 0:
        # look at ellipticals vs total
        condition = 'z.t01_smooth>0'
        refcondition = 'a.galcount>0'
        do_panel(condition, refcondition, 'Ell vs.total', cursor)

        #sys.exit()

        # look at disks vs total
        condition = 'z.t01_features_disk>0'
        refcondition = 'a.galcount>0'
        do_panel(condition, refcondition, 'disk vs total',cursor)

        # look at face vs edge-on disks
        refcondition = 'z.t02_edgeon_no>0'
        condition = 'z.t02_edgeon_yes>0'
        do_panel(condition, refcondition, 'edge on vs face on',cursor)

    # look at bar vs no bar
    refcondition = 'z.t03_no_bar>0'
    condition = 'z.t03_bar>0'
#    do_panel(condition, refcondition, 'bar vs no bar',cursor)
    do_panel(condition, refcondition, '',cursor, band = band)

    if 0:
        # look at edge-on nobulge vs edge-on bulge
        refcondition = 'z.t02_edgeon_yes>0'
        condition = 'z.t02_edgeon_yes>0 and z.t09_bulge_rounded>0'
        do_panel(condition, refcondition, 'edge on r-bulge vs all edge',cursor)

        # look at edge-on nobulge vs edge-on bulge
        refcondition = 'z.t02_edgeon_yes>0'
        condition = 'z.t02_edgeon_yes>0 and z.t09_bulge_boxy>0'
        do_panel(condition, refcondition, 'edge on b-bulge vs all edge',cursor)

        # look at edge-on nobulge vs edge-on bulge
        refcondition = 'z.t02_edgeon_yes>0'
        condition = 'z.t02_edgeon_yes>0 and z.t09_no_bulge>0'
        do_panel(condition, refcondition, 'edge on no-bulge vs all edge',cursor)

        # look at merger vs total
        condition = 'z.t08_merger>0'
        refcondition = 'a.galcount>0'
        do_panel(condition, refcondition, 'merger vs.total', cursor)

        # look at disturbed vs total
        condition = 'z.t08_disturbed>0'
        refcondition = 'a.galcount>0'
        do_panel(condition, refcondition, 'disturbed vs.total', cursor)

        # look at dustlane vs total
        condition = 'z.t08_dust_lane>0'
        refcondition = 'a.galcount>0'
        do_panel(condition, refcondition, 'dust lane vs.total', cursor)
    
    
