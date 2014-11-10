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


def check_done(incat, outcat):
    indat = loadnames(incat)
    num_to_run = len(indat)
    goodness = 1
    if num_to_run>0:
        try:
            outfile = open(outcat)


            try:
                outstr = outfile.read()
                outfile.close()
            except IOError:
                goodness = 0

            if goodness: #If we haven't screwed up yet, check completeness
                fitcount = 0
                for line in indat:
                    if line in outstr:
                        fitcount +=1

                print "len = ", fitcount

            complete_prop = float(fitcount)/float(num_to_run)

            if num_to_run < 10:
                prop = 0.0
            elif num_to_run < 25:
                prop = 0.7
            elif num_to_run < 50:
                prop = 0.9
            else:
                prop = 0.95

            if complete_prop < prop:
                goodness = 0
            else:
                goodness = 1


        except IOError:
            goodness = 0
    return goodness

    
