from mysql.mysql_class import *
from flag_configuration import autoflag_dict, uflag_dict
from flag_analysis import flag_set, get_percent

def run_uflags(folder_num, info_dict, print_flags = False):
    cursor = info_dict['cursor']

    cmd = """select a.galcount, a.flag, z.BT from {table} as a, M2010 as b, r_band_{model} as z where a.flag >=0 and a.band = '{band}' and a.model = '{model}' and a.ftype = '{autoflag_ftype}' and a.galcount = b.galcount and a.galcount = z.galcount and (a.galcount between {low_gal} and {high_gal}) order by a.galcount;""".format(table = 'Flags_catalog', band=info_dict['band'], model=info_dict['model'], autoflag_ftype=info_dict['autoflag_ftype'], low_gal = 250*(folder_num-1)+1, high_gal = 250*folder_num)
    
    galcount, flags, BT = cursor.get_data(cmd)
    galcount = np.array(galcount, dtype = int)
    flags = np.array(flags, dtype = int)
    BT = np.array(BT, dtype =float)


    bulge_dominates = flag_set(np.where(BT>=0.5,1,0))

    galfit_failure = flag_set(np.where(flags&2**autoflag_dict['galfit failure']>0,1,0))
    center_probs = flag_set(np.where(flags&2**autoflag_dict['centering']>0,1,0))
    bulge_contam_or_sky = flag_set(
              np.where(flags&2**autoflag_dict['bulge contaminated']>0,1,0)
              | np.where(flags&2**autoflag_dict['bulge is sky']>0,1,0))
    disk_contam_or_sky = flag_set(
              np.where(flags&2**autoflag_dict['disk contaminated']>0,1,0)
              | np.where(flags&2**autoflag_dict['disk is sky']>0,1,0))

    poll_frac = flag_set(np.where(flags&2**autoflag_dict['polluted']>0,1,0)|np.where(flags&2**autoflag_dict['fractured']>0,1,0))


    disk_inner = flag_set(np.where(flags&2**autoflag_dict['disk fitting inner']>0,1,0))
    bulge_outer = flag_set(np.where(flags&2**autoflag_dict['bulge fitting outer']>0,1,0))
    bulge_is_disk = flag_set(np.where(flags&2**autoflag_dict['bulge is disk']>0,1,0))
    low_n_bulge = flag_set(np.where(flags&2**autoflag_dict['low n bulge']>0,1,0))
    
    # select out the 1 component cases
    no_bulge = flag_set(np.where(flags&2**autoflag_dict['no bulge likely']>0,1,0))
    no_disk = flag_set(np.where(flags&2**autoflag_dict['no disk likely']>0,1,0))
    disk_dominates_always = flag_set(np.where(flags&2**autoflag_dict['disk dominates always']>0,1,0))
    bulge_dominates_always = flag_set(np.where(flags&2**autoflag_dict['bulge dominates always']>0,1,0))

    other_bad_fits = flag_set(np.where(no_bulge.vals+no_disk.vals+
                     disk_dominates_always.vals+
                     bulge_dominates_always.vals > 1, 1,0)|(bulge_dominates.vals*(no_bulge.vals|disk_dominates_always.vals))|(bulge_dominates.invert()*(no_disk.vals|bulge_dominates_always.vals)))
             # these are fits that have incorrect measurements ...
  
    bad_gals = flag_set( galfit_failure.vals|center_probs.vals |bulge_contam_or_sky.vals |disk_contam_or_sky.vals| other_bad_fits.vals | poll_frac.vals)

    #now update the 1com gals to remove bad ones
    no_bulge.vals = no_bulge.vals*bad_gals.invert()
    no_disk.vals = no_disk.vals*bad_gals.invert()
    disk_dominates_always.vals = disk_dominates_always.vals*bad_gals.invert()
    bulge_dominates_always.vals = bulge_dominates_always.vals*bad_gals.invert()

    parallel_com = flag_set(bad_gals.invert()*np.where(flags&2**autoflag_dict['parallel components']>0,1,0))

    #now update again to remove parallel components
    no_bulge.vals = no_bulge.vals*parallel_com.invert()
    no_disk.vals = no_disk.vals*parallel_com.invert()
    disk_dominates_always.vals = disk_dominates_always.vals*parallel_com.invert()
    bulge_dominates_always.vals = bulge_dominates_always.vals*parallel_com.invert()

    ser_bulge_dominates_always = flag_set(bulge_dominates_always.vals*bulge_is_disk.invert()*low_n_bulge.invert())
    flip_bulge_dominates_always = flag_set(bulge_dominates_always.vals*(bulge_is_disk.vals|low_n_bulge.vals))

    ser_no_disk = flag_set(no_disk.vals*bulge_is_disk.invert()*low_n_bulge.invert())
    flip_no_disk = flag_set(no_disk.vals*(bulge_is_disk.vals|low_n_bulge.vals))

    single_bulge = flag_set(ser_no_disk.vals|ser_bulge_dominates_always.vals)
    single_disk = flag_set(flip_no_disk.vals|flip_bulge_dominates_always.vals
                           |no_bulge.vals | disk_dominates_always.vals|
                           parallel_com.vals )

    prob_2com_gals = flag_set(bad_gals.invert()*parallel_com.invert()*no_bulge.invert()*no_disk.invert() *disk_dominates_always.invert() *bulge_dominates_always.invert())
    no_flags = flag_set(np.where(flags==0,1,0))

    bulge_truly_outer = flag_set(bulge_outer.vals*bulge_is_disk.invert()*disk_inner.invert()*low_n_bulge.invert()*prob_2com_gals.vals)
    disk_truly_inner = flag_set(bulge_outer.invert()*bulge_is_disk.invert()*disk_inner.vals*prob_2com_gals.vals)

    bulge_shape = flag_set(np.where(flags&2**autoflag_dict['high e bulge']>0,1,0)* np.where(flags&2**autoflag_dict['bulge pa problem']>0,1,0))
    disk_shape = flag_set(np.where(flags&2**autoflag_dict['high e disk']>0,1,0)* np.where(flags&2**autoflag_dict['disk pa problem']>0,1,0))

    bad_bulge_shapes = flag_set(prob_2com_gals.vals*bulge_dominates.vals*disk_shape.vals*bulge_truly_outer.invert()*disk_truly_inner.invert())
    bad_disk_shapes = flag_set(prob_2com_gals.vals*bulge_dominates.invert()*bulge_shape.vals*bulge_truly_outer.invert()*disk_truly_inner.invert())

    problem_2com_fits =flag_set(prob_2com_gals.vals*( bulge_truly_outer.vals|disk_truly_inner.vals | bad_bulge_shapes.vals | bad_disk_shapes.vals))
    
    tiny_bulge = flag_set(np.where(flags&2**autoflag_dict['tinybulge']>0,1,0)*prob_2com_gals.vals* problem_2com_fits.invert())
                       
    problem_2com_fits =flag_set(problem_2com_fits.vals|tiny_bulge.vals)

    good_flip_2com =  flag_set( prob_2com_gals.vals*problem_2com_fits.invert()* no_flags.invert()*(np.where(bulge_is_disk.vals+bulge_outer.vals+disk_inner.vals >1, 1,0)| disk_inner.vals*low_n_bulge.vals | bulge_is_disk.vals))
    good_good_2com =  flag_set(prob_2com_gals.vals* problem_2com_fits.invert()*no_flags.invert()*good_flip_2com.invert())


    cats_to_plot = [("Good Total Magnitudes and Sizes", bad_gals.invert()),
                    ("\tTwo-Component Galaxies", prob_2com_gals.vals*problem_2com_fits.invert()), 
                    ("\t\tNo Flags", no_flags.vals),   
                    ("\t\tGood Ser, Good Exp (Some Flags)",good_good_2com.vals ), 
                    ("\t\tFlip Components, n$_{Ser}<$2", good_flip_2com.vals),     
                    ("\tBulge Galaxies", single_bulge.vals),
                    ("\t\tNo Exp Component, n$_{Ser}>=$2", ser_no_disk.vals),
                    ( "\t\tSer Dominates Always, n$_{Ser}>=$2", ser_bulge_dominates_always.vals),

                    ("\tDisk Galaxies", single_disk.vals),
                    ("\t\tNo Ser Component", no_bulge.vals),
                    ( "\t\tNo Exp, n$_{Ser}<$2, Flip Components", flip_no_disk.vals),
                    ( "\t\tSer Dominates Always, n$_{Ser}<$2",flip_bulge_dominates_always.vals),
                    ("\t\tExp Dominates Always", disk_dominates_always.vals),
                    ( "\t\tParallel Components", parallel_com.vals),
                 
                    ("\tProblemmatic Two-Component Galaxies", problem_2com_fits.vals),
                    ("\t\tSer Outer Only", bulge_truly_outer.vals),
                    ("\t\tExp Inner Only", disk_truly_inner.vals),
                    ("\t\tGood Ser, Bad Exp, B/T$>=$0.5", bad_bulge_shapes.vals),
                    ("\t\tBad Ser, Good Exp, B/T$<$0.5", bad_disk_shapes.vals),
                    ("\t\tTiny Bulge, otherwise good", tiny_bulge.vals),

                    ("Bad Total Magnitudes and Sizes", bad_gals.vals),
                    ("\tCentering Problems", center_probs.vals),  
                    ("\tSer Component Contamination by Neighbors or Sky", bulge_contam_or_sky.vals), 
                    ("\tExp Component Contamination by Neighbors or Sky", disk_contam_or_sky.vals),
                    ("\tBad Ser and Bad Exp Components", other_bad_fits.vals),    
                    ("\tGalfit Failure", galfit_failure.vals),   
                    ("\tPolluted or Fractured", poll_frac.vals)
                    ]
    
    uflags = np.zeros_like(flags)
 
    for a in cats_to_plot:
        if a[0] in uflag_dict.keys():
            uflags += a[1]*(2**uflag_dict[a[0]])
        else:
            print "Not setting flag '%s' ... It doesn't exist!!" %a[0]

    if print_flags:
        print "uflags"
        for a in zip(galcount, uflags):
            print a[0], a[1]

    
    return galcount,uflags

