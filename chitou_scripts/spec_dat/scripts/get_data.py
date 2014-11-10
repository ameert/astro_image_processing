import os
from astro_image_processing.mysql import *

def download_files(gal):
    data_dir = '/scratch/spec_dat/spectra/'
    
    for count in range(len(gal['thing_id'])):       
        nm1  = 'spec-%04d-%05d-%04d.fits' %(gal['plate'][count],gal['mjd'][count],gal['fiber'][count])
        nm2 = '%09d-spec.fits' %gal['thing_id'][count]
        str1 = 'http://data.sdss3.org/sas/dr9/boss/spectro/redux/v5_4_45/spectra/%04d/' %(gal['plate'][count])
        #print nm1, str1, data_dir
        #get_file(nm1,nm2, str1, data_dir)
        
        nm1  = 'spZbest-%04d-%05d.fits' %(gal['plate'][count],gal['mjd'][count])
        nm2 = '%09d-spZbest.fits' %gal['thing_id'][count]
        str1 = 'http://data.sdss3.org/sas/dr9/boss/spectro/redux/v5_4_45/%04d/v5_4_45/' %(gal['plate'][count])
        print nm1, str1, data_dir
        get_file(nm1,nm2, str1, data_dir)
        
        nm1  = 'spPlate-%04d-%05d.fits' %(gal['plate'][count],gal['mjd'][count])
        nm2 = '%09d-spPlate.fits' %gal['thing_id'][count]
        str1 = 'http://data.sdss3.org/sas/dr9/boss/spectro/redux/v5_4_45/%04d/' %(gal['plate'][count])
        #print nm1, str1, data_dir
        #get_file(nm1,nm2, str1, data_dir)
    return

def get_file(nm1,nm2, str1, download_dir):
    if not os.path.isfile(download_dir+nm2):
        if not os.path.isfile(download_dir+nm1):
            command = 'wget -P %s %s' %(download_dir, str1+nm1)
            #os.system(command)
        os.system('cp %s%s %s%s' %(download_dir, nm1, download_dir, nm2))
    return

#cursor =  mysql_connect('catalog','pymorph', 'pymorph')

#thing_id, color_ri, kcorr_r, zspec, plate, mjd, fiber = cursor.get_data("select a.thing_id, a.modelMag_r-a.extinction_r-a.kcorrR-a.modelMag_i+a.extinction_i+a.kcorrI as color_ri, a.kcorrR, a.zspec, b.plate, b.MJD, b.fibre from claudia_dr10_modelmag as a, claudia_values as b where a.thing_id=b.thing_id and a.zspec between 0.5 and 0.6 and a.kcorrR between 0.0 and 0.5 and a.modelMag_r-a.extinction_r-a.kcorrR-a.modelMag_i+a.extinction_i+a.kcorrI between 0.4 and 0.75 order by RAND(20) limit 200;")

thing_id, color_ri, kcorrR, zspec, plate, mjd, fiber = np.loadtxt('color_red_low.txt', unpack = True, skiprows=1)
gal = {'thing_id':np.array(thing_id, dtype=int),
       'plate':np.array(plate, dtype=int),
       'mjd':np.array(mjd, dtype=int),
       'fiber':np.array(fiber, dtype=int)
       }

download_files(gal)


#thing_id, color_ri, kcorr_r, zspec, plate, mjd, fiber = cursor.get_data("select a.thing_id, a.modelMag_r-a.extinction_r-a.kcorrR-a.modelMag_i+a.extinction_i+a.kcorrI as color_ri, a.kcorrR, a.zspec, b.plate, b.MJD, b.fibre from claudia_dr10_modelmag as a, claudia_values as b where a.thing_id=b.thing_id and a.zspec between 0.5 and 0.6 and a.kcorrR between 1.0 and 1.1 and a.modelMag_r-a.extinction_r-a.kcorrR-a.modelMag_i+a.extinction_i+a.kcorrI between 0.25 and 0.40 order by RAND(40) limit 200;")

thing_id, color_ri, kcorrR, zspec, plate, mjd, fiber = np.loadtxt('color_blue_high.txt', unpack = True, skiprows=1)
gal = {'thing_id':np.array(thing_id, dtype=int),
       'plate':np.array(plate, dtype=int),
       'mjd':np.array(mjd, dtype=int),
       'fiber':np.array(fiber, dtype=int)
       }

download_files(gal)
