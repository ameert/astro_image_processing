from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn import svm
import pylab as pl
from mysql_class import *
import numpy as np
from svm_functs import *

# Loading the datasets
dba = 'simulations'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)

X_test_arr, X_test_uncorr, y_test, mean, std = fetch_data(cursor, 1, mean = None, std = None)

X_CV_arr,X_CV_uncorr,y_CV,mean,std = fetch_data(cursor,2,mean = mean,std = std)

X_eval_arr,X_eval_uncorr,y_eval,mean,std = fetch_data(cursor,3,mean = mean,std = std)

# Set the parameters by cross-validation
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-2, 1e-3, 1e-4, 1e-5],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

scores = [
    ('precision', precision_score),
    ('recall', recall_score),
    ('f1', f1_score)
]

for score_name, score_func in scores:
    print "# Tuning hyper-parameters for %s" % score_name
    print

    clf = GridSearchCV(svm.SVC(), tuned_parameters, score_func=score_func)
    clf.fit(X_test_arr, y_test, cv=5)

    print "Best parameters set found on development set:"
    print
    print clf.best_estimator_
    print
    print "Grid scores on development set:"
    print
    for params, mean_score, scores in clf.grid_scores_:
        print "%0.3f (+/-%0.03f) for %r" % (
            mean_score, scores.std() / 2, params)
    print

    print "Detailed classification report:"
    print
    print "The model is trained on the full development set."
    print "The scores are computed on the full evaluation set."
    print
    y_true, y_pred = y_eval, clf.predict(X_eval_arr)
    print classification_report(y_true, y_pred)
    print
