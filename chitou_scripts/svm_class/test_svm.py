from sklearn import svm
import pylab as pl
from mysql_class import *
from sklearn.metrics import classification_report
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import precision_recall_curve
import numpy as np
from svm_functs import *
from matplotlib import cm

dba = 'simulations'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

X_test_arr, X_test_uncorr, y_test, mean, std, galcount = fetch_data(cursor, 1, mean = None, std = None)

clf = svm.SVC(kernel='rbf',probability=True)#, C = 1000, gamma=0.01 )
clf.fit(X_test_arr, y_test) 

X_eval_arr,X_eval_uncorr,y_eval,mj,sj, galcount = fetch_data(cursor,3,mean = mean,std = std)

prediction  = clf.predict(X_eval_arr)
prediction_prob  = clf.predict_proba(X_eval_arr)
print "score: ", clf.score(X_eval_arr, y_eval)

true_serexp = np.extract(y_eval==1, prediction)
true_ser = np.extract(y_eval==0, prediction)
 
true_serexp_prob = np.extract(y_eval==1, prediction_prob[:,1]).flatten()
true_ser_prob = np.extract(y_eval==0, prediction_prob[:,0]).flatten()
true_serexp_BT = np.extract(y_eval==1, X_eval_uncorr[:,7]).flatten()
true_ser_BT = np.extract(y_eval==0, X_eval_uncorr[:,7]).flatten()
true_serexp_nser = np.extract(y_eval==1, X_eval_uncorr[:,0]).flatten()
true_ser_nser = np.extract(y_eval==0, X_eval_uncorr[:,0]).flatten()

target_names = ['Ser', 'SerExp']
print(classification_report(y_eval, prediction, target_names=target_names))
print matthews_corrcoef(y_eval, prediction) 
precision, recall, threshold = precision_recall_curve(y_eval, prediction_prob[:,1])
print precision[:-1], precision.shape
print recall[:-1], recall.shape
print threshold, threshold.shape

pl.plot(threshold, recall[:-1], c = 'b', label = 'recall')
pl.plot(threshold, precision[:-1], c = 'g', label = 'precision')
pl.xlim(0,1)
pl.ylim(0,1)
pl.legend(loc = 3)
pl.show()

pl.subplot(2,2,1)
pl.hist(true_serexp_prob, range = (0,1), bins = 20, normed = True)
pl.xlabel('P(serexp)')
pl.ylabel('n')
pl.title('P(serexp) pdf for SerExp')
pl.subplot(2,2,3)
pl.hist(true_serexp_prob, range = (0,1), bins = 20, normed = True, cumulative = True)
pl.xlabel('P(serexp)')
pl.ylabel('n')
pl.title('P(serexp) cdf for SerExp')

pl.subplot(2,2,2)
pl.hist(true_ser_prob, range = (0,1), bins = 20, normed = True)
pl.xlabel('P(ser)')
pl.ylabel('n')
pl.title('P(ser) pdf for Ser')
pl.subplot(2,2,4)
pl.hist(true_ser_prob, range = (0,1), bins = 20, normed = True, cumulative = True)
pl.xlabel('P(ser)')
pl.ylabel('n')
pl.title('P(ser) cdf for Ser')
pl.show()


pl.subplot(2,1,1)
pl.scatter(true_serexp_BT,true_serexp_prob, s = 4, edgecolor = 'none')#, c = true_serexp_nser, vmin = 0, vmax = 1)
pl.ylabel('P(serexp)')
pl.xlabel('BT')
pl.title('P(serexp) vs BT SerExp')
pl.xlim(0,1)
pl.ylim(0,1)

pl.subplot(2,1,2)
pl.scatter(true_ser_BT,true_ser_prob, s = 4, edgecolor = 'none')#, c = true_serexp_nser, vmin = 0, vmax = 1)
pl.ylabel('P(ser)')
pl.xlabel('BT')
pl.title('P(ser) vs BT Ser')
pl.xlim(0,1)
pl.ylim(0,1)
pl.show()

