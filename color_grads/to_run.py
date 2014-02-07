import os

gals=[
'data/9999/00056653_mag_corr_ser.npz',  'data/9999/00384100_mag_corr_ser.npz',
'data/9999/00107249_mag_corr_ser.npz',  'data/9999/00395905_mag_corr_ser.npz',
'data/9999/00109251_mag_corr_ser.npz',  'data/9999/00414847_mag_corr_ser.npz',
'data/9999/00111116_mag_corr_ser.npz',  'data/9999/00416404_mag_corr_ser.npz',
'data/9999/00123017_mag_corr_ser.npz',  'data/9999/00429651_mag_corr_ser.npz',
'data/9999/00129965_mag_corr_ser.npz',  'data/9999/00431805_mag_corr_ser.npz',
'data/9999/00134893_mag_corr_ser.npz',  'data/9999/00433599_mag_corr_ser.npz',
'data/9999/00144038_mag_corr_ser.npz',  'data/9999/00440635_mag_corr_ser.npz',
'data/9999/00144316_mag_corr_ser.npz',  'data/9999/00444874_mag_corr_ser.npz',
'data/9999/00149949_mag_corr_ser.npz',  'data/9999/00452201_mag_corr_ser.npz',
'data/9999/00155144_mag_corr_ser.npz',  'data/9999/00459813_mag_corr_ser.npz',
'data/9999/00165433_mag_corr_ser.npz',  'data/9999/00467666_mag_corr_ser.npz',
'data/9999/00171282_mag_corr_ser.npz',  'data/9999/00486979_mag_corr_ser.npz',
'data/9999/00173926_mag_corr_ser.npz',  'data/9999/00499188_mag_corr_ser.npz',
'data/9999/00191763_mag_corr_ser.npz',  'data/9999/00520345_mag_corr_ser.npz',
'data/9999/00201772_mag_corr_ser.npz',  'data/9999/00532120_mag_corr_ser.npz',
'data/9999/00218334_mag_corr_ser.npz',  'data/9999/00541543_mag_corr_ser.npz',
'data/9999/00246800_mag_corr_ser.npz',  'data/9999/00546340_mag_corr_ser.npz',
'data/9999/00249509_mag_corr_ser.npz',  'data/9999/00549258_mag_corr_ser.npz',
'data/9999/00266367_mag_corr_ser.npz',  'data/9999/00587097_mag_corr_ser.npz',
'data/9999/00269911_mag_corr_ser.npz',  'data/9999/00604781_mag_corr_ser.npz',
'data/9999/00297419_mag_corr_ser.npz',  'data/9999/00605546_mag_corr_ser.npz',
'data/9999/00300617_mag_corr_ser.npz',  'data/9999/00616680_mag_corr_ser.npz',
'data/9999/00309194_mag_corr_ser.npz',  'data/9999/00620279_mag_corr_ser.npz',
'data/9999/00334338_mag_corr_ser.npz',  'data/9999/00632506_mag_corr_ser.npz',
'data/9999/00350019_mag_corr_ser.npz',  'data/9999/00633138_mag_corr_ser.npz',
'data/9999/00364909_mag_corr_ser.npz',  'data/9999/00634802_mag_corr_ser.npz',
'data/9999/00375120_mag_corr_ser.npz',  'data/9999/00643812_mag_corr_ser.npz',
'data/9999/00382743_mag_corr_ser.npz',  'data/9999/00659553_mag_corr_ser.npz']

for gal in gals:
    ng = gal.split('/')[-1]
    ng = ng.split('_')[0]
    print 'python measure_profs_new.py %s' %ng
    print 'python measure_profs_data.py %s' %ng
    os.system('python measure_profs_new.py %s' %ng)
    os.system('python measure_profs_data.py %s' %ng)
