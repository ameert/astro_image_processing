from mysql_class import *
from load_table import load_table

cursor = mysql_connect('MB','pymorph','pymorph')

model={1:'ser', 2:'devexp', 3:'serexp', 4:'simard_ser', 
       5:'simard_devexp', 6:'simard_serexp'}

columns = ['galcount', 'ra_gal', 'dec_gal']

column_types = ['int', 'float', 'float']

for count in range(1,7):
    tablename = 'old_bcg_'+model[count]
    filename = '/scratch/MB_BCGs/tbcg_%d.txt' %count
    load_table(cursor, tablename, filename, columns, column_types, delimiter = ' ', make_table = 1)
