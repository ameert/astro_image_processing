import scikits.bootstrap as bootstrap
import numpy as np
data = [(1.,4.), (2.,5.), (3.,6.)]

def get_val(alldata):
    percentile = 0.5
    data = np.array(alldata[:,0])
    weights = np.array(alldata[:,1])
    
    indicies = np.argsort(data)
    sdata = data[indicies]
    sweights = weights[indicies]/np.sum(weights)
    cumweight = np.cumsum(sweights)
    pos = np.where(cumweight<=percentile)[0]
    if len(pos)<1:
        pos = 0
    else:
        pos = np.max(pos)
    return sdata[pos]

CIs = bootstrap.ci(data=data, statfunction=get_val)  
print CIs
