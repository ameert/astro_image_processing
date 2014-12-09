from mysql_class import *
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report

# Loading the datasets
dba = 'simulations'
usr = 'pymorph'
pwd = 'pymorph'

cursor = mysql_connect(dba, usr, pwd)


def get_score(test_val, true_val):
    TP = np.sum(test_val*true_val)
    TN = np.sum(np.where(test_val==0, 1,0) * np.where(true_val==0, 1,0))
    FP = np.sum(test_val * np.where(true_val==0, 1,0)) 
    FN = np.sum(np.where(test_val==0, 1,0) * true_val)

    mcc = TP * TN - FP *FN
    mcc = mcc/np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    
    return mcc

def get_data(sample):
    cmd = 'select a.galcount, c.trusted_serexp, a.p_serexp  from svm_probs as a join  sim_input as c on c.simcount = a.galcount where c.samplegroup = %d;' %sample

    galcount, is_serexp, p_serexp  = cursor.get_data(cmd)
    
    galcount = np.array(galcount, dtype = int)
    is_serexp = np.array(is_serexp, dtype = float)
    p_serexp = np.array(p_serexp, dtype = float)


    p_serexp = np.where(p_serexp>=0.5, 1, 0)
    is_serexp = np.where(is_serexp>=0.5, 1, 0)
    
    return galcount, is_serexp, p_serexp


for count in [1,2,3]:
    galcount, is_serexp, p_serexp = get_data(count)

    print 'sample %d' %count
    print classification_report(is_serexp, p_serexp)
    print "MCC: %.2f" %get_score(p_serexp, is_serexp)
