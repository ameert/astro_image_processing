#!/data2/home/ameert/python/bin/python2.5

import os
import sys

band  = sys.argv[1]
count = int(sys.argv[2])
#model = sys.argv[3]

path = '/data2/home/ameert/catalog/%s/fits/' %band
    
for model in ['dev','ser','devexp','serexp','masks']:
    merge_in = '%s/%s/%04d/' %(path, model, count)
    merge_out = '%s/rerun/%s/%04d/' %(path, model, count)

    if model == 'masks':
        files_to_move = ['[E,M]*.fits']
    else:
        files_to_move =  ['*.in', '*.out', '*.con', 'sex*.txt']

    for fname in files_to_move:
        os.system('mv %s/%s %s' %(merge_out, fname,merge_in))
        print 'mv %s/%s %s' %(merge_out, fname,merge_in)
    os.system('rm %s*' %(merge_out))
    print 'rm %s*' %(merge_out)



