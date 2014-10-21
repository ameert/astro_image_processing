import os
import datetime
from make_new_query import *
import subprocess as sub
import sys
import numpy as np
import pyfits as pf
from astro_image_processing.casjobs_query.casjobs_new_query import exec_cmd

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
