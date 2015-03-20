from mysql_class import *

cursor = mysql_connect('pymorph', 'pymorph', 'pymorph9455', 'shredder')

model = 'ser'

galcount, hrad = cursor.get_data('select galcount, alan_hrad_pix from full_dr7_r_%s where alan_hrad_pix < 0 order by galcount;' %model)

a = open('%s_count.txt' %model,'w')

#for count in range(1,200001):
#    if count not in galcount:
#        a.write('%d\n' %count)

for count in galcount:
    a.write('%d\n' %count)
    
a.close()


