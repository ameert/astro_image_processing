import numpy as np
import pylab as pl
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
from cmp_functions import *

ttype, pell, ps0, psab, pscd = np.loadtxt('calib_gals.txt', unpack=True)

probs = np.array([list(pell), list(ps0), list(psab), list(pscd)]).T

perfect_t = np.array([-6, -3, 2, 8])
perfect_probs = np.array([[1.0,0.0,0.0,0.0], [0.0,1.0,0.0,0.0], [0.0,0.0,1.0,0.0], [0.0,0.0,0.0,1.0]])
#perfect_t = np.array([-6, 8])
#perfect_probs = np.array([[1.0,0.0], [0.0,1.0]])

# Split the data into training/testing sets
probs_train, probs_test, ttype_train, ttype_test = train_test_split(
    probs, ttype, test_size=0.33, random_state=42)
probs_train, probs_cross, ttype_train, ttype_cross = train_test_split(
    probs_train, ttype_train, test_size=0.33, random_state=79)

# Create linear regression object
regr = linear_model.LinearRegression(fit_intercept=False)

# Train the model using the training sets
regr.fit(probs_train, ttype_train)
bins = np.arange(-9.75, 15.251,0.5)
wbins, edges = np.histogram(ttype, bins = bins)
wdig = np.digitize(ttype, bins=bins)

w = 1.0/(wbins[wdig-1]*np.sum(np.where(wbins>0,1,0)).astype(float))

#a = np.array([[np.sum(w*pell**2*pell**2),np.sum(w*pell**2*pell),np.sum(w*pell**2*ps0),np.sum(w*pell**2*psab),np.sum(w*pell**2*pscd),np.sum(w*pell**2*pscd**2)],
#[np.sum(w*pell*pell**2),np.sum(w*pell*pell),np.sum(w*pell*ps0),np.sum(w*pell*psab),np.sum(w*pell*pscd),np.sum(w*pell*pscd**2)],
#[np.sum(w*ps0*pell**2),np.sum(w*ps0*pell),np.sum(w*ps0*ps0),np.sum(w*ps0*psab),np.sum(w*ps0*pscd),np.sum(w*ps0*pscd**2)],
#[np.sum(w*psab*pell**2),np.sum(w*psab*pell),np.sum(w*psab*ps0),np.sum(w*psab*psab),np.sum(w*psab*pscd),np.sum(w*psab*pscd**2)],
#[np.sum(w*pscd*pell**2),np.sum(w*pscd*pell),np.sum(w*pscd*ps0),np.sum(w*pscd*psab),np.sum(w*pscd*pscd),np.sum(w*pscd*pscd**2)],
#[np.sum(w*pscd**2*pell**2),np.sum(w*pscd**2*pell),np.sum(w*pscd**2*ps0),np.sum(w*pscd**2*psab),np.sum(w*pscd**2*pscd),np.sum(w*pscd**2*pscd**2)]]
#)
#a = np.array([[np.sum(w*pell*pell),np.sum(w*pell*ps0),np.sum(w*pell*psab),np.sum(w*pell*pscd)],[np.sum(w*ps0*pell),np.sum(w*ps0*ps0),np.sum(w*ps0*psab),np.sum(w*ps0*pscd)],[np.sum(w*psab*pell),np.sum(w*psab*ps0),np.sum(w*psab*psab),np.sum(w*psab*pscd)],[np.sum(w*pscd*pell),np.sum(w*pscd*ps0),np.sum(w*pscd*psab),np.sum(w*pscd*pscd)]])
              
#b = np.array([np.sum(w*ttype*pell),np.sum(w*ttype*ps0),np.sum(w*ttype*psab),np.sum(w*ttype*pscd)])
#x = np.linalg.solve(a, b)

# The coefficients
print('Coefficients: ', regr.coef_)
print('intercept: ', regr.intercept_)
# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((regr.predict(probs_cross) - ttype_cross) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(probs_cross, ttype_cross))

# The coefficients
print('Coefficients: ', regr.coef_)
print('intercept: ', regr.intercept_)
# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((regr.predict(probs_cross) - ttype_cross) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(probs_cross, ttype_cross))

# Plot outputs


#pl.xticks(())
#pl.yticks(())


#for a in zip(ttype_cross[:10], regr.predict(probs_cross[:10]),probs_cross[:10]):
#    print a


print perfect_probs
#print x




oplot = outlier_fig(figsize=(6,6))

oplot.set_ticks(2, 0.5, '%d',2, 0.5, '%d',)
oplot.setdenselims(0.01*len(perfect_probs),0.25*len(perfect_probs))
oplot.setminval(0.01*len(perfect_probs))

#oplot.makeplot(regr.predict(probs_cross), regr.predict(probs_cross)-ttype_cross,
#           (-6.5,12.0),(-10.0,10.0)) 
oplot.makeplot(ttype_cross, regr.predict(probs_cross)-ttype_cross,
           (-6.5,12.0),(-10.0,10.0)) 

pl.xlabel('Tin', fontsize=10)
pl.ylabel('Tout-Tin', fontsize=10)
oplot.bin_it(np.arange(-6.5, 12.51,1.0),-10,10)
oplot.add_bars('r')
#pl.plot(pl.xlim(), [0,0], 'k-')
#pl.title(options['title'], fontsize=8)
#oplot.savefig('%s_%s_%s_%s_%s_%s%s.eps' %(options['band'], options['table1'],options['table2'], options['model2'], options['xchoice'], options['ychoice'], options['postfix']))

pl.show()

prob_range = np.arange(0.0,1.0, 0.001)

prob_x, prob_y = np.meshgrid(prob_range, prob_range)


xflat = prob_x.view().flatten()
yflat = prob_y.view().flatten()

print xflat
print yflat

#predict = regr.predict(np.array([xflat, yflat]).T )
#predict.shape = prob_x.shape

#predict = np.where(predict<=-4, -5, predict)
#predict = np.where(np.where(predict>-4, 1,0)*np.where(predict<=0.5, 1,0), -3, predict)
#predict = np.where(np.where(predict>0.5, 1,0)*np.where(predict<=4.0, 1,0), 2, predict)
#predict = np.where(predict>4, 6, predict)


#pl.imshow(predict, vmin = -6, vmax = 10, origin='lower', extent = [prob_range[0], prob_range[-1],prob_range[0], prob_range[-1]])
#pl.colorbar()
#print predict
pl.show()

