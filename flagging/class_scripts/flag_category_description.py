from mysql_class import *
from flag_defs import new_finalflag_vals, new_finalflag_dict
import pylab as pl
import matplotlib.ticker as mticker

class flag_set():
    def __init__(self, flag_vals):
        self.vals = flag_vals
    def invert(self):
        return np.where(self.vals==1,0,1)
    def total(self):
        return np.sum(self.vals)
    def sample_size(self):
        return vals.size
    def fraction(self):
        return float(self.total())/self.sample_size()
    def percent(self):
        return 100.0*self.fraction()

def get_percent(flag_arr):
    return 100.0*np.sum(flag_arr)/flag_arr.size

def anal_table(flags, BT, outfile_name):

    no_flags = flag_set(np.where(flags==0,1,0))
    galfit_failure = flag_set(np.where(flags&2**new_finalflag_dict['galfit failure']>0,1,0))
    good_total = flag_set(np.where(flags&2**new_finalflag_dict['Bad total fit']==0,1,0)*galfit_failure.invert())
    no_bulge = flag_set(np.where(flags&2**new_finalflag_dict['no bulge likely']>0,1,0))
    no_disk = flag_set(np.where(flags&2**new_finalflag_dict['no disk likely']>0,1,0))
    disk_dominates_always = flag_set(np.where(flags&2**new_finalflag_dict['disk dominates always']>0,1,0))
    bulge_dominates_always = flag_set(np.where(flags&2**new_finalflag_dict['bulge dominates always']>0,1,0))
    
    bulge_low_n = flag_set(np.where(flags&2**new_finalflag_dict['low n bulge']>0,1,0))
    
    bulge_dominated = flag_set(np.where(BT>=0.5,1,0))
    parallel_com = flag_set(np.where(flags&2**new_finalflag_dict['parallel components']>0,1,0))

    disk_inner = flag_set(np.where(flags&2**new_finalflag_dict['disk fitting inner']>0,1,0))
    other_disk_probs = flag_set(np.where(flags&(2**new_finalflag_dict['disk contaminated']+2**new_finalflag_dict['high e disk']+2**new_finalflag_dict['disk pa problem'])>0,1,0))


    bulge_outer = flag_set(np.where(flags&2**new_finalflag_dict['bulge fitting outer']>0,1,0))
    bulge_is_disk = flag_set(np.where(flags&2**new_finalflag_dict['bulge is disk']>0,1,0))
    other_bulge_probs = flag_set(np.where(flags&(2**new_finalflag_dict['high e bulge']+2**new_finalflag_dict['bulge pa problem']+2**new_finalflag_dict['bulge contaminated'])>0,1,0))


    possible_2com = flag_set(good_total.vals*disk_dominates_always.invert()*bulge_dominates_always.invert()*no_disk.invert() *no_bulge.invert()*parallel_com.invert())

    flip_components =  flag_set(np.where(flags&2**new_finalflag_dict['flip components']==0,0,1))

