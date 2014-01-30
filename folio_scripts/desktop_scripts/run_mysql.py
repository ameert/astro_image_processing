from mysql_funcs import *

cursor = mysql_connect('pymorph','pymorph','pymorph9455','shredder')

table = 'r_full_re_detail'
filter = 'r'

#make_big_table(table, filter, cursor, max_galcount=26153)

#update_single_tables(cursor, filter = 'r', models = ['dev'])

#load_table_main_data(table, 'r_cas', cursor, filter)

#add_bt_bd_err(cursor, ['serexp'], 're_detail_')#['dev','ser','devexp','serexp'], 're_')

#combine_models(cursor, ['dev','ser','devexp','serexp'], 're_', 'r_full_re_detail')
