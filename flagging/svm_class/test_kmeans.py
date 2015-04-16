from sklearn import cluster, datasets
import pylab as pl
from mysql_class import *

iris = datasets.load_iris()
X_iris = iris.data
y_iris = iris.target

k_means = cluster.KMeans(n_clusters=3)
k_means.fit(X_iris)


dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

cmd = 'select a.galcount, a.n, b.n, b.BT, c.ProbaE from full_dr7_r_ser as a,full_dr7_r_serexp as b, M2010 as c where b.galcount = a.galcount and c.galcount = a.galcount and c.ProbaEll > .5 and (a.n between 0 and 7.9) and (b.n between 0 and 7.9) order by rand() limit 4000;'

galcount, n_ser, n_serexp, BT, pEll = cursor.get_data(cmd)


X_data = zip(n_serexp, BT, n_ser, pEll)
X_data_arr = np.array(X_data)
means = np.mean(X_data_arr, axis = 0)
print X_data_arr
print means
X_data_arr -= means
print X_data_arr
std = np.std(X_data_arr, axis = 0)
X_data_arr /= std
print X_data_arr


kmeans = cluster.KMeans(n_clusters = 4)
kmeans.fit(X_data_arr)
Z = kmeans.predict(X_data_arr)

pl.subplot(231)
pl.scatter(n_ser, n_serexp, c = Z)
pl.xlabel('n_ser')
pl.ylabel('n_serexp')

pl.subplot(232)
pl.scatter(n_ser, BT, c = Z)
pl.xlabel('n_ser')
pl.ylabel('BT')

pl.subplot(233)
pl.scatter(n_ser, pEll, c = Z)
pl.xlabel('n_ser')
pl.ylabel('pEll')

pl.subplot(234)
pl.scatter(n_serexp, BT, c = Z)
pl.xlabel('n_serexp')
pl.ylabel('BT')

pl.subplot(235)
pl.scatter(n_serexp, pEll, c = Z)
pl.xlabel('n_serexp')
pl.ylabel('pEll')

pl.subplot(236)
pl.scatter(BT, pEll, c = Z)
pl.xlabel('BT')
pl.ylabel('pEll')

pl.show()




