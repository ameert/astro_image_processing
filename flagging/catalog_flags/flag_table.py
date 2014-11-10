from numpy import *
from astro_image_processing.mysql import *

from flag_analysis import get_percent
from flag_configuration import uflag_dict

info_dict = {'dba':'catalog', 'usr':'pymorph', 'pwd':'pymorph', 'host':'',
             'band':'r', 'model':'serexp','autoflag_ftype':'r',
             'uflag_ftype':'u',}
info_dict['cursor']=mysql_connect(info_dict['dba'],info_dict['usr'],info_dict['pwd'],info_dict['host'])

cursor = mysql_connect(info_dict['dba'],info_dict['usr'],info_dict['pwd'],info_dict['host'])


def write_full_table(models):
    row1str = ' c '*len(models)
    row2str = ["""\\textbf{{\% {modname}}}""".format(modname=modname) for modname in models]

    row2str = ' & '.join(row2str)

    indata = []

    for mod in models:
        indat1 = np.loadtxt('%s_catalog.table' %mod, delimiter = ':', usecols = [1])
        indata.append(indat1)


    indata = np.array(indata).T
    outstr = ["""\\begin{tabular}{l l l %s}""",
              """\\multicolumn{3}{l}{\\textbf{Descriptive Category}} &  %s \\\\ \\hline \\hline""",
"""\\multicolumn{3}{l}{\\textbf{Trust Total and Component Magnitudes and Sizes}} & %s\\\\ \\hline""",
"""& \\multicolumn{2}{l}{\\textbf{Two-Component Galaxies}} & %s \\\\""",
""" & & No Flags & %s \\\\""",
""" & & Good \\Ser, Good \\Exp\\ (Some Flags) & %s \\\\""",
""" & &Flip Components, n$_{\\Ser}<$2 & %s \\\\ \\hline""",
"""\\multicolumn{3}{l}{\\textbf{Trust Total Magnitudes and Sizes Only}} & %s\\\\ \\hline""",
"""& \\multicolumn{2}{l}{\\textbf{Bulge Galaxies}} &  %s\\\\""",
"""& &No \\Exp\\ Component, n$_{\\Ser}>$2&  %s \\\\""",
"""& &\\Ser\\ Dominates Always &  %s \\\\""",
"""& \\multicolumn{2}{l}{\\textbf{Disk Galaxies}} &  %s\\\\""",
"""& & No \\Ser\\ Component &   %s\\\\""",
"""& & No \\Exp, n$_{Ser}<$2, Flip Components &   %s\\\\""",
"""& & \\Ser\\ Dominates Always, n$_{\\Ser}<$2 &  %s\\\\""",
"""& & \\Exp\\ Dominates Always &   %s\\\\""",
"""& & Parallel Components &   %s\\\\""",
"""& \\multicolumn{2}{l}{\\textbf{Problematic Two-Component Galaxies}} &  %s\\\\""",
"""& & \\Ser\\ Outer Only &   %s\\\\""",
"""& & \\Exp\\ Inner Only &   %s\\\\""",
"""& & Good \\Ser, Bad \\Exp, B/T$>=$0.5 &   %s \\\\""",
"""& & Bad \\Ser, Good \\Exp, B/T$<$0.5 &   %s \\\\ \\hline \\hline""",
"""\\multicolumn{3}{l}{\\textbf{Bad Total Magnitudes and Sizes}} &  %s\\\\ \\hline""",
"""& \\multicolumn{2}{l}{Centering Problems} &  %s \\\\""",
"""& \\multicolumn{2}{l}{\\Ser\\ Component Contamination by Neighbors or Sky} &  %s \\\\""",
"""& \\multicolumn{2}{l}{\\Exp\\ Component Contamination by Neighbors or Sky} &  %s \\\\""",
"""& \\multicolumn{2}{l}{Bad \\Ser\\ and Bad \\Exp\\ Components} &  %s \\\\""",
"""& \\multicolumn{2}{l}{Galfit Failure} & %s \\\\""",
"""\\end{tabular}"""]

    outstr[0] = outstr[0] %row1str
    outstr[1] = outstr[1] %row2str

    for rowcount, row in enumerate(indata):
        rowvals = ['%.3f' %a for a in row]
        rowvals = ' & '.join(rowvals)
        outstr[2+rowcount]= outstr[2+rowcount] %rowvals

    outfile = open('table_tex.tex', 'w')
    outfile.write( "\n".join(outstr))
    outfile.close()
    return

