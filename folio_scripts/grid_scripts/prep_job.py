#!/data2/home/ameert/python/bin/python2.5

import os
import sys

def write_config(filename, cat_name, tablename, outdir, indir, detail = 0, fit_type = 0, fit_sky = 0, band = 'r'):
    if fit_type == 'ser':
        cas_str = 'True'
    else:
        cas_str = 'False'
    
    if fit_type in ['dev','devexp']:
        devac_str = 'True'
    else:
        devac_str = 'False'
    
    if detail:
        detail_str = 'True'
    else:
        detail_str = 'False'

    if fit_type == 'serexp' or fit_type == 'devexp' or fit_type == 'cmodel':
        fit_str = "'bulge', 'disk'"
    elif fit_type == 'dev' or fit_type == 'ser':
        fit_str = "'bulge'"
    elif fit_type == 'exp':
        fit_str = "'disk'"

    if fit_sky:
        sky_str = '1'
    else:
        sky_str = '0'
    
    str_to_wr = """
#Configure file for PyMorph. Authors: Vinu Vikram, Yogesh Wadadekar and Ajit Kembhavi 2008
        
###----Specify the input images and Catalogues----###
imagefile = 'j8f643-1-1_drz_sci.fits'
whtfile = 'j8f643-1-1_drz_rms.fits'   #The weight image. If it contains the 
                                      #string 'rms', this will treated as 
				      #RMS_MAP and if it contains weight, then 
                                      #that will be treated as WEIGHT_MAP. 
				      #If nothing found, then by default it 
				      #is treated as MAP_RMS 
sex_cata = 'sdss_sex.cat'           #The sextractor catalogue which has 
                                      #the format given in the file
clus_cata = '%s'         #catalogue of galaxies from
#clus_cata = 'sdss_sim_test.cat'       #online catalogu service
                                      #online catalogu service
                                      #(name ra1 ra2 ra2 dec1 dec2 dec3)

datadir = '%s/' #the directory containing input images
                                       #if commented out, then program uses
                                       # current directory

###----Specify the output names of images and catalogues----###
out_cata = 'sdss_r_out.cat'      #catalogue of galaxies in the field
rootname = '%s'
#Filter = 'r' 
outdir = '%s/'  #the directory containing output data

                                       #if commented out, then program uses
                                       # current directory
""" %(cat_name, indir, band, outdir)  

    str_to_wr +="""

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
mag_zero = 24.8425                     #magnitude zero point

###----Conditions for Masking----###
manual_mask = 0
mask_reg = 2.0
thresh_area = 0.2
threshold = 3.0                      #Masking will be done for neighbours 
                                      #whose semimajor*threshold overlaps with 
                                      #threshold * semi-major axis of 
                                      #the object and area of the neighbour 
                                      #less than thresh_area * object area in
                                      #sq.pixel. 
                                      #The masking will be for a circular 
                                      #region of radius mask_reg*semi-major 
                                      #axis of the nighbour with respect to 
                                      #the center of the neightbour.


#SEx_DETECT_THRESH = 1.7 #1.5
#SEx_DETECT_MINAREA = 9 #6
#SEx_BACK_SIZE = 256 #64

###---Size of the cut out and search conditions---###
###---size = [resize?, varsize?, fracrad, square?, fixsize]---###
size = [0, 1, 9, 1, 120]              #size of the stamp image
searchrad = '0.3arc'                    #The search radius  

###----Parameters for calculating the physical parameters of galaxy----###
pixelscale =  0.396                    #Pixel scale (arcsec/pixel)
H0 = 70                               #Hubble parameter
WM = 0.3                             #Omega matter
WV = 0.7                             #Omega Lambda

###----Parameters to be set for calculating the CASGM----###
back_extraction_radius = 15.0
#back_ini_xcntr = 32.0 
#back_ini_ycntr = 22.0
angle = 180.0

"""

    str_to_wr +="""
###----Fitting modes----###
repeat = False                        #Repeat the pipeline manually
galcut = True                        #True if we provide cutouts
decompose = True
detail = %s #Detailed fitting
galfit = True #Always keep this True as it is not functional yet!
cas = %s
findandfit = 0
maglim = [22, 15] #if findandfit= 1, then maglim = [faint_mag, bright_mag]
stargal = 0.8 #Star-galaxy classification 
crashhandler = 0

###---Galfit Controls---###
components = [%s]        #The components to be fitted to the objec
devauc = %s # set to False to fit sersic bulge, set to true to fit devacouler's bulge (n = 4)
UN = 15.0
""" %(detail_str, cas_str, fit_str, devac_str)

    str_to_wr +="""
###---fixing = [bulge_center, disk_center, sky]
fitting = [1, 1, %s]                    # = 0, Fix params at SExtractor value

###----Set the SExtractor and GALFIT path here----###
GALFIT_PATH ='/data2/home/ameert/galfit/galfit'
SEX_PATH = '/data2/home/ameert/sextractor-2.5.0/sex/bin/sex'
PYMORPH_PATH = '/data2/home/ameert/pymorph/pymorph/'
galfitv = '2.0'

###----The following conditions are used to classify fit goo/bad----###
chi2sq = 2.5                          #< chi2sq
Goodness = 0.60                       #> Goodness
center_deviation = 3.0                #< abs(center - fitted center)
center_constrain = 2.0                #Keep center within +/- center_constrain

###----Database Informations----###
host = 'shredder'
database = 'pymorph'
table = '%s'
usr = 'pymorph'
pword = 'pymorph9455'
dbparams = ['Morphology:%s', 'ObsID:1:int']
""" %(sky_str, tablename, fit_type)

    f = open(filename, 'w')
    f.write(str_to_wr)
    f.close()

    return








