#!/data2/home/ameert/python/bin/python2.5
import os
from mysql_connect import *
import numpy as np

galmax = 26500
models = ['dev', 'ser', 'devexp', 'serexp']
#models = ['serexp']


good_rep = [['r_dev', 'r_ser', 'r_devexp', 'r_serexp'],["Dev","Ser","DevExp","SerExp"], ["['bulge']","['bulge']","['bulge', 'disk']","['bulge', 'disk']"], ["True", "False", "True", "False"], ["/data2/home/ameert/sdss_sample/fits/dev/","/data2/home/ameert/sdss_sample/fits/ser/","/data2/home/ameert/sdss_sample/fits/devexp/","/data2/home/ameert/sdss_sample/fits/serexp/"], ["sdss_sex.cat","sdss_sex.cat","sdss_sex.cat","sdss_sex.cat"], ["sdss_r_out.cat","sdss_r_out.cat","sdss_r_out.cat","sdss_r_out.cat"], ["sdss_r.cat", "sdss_r.cat", "sdss_r.cat", "sdss_r.cat"]]

cursor = mysql_connect('pymorph','pymorph','pymorph9455')

cmd = 'select galcount, z from r_full order by galcount;'
cursor.execute(cmd)

rows = cursor.fetchall()
rows = list(rows)
gal_list = []
z_list = []
for row in rows:
    gal_list.append(int(row[0]))
    z_list.append(float(row[1]))

