import numpy as np
import os
from sklearn.cross_validation import train_test_split


#os.system("""mysql -u pymorph -ppymorph catalog -e "select a.galcount, a.n_bulge, b.BT, b.r_bulge/f.petroR50_r, b.r_disk/f.petroR50_r, fs.flag as flags,  fde.flag as flagde,  fse.flag as flagse from r_band_ser as a,r_band_devexp as b, CAST as f, Flags_catalog as fs join Flags_catalog as fde on fs.galcount = fde.galcount join Flags_catalog as fse on fde.galcount = fse.galcount where a.galcount=b.galcount and b.galcount=f.galcount and f.galcount = fs.galcount and fs.model = 'ser' and fde.model = 'devexp' and fse.model = 'serexp' and fs.ftype = 'u' and fde.ftype = 'u' and fse.ftype = 'u'  and fs.band = 'r' and fde.band = 'r' and fse.band = 'r' order by f.galcount;" > model_learning_dataset.txt""")

galcount, n_ser, BT_devexp, re_rp, rd_rp, fs, fde, fse = np.loadtxt('model_learning_dataset.txt', unpack = True, skiprows=1)

galcount = galcount.astype(int)
fs = fs.astype(int)
fde = fde.astype(int)
fse =fse.astype(int)

bad_s = np.where(fs&(2**20),1,0)
bad_de = np.where(fde&(2**20),1,0)
bad_se = np.where(fse&(2**20),1,0)

print np.sum(bad_s),np.sum(bad_de),np.sum(bad_se),np.sum(bad_s*bad_se),np.sum(bad_s*bad_de),np.sum(bad_se*bad_de),np.sum(bad_s*bad_de*bad_se)
 
bad_all = np.extract(bad_s*bad_de*bad_se==1, galcount)
bad_ser = np.extract(bad_s==1, galcount)
bad_de_se = np.extract((bad_se*bad_de*np.where(bad_s==1,0,1))==1, galcount)

np.random.shuffle(bad_all)
np.random.shuffle(bad_ser)
np.random.shuffle(bad_de_se)


outfile = open('/home/ameert/Desktop/bad_all.txt','w')
outfile.write('this file has galaxies that fail in all three models\n')
for gal in bad_all:
    outfile.write('%d\n' %gal)
outfile.close()

outfile = open('/home/ameert/Desktop/bad_sede.txt','w')
outfile.write('this file has galaxies that fail in all the se and de fits but not ser fits\n')
for gal in bad_de_se:
    outfile.write('%d\n' %gal)
outfile.close()