#    good_bulge = flag_set(np.where(flags&(2**new_finalflag_dict['bad bulge']+2**new_finalflag_dict['parallel components'])>0,0,1))
#    good_disk = flag_set(np.where(flags&(2**new_finalflag_dict['bad disk']+2**new_finalflag_dict['parallel components'])>0,0,1))
    good_bulge = flag_set(np.where((flags&2**new_finalflag_dict['bad bulge'])>0, 0,1))
    good_disk = flag_set(np.where((flags&2**new_finalflag_dict['bad disk'])>0, 0,1))

    bulge_truly_outer = flag_set(bulge_outer.vals*bulge_is_disk.invert()*disk_inner.invert())


    problem2com = flag_set((possible_2com.vals*bulge_outer.vals*(good_bulge.vals|good_disk.vals)*flip_components.invert()*parallel_com.invert())| (possible_2com.vals*disk_inner.vals*(good_bulge.vals|good_disk.vals)*flip_components.invert()*parallel_com.invert()) | (possible_2com.vals*parallel_com.invert()*flip_components.vals*(good_bulge.invert()|good_disk.invert())) | (parallel_com.vals*possible_2com.vals) | (possible_2com.vals*good_bulge.invert()*good_disk.invert()*parallel_com.invert()*flip_components.invert()))


    for a, b, c, d in zip(galcount,  good_total.vals*good_bulge.vals*bulge_low_n.vals*no_disk.vals*no_bulge.invert()*bulge_dominates_always.invert()*disk_dominates_always.invert(),flags,  flip_components.vals  ):
        if b>0:
            print a, c, [c&2**x for x in range(0,24)],d 


    cats_to_plot = [
                    ["Good Total",good_total.vals],
                    ["Probable 1com, OK components", good_total.vals*possible_2com.invert()*bulge_dominates_always.invert()*disk_dominates_always.invert()*parallel_com.invert()],
                    ["\tNo Bulge", good_total.vals*no_bulge.vals*no_disk.invert()*bulge_dominates_always.invert()*disk_dominates_always.invert()],
                    #["\t\tNo bulge, Good Disk [1com]", good_total.vals*no_bulge.vals*good_disk.vals*no_disk.invert()*bulge_dominates_always.invert()*disk_dominates_always.invert()],
                    #["\t\tNo bulge, Bad disk[1com]", good_total.vals*no_bulge.vals*good_disk.invert()*no_disk.invert()*bulge_dominates_always.invert()*disk_dominates_always.invert()],
                    
                    
                    ["\tNo Disk", good_total.vals*no_bulge.invert()*no_disk.vals*bulge_dominates_always.invert()*disk_dominates_always.invert()],
                    ["\t\tGood bulge, n>2, No disk [1com]",good_total.vals*good_bulge.vals*bulge_low_n.invert()*no_disk.vals*no_bulge.invert()*bulge_dominates_always.invert()*disk_dominates_always.invert()],
                    ["\t\tGood bulge, n<2, No disk [1com],Flip Components",good_total.vals*good_bulge.vals*bulge_low_n.vals*no_disk.vals*no_bulge.invert()*bulge_dominates_always.invert()*disk_dominates_always.invert()**flip_components.vals],
                    #["\t\tBad bulge, no disk[1com]", good_total.vals*good_bulge.invert()*no_disk.vals*no_bulge.invert()*bulge_dominates_always.invert()*disk_dominates_always.invert()],

                    ["possible 2com, components OK", good_total.vals*possible_2com.vals*problem2com.invert()],
                    ["\tNo flags [2com]", no_flags.vals],
                    ["\tGood bulge, Good disk", possible_2com.vals*good_bulge.vals*good_disk.vals*no_flags.invert()*flip_components.invert()*parallel_com.invert()*bulge_outer.invert()*disk_inner.invert()*bulge_is_disk.invert()],
                    ["\tGood bulge, Bad disk, B/T>=0.5", possible_2com.vals*good_bulge.vals*good_disk.invert()*bulge_dominated.vals*bulge_outer.invert()*flip_components.invert()*disk_inner.invert()*bulge_is_disk.invert()*parallel_com.invert()],
                    ["\tBad bulge, Good disk, B/T<0.5", possible_2com.vals*good_bulge.invert()*good_disk.vals*bulge_outer.invert()*flip_components.invert()*disk_inner.invert()*bulge_is_disk.invert()*bulge_dominated.invert()*parallel_com.invert()],
                    ["\tFlip Components, otherwise good", possible_2com.vals*flip_components.vals*parallel_com.invert()*good_bulge.vals*good_disk.vals],
 
                    #["\tGood bulge, Bad disk, B/T<0.5", possible_2com.vals*good_bulge.vals*good_disk.invert()*bulge_outer.invert()*flip_components.invert()*disk_inner.invert()*bulge_is_disk.invert()*bulge_dominated.invert()*parallel_com.invert()],
                    #["\tBad bulge, Good disk, B/T>=0.5", possible_2com.vals*good_bulge.invert()*good_disk.vals*bulge_outer.invert()*flip_components.invert()*disk_inner.invert()*bulge_is_disk.invert()*bulge_dominated.vals*parallel_com.invert()],

                    #["\tbulge is disk only", possible_2com.vals*bulge_is_disk.vals*(good_bulge.vals|good_disk.vals)*flip_components.invert()*parallel_com.invert()],


                    ["Probable 1com, bad components", good_total.vals*possible_2com.invert()*no_bulge.invert()*no_disk.invert()],
                    ["\tbulge dominates always",  good_total.vals*no_bulge.invert()*no_disk.invert()*bulge_dominates_always.vals*disk_dominates_always.invert()*parallel_com.invert()],#disk_dominates_always.invert()*no_bulge.invert()*no_disk.invert()
                    #["\t\tGood bulge, Good Disk [1com]", good_total.vals*bulge_dominates_always.vals*good_bulge.vals*good_disk.vals*bulge_low_n.invert()],
                    #["\t\tGood bulge, Bad Disk [1com]", good_total.vals*bulge_dominates_always.vals*good_bulge.vals*good_disk.invert()*bulge_low_n.invert()], 
                    #["\t\tGood bulge, low n bulge, Good Disk [1com]", good_total.vals*bulge_dominates_always.vals*good_bulge.vals*good_disk.vals*bulge_low_n.vals],
                    #["\t\tGood bulge, low n bulge, Bad Disk [1com]", good_total.vals*bulge_dominates_always.vals*good_bulge.vals*good_disk.invert()*bulge_low_n.vals],
                    #["\t\tBad bulge, Bad Disk [1com]", good_total.vals*bulge_dominates_always.vals*good_bulge.invert()*good_disk.invert()*bulge_low_n.invert()],
                    #["\t\tBad bulge, Bad Disk, low n [1com]", good_total.vals*bulge_dominates_always.vals*good_bulge.invert()*good_disk.invert()*bulge_low_n.vals],

                    
                    ["\tdisk dominates always",  good_total.vals*disk_dominates_always.vals*bulge_dominates_always.invert()*no_bulge.invert()*no_disk.invert()*parallel_com.invert()],
                    #["\t\tDisk dominates always, Good bulge, n>2, Good Disk [1com]", good_total.vals*disk_dominates_always.vals*good_bulge.vals*good_disk.vals*bulge_low_n.invert()],
                    #["\t\tDisk dominates always, Good bulge, n<2, Good Disk [1com]", good_total.vals*disk_dominates_always.vals*good_bulge.vals*good_disk.vals*bulge_low_n.vals],
                    #["\t\tDisk dominates always, Good bulge, n>2, Bad Disk [1com]",  good_total.vals*disk_dominates_always.vals*good_bulge.vals*good_disk.invert()*bulge_low_n.invert()],
                    #["\t\tDisk dominates always, Good bulge, n<2, Bad Disk [1com]",  good_total.vals*disk_dominates_always.vals*good_bulge.vals*good_disk.invert()*bulge_low_n.vals],
                    #["\t\tDisk dominates always, Bad bulge, n>2, Good Disk [1com]",  good_total.vals*disk_dominates_always.vals*good_bulge.invert()*good_disk.vals*bulge_low_n.invert()],
                    #["\t\tDisk dominates always, Bad bulge, n<2, Good Disk [1com]",  good_total.vals*disk_dominates_always.vals*good_bulge.invert()*good_disk.vals*bulge_low_n.vals],
                    #["\t\tDisk dominates always, Bad bulge, n>2, Bad Disk [1com]",  good_total.vals*disk_dominates_always.vals*good_bulge.invert()*good_disk.invert()*bulge_low_n.invert()],
                    #["\t\tDisk dominates always, Bad bulge, n<2, Bad Disk [1com]",  good_total.vals*disk_dominates_always.vals*good_bulge.invert()*good_disk.invert()*bulge_low_n.vals],
                    ["\tParallel Components",  good_total.vals*parallel_com.vals*possible_2com.invert()],
                    
                    ["possible 2com, problems component", good_total.vals*possible_2com.vals*problem2com.vals],
                    ["\tbulge outer only", possible_2com.vals*bulge_outer.vals*(good_bulge.vals|good_disk.vals)*flip_components.invert()*parallel_com.invert()],
                    ["\tdisk inner only", possible_2com.vals*disk_inner.vals*(good_bulge.vals|good_disk.vals)*flip_components.invert()*parallel_com.invert()],
                    ["\t\tFlip Components, and bad components", possible_2com.vals*parallel_com.invert()*flip_components.vals*(good_bulge.invert()|good_disk.invert())],
                    ["\tBad bulge, Bad disk", possible_2com.vals*good_bulge.invert()*good_disk.invert()*parallel_com.invert()*flip_components.invert()],

                    ["Untrustworthy Fit",good_total.invert()],
                    ["Bad Total",good_total.invert()*galfit_failure.invert()],
                    #["\tNo Bulge,bulge dominates always", no_bulge.vals*bulge_dominates_always.vals],                    
                    #["\tNo Bulge,disk dominates always", no_bulge.vals*disk_dominates_always.vals],
                    #["\tbulge dominates always,Disk dominates always", disk_dominates_always.vals*bulge_dominates_always.vals],
                    #["\tNo Disk,Disk dominates always", no_disk.vals*disk_dominates_always.vals],
                    #["\tNo Disk,bulge dominates always", no_disk.vals*bulge_dominates_always.vals],
                    #["\tNo Bulge,No disk", no_bulge.vals*no_disk.vals],                    
                    ["Galfit Failure",galfit_failure.vals],
                    ]
    

