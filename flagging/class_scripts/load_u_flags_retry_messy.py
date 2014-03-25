from mysql_class import *
from flag_defs import new_finalflag_vals, new_finalflag_dict,category_flag_dict
import pylab as pl
import matplotlib.ticker as mticker

class flag_set():
    def __init__(self, flag_vals):
        self.vals = flag_vals
    def invert(self):
        return np.where(self.vals==1,0,1)

def get_percent(flag_arr):
    return 100.0*np.sum(flag_arr)/flag_arr.size

def anal_table(flags, BT):
    bulge_dominates = flag_set(np.where(BT>=0.5,1,0))

    galfit_failure = flag_set(np.where(flags&2**new_finalflag_dict['galfit failure']>0,1,0))
    center_probs = flag_set(np.where(flags&2**new_finalflag_dict['centering']>0,1,0))
    bulge_contam_or_sky = flag_set(
              np.where(flags&2**new_finalflag_dict['bulge contaminated']>0,1,0)
              | np.where(flags&2**new_finalflag_dict['bulge is sky']>0,1,0))
    disk_contam_or_sky = flag_set(
              np.where(flags&2**new_finalflag_dict['disk contaminated']>0,1,0)
              | np.where(flags&2**new_finalflag_dict['disk is sky']>0,1,0))


    disk_inner = flag_set(np.where(flags&2**new_finalflag_dict['disk fitting inner']>0,1,0))
    bulge_outer = flag_set(np.where(flags&2**new_finalflag_dict['bulge fitting outer']>0,1,0))
    bulge_is_disk = flag_set(np.where(flags&2**new_finalflag_dict['bulge is disk']>0,1,0))
    low_n_bulge = flag_set(np.where(flags&2**new_finalflag_dict['low n bulge']>0,1,0))
    
    # select out the 1 component cases
    no_bulge = flag_set(np.where(flags&2**new_finalflag_dict['no bulge likely']>0,1,0))
    no_disk = flag_set(np.where(flags&2**new_finalflag_dict['no disk likely']>0,1,0))
    disk_dominates_always = flag_set(np.where(flags&2**new_finalflag_dict['disk dominates always']>0,1,0))
    bulge_dominates_always = flag_set(np.where(flags&2**new_finalflag_dict['bulge dominates always']>0,1,0))

    other_bad_fits = flag_set(np.where(no_bulge.vals+no_disk.vals+
                     disk_dominates_always.vals+
                     bulge_dominates_always.vals > 1, 1,0)|(bulge_dominates.vals*(no_bulge.vals|disk_dominates_always.vals))|(bulge_dominates.invert()*(no_disk.vals|bulge_dominates_always.vals)))
             # these are fits that have incorrect measurements ...
  
    bad_gals = flag_set( galfit_failure.vals|center_probs.vals |bulge_contam_or_sky.vals |disk_contam_or_sky.vals| other_bad_fits.vals)

    #now update the 1com gals to remove bad ones
    no_bulge.vals = no_bulge.vals*bad_gals.invert()
    no_disk.vals = no_disk.vals*bad_gals.invert()
    disk_dominates_always.vals = disk_dominates_always.vals*bad_gals.invert()
    bulge_dominates_always.vals = bulge_dominates_always.vals*bad_gals.invert()

    parallel_com = flag_set(bad_gals.invert()*np.where(flags&2**new_finalflag_dict['parallel components']>0,1,0))

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

    bulge_shape = flag_set(np.where(flags&2**new_finalflag_dict['high e bulge']>0,1,0)* np.where(flags&2**new_finalflag_dict['bulge pa problem']>0,1,0))
    disk_shape = flag_set(np.where(flags&2**new_finalflag_dict['high e disk']>0,1,0)* np.where(flags&2**new_finalflag_dict['disk pa problem']>0,1,0))

    bad_bulge_shapes = flag_set(prob_2com_gals.vals*bulge_dominates.vals*disk_shape.vals*bulge_truly_outer.invert()*disk_truly_inner.invert())
    bad_disk_shapes = flag_set(prob_2com_gals.vals*bulge_dominates.invert()*bulge_shape.vals*bulge_truly_outer.invert()*disk_truly_inner.invert())

    problem_2com_fits =flag_set(prob_2com_gals.vals*( bulge_truly_outer.vals|disk_truly_inner.vals | bad_bulge_shapes.vals | bad_disk_shapes.vals))

    good_flip_2com =  flag_set( prob_2com_gals.vals*problem_2com_fits.invert()* no_flags.invert()*(np.where(bulge_is_disk.vals+bulge_outer.vals+disk_inner.vals >1, 1,0)| disk_inner.vals*low_n_bulge.vals | bulge_is_disk.vals))
    good_good_2com =  flag_set(prob_2com_gals.vals* problem_2com_fits.invert()*no_flags.invert()*good_flip_2com.invert())
   

    cats_to_plot = [("Good Total Magnitudes and Sizes", bad_gals.invert()),
                    ("Trust Total and Component Magnitudes and Sizes", prob_2com_gals.vals*problem_2com_fits.invert()),
                    ("\tTwo-Component Galaxies", prob_2com_gals.vals*problem_2com_fits.invert()), 
                    ("\t\tNo Flags", no_flags.vals),   
                    ("\t\tGood Ser, Good Exp (Some Flags)",good_good_2com.vals ), 
                    ("\t\tFlip Components, n$_{Ser}<$2", good_flip_2com.vals),     
                    
                    ("Trust Total Magnitudes and Sizes Only", problem_2com_fits.vals|single_bulge.vals|single_disk.vals),
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

                    ("Bad Total Magnitudes and Sizes", bad_gals.vals),
                    ("\tCentering Problems", center_probs.vals),  
                    ("\tSer Component Contamination by Neighbors or Sky", bulge_contam_or_sky.vals), 
                    ("\tExp Component Contamination by Neighbors or Sky", disk_contam_or_sky.vals),
                    ("\tBad Ser and Bad Exp Components", other_bad_fits.vals),    
                    ("\tGalfit Failure", galfit_failure.vals),   
                    ]
    
    new_flags = np.zeros_like(flags)

    for a in cats_to_plot:
        print '%s: %5.3f' %(a[0], get_percent(a[1]))

 
    for a in cats_to_plot:
        if a[0] in category_flag_dict.keys():
            new_flags += a[1]*(2**category_flag_dict[a[0]])
        else:
            print "Not setting flag '%s' ... It doesn't exist!!" %a[0]

    return new_flags