serexp_bt = np.extract(prediction ==1, X_eval_uncorr[:,7])
serexp_nser = np.extract(prediction ==1, X_eval_uncorr[:,0])
serexp_btDevexp = np.extract(prediction ==1, X_eval_uncorr[:,1])

ser_bt = np.extract(prediction ==0, X_eval_uncorr[:,7])
ser_nser = np.extract(prediction ==0, X_eval_uncorr[:,0])
ser_btDevexp = np.extract(prediction ==0, X_eval_uncorr[:,1])

pl.subplot(3,3,1)
pl.hist(serexp_bt, range = (0,1), bins = 20, histtype = 'step', color = 'b', normed = True)
pl.hist(ser_bt, range = (0,1), bins = 20, histtype = 'step', color = 'g', normed = True)
pl.xlabel('BT_serexp')
pl.ylabel('n')
pl.title('BT pdf for all by pclass')

pl.subplot(3,3,2)
pl.hist(serexp_nser, range = (0,8), bins = 16, histtype = 'step', color = 'b', normed = True)
pl.hist(ser_nser, range = (0,8), bins = 16, histtype = 'step', color = 'g', normed = True)
pl.xlabel('n_ser')
pl.ylabel('n')
pl.title('n_ser pdf for all by pclass')

pl.subplot(3,3,3)
pl.hist(serexp_btDevexp, range = (0,1), bins = 20, histtype = 'step', color = 'b', normed = True)
pl.hist(ser_btDevexp, range = (0,1), bins = 20, histtype = 'step', color = 'g', normed = True)
pl.xlabel('BT_devexp')
pl.ylabel('n')
pl.title('BT pdf for all by pclass')

serexp_bt = np.extract((prediction ==1)*((prediction - y_eval) ==0), X_eval_uncorr[:,7])
serexp_nser = np.extract((prediction ==1)*((prediction - y_eval) ==0), X_eval_uncorr[:,0])
serexp_btDevexp = np.extract((prediction ==1)*((prediction - y_eval) ==0), X_eval_uncorr[:,1])

ser_bt = np.extract((prediction ==0)*((prediction - y_eval) ==0), X_eval_uncorr[:,7])
ser_nser = np.extract((prediction ==0)*((prediction - y_eval) ==0), X_eval_uncorr[:,0])
ser_btDevexp = np.extract((prediction ==0)*((prediction - y_eval) ==0), X_eval_uncorr[:,1])

pl.subplot(3,3,4)
pl.hist(serexp_bt, range = (0,1), bins = 20, histtype = 'step', color = 'b', normed = True)
pl.hist(ser_bt, range = (0,1), bins = 20, histtype = 'step', color = 'g', normed = True)
pl.xlabel('BT_serexp')
pl.ylabel('n')
pl.title('BT pdf for true by pclass')

pl.subplot(3,3,5)
pl.hist(serexp_nser, range = (0,8), bins = 16, histtype = 'step', color = 'b', normed = True)
pl.hist(ser_nser, range = (0,8), bins = 16, histtype = 'step', color = 'g', normed = True)
pl.xlabel('n_ser')
pl.ylabel('n')
pl.title('n_ser pdf for true by pclass')

pl.subplot(3,3,6)
pl.hist(serexp_btDevexp, range = (0,1), bins = 20, histtype = 'step', color = 'b', normed = True)
pl.hist(ser_btDevexp, range = (0,1), bins = 20, histtype = 'step', color = 'g', normed = True)
pl.xlabel('BT_devexp')
pl.ylabel('n')
pl.title('BT pdf for true by pclass')

serexp_bt = np.extract((prediction ==1)*((prediction - y_eval) != 0), X_eval_uncorr[:,7])
serexp_nser = np.extract((prediction ==1)*((prediction - y_eval) != 0), X_eval_uncorr[:,0])
serexp_btDevexp = np.extract((prediction ==1)*((prediction - y_eval) != 0), X_eval_uncorr[:,1])

