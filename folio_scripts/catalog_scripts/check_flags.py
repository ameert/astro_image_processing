from mysql_class import *
import numpy as np

model = 'dev'
tablename = 'full_dr7_r_flags_%s' %model

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

cmd = 'select galcount, old_flag, old_fitflag, flag, fitflag from %s ;' %tablename
print cmd
galcount, flag_old, fitflag_old, flag, fitflag = cursor.get_data(cmd)

for gc, fo, ffo, f, ff in zip(galcount, flag_old, fitflag_old, flag, fitflag):
    for key in FlagDict:
        if ((2**FlagDict[key][0]) & fo)>0:
            if ((2**FlagDict[key][1]) & f) == 0:
                print '%d bad unset flag %s' %(gc, key)
        elif ((2**FlagDict[key][0]) & fo)==0:
            if ((2**FlagDict[key][1]) & f) > 0:
                print '%d bad set flag %s' %(gc, key)

    for key in FitFlagDict:
        if ((2**FitFlagDict[key][0]) & ffo)>0:
            if ((2**FitFlagDict[key][1]) & ff) == 0:
                print '%d bad unset fitflag %s' %(gc, key)
        elif ((2**FitFlagDict[key][0]) & ffo)==0:
            if ((2**FitFlagDict[key][1]) & ff) > 0:
                print '%d bad set fitflag %s' %(gc, key)

        