def load_newflags(cursor, galcount, new_flags, model):
    for gal in zip(galcount, new_flags):
        cmd = "update Flags_optimize set flag = %d where galcount = %d and band = 'r' and ftype='u' and model='%s';" %(gal[1],gal[0],model)
        cursor.execute(cmd)



cursor = mysql_connect('catalog','pymorph','pymorph','')
#cursor = mysql_connect('simulations','pymorph','pymorph','')

#cmd = """select a.galcount, a.flag, z.BT from Flags_optimize as a, M2010 as b, r_sims_serexp as z where a.flag >=0 and a.band = 'r' and a.model = 'serexp' and a.ftype = 'r' and a.galcount = b.galcount and a.galcount = z.galcount order by a.galcount limit 1000000;"""
if 0:
    cmd = """select a.galcount, a.flag, z.BT from Flags_optimize as a, M2010 as b, r_band_serexp as z where a.flag >=0 and a.band = 'r' and a.model = 'serexp' and a.ftype = 'r' and a.galcount = b.galcount and a.galcount = z.galcount order by a.galcount;"""
    galcount, flags, BT = cursor.get_data(cmd)

    galcount = np.array(galcount, dtype = int)
    flags = np.array(flags, dtype = int)
    BT = np.array(BT, dtype =float)

    print "\n\nFor the SerExp Catalog"
    new_flags = anal_table(flags, BT)
    load_newflags(cursor, galcount, new_flags, 'serexp')

    cmd = """select a.galcount, a.flag, z.BT from Flags_optimize as a, M2010 as b, r_band_devexp as z where a.flag >=0 and a.band = 'r' and a.model = 'devexp' and a.ftype = 'r' and a.galcount = b.galcount and a.galcount = z.galcount order by a.galcount;"""
    galcount, flags, BT = cursor.get_data(cmd)

    galcount = np.array(galcount, dtype = int)
    flags = np.array(flags, dtype = int)
    BT = np.array(BT, dtype =float)

    print "\n\nFor the DevExp Catalog"
    new_flags = anal_table(flags, BT)
    load_newflags(cursor, galcount, new_flags, 'devexp')

    cmd = """select a.galcount, a.flag, z.BT from Flags_optimize as a, M2010 as b, r_band_dev as z where a.flag >=0 and a.band = 'r' and a.model = 'dev' and a.ftype = 'r' and a.galcount = b.galcount and a.galcount = z.galcount order by a.galcount;"""
    galcount, flags, BT = cursor.get_data(cmd)

    galcount = np.array(galcount, dtype = int)
    flags = np.array(flags, dtype = int)
    BT = np.array(BT, dtype =float)

    print "\n\nFor the Dev Catalog"
    new_flags = anal_table(flags, BT)
    load_newflags(cursor, galcount, new_flags, 'dev')

cmd = """select a.galcount, a.flag, z.BT from Flags_optimize as a, M2010 as b, r_band_ser as z where a.flag >=0 and a.band = 'r' and a.model = 'ser' and a.ftype = 'r' and a.galcount = b.galcount and a.galcount = z.galcount order by a.galcount;"""
galcount, flags, BT = cursor.get_data(cmd)

galcount = np.array(galcount, dtype = int)
flags = np.array(flags, dtype = int)
BT = np.array(BT, dtype =float)

print "\n\nFor the Ser Catalog"
new_flags = anal_table(flags, BT)
load_newflags(cursor, galcount, new_flags, 'ser')



