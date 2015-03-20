# create table log_reg_serexp (galcount int primary key, PS float, Pn4 float, PnS float, is_ser int, is_devexp int, is_serexp int, training int, cross_val int, validation int);
# insert into log_reg_serexp (galcount, PS, Pn4, PnS) select galcount, PS, Pn4, PnS from chis2 where galcount >20000;
# update log_reg_serexp as a, sim_input as b set a.is_serexp = 1, a.is_devexp = 0, a.is_ser = 0 where a.galcount = b.simcount and (b.BT between 0.2 and 0.8) and (b.n > 2 or b.re/b.rd < 0.4) and (b.eb >0.5 or abs(b.dpa - b.bpa)>30 );
# update log_reg_serexp as a, sim_input as b set a.is_serexp = 0, a.is_devexp = 1, a.is_ser = 0 where a.galcount = b.simcount and (b.BT between 0.2 and 0.8) and (b.n > 2 or b.re/b.rd < 0.4) and (b.eb >0.5 or abs(b.dpa - b.bpa)>30 ) and(b.n between 3 and 5);
# update log_reg_serexp set is_ser = 1, is_devexp = 0, is_serexp = 0 where is_ser is null;

from mysql_class import *
import os
import numpy as np
import sys
import pylab as pl
import matplotlib.cm as cm

dba = 'simulations'
usr = 'pymorph'
pwd = 'pymorph'
cursor = mysql_connect(dba, usr, pwd)

table = 'log_reg_serexp'

def select_samples(cursor):
    for model in ['ser','devexp','serexp']:
        galcount, = cursor.get_data('select galcount from %s where is_%s = 1 order by rand();' %(table,model))
        galcount = np.array(galcount, dtype = int)
        training = np.round(len(galcount)*.5)-1
        cross_val = np.round(len(galcount)*.75)-1

        for gal in galcount[0:training]:
            cmd = 'update %s set training = 1, cross_val = 0, validation = 0 where galcount = %d;' %(table,gal)
            cursor.execute(cmd)
        for gal in galcount[training:cross_val]:
            cmd = 'update %s set training = 0, cross_val = 1, validation = 0 where galcount = %d;' %(table,gal)
            cursor.execute(cmd)
        for gal in galcount[cross_val:]:
            cmd = 'update %s set training = 0, cross_val = 0, validation = 1 where galcount = %d;' %(table,gal)
            cursor.execute(cmd)

    return

# we have already assigned samples, so this is now commented out
#select_samples(cursor)

cmd = 'select galcount,PS, PnS, Pn4, is_ser, is_devexp, is_serexp, training, cross_val, validation from %s where PS>=0 and PnS >= 0 and Pn4>=0;' %table

galcount, PS, PnS, Pn4, is_ser, is_devexp, is_serexp, training, cross_val, validation  = cursor.get_data(cmd)

galcount = np.array(galcount, dtype = int)

P_arr = np.array([PS, PnS, Pn4]).transpose()
is_arr = np.array([is_ser,is_devexp,is_serexp]).transpose()
sample = np.array([training, cross_val, validation]).transpose()

from sklearn import linear_model

train_index = np.where(sample[:,0] == 1)
train_P =  P_arr[train_index, :][0][:,0:2]
train_is_ser = is_arr[train_index,2].transpose()

print train_P.shape
print train_is_ser.shape

print train_P[:,0] 
print train_P[:,1]
print train_is_ser.flatten()

#sys.exit()


regr = linear_model.LogisticRegression()

regr.fit(train_P, train_is_ser)
print regr.coef_

print regr.score(train_P, train_is_ser)


pnS_vals = np.arange(0,1,.01)
pS_vals = np.arange(0,1,.01)

pS_grid, pnS_grid = np.meshgrid(pS_vals, pnS_vals)
print pS_grid
print pS_grid.shape

ps_flat = pS_grid.flatten()
pns_flat = pnS_grid.flatten()

test_flat = np.array([ps_flat, pns_flat]).transpose()

predictions = regr.predict(test_flat)

test_im = np.reshape(predictions, pS_grid.shape)

im = pl.imshow(test_im, interpolation='nearest', cmap=cm.YlGn,
                origin='lower', extent=[0,1,0,1],
                vmax=1, vmin=0)
pl.xlabel('pS')
pl.ylabel('pnS')
pl.scatter(train_P[:,0], train_P[:,1], s = 8,c = train_is_ser.flatten(), vmin = 0, vmax = 1, edgecolor = 'none')
pl.xlim(-0.01,1.01)
pl.ylim(-0.01,1.01)
pl.show()

