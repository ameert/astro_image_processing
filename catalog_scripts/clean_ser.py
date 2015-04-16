#!/data2/home/ameert/python/bin/python2.5
import os
import sys

model ='ser'
filter = sys.argv[1]
innum = int(sys.argv[2])

incat = '/data2/home/ameert/catalog/%s/data/%04d/sdss_rerun_%s_%d.cat' %(filter,innum, filter, innum)
orig_incat = '/data2/home/ameert/catalog/%s/data/%04d/sdss_%s_%d.cat' %(filter, innum, filter, innum)
outpath = '/data2/home/ameert/catalog/%s/fits/%s_new/%04d/' %(filter, model, innum)

def load_incat(cat):
    infile = open(cat)
    infile.readline()
    gals = []
    for line in infile.readlines():
        gals.append(int(line.split('_')[0]))
    infile.close()
    return gals

shortlist = load_incat(incat)
longlist = load_incat(orig_incat)

print shortlist
print longlist

for val in longlist:
    if val not in shortlist:
        #print 'rm %s/*%08d*' %(outpath, val)
        os.system('rm %s/*%08d*' %(outpath, val))
