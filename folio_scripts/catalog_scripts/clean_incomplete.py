import os
import sys

model = sys.argv[1]
innum = int(sys.argv[2])

incat = '/data2/scratch/ameert/CMASS/i/data/%04d/sdss_i_%d.cat' %(innum,innum)
outpath = '/data2/scratch/ameert/CMASS/i/fits/%s/%04d/' %(model, innum)

infile=open(outpath+'/result.csv')
infile.readline()
file_stems = []
for line in infile.readlines():
    line = line.split(',')[0]
    file_stems.append(line[2:])
infile.close()

print file_stems

infile = open(incat)
infile.readline()
for line in infile.readlines():
    line = line.split()[0]
    if line not in file_stems:
        print 'rm %s/*%s*' %(outpath, line)
        os.system('rm %s/*%s*' %(outpath, line))
        pass
infile.close()
            