def load_uflags(galcount, uflags, info_dict, print_info = False):
    cursor = info_dict['cursor']

    for gal, flagval in zip(galcount, uflags):
        cmd = """update {table} set flag = {finalval} where galcount = {galcount} and band = '{band}' and model = '{model}' and ftype = '{uflag_ftype}';""".format(table = 'Flags_catalog', finalval = flagval, band=info_dict['band'], model=info_dict['model'], galcount = gal, uflag_ftype=info_dict['uflag_ftype'])
        if print_info:
            print cmd
        cursor.execute(cmd)
    return


if __name__ == "__main__":
    
    info_dict = {'dba':'catalog', 'usr':'pymorph', 'pwd':'pymorph', 'host':'',
                 'band':'r', 'model':'serexp','autoflag_ftype':'r',
                 'uflag_ftype':'u',}
    info_dict['cursor']=mysql_connect(info_dict['dba'],info_dict['usr'],info_dict['pwd'],info_dict['host'])
    
    folder_num = int(sys.argv[1])
    print "\n\nFor the %s band %s Catalog" %(info_dict['band'],info_dict['model'])
    galcount, uflags_out = run_uflags(folder_num, info_dict,print_flags = False)
    load_uflags(galcount, uflags_out, info_dict, print_info = False)
    






