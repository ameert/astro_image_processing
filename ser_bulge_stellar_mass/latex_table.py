import sys
import os
import numpy as np
import bin_stats as bs
import pylab as pl
from MatplotRc import *

def add_row(add_command, choice):
    if choice =='all':
        choice_str = 'u.flag>=0'
    elif choice == 'good':
        choice_str = '(u.flag&pow(2,0)>0)'
    elif choice == "bad":
        choice_str = '(u.flag&pow(2,19)>0)'
    elif choice == "nr_cut":
        choice_str = ' (u.flag&pow(2,11)>0 or u.flag&pow(2,12)>0) and  r_bulge>0.1 and n_bulge<7.95'
    cmd = """mysql -u pymorph -ppymorph catalog -e "select count(*) from  M2010 as m, Flags_optimize as u, SSDR6 as a, CAST as c, DERT as d, r_band_serexp as b where c.galcount = m.galcount and a.galcount = c.galcount and c.galcount = b.galcount and c.galcount = d.galcount and c.galcount = u.galcount and u.ftype = 'u' and u.band = 'r' and u.model = 'serexp' and %s {add_cmd};" >> table.txt """ %choice_str
    
    #all gals
    os.system(cmd.format(add_cmd=add_command)) 
    #Ell gals
    os.system(cmd.format(add_cmd=add_command+' and ((-6.0*m.probaEll -3.0*m.probaS0+4.0*m.probaSab+8.0*m.probaScd) between -8.0 and -4.0)'))
    #S0 gals
    os.system(cmd.format(add_cmd=add_command+' and ((-6.0*m.probaEll -3.0*m.probaS0+4.0*m.probaSab+8.0*m.probaScd) between -4.0 and 0.5)'))
    #Sab gals
    os.system(cmd.format(add_cmd=add_command+' and ((-6.0*m.probaEll -3.0*m.probaS0+4.0*m.probaSab+8.0*m.probaScd) between 0.5 and 4.0)'))
    #Scd gals
    os.system(cmd.format(add_cmd=add_command+' and ((-6.0*m.probaEll -3.0*m.probaS0+4.0*m.probaSab+8.0*m.probaScd) between 4.0 and 10.0)'))
    
    return

def to_table(filename, outtable):
    infile = open(filename)
    count = -1
    outstr = """ \\begin{tabular}{l | c c c c c}
   & All Galaxies & Ell & S0 & Sab & Scd """
    linestart = ["Any type",  "Pure Disk", "0.0$<$B/T$\leq$0.2", "0.2$<$B/T$\leq$0.4" , "0.4$<$B/T$\leq$0.6" , "0.6$<$B/T$\leq$0.8", "0.8$<$B/T$\leq$1.0",  "Pure Bulge"] 
    
    for line in infile.readlines():
        try:
            val = int(line)
            count+=1
            if count%5 == 0:
                outstr += """ \\\\ \n """+linestart[count/5]
            outstr += " & %d " %val
        except:
            pass
    
    infile.close()

    outstr += """\\\\ \n  \\end{tabular}""" 
    outfile = open( outtable, 'w')
    outfile.write(outstr)
    outfile.close()

    return


os.system('/bin/rm table.txt')

add_row('', choice = 'all')
add_row(' and u.flag&pow(2,4)>0 ', choice = 'all')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0)  and (BT between 0.0 and 0.2) ', choice = 'all')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0)  and (BT between 0.2 and 0.4) ', choice = 'all')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0)  and (BT between 0.4 and 0.6) ', choice = 'all')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0)  and (BT between 0.6 and 0.8) ', choice = 'all')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0) and (BT between 0.8 and 1.0) ', choice = 'all')
add_row(' and u.flag&pow(2,1)>0 ', choice = 'all')

to_table('table.txt', 'all_fits.txt')



os.system('/bin/rm table.txt')

add_row('', choice = 'good')
add_row(' and u.flag&pow(2,4)>0 ', choice = 'good')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0)  and (BT between 0.0 and 0.2) ', choice = 'good')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0)  and (BT between 0.2 and 0.4) ', choice = 'good')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0)  and (BT between 0.4 and 0.6) ', choice = 'good')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0)  and (BT between 0.6 and 0.8) ', choice = 'good')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0) and (BT between 0.8 and 1.0) ', choice = 'good')
add_row(' and u.flag&pow(2,1)>0 ', choice = 'good')

to_table('table.txt', 'good_fits.txt')

os.system('/bin/rm table.txt')

add_row('', choice = 'bad')
add_row(' and u.flag&pow(2,4)>0 ', choice = 'bad')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0)  and (BT between 0.0 and 0.2) ', choice = 'bad')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0)  and (BT between 0.2 and 0.4) ', choice = 'bad')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0)  and (BT between 0.4 and 0.6) ', choice = 'bad')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0)  and (BT between 0.6 and 0.8) ', choice = 'bad')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0) and (BT between 0.8 and 1.0) ', choice = 'bad')
add_row(' and u.flag&pow(2,1)>0 ', choice = 'bad')

to_table('table.txt', 'bad_fits.txt')

os.system('/bin/rm table.txt')

add_row('', choice = 'nr_cut')
add_row(' and u.flag&pow(2,4)>0 ', choice = 'nr_cut')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0)  and (BT between 0.0 and 0.2) ', choice = 'nr_cut')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0)  and (BT between 0.2 and 0.4) ', choice = 'nr_cut')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0)  and (BT between 0.4 and 0.6) ', choice = 'nr_cut')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0)  and (BT between 0.6 and 0.8) ', choice = 'nr_cut')
add_row(' and (u.flag&pow(2,10)>0 or u.flag&pow(2,14)>0) and (BT between 0.8 and 1.0) ', choice = 'nr_cut')
add_row(' and u.flag&pow(2,1)>0 ', choice = 'nr_cut')

to_table('table.txt', 'nr_cut_fits.txt')


