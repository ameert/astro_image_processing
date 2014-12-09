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
prediction_prob  = clf.predict_proba(X_test_arr)
prediction  = clf.predict(X_test_arr)

for gal, prob, predict in zip(galcount, prediction_prob, prediction):
    cmd = 'update simulations.svm_probs set p_ser = %f, p_serexp = %f, ser_serexp_choice = %d where galcount = %d;' %(prob[0], prob[1], predict, gal)
    cursor.execute(cmd)

X_eval_arr,X_eval_uncorr,y_eval,mj,sj, galcount = fetch_data(cursor,2,mean = mean,std = std)
prediction_prob  = clf.predict_proba(X_eval_arr)
prediction  = clf.predict(X_eval_arr)

for gal, prob, predict in zip(galcount, prediction_prob, prediction):
    cmd = 'update simulations.svm_probs set p_ser = %f, p_serexp = %f, ser_serexp_choice = %d where galcount = %d;' %(prob[0], prob[1], predict, gal)
    cursor.execute(cmd)

X_eval_arr,X_eval_uncorr,y_eval,mj,sj, galcount = fetch_data(cursor,3,mean = mean,std = std)
prediction_prob  = clf.predict_proba(X_eval_arr)
prediction  = clf.predict(X_eval_arr)

for gal, prob, predict in zip(galcount, prediction_prob, prediction):
    cmd = 'update simulations.svm_probs set p_ser = %f, p_serexp = %f, ser_serexp_choice = %d where galcount = %d;' %(prob[0], prob[1], predict, gal)
    cursor.execute(cmd)

X_nair_arr,X_nair_uncorr,y_nair,mj,sj,galcount= fetch_data_nair(cursor,mean = mean,std = std)
prediction_prob  = clf.predict_proba(X_nair_arr)
prediction  = clf.predict(X_nair_arr)

for gal, prob, predict in zip(galcount, prediction_prob, prediction):
    cmd = 'update catalog.svm_probs set p_ser = %f, p_serexp = %f, ser_serexp_choice = %d where galcount = %d;' %(prob[0], prob[1], predict, gal)
    cursor.execute(cmd)
