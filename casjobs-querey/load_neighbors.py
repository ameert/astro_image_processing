#!/usr/bin/python

from mysql_class import *
import numpy as np
from load_table import *

infile = '../neighbor_info_upenn_pymorph.csv'
table_name = 'CAST_neighbors'

cursor = mysql_connect('catalog', 'pymorph', 'pymorph')

columns = ['galcount','distance','objid',
'ra_gal','dec_gal','ModelMag_r','ModelMagErr_r',
'fracdev_r','petroMag_r','petroMagErr_r','petroR90_r',
'petroR50_g','petroR50_r','extinction_r','rowc_r','colc_r']

column_types = ['int ','float ','bigint primary key', 
'float','float','float','float',
'float','float','float','float',
'float','float','float','float','float']

load_table(cursor, table_name, infile, columns, column_types, make_table=0)