chunk = 0
while chunk < np.ceil(float(galmax)/1000.0):
    if not os.path.isfile('./fit_data/sdss_r_%d.cat' %(chunk+1)):
        f = open('./fit_data/sdss_r_%d.cat' %(chunk+1), 'w') #give filter
        f.writelines(['gal_id gimg wimg star z\n'])
        for gal_id, z in zip(gal_list, z_list):
            if gal_id > chunk*1000 and gal_id <= (chunk + 1)*1000:
                f.write('%08d_r_stamp %08d_r_stamp.fits %08d_r__r_W.fits %08d_r_psf.fits %f\n' %(gal_id, gal_id, gal_id, gal_id, z))

        f.close()

    for mod_count, model in enumerate(models):
        # mod_count += 3 #this is for serexp only
        if not os.path.isdir('./fits_ser_detailed/%s/%d' %(model, chunk+1)):
            os.system('mkdir ./fits_ser_detailed/%s/%d' %(model, chunk+1))
        
        file = """
#Configure file for PyMorph. Authors: Vinu Vikram, Yogesh Wadadekar and Ajit Kembhavi 2008
        
###----Specify the input images and Catalogues----###
imagefile = 'j8f643-1-1_drz_sci.fits'
whtfile = 'j8f643-1-1_drz_rms.fits'   #The weight image. If it contains the 
                                      #string 'rms', this will treated as 
				      #RMS_MAP and if it contains weight, then 
                                      #that will be treated as WEIGHT_MAP. 
				      #If nothing found, then by default it 
				      #is treated as MAP_RMS 
sex_cata = '%s'           #The sextractor catalogue which has 
                                      #the format given in the file
clus_cata = '%s'         #catalogue of galaxies from
                                      #online catalogu service
                                      #(name ra1 ra2 ra2 dec1 dec2 dec3)

datadir = '/data2/home/ameert/sdss_sample/fit_data/' #the directory containing input images
                                       #if commented out, then program uses
                                       # current directory

###----Specify the output names of images and catalogues----###
out_cata = '%s'      #catalogue of galaxies in the field
rootname = 'r'
#Filter = 'r' 
outdir = '/data2/home/ameert/sdss_sample/fits_ser_detailed/%s'  #the directory containing output data

                                       #if commented out, then program uses
                                       # current directory

###----Psf list----###
psfselect = 0                         #0 => No psfselection
                                      #1 => Only Select psf 
                                      #2 => Select psf and run pipeline
                                      #Recommended: Run with '1' and then run
                                      #pipeline
starsize = 20                         #psf image size will be startsize times 
                                      #the SMA given by SExtractor
#psflist = ['psf_1216382-1200443.fits', 'psf_1216408-1200251.fits', 'psf_1216424-1202057.fits','psf_1216487-1201246.fits','psf_1216504-1202104.fits']   
psflist = '@psflist.list'
                                      #List of psf containg their 
                                      #position information in the 
                                      #header (RA_TARG, DEC_TARG). 
                                      #Make psf with the names as here 
                                      #and use psf_header_update.py. 
                                      #It will update the header information.
mag_zero = 25.256                     #magnitude zero point

###----Conditions for Masking----###
manual_mask = 0
mask_reg = 2.0
thresh_area = 0.2
threshold = 3.0                       #Masking will be done for neighbours 
                                      #whose semimajor*threshold overlaps with 
                                      #threshold * semi-major axis of 
                                      #the object and area of the neighbour 
                                      #less than thresh_area * object area in
                                      #sq.pixel. 
                                      #The masking will be for a circular 
                                      #region of radius mask_reg*semi-major 
                                      #axis of the nighbour with respect to 
                                      #the center of the neightbour.

###---Size of the cut out and search conditions---###
###---size = [resize?, varsize?, fracrad, square?, fixsize]---###
size = [0, 1, 9, 1, 120]              #size of the stamp image
searchrad = '0.3arc'                    #The search radius  

###----Parameters for calculating the physical parameters of galaxy----###
pixelscale = 0.39                    #Pixel scale (arcsec/pixel)
H0 = 71                               #Hubble parameter
WM = 0.27                             #Omega matter
WV = 0.73                             #Omega Lambda

###----Parameters to be set for calculating the CASGM----###
back_extraction_radius = 15.0
#back_ini_xcntr = 32.0 
#back_ini_ycntr = 22.0
angle = 180.0

###----Fitting modes----###
repeat = False                        #Repeat the pipeline manually
galcut = True                        #True if we provide cutouts
decompose = True
detail = True #Detailed fitting
galfit = True #Always keep this True as it is not functional yet!
cas = False
findandfit = 0
maglim = [22, 15] #if findandfit= 1, then maglim = [faint_mag, bright_mag]
stargal = 0.8 #Star-galaxy classification 
crashhandler = 0

###---Galfit Controls---###
components = %s        #The components to be fitted to the objec
devauc = %s # set to False to fit sersic bulge, set to true to fit devacouler's bulge (n = 4)

###---fixing = [bulge_center, disk_center, sky]
fitting = [1, 1, 1]                    # = 0, Fix params at SExtractor value

###----Set the SExtractor and GALFIT path here----###
GALFIT_PATH ='/data2/home/ameert/galfit/galfit'
SEX_PATH = '/data2/home/ameert/sextractor-2.5.0/sex/bin/sex'
PYMORPH_PATH = '/data2/home/ameert/serial_pipeline/trunk/pymorph/'

###----The following conditions are used to classify fit goo/bad----###
chi2sq = 2.5                          #< chi2sq
Goodness = 0.60                       #> Goodness
center_deviation = 3.0                #< abs(center - fitted center)
center_constrain = 2.0                #Keep center within +/- center_constrain

###----Database Informations----###
database = 'pymorph'
table = '%s'
usr = 'pymorph'
pword = 'pymorph9455'
dbparams = ['Morphology:%s', 'ObsID:1:int']
""" %( "sdss_sex_"+str(chunk+1)+'.cat',"sdss_r_"+str(chunk+1)+'.cat',"sdss_r_out_" + str(chunk+1)+'.cat',model+'/'+str(chunk+1)+'/',good_rep[2][mod_count], good_rep[3][mod_count],good_rep[0][mod_count]+'detailed_fit',good_rep[1][mod_count])


        config = open("./fits_ser_detailed/%s/%d/config.py" %(model, chunk+1), "w")
        config.write(file)


        config.close()
    chunk += 1

cursor.close()
