from mysql_class import * 
import sys

cursor = mysql_connect('pymorph', 'pymorph','pymorph9455', 'shredder')

table_nm = 'CASGM_r_agmresult'
filestem = 'agm_result_with_radius.csv'

o_ent_str = 'insert ignore into '+table_nm+" "

ocols = ['Name','C','C_err','A','A_err','A_flag','image_A','back_A','A_20','A_20_with_zsum',
            'S','S_err','r20','r20e','r50','r50e','r80','r80e','r90','r90e','extraction_radius','G',
            'G_res','G80','G50','G20','M','M_res','M80','M50','M20']


for folder_num in range(100,2684):
    print folder_num
    filename = '/data2/home/ameert/catalog/r/fits/CASGM/dev/%04d/%s' %(folder_num, filestem)
    infile = open(filename)

    tcols = infile.readline()

    cols_to_str = [0]

    cols = ','.join(ocols)

    curr_ent_str = o_ent_str+'('+cols+') Values ('

    for line in infile.readlines():
        line = line.replace('-nan', '-99.99')
        line = line.replace('-inf', '-99.99')
        line = line.replace('nan', '-99.99')
        line = line.replace('inf', '-99.99')
        line = line.replace('--', '-88.88')
        line = line.split(',')
        for cc in cols_to_str:
            line[cc] = "'" + line[cc] + "'"

        cmd = curr_ent_str + ','.join(line) + ');'
        #print cmd
        cursor.execute(cmd)


    infile.close()
    
        
