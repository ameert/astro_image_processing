import numpy as np
import pylab as pl
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
from sklearn import neighbors
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.naive_bayes import GaussianNB

ttype, pell, ps0, psab, pscd = np.loadtxt('calib_gals.txt', unpack=True)

probs = np.array([list(pell), list(ps0), list(psab), list(pscd)]).T


# Split the data into training/testing sets
probs_train, probs_test, ttype_train, ttype_test = train_test_split(
    probs, ttype, test_size=0.33, random_state=42)

n_neighbors = 200
weights= 'uniform' #'distance' #

regr = GaussianNB()
#regr=NearestCentroid()
#regr = neighbors.KNeighborsRegressor(n_neighbors, weights=weights)
regr.fit(probs_train, ttype_train)

# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((regr.predict(probs_test) - ttype_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(probs_test, ttype_test))

# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((regr.predict(probs_test) - ttype_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(probs_test, ttype_test))

# Plot outputs
perfect_t = np.array([-6, -3, 2, 8])
perfect_probs = np.array([[1.0,0.0,0.0,0.0], [0.0,1.0,0.0,0.0], [0.0,0.0,1.0,0.0], [0.0,0.0,0.0,1.0]])


#pl.xticks(())
#pl.yticks(())


#for a in zip(ttype_test[:10], regr.predict(probs_test[:10]),probs_test[:10]):
#    print a


print perfect_probs
#print x

pl.scatter(ttype_test, regr.predict(probs_test), s=2, edgecolor='none',
           color='black')
pl.plot(perfect_t, regr.predict(perfect_probs),  color='blue', linewidth=3)
#pl.plot(perfect_t, np.sum(perfect_probs*x,axis=1),  color='g', linewidth=3)
pl.plot([-10,10],[-10,10], 'r')
pl.show()
