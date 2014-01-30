import os
import sys

model = sys.argv[1]
innum = int(sys.argv[2])

incat = '/data2/home/ameert/z_sims/z10/data/sdss_z10_%d.cat' %(innum)
outpath = '/data2/home/ameert/z_sims/z10/fits/%s/%04d/' %(model, innum)

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
        #print 'rm %s/*%s*' %(outpath, line)
        #os.system('rm %s/*%s*' %(outpath, line))
        pass
infile.close()
            

