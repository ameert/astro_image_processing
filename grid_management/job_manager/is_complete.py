import os
import numpy as np

def loadnames(infile):
    a = open(infile)
    names = []
    a.readline()
    for line in a.readlines():
        line = line.split()
        names.append(line[0])
    a.close()

    return names


def check_done(incat, outcat, doneness= 0.05):
    indat = loadnames(incat)
    try:
        outfile = open(outcat)
        goodness = 1

        if len(indat) > 0:
            try:
                outstr = outfile.read()
                outfile.close()
            except IOError:
                goodness = 0

            if goodness: #If we haven't screwed up yet, check completeness
                count = 0
                for line in indat:
                    if line not in outstr:
                        count +=1

                print "len = ", count

                if count/float(len(indat)) > .05:
                    goodness = 0
                else:
                    goodness = 1
    except IOError:
        goodness = 0
    return goodness


    