#    cats_to_plot[0][1] = np.where(np.sum(np.array([cats_to_plot[a][1] for a in range(1,4)]), axis = 0)>0, 1,0)
#    cats_to_plot[4][1] = np.where(np.sum(np.array([cats_to_plot[a][1] for a in range(5,13)]), axis = 0)>0, 1,0)
#    cats_to_plot[13][1] = np.where(np.sum(np.array([cats_to_plot[a][1] for a in range(14,19)]), axis = 0)>0, 1,0)


    for a in cats_to_plot:
        print "%s: %.3f" %(a[0], get_percent(a[1]))

#    outfile = open(outfile_name, 'w')
#    for a in cats_to_plot:
#        outfile.write("%s: %.3f\n" %(a[0], get_percent(a[1])))
#    outfile.close()
    return




def anal_table2(flags, BT):
    no_flags = flag_set(np.where(flags==0,1,0))
    good_total = flag_set(np.where(flags&2**new_finalflag_dict['Bad total fit']==0,1,0))
    no_bulge = flag_set(np.where(flags&2**new_finalflag_dict['no bulge likely']>0,1,0))
    no_disk = flag_set(np.where(flags&2**new_finalflag_dict['no disk likely']>0,1,0))
    good_bulge = flag_set(np.where(flags&2**new_finalflag_dict['bad bulge']==0,1,0))
    good_disk = flag_set(np.where(flags&2**new_finalflag_dict['bad disk']==0,1,0))

    bulge_dominated = flag_set(np.where(BT>=0.5,1,0))

    disk_inner = flag_set(np.where(flags&2**new_finalflag_dict['disk fitting inner']>0,1,0))
    bulge_outer = flag_set(np.where(flags&2**new_finalflag_dict['bulge fitting outer']>0,1,0))
    bulge_is_disk = flag_set(np.where(flags&2**new_finalflag_dict['bulge is disk']>0,1,0))
    other_bulge_probs = flag_set(np.where(flags&(2**new_finalflag_dict['high e bulge']+2**new_finalflag_dict['bulge pa problem']+2**new_finalflag_dict['bulge contaminated'])>0,1,0))
    other_disk_probs = flag_set(np.where(flags&(2**new_finalflag_dict['disk contaminated']+2**new_finalflag_dict['high e disk']+2**new_finalflag_dict['disk pa problem'])>0,1,0))

    cats_to_plot = [["good fits", 0.0],
                    ["\tNo flags", no_flags.vals],
                    ["\tGood total, no bulge, good disk", good_total.vals*no_bulge.vals*good_disk.vals],
                    ["\tGood total, good bulge, no disk",good_total.vals*good_bulge.vals*no_disk.vals],
                    ["conditionally good fits", 0.0],
                    ["\tGood total, good bulge, bad disk, B/T>=0.5", good_total.vals*good_bulge.vals*good_disk.invert()*bulge_dominated.vals],
                    ["\tGood total, bad bulge, good disk, B/T<0.5", good_total.vals*good_bulge.invert()*good_disk.vals*bulge_dominated.invert()],
                    ["\tGood total, no bulge, bad disk", good_total.vals*no_bulge.vals*good_disk.invert()],
                    ["\tGood total, bad bulge, no disk", good_total.vals*good_bulge.invert()*no_disk.vals],
                    ["\tGood total, good bulge, bad disk, B/T<0.5", good_total.vals*good_bulge.vals*good_disk.invert()*bulge_dominated.invert()],
                    ["\tGood total, bad bulge, good disk, B/T>=0.5", good_total.vals*good_bulge.invert()*good_disk.vals*bulge_dominated.vals],
                    ["\tGood Total, Bulge fitting Outer, Disk Fitting Inner", good_total.vals*bulge_outer.vals*disk_inner.vals*other_bulge_probs.invert()*other_disk_probs.invert()],
                    ["\tGood Total, Bulge is Disk, Bulge Fitting Outer, Disk Fitting Inner", good_total.vals*bulge_is_disk.vals*disk_inner.vals*other_bulge_probs.invert()*other_disk_probs.invert()],
                    ["bad fits", 0.0],
                    ["\tGood total, bad bulge, bad disk", np.where(good_total.vals*good_bulge.invert()*good_disk.invert() - good_total.vals*bulge_outer.vals*disk_inner.vals*other_bulge_probs.invert()*other_disk_probs.invert()-good_total.vals*bulge_is_disk.vals*disk_inner.vals*other_bulge_probs.invert()*other_disk_probs.invert()>0, 1, 0)],
                    ["\tBad total, good bulge, good disk", good_total.invert()*good_bulge.vals*good_disk.vals],
                    ["\tBad total, bad bulge, good disk", good_total.invert()*good_bulge.invert()*good_disk.vals],
                    ["\tBad total, good bulge, bad disk", good_total.invert()*good_bulge.vals*good_disk.invert()],
                    ["\tBad total, bad bulge, bad disk", good_total.invert()*good_bulge.invert()*good_disk.invert()],
                    ]
    

    cats_to_plot[0][1] = np.where(np.sum(np.array([cats_to_plot[a][1] for a in range(1,4)]), axis = 0)>0, 1,0)
    cats_to_plot[4][1] = np.where(np.sum(np.array([cats_to_plot[a][1] for a in range(5,13)]), axis = 0)>0, 1,0)
    cats_to_plot[13][1] = np.where(np.sum(np.array([cats_to_plot[a][1] for a in range(14,19)]), axis = 0)>0, 1,0)


    for a in cats_to_plot:
        print "%s: %.2f" %(a[0], get_percent(a[1]))

    return
        

