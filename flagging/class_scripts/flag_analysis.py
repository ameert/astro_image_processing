import numpy as np


def get_score(test_val, true_val):
    """reports the Matthew's correlation coeeficient for the given flag"""
    TP = np.max([.0001,float(np.sum(test_val*true_val))])
    TN = np.max([.0001,float(np.sum(np.where(test_val==0, 1,0) * np.where(true_val==0, 1,0)))])
    FP = np.max([.0001,float(np.sum(test_val * np.where(true_val==0, 1,0)) )])
    FN = np.max([.0001,float(np.sum(np.where(test_val==0, 1,0) * true_val))])

    
    mcc = TP * TN - FP *FN
    mcc = mcc/np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    print "tp: %d, tn: %d, fp: %d, fn:%d, mcc:%f" %(TP,TN,FP,FN, mcc)
    return mcc

def print_flags(flag_str, flag_vals, print_gals = False):
    print "%s: %d" %(flag_str, np.sum(flag_vals))
    if print_gals:
        print np.extract(flag_vals==1, data['galcount'])
    return np.sum(flag_vals)

class flag_set():
    def __init__(self, flag_vals):
        self.vals = flag_vals
    def invert(self):
        return np.where(self.vals==1,0,1)

def get_percent(flag_arr):
    return 100.0*np.sum(flag_arr)/flag_arr.size

def print_flag_table(flag_list, flag_vals):
    for a in flag_list:
        flag_arr = np.where(flag_vals&2**a[1]>0,1,0)
        print '%s: %5.3f' %(a[0], get_percent(flag_arr))
    return

