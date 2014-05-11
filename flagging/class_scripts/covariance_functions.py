import os
import numpy as np
import sys
import pylab as pl
import matplotlib.cm as cm
from flag_defs import category_flag_dict

def get_score(true_val, test_val, trueflag, testflag):

    true_class = np.where(true_val&trueflag>0, 1, 0)
    test_class = np.where(test_val&testflag>0, 1, 0)

    TP = np.max([.0001,float(np.sum(test_class*true_class))])
    TN = np.max([.0001,float(np.sum(np.where(test_class==0, 1,0) * np.where(true_class==0, 1,0)))])
    FP = np.max([.0001,float(np.sum(test_class * np.where(true_class==0, 1,0)) )])
    FN = np.max([.0001,float(np.sum(np.where(test_class==0, 1,0) * true_class))])

    
    mcc = TP * TN - FP *FN
    mcc = mcc/np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    precision = (TP)/(FP+TP)
    recall = (TP)/(FN+TP)
    TNR = TN/(TN+FP)
    accuracy = (TP+TN)/(TP+TN+FP+FN)
    f1 = 2.0*precision*recall/(precision+recall)
    mcc_max = np.min([(TP+FP)*(TN+FP),(TP+FN)*(TN+FN)])/np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))

    #mcc = mcc/mcc_max
    #mcc=f1
    print "tp: %d, tn: %d, fp: %d, fn:%d, mcc:%f" %(TP,TN,FP,FN, mcc)
    return mcc

def cov(data1, data2, d1flags, d2flags):
    cov_mat = np.zeros((len(d1flags), len(d2flags)))
    for c1, d1 in enumerate(d1flags):
        for c2, d2 in enumerate(d2flags):
            print c1, c2, d1, d2
            cov_mat[c1,c2] = get_score(data1, data2, d1, d2)
    return cov_mat


def make_disp_matrix(in_mat, whitesec=None):
    """makes a copy of a matrix with the region above or below the diagonal 
set to nan values so that no color shows up during plotting"""

    disp_mat = in_mat.copy()
    
    if whitesec == 'upper':
        for a in range(disp_mat.shape[0]):
            for b in range(a+1,disp_mat.shape[1]):
                disp_mat[a,b] = np.nan
    elif whitesec == 'lower':
        for a in range(disp_mat.shape[0]):
            for b in range(0,a):
                disp_mat[a,b] = np.nan
    return disp_mat

def print_nums(disp_mat, printsec=None):
    """prints the numbers associated with a matrix cell. 
use printsec to select the upper or lower triangle, otherwise prints all"""

    if printsec == 'upper':
        for a in range(disp_mat.shape[0]):
            for b in range(a+1,disp_mat.shape[1]):
                pl.text(b,a, '% 03.2f' %disp_mat[a,b], 
                        horizontalalignment='center',
                        verticalalignment='center', fontsize = 8)
    elif printsec == 'lower':
        for a in range(disp_mat.shape[0]):
            for b in range(0,a):
                pl.text(b,a, '% 03.2f' %disp_mat[a,b], 
                        horizontalalignment='center',
                        verticalalignment='center', fontsize = 8)
    else:
        for a in range(disp_mat.shape[0]):
            for b in range(0,disp_mat.shape[1]):
                pl.text(b,a, '% 03.2f' %disp_mat[a,b], 
                        horizontalalignment='center',
                        verticalalignment='center', fontsize = 8)
    
    return disp_mat

def cov_to_correlation(covmat):
    """converts a covariance matrix to correlation by dividing each element by 
the value on the diagonal for that element"""
    diag = np.sqrt(1.0/np.diag(covmat))
    corr = diag*covmat*diag.T

    return corr


#flagvals
# bulges - 1
# disks  - 2
# 1com   - 4
# devexp - 8
# serexp - 16
# 2com   - 32
# bad2com - 64
# bad     -128

def lg12_to_class(model, n_ser):
    #1com
    l_flag = np.where(model==1, 1,0)
    l_flag += np.where(model==2, 2,0)
    l_flag += np.where(model==3, 1,0)*np.where(n_ser>=2, 1,0)
    l_flag += np.where(model==3, 2,0)*np.where(n_ser<2, 1,0)
    l_flag += np.where(l_flag>0, 4,0)
    #2com
    l_flag += np.where(model==4, 32,0)
    l_flag += np.where(model==5, 40,0)
    #print l_flag
    return l_flag

def Men14_to_class(model):
    #1com
    m_flag = np.where(model==1, 1,0)
    m_flag += np.where(model==2, 2,0)
    m_flag += np.where(m_flag>0, 4,0)
    #2com
    m_flag += np.where(model==4, 40,0)
    m_flag += np.where(model==3, 128,0)
    #print m_flag
    return m_flag
    
def sim_prob_to_class(pS, pn4, n_ser):
    #1com
    sim_flag = np.where(pS>0.32, 4,0)
    sim_flag += np.where(pS>0.32, 1,0)*np.where(n_ser>=2, 1,0)
    sim_flag += np.where(pS>0.32, 2,0)*np.where(n_ser<2, 1,0)
    #2com
    sim_flag += np.where(pS<=0.32, 32,0)
    sim_flag += np.where(pS<=0.32, 8,0)*np.where(pn4>0.32, 1,0)
    sim_flag += np.where(pS<=0.32, 16,0)*np.where(pn4<=0.32, 1,0)
    #print sim_flag
    return sim_flag

def meert_flag_to_class(flag):
    #1com
    meert_flag= np.where(flag&2**category_flag_dict["\tBulge Galaxies"], 1,0)
    meert_flag +=np.where(flag&2**category_flag_dict["\tDisk Galaxies"], 2,0)
    meert_flag +=np.where(meert_flag>0, 4,0)
    #2com
    meert_flag +=np.where(flag&(2**category_flag_dict["\tTwo-Component Galaxies"]+2**category_flag_dict["\tProblemmatic Two-Component Galaxies"]), 32,0)
    meert_flag +=np.where(flag&(2**category_flag_dict["\tTwo-Component Galaxies"]+2**category_flag_dict["\tProblemmatic Two-Component Galaxies"]), 16,0)
    meert_flag +=np.where(flag&2**category_flag_dict["\tProblemmatic Two-Component Galaxies"], 64,0)
    meert_flag +=np.where(flag&2**category_flag_dict["Bad Total Magnitudes and Sizes"], 128,0)
    #print meert_flag
    return meert_flag