ser_bt = np.extract((prediction ==0)*((prediction - y_eval) !=0), X_eval_uncorr[:,7])
ser_nser = np.extract((prediction ==0)*((prediction - y_eval) !=0), X_eval_uncorr[:,0])
ser_btDevexp = np.extract((prediction ==0)*((prediction - y_eval) !=0), X_eval_uncorr[:,1])

pl.subplot(3,3,7)
pl.hist(serexp_bt, range = (0,1), bins = 20, histtype = 'step', color = 'b', normed = True)
pl.hist(ser_bt, range = (0,1), bins = 20, histtype = 'step', color = 'g', normed = True)
pl.xlabel('BT_serexp')
pl.ylabel('n')
pl.title('BT pdf for false by pclass')

pl.subplot(3,3,8)
pl.hist(serexp_nser, range = (0,8), bins = 16, histtype = 'step', color = 'b', normed = True)
pl.hist(ser_nser, range = (0,8), bins = 16, histtype = 'step', color = 'g', normed = True)
pl.xlabel('n_ser')
pl.ylabel('n')
pl.title('n_ser pdf for false by pclass')

pl.subplot(3,3,9)
pl.hist(serexp_btDevexp, range = (0,1), bins = 20, histtype = 'step', color = 'b', normed = True)
pl.hist(ser_btDevexp, range = (0,1), bins = 20, histtype = 'step', color = 'g', normed = True)
pl.xlabel('BT_devexp')
pl.ylabel('n')
pl.title('BT pdf for false by pclass')

pl.subplots_adjust(left = 0.07, 
                      right = 0.97,
                      bottom = 0.1,
                      top = 0.95,   
                      wspace = 0.25, 
                      hspace = 0.25) 

pl.show()

X_nair_arr,X_nair_uncorr,y_nair,mj,sj, galcount = fetch_data_nair(cursor,mean = mean,std = std)
prediction_nair  = clf.predict(X_nair_arr)
prediction_prob_nair  = clf.predict_proba(X_nair_arr)

print y_nair.shape
type_spread = y_nair - 0.5*(np.random.rand(y_nair.shape[0]) - 0.5)

pl.subplots_adjust(left = 0.09, 
                      right = 0.95,
                      bottom = 0.1,
                      top = 0.95,   
                      wspace = 0.25, 
                      hspace = 0.4) 

pl.subplot(2,1,1)
pl.scatter(type_spread,prediction_prob_nair[:,1], s = 4, edgecolor = 'none', c =X_nair_uncorr[:,7] , vmin = 0, vmax = 1)
pl.ylabel('P(serexp)')
pl.xlabel('Ttype')
pl.title('P(serexp) vs Nair Ttype colored by BT')
pl.xlim(-6,11)
pl.ylim(0,1)
pl.colorbar()

pl.subplot(2,1,2)
pl.scatter(X_nair_uncorr[:,7],prediction_prob_nair[:,1], s = 4, edgecolor = 'none', c = y_nair, vmin = -5, vmax = 10, cmap = cm.jet_r)
pl.ylabel('P(serexp)')
pl.title('P(serexp) vs BT(serexp) colored by type')
pl.xlabel('BT')
pl.colorbar()


output = np.array([ -452.90002401,1364.31502333,-1677.8076632,
                     1075.92230354,-382.59809833,72.53241043,-5.14678387])
p = np.poly1d(output)

bt_out = np.arange(0.1, 0.801, 0.001)

yvals_out =p(bt_out)

pl.plot(bt_out, yvals_out, 'k-')



pl.xlim(0,1)
pl.ylim(0,1)




#bt =   [0.8,0.75,0.7,0.6,0.55,0.5, 0.4,0.3,0.2, 0.15]
#prob = [0.0,0.2 ,0.4,0.55,0.60,0.65,0.7,0.6,0.4, 0.0 ]
#pl.plot(bt, prob, 'k-', lw = 6)


pl.show()







