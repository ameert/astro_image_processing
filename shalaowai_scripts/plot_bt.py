#!/usr/bin/python

import numpy as np
import pyfits as pf
import pylab as pl
import pickle
import sys
import os

sys.path.append('/home/ameert/alans-image-processing-pipeline')
sys.path.append('/home/ameert/shalaowai_package')

from flag_defs import *
from mysql import *

galcount = int(sys.argv[1])

try:
    models = [a for a in sys.argv[2:]]
except:
    sys.exit()

cursor = mysql_connect('catalog','pymorph','pymorph','localhost')

uname = 'alan'

for model in models:
    folder_num = (galcount-1)/250 +1
    
    outfile = '/home/ameert/public_html/fit_catalog/plot_dir/%08d_%s_BT_chi_profile_%s.png' %(galcount, model, uname)
    
    if not os.path.isfile(outfile):
        proffile = '/home/ameert/public_html/fit_catalog/data_dir/total_profile_%s_%d.pickle' %(model,folder_num)
        if not os.path.isfile(proffile):
            os.system('scp ameert@chitou.physics.upenn.edu:/home/ameert/to_classify/flagfiles/%s/total_profile_%d.pickle %s' %(model, folder_num, proffile))

        infile = open(proffile)
        inprofs = pickle.load(infile)
        infile.close()

        inprofs_pos= np.where(np.array(inprofs['galcount'], dtype=int)==galcount)[0][0]


        fig = pl.figure(figsize=(8.0,6.0))
        pl.subplots_adjust(left = 0.35, wspace = .5, hspace = .5)
        pl.figtext(0.5, 0.97, '%08d %s' %(galcount,model), ha='center')

        top = .8

        newcolormap = pl.get_cmap('jet')

        pl.subplot(2,1,1)
        pl.plot(inprofs['bt_prof'][inprofs_pos][0], inprofs['bt_prof'][inprofs_pos][1], 'b:', linewidth=1, label = 'bt rad')
        pl.plot(inprofs['bt_prof'][inprofs_pos][0], inprofs['bt_prof'][inprofs_pos][2], 'b--', linewidth=1, label = 'bt_cum')
        pl.plot(inprofs['bt_prof'][inprofs_pos][0], inprofs['bt_prof'][inprofs_pos][3], 'b-', linewidth=1, label = 'tot light')
        pl.legend(loc = 'center',  bbox_to_anchor = (-0.4, 1.0))
        pl.title('BT')
        pl.ylim(0,1.0)
        pl.xlim(0, 6.0)
        pl.ylabel('BT')
        pl.xlabel('r/hrad')


        pl.subplot(2,1,2)
        pl.plot(inprofs['chi_prof'][inprofs_pos][0], inprofs['chi_prof'][inprofs_pos][1], 'b-', linewidth=1)
        pl.title('$\chi^2$')
        pl.ylim(0,10.0)
        pl.xlim(0, 6.0)
        pl.ylabel('$\chi^2$')
        pl.xlabel('r/hrad')

        hor_al = 0.12
        top = .7
        pl.figtext(hor_al, top, 'auto flag', ha='center', size='large')
        top -= 0.03


        cmd = """select a.flag from Flags_optimize as a where a.band = 'r' and a.model = '{model}' and a.ftype = 'r' and a.galcount =  {galcount};""".format(model=model, galcount = galcount) 
        fflags, = cursor.get_data(cmd)
        ff = fflags[0]

        if ff >= 0:
            for curr_flag in ([('no fitflags', -1)]+new_finalflag_vals):
                if check_flags(ff, curr_flag[1]):
                    pl.figtext(hor_al, top, curr_flag[0], ha='center', size='x-small')
                    top -= 0.03
        else:
            pl.figtext(hor_al, top, 'NOT CLASSIFIED', ha='center', size='x-small')



        pl.savefig(outfile)
        pl.clf()

