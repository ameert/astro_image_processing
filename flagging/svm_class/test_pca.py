from sklearn import decomposition
import pylab as pl
from mysql_class import *

dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

cmd = 'select a.galcount, a.n, a.re_pix, b.n, b.BT, b.re_pix/b.rd_pix, c.ProbaE from full_dr7_r_ser as a,full_dr7_r_serexp as b, M2010 as c where b.galcount = a.galcount and c.galcount = a.galcount and (a.n between 0 and 7.9) and (b.n between 0 and 7.9) order by rand() limit 4000;'

galcount, n_ser, re_ser, n_serexp, BT, rerd_serexp, pE  = cursor.get_data(cmd)

X_data = zip(n_ser, n_serexp, BT, list(np.array(rerd_serexp)),  pE)
X_data_arr = np.array(X_data)
means = np.mean(X_data_arr, axis = 0)
print X_data_arr
print means
X_data_arr -= means
print X_data_arr
std = np.std(X_data_arr, axis = 0)
X_data_arr /= std
print X_data_arr

pca = decomposition.PCA()
pca.fit(X_data_arr)


print pca.explained_variance_
for count in range(0,5):
    pl.plot( pca.components_[count], label ='com %d' %count)
pl.legend()
pl.xticks(range(0, 5), ['n_s', 'n_se', 'BT', 'rerd_se', 'PE'])
pl.show()


pca.n_components = 2
X_reduced = pca.fit_transform(X_data_arr)

X_reduced.shape

