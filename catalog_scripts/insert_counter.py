from mysql_class import *

cursor = mysql_connect('pymorph', 'pymorph', 'pymorph9455', 'shredder')

galcount, = cursor.get_data('select galcount from CAST_incomplete order by galcount;')

cat_count = 1
count = 0

for a in galcount:
    count +=1
    cursor.execute('update CAST_incomplete set cat_count = %d where galcount = %d;' %(cat_count, a))

    if count == 250:
        cat_count +=1
        count = 0

    
