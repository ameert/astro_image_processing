import os
import datetime
from make_new_query import *
import subprocess as sub
import sys
import numpy as np
import pyfits as pf

#data_types = {}
def exec_cmd(job_str):
    p1=sub.Popen(job_str, shell=True, stdout = sub.PIPE)
    output = p1.communicate()[0]
    output = output.strip()
    return output

def clean_cat(infile, outfile):
    fip = open(infile)
    fop = open(outfile, 'w')
    firstline = fip.readline()
    fop.write('# NOTE: Null values have be replaced by -888\n')
    fop.write('# '+firstline)
    for line in fip.readlines():
        if firstline not in line:
            line = line.replace('null', '-888')
            fop.write(line)
        else:
            line = line.split(firstline)
            print line[0] 
            fop.write(line[0]+'\n')


    fip.close()
    fop.close()

    return







    #names = fip.readline().strip()
    #for a in names.split(','):
    #    print "'%s':floata
    #return
    #for line in fip.readlines():
    #    if 'null' in line:
    #        print line

#    fip.close()
