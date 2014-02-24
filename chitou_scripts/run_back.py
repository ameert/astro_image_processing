import os
import sys

start = int(sys.argv[1])
stop = int(sys.argv[2])

for count in range(start,stop):
    infile = './get_field_data/background_%d.fit' %count
    outfile = 'flat_back_%d.fits' %count
    os.system('python make_image.py %s %s %d' %(infile, outfile, count))
    os.system('rm %d_*psf.fits' %count)
    
           