def model_table(flags, model_type):
    
    cats_to_plot = ["\tTwo-Component Galaxies", 
                    "\t\tNo Flags",   
                    "\t\tGood Ser, Good Exp (Some Flags)", 
                    "\t\tFlip Components, n$_{Ser}<$2",      
                    "\tBulge Galaxies", 
                    "\t\tNo Exp Component, n$_{Ser}>=$2",
                     "\t\tSer Dominates Always, n$_{Ser}>=$2", 
                    "\tDisk Galaxies", 
                    "\t\tNo Ser Component",
                     "\t\tNo Exp, n$_{Ser}<$2, Flip Components", 
                     "\t\tSer Dominates Always, n$_{Ser}<$2",
                    "\t\tExp Dominates Always", 
                     "\t\tParallel Components", 
                    "\tProblemmatic Two-Component Galaxies", 
                    "\t\tSer Outer Only", 
                    "\t\tExp Inner Only", 
                    "\t\tGood Ser, Bad Exp, B/T$>=$0.5", 
                    "\t\tBad Ser, Good Exp, B/T$<$0.5", 
                    "\t\tTiny Bulge, otherwise good",
                    "Bad Total Magnitudes and Sizes", 
                    "\tCentering Problems",   
                    "\tSer Component Contamination by Neighbors or Sky",  
                    "\tExp Component Contamination by Neighbors or Sky", 
                    "\tBad Ser and Bad Exp Components",     
                    "\tGalfit Failure",
                    "\tPolluted or Fractured"
                    ]

    cats_to_plot = [(a, '%f' %get_percent(np.where(flags&2**uflag_dict[a]>0,1,0))) for a in cats_to_plot]
 
    cats_to_plot.insert(0,("Trust Total and Component Magnitudes and Sizes", '%f' %get_percent(np.where(flags&2**uflag_dict["\tTwo-Component Galaxies"]>0,1,0))))
    cats_to_plot.insert(5,("Trust Total Magnitudes and Sizes Only", '%f' %get_percent(np.where(flags&2**uflag_dict["\tTwo-Component Galaxies"]==0,1,0)*np.where(flags&2**uflag_dict["Good Total Magnitudes and Sizes"]>0,1,0) )))

    outfile = open('%s_catalog.table' %model_type, 'w')
    outfile.write( "\n".join([':'.join(a) for a in cats_to_plot]))
    outfile.close()
    return


cmd = """select a.flag from {table} as a, classify_test as b where a.flag >=0 and a.band = '{band}' and a.model = '{model}' and a.ftype = '{uflag_ftype}' and b.galaxy = a.galcount and b.band='r' order by a.galcount;""".format(table = 'Flags_catalog', band='r', model='serexp', uflag_ftype='u')

flags = info_dict['cursor'].get_data(cmd)
flags = np.array(flags, dtype = int)

model_table(flags, 'Test')
sys.exit()
for model in ['dev','ser','devexp','serexp']:
    info_dict['model'] = model
    cmd = """select a.flag from {table} as a where a.flag >=0 and a.band = '{band}' and a.model = '{model}' and a.ftype = '{uflag_ftype}' order by a.galcount;""".format(table = 'Flags_optimize', band=info_dict['band'], model=info_dict['model'], uflag_ftype=info_dict['uflag_ftype'])

    flags = info_dict['cursor'].get_data(cmd)
    flags = np.array(flags, dtype = int)

    model_table(flags, info_dict['model'])

write_full_table(['Test', 'serexp', 'devexp'])

