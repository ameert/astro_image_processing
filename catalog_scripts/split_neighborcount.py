import numpy as np

rerun_gals = np.loadtxt('/data2/home/ameert/catalog_scripts/multi_targets.txt', unpack=True, usecols=[0])

rerun_gals = rerun_gals.astype(int)


for count in range(1,2684):
    infile = open('/data2/home/ameert/catalog/r/data/%04d/sdss_r_%d.cat' %(count, count))
    outfile = open('/data2/home/ameert/catalog/r/data/%04d/sdss_multi_r_%d.cat' %(count, count), 'w')

    outfile.write(infile.readline())
    for line in infile.readlines():
        gal = int(line.split('_')[0])
        if gal in rerun_gals:
            outfile.write(line)

    outfile.close()
    infile.close()

    
