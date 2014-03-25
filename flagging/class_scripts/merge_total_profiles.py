import pickle
import numpy as np
import sys

band = 'r'
model = sys.argv[1]

filepath = '/home/ameert/to_classify/flagfiles/%s/%s' %(band,model)

for count in range(1,2684):
    print count
    infile = open('%s/total_profile_%d.pickle' %(filepath, count))
    new_data = open('%s/total_profile_%d_neighbor.pickle' %(filepath, count))

    indat = pickle.load(infile)
    newdat = pickle.load(new_data)

    infile.close()
    new_data.close()
    
    for pos, val in enumerate(newdat['bt_prof']):
        if val[0][0]>0:
            indat['im_ctr'][pos]=newdat['im_ctr'][pos]
            indat['bt_prof'][pos]=newdat['bt_prof'][pos]
            indat['chi_prof'][pos]=newdat['chi_prof'][pos]

    outfile = open('%s/total_profile_%d.pickle' %(filepath, count), 'w')
    pickle.dump(indat, outfile)
    outfile.close()
