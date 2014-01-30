import numpy as np
import pylab
from mysql_class import *
from MatplotRc import *


dba = 'pymorph'
usr = 'pymorph'
pwd = 'pymorph9455'
host = 'shredder'
cursor = mysql_connect(dba, usr, pwd, host)

models = ['serexp']#['dev', 'ser']#['devexp', 'serexp']

for model in models:
    r_full_cmd = 'select galcount, Ie_%s, Id_%s, re_pix_%s, rd_pix_%s, n_%s, BT_%s, GalSky_%s from r_full where fit_%s > 0 and Ie_%s and re_pix_%s > 0 ;' %( model, model, model, model, model, model, model, model, model, model)
#, model     and rd_pix_%s > 0
    r_mod_cmd = 'select Name, Ie, Id, re_pix, rd_pix, n, BT, GalSky from combined_detail where fit >0 and Ie > 0 and re_pix > 0;'
# and rd_pix > 0
    Name, Ie_mod, Id_mod, re_pix_mod, rd_pix_mod, n_mod, BT_mod, GalSky_mod = cursor.get_data(r_mod_cmd)

    galcount, Ie_old, Id_old, re_pix_old, rd_pix_old, n_old, BT_old, GalSky_old = cursor.get_data(r_full_cmd)


    galcount = np.array(galcount)

    
    Name_clean = []
    Ie_mod_clean = []
    Id_mod_clean = []
    re_pix_mod_clean = []
    rd_pix_mod_clean = []
    n_mod_clean = []
    BT_mod_clean = []
    GalSky_mod_clean = []
    galcount_clean = []
    Ie_old_clean = []
    Id_old_clean = []
    re_pix_old_clean = []
    rd_pix_old_clean = []
    n_old_clean = []
    BT_old_clean = []
    GalSky_old_clean = []


    for Name1, Ie_mod1, Id_mod1, re_pix_mod1, rd_pix_mod1, n_mod1, BT_mod1, GalSky_mod1 in zip(Name, Ie_mod, Id_mod, re_pix_mod, rd_pix_mod, n_mod, BT_mod, GalSky_mod):
        tmp_count = int(Name1.split('_')[0])
        tmp_loc = np.where(galcount == tmp_count)
        tmp_loc = tmp_loc[0]
        if tmp_loc != -1:
                Name_clean.append(Name1)
                Ie_mod_clean.append(Ie_mod1)
                Id_mod_clean.append(Id_mod1)
                re_pix_mod_clean.append(re_pix_mod1)
                rd_pix_mod_clean.append(rd_pix_mod1)
                n_mod_clean.append(n_mod1)
                BT_mod_clean.append(BT_mod1)
                GalSky_mod_clean.append(GalSky_mod1)
                galcount_clean.append(galcount[tmp_loc])
                Ie_old_clean.append(Ie_old[tmp_loc])
                Id_old_clean.append(Id_old[tmp_loc])
                re_pix_old_clean.append(re_pix_old[tmp_loc])
                rd_pix_old_clean.append(rd_pix_old[tmp_loc])
                n_old_clean.append(n_old[tmp_loc])
                BT_old_clean.append(BT_old[tmp_loc])
                GalSky_old_clean.append(GalSky_old[tmp_loc])


    matrc1()
    pylab.scatter(Ie_old_clean, Ie_mod_clean, s=1)
    pylab.title("Ie")
    pylab.xlabel('old')
    pylab.ylabel('new')
    pylab.savefig("ie_%s.png" %(model), format = 'png')
    pylab.clf()
    
    pylab.scatter(Id_old_clean, Id_mod_clean, s=1)
    pylab.title("Id")
    pylab.xlabel('old')
    pylab.ylabel('new')
    pylab.savefig("id_%s.png" %(model), format = 'png')
    pylab.clf()
   

    pylab.scatter(re_pix_old_clean, re_pix_mod_clean, s=1)
    pylab.xlim([.01, np.max(re_pix_old_clean)])
    pylab.ylim([.01, np.max(re_pix_mod_clean)])
    pylab.xscale('log') 
    pylab.yscale('log') 
    pylab.title("re")
    pylab.xlabel('old')
    pylab.ylabel('new')
    pylab.savefig("re_%s.png" %(model), format = 'png')
    pylab.clf()
   
    try:
        pylab.scatter(rd_pix_old_clean, rd_pix_mod_clean, s=1)
        pylab.xlim([.01, np.max(rd_pix_old_clean)])
        pylab.ylim([.01, np.max(rd_pix_mod_clean)])
        pylab.xscale('log') 
        pylab.yscale('log') 
        pylab.title("rd")
        pylab.xlabel('old')
        pylab.ylabel('new')
        pylab.savefig("rd_%s.png" %(model), format = 'png')
    except:
        pass
    pylab.clf()
   

    pylab.scatter(n_old_clean, n_mod_clean, s=1)
    pylab.title("n")
    pylab.xlabel('old')
    pylab.ylabel('new')
    pylab.savefig("n_%s.png" %(model), format = 'png')
    pylab.clf()
   

    pylab.scatter(BT_old_clean, BT_mod_clean, s=1)
    pylab.title("BT")
    pylab.xlabel('old')
    pylab.ylabel('new')
    pylab.savefig("BT_%s.png" %(model), format = 'png')
    pylab.clf()
   

    pylab.scatter(GalSky_old_clean, GalSky_mod_clean, s=1)
    pylab.title("galsky")
    pylab.xlabel('old')
    pylab.ylabel('new')
    pylab.savefig("galsky_%s.png" %(model), format = 'png')
    pylab.clf()
   
    






del(cursor)
