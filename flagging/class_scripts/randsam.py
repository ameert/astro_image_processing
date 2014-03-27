import random as rand
from mysql.mysql_class import *

a = range(1,2684)

rand.shuffle(a)

outfile = open('folders.txt','w')
for count in a[:86]:
    outfile.write('%d\n' %count)

outfile.close()


