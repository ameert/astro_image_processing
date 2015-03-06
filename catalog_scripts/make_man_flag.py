from mysql_class import *
import numpy as np

#model_names = ['ser','dev','highN_ser','devexp', 'serexp','highN_serexp']
model_names = ['ser','dev', 'devexp','serexp','highN_ser','highN_serexp']

for model in model_names:
	tablename = 'full_dr7_i_%s' %model


	FlagDict = dict([('GALFIT_FAIL', [15,1]),
			 ('NEIGHBOUR_FIT', [8,0]),
			 ('ERRORS_FAILED', [17,2])
			 ])

	cursor = mysql_connect('pymorph', 'pymorph', 'pymorph9455', 'shredder')

	cmd = 'update %s set Manual_flag = 0;' %tablename
	print cmd
	cursor.execute(cmd)

	for key in FlagDict.keys():
		cmd = 'update %s set Manual_flag = Manual_flag + pow(2,%d) where (flag & pow(2,%d))>0;' %(tablename, FlagDict[key][1],FlagDict[key][0]) 
		print cmd
		cursor.execute(cmd)

	OutputFlagDict = dict([('ODD_MAG', ['-2.5*log10(pow(10,-0.4*(abs(a.Ie)-a.magzp-c.aa_r-c.airmass_r*c.kk_r-c.extinction_r))+pow(10,-0.4*(abs(a.Id)-a.magzp-c.aa_r-c.airmass_r*c.kk_r-c.extinction_r))) not between 14.0 and 17.77' ,3,1]),
			    ('BAD_TARGET', ['a.num_targets > 1',4,1]),
			    ('BIG_RE_KPC', ['a.re_kpc > 40',5,1]),
			    ('BAD_RE_RD', ['a.re_pix/a.rd_pix > 1 and a.BT > .2 and a.BT < .8',6,2]),
			    ('BULGE_FIT_DISK', ['a.n < 2.5 and a.re_pix/a.rd_pix > 1.0 and a.BT< .5',7,2]),
			    ('BULGE_FIT_ALL', ['a.n < 2.5 and a.BT> .8',8,2]),
			    ('BULGE_HIGH_E', ['a.eb < 0.3 and a.BT >.2',9,1])
			    ])	                 


	for key in OutputFlagDict:
		if OutputFlagDict[key][2] ==1 or (OutputFlagDict[key][2] ==2 and (model in ['serexp','devexp'])):
			cmd = 'update %s as a, CAST as c set a.Manual_flag = a.Manual_flag + pow(2,%d) where a.galcount = c.galcount and %s;' %(tablename,OutputFlagDict[key][1],OutputFlagDict[key][0])
			print cmd
			cursor.execute(cmd)

