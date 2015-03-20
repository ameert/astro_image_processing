import os
import sys

old_path = '/data2/home/ameert/catalog/r/fits/serexp/'
new_path = '/data2/home/ameert/catalog/r/fits/neighbor/serexp/'

outdata = open('neighborcount_gals.txt', 'w')
outdata.write("""# these galaxies have different numbers of neighbors
# between reruns for some reason...they should be rerun
# galcount, old_neighbors, new_neighbors
""")

def count_neighbors(infile):
    try:
        indat = open(infile)
        inlines = indat.readlines()
        indat.close()
        inlines = ' '.join(inlines)
        inlines = inlines.split('0) sky')[1]
        inlines = inlines.split('0) sersic')

        neighbors = len(inlines)-1
    except IOError:
        neighbors = -999
        print "oh no"
    return neighbors
    


for folder_num in range(1,2684): 
    galmin = (folder_num-1)*250 +1
    galmax = folder_num*250 +1
    for galcount in range(galmin, galmax):
        old_neigh = count_neighbors(old_path+'%04d/G_r_%08d_r_stamp.in' %(folder_num, galcount))
        new_neigh = count_neighbors(new_path+'%04d/G_r_%08d_r_stamp.in' %(folder_num, galcount))
        if old_neigh != new_neigh:
            outdata.write("%08d %4d %4d\n" %(galcount, old_neigh ,new_neigh))

outdata.close()

        
