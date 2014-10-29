import numpy as np
import pylab as pl
from matplotlib import cm

from mysql_class import *

from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import precision_recall_curve
from sklearn import preprocessing


# command used to create datafile used for fitting:
# start_mysql -e "select a.galcount, a.n_bulge, b.BT, b.r_bulge/f.petroR50_r, b.r_disk/f.petroR50_r, fs.flag as flags,  fde.flag as flagde,  fse.flag as flagse from r_band_ser as a,r_band_devexp as b, CAST as f, Flags_catalog as fs join Flags_catalog as fde on fs.galcount = fde.galcount join Flags_catalog as fse on fde.galcount = fse.galcount where a.galcount=b.galcount and b.galcount=f.galcount and f.galcount = fs.galcount and fs.model = 'ser' and fde.model = 'devexp' and fse.model = 'serexp' and fs.ftype = 'u' and fde.ftype = 'u' and fse.ftype = 'u'  and fs.band = 'r' and fde.band = 'r' and fse.band = 'r' order by f.galcount limit 10;" > model_learning_dataset
  
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