cursor = mysql_connect('catalog','pymorph','pymorph','')

cmd = """select a.galcount, a.flag, z.BT from Flags_optimize as a, M2010 as b, classify_test as c, r_band_serexp as z where a.flag >=0 and a.band = 'r' and a.model = 'serexp' and a.ftype = 'r' and c.band='r' and a.galcount = b.galcount and a.galcount = c.galaxy and a.galcount = z.galcount order by a.galcount limit 1000000;"""
#galcount, flags, BT = cursor.get_data(cmd)

#galcount = np.array(galcount, dtype = int)
#flags = np.array(flags, dtype = int)
#BT = np.array(BT, dtype =float)

print "For the test sample"
#anal_table(flags, BT, 'Test_catalog.table')

cmd = """select a.galcount, a.flag, z.BT from Flags_optimize as a, M2010 as b, r_band_serexp as z where a.flag >=0 and a.band = 'r' and a.model = 'serexp' and a.ftype = 'r' and a.galcount = b.galcount and a.galcount = z.galcount order by a.galcount limit 50000;"""
galcount, flags, BT = cursor.get_data(cmd)

galcount = np.array(galcount, dtype = int)
flags = np.array(flags, dtype = int)
BT = np.array(BT, dtype =float)

print "\n\nFor the SerExp Catalog"
anal_table(flags, BT, 'SerExp_catalog.table')

cmd = """select a.galcount, a.flag, z.BT from Flags_optimize as a, M2010 as b, r_band_serexp as z where a.flag >=0 and a.band = 'r' and a.model = 'devexp' and a.ftype = 'r' and a.galcount = b.galcount and a.galcount = z.galcount order by a.galcount limit 1000000;"""
#galcount, flags, BT = cursor.get_data(cmd)

#galcount = np.array(galcount, dtype = int)
#flags = np.array(flags, dtype = int)
#BT = np.array(BT, dtype =float)

#print "\n\nFor the DevExp Catalog"
#anal_table(flags, BT, 'DevExp_catalog.table')
