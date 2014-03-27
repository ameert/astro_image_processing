import numpy as np


infile = open('/home/ameert/fit_catalog/sdss_sample/sample_selection/sdss_sample_first.txt')

g_in = []
s_in = []

for line in infile.readlines():
    line = line.split()
    if len(line) == 2:
        g_in.append(int(line[0]))
        s_in.append(int(line[1]))
        

infile.close()

g_in = np.array(g_in)
s_in = np.array(s_in)

# do simard sample
full_lines = []
infile = open('M2010.txt')

for line in infile.readlines():
    full_lines.append(line)

infile.close()

outfile = open('M2010_ordered.txt','w')
outfile.write(full_lines[0])

for count in range(1,261303):
    outfile.write(full_lines[np.extract(s_in == count, g_in)[0]])


outfile.close()
