import os

for band in 'r':
    for model in ['dev','ser','devexp','serexp']:
        for count in range(1,2684):
            print "file number: %d" %count
            os.system('python create_flag_file_catalog.py %d %s %s' %(count, model, band))


