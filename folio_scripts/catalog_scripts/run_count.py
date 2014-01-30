import sys
import os


start = int(sys.argv[1])
end  =int(sys.argv[2])

for count in range(start, end):
    print count
    os.system('python2.5 count_neighbors.py new_new_neighborcount ser r %d' %count)
    
#full_exp_neighborcount
