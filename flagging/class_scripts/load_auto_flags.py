from mysql_class import *
import pickle
import sys

cursor = mysql_connect('catalog','pymorph','pymorph','')

band = sys.argv[1]
model = sys.argv[2]

for folder_num in range(1, 2):#684):
    print 'folder %d' %folder_num
    print '/home/ameert/to_classify/flagfiles/%s/%s/autoflags_%d_revised.pickle' %(band,model,folder_num)
    infile = open('/home/ameert/to_classify/flagfiles/%s/%s/autoflags_%d_revised.pickle' %(band,model,folder_num))
    data = pickle.load(infile)
    infile.close()

    #print zip(data['galcount'], data['autoflags'])

    for galcount,flagval in zip(data['galcount'], data['autoflags']):
        cmd = """update {table} set flag = {finalval} where galcount = {galcount} and band = '{band}' and model = '{model}' and ftype = 'x';""".format(table = 'Flags_optimize', finalval = flagval, band=band, model=model, galcount = galcount)
        #print cmd
        cursor.execute(cmd)
                    
