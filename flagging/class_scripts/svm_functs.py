from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn import svm
import pylab as pl
from mysql_class import *
import numpy as np


def angdiff(theta1, theta2, ba1, ba2):
    """This function finds the angle difference between two angles weighted by the ellipticity of the vectors. Circular vectors should not care about large angle differences"""
    theta1 = np.deg2rad(theta1)
    theta2 = np.deg2rad(theta2)
    vec1 = np.array([np.cos(theta1), np.sin(theta1)])
    vec2 = np.array([np.cos(theta2), np.sin(theta2)])
    dot = np.sum(vec1*vec2, axis = 0)
    diff = np.minimum(np.arccos(dot),np.arccos(-1.0*dot))
    diff = np.rad2deg(diff)*np.sqrt((1.0-ba1)*(1.0-ba2))*10
    return diff


def fetch_data(cursor, sample, mean = None, std = None):
    """grab the data used for testing, normalize by mean and std. dev supplied or generate from the data. Return the normalized data, unnormalized data, correct classification,  mean, and std. dev used. Sample 1 is the training sample, sample 2 is the cross-validation sample, sample 3 is the evaulation set"""

    cmd = 'select a.galcount, b.n, d.BT, a.re_pix, a.n, a.eb, a.bpa, a.rd_pix, a.ed, a.dpa, a.BT, a.re_pix/a.rd_pix, c.trusted_serexp from psf_serexp as a,psf_ser as b,psf_devexp as d, sim_input as c where  c.simcount = a.galcount and c.simcount = b.galcount and c.simcount = d.galcount and c.samplegroup = %d;' %sample

    galcount, n_ser, BT_devexp, re_serexp, n_serexp, eb_serexp, bpa, rd_serexp, ed_serexp, dpa, BT, rerd_serexp, is_serexp  = cursor.get_data(cmd)
    diff_pa = angdiff(np.array(bpa),np.array(dpa),np.array(eb_serexp),np.array(ed_serexp))
    
    X_data = zip(n_ser, BT_devexp,re_serexp, n_serexp, eb_serexp, rd_serexp, ed_serexp, BT, rerd_serexp, diff_pa)
    X_data_arr = np.array(X_data)
    X_unnorm = np.array(X_data)
    y = np.array(is_serexp)
    
    if mean == None: 
        mean = np.mean(X_data_arr, axis = 0)
    X_data_arr -= mean
    if std == None:
        std = np.std(X_data_arr, axis = 0)
    X_data_arr /= std
    
    return X_data_arr, X_unnorm, y, mean, std, galcount


def fetch_data_nair(cursor, mean = None, std = None):
    """grab the data used for testing, normalize by mean and std. dev supplied or generate from the data. Return the normalized data, unnormalized data, correct classification,  mean, and std. dev used. Sample 1 is the training sample, sample 2 is the cross-validation sample, sample 3 is the evaulation set"""

    cmd = 'select a.galcount, b.n_bulge, d.BT, a.r_bulge, a.n_bulge, a.ba_bulge, a.pa_bulge, a.r_disk, a.ba_disk, a.pa_disk, a.BT, a.r_bulge/a.r_disk, c.Ttype from catalog.r_band_serexp as a,catalog.r_band_ser as b,catalog.r_band_devexp as d, catalog.Nair as c where  c.galcount = a.galcount and a.galcount = b.galcount and a.galcount = d.galcount and a.r_bulge>0 and b.r_bulge>0 and d.r_bulge >0;' 

    galcount, n_ser, BT_devexp, re_serexp, n_serexp, eb_serexp, bpa, rd_serexp, ed_serexp, dpa, BT, rerd_serexp, Ttype  = cursor.get_data(cmd)
    diff_pa = angdiff(np.array(bpa),np.array(dpa),np.array(eb_serexp),np.array(ed_serexp))
    
    X_data = zip(n_ser, BT_devexp,re_serexp, n_serexp, eb_serexp, rd_serexp, ed_serexp, BT, rerd_serexp, diff_pa)
    X_data_arr = np.array(X_data)
    X_unnorm = np.array(X_data)
    y = np.array(Ttype)
    
    if mean == None: 
        mean = np.mean(X_data_arr, axis = 0)
    X_data_arr -= mean
    if std == None:
        std = np.std(X_data_arr, axis = 0)
    X_data_arr /= std
    
    return X_data_arr, X_unnorm, y, mean, std, galcount
