from mysql_class import *
import numpy as np

model = 'serexp'
tablename = 'full_dr7_r_%s' %model


FlagDict = dict([('REPEAT', [0,0]),
		 ('FIT_BULGE_CNTR', [1,1]),
		 ('FIT_DISK_CNTR', [2,2]),
		 ('FIT_SKY', [3,5]),
		 ('EXCEED_SIZE', [4,9]),
		 ('ELLIPSE_FAIL', [5,13]),
		 ('CASGM_FAIL', [6,14]),
		 ('GALFIT_FAIL', [7,15]),
		 ('PLOT_FAIL', [8,16]),
		 ('FIT_BULGE', [9,3]),
		 ('FIT_DISK', [10,4]),
		 ('FIT_POINT', [11,6]),
		 ('NEIGHBOUR_FIT', [12,8]),
		 ('ASYM_NOT_CONV', [13,11]),
		 ('ASYM_OUT_FRAME', [14,12]),
		 ('FIT_BAR', [15,7]),
		 ('ERRORS_FAILED', [16,17]),
		 ('AVGIE_FAILED', [17,18]),
		 ('NO_TARGET', [18,10]),
		 ('BACK_FAILED', [20,19]),
		 ('DETAIL_FAILED', [21,20]),
		 ])

FitFlagDict = dict([('LARGE_CHISQ', [0,0]),
		    ('SMALL_GOODNESS', [1,1]),
		    ('FAKE_CNTR', [2,2]),
		    ('IE_AT_LIMIT', [3,3]),
		    ('ID_AT_LIMIT', [4,4]),
		    ('RERD_AT_LIMIT', [6,5]),
		    ('BT_AT_LIMIT', [7,6]),
		    ('N_AT_LIMIT', [8,7]),
		    ('RE_AT_LIMIT', [9,8]),
		    ('RD_AT_LIMIT', [10,9]),
		    ('EB_AT_LIMIT', [11,10]),
		    ('ED_AT_LIMIT', [12,11])
		    ])	                 

cursor = mysql_connect('pymorph', 'pymorph', 'pymorph9455', 'shredder')

cmds = ['alter table %s add column tmp_flag bigint;'%tablename,
       'update %s set tmp_flag = 0;' %tablename,
       'alter table %s add column tmp_fitflag bigint;'%tablename,
       'update %s set tmp_fitflag = 0;' %tablename]
for cmd in cmds:
	print cmd
	cursor.execute(cmd)

for key in FlagDict.keys():
	cmd = 'update %s set tmp_flag = tmp_flag + pow(2,%d) where flag & pow(2,%d);' %(tablename, FlagDict[key][1],FlagDict[key][0]) 
	print cmd
	cursor.execute(cmd)

for key in FitFlagDict.keys():
	cmd = 'update %s set tmp_fitflag = tmp_fitflag + pow(2,%d) where fitflag & pow(2,%d);' %(tablename, FitFlagDict[key][1],FitFlagDict[key][0]) 
	print cmd
	cursor.execute(cmd)

cmds = ['update %s set flag = tmp_flag;' %tablename,
       'update %s set fitflag = tmp_fitflag;' %tablename,
	'alter table %s drop column tmp_flag;'%tablename,
	'alter table %s drop column tmp_fitflag;'%tablename]
for cmd in cmds:
	print cmd
	cursor.execute(cmd)
