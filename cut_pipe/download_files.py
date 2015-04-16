#++++++++++++++++++++++++++
#
# TITLE: download_files 
#
# PURPOSE: This program downloads data
#          for galaxies from sdss in all 
#          bands that are selected.
#
# INPUTS: gal: dictionary containing at least these entries
#              index: the index number used for naming the galaxy
#              run:   the sdss run number
#              rerun: the sdss rerun number
#              camCol: the sdss camera column number
#              field: the sdss field number     
#         data_dir: string path to directory that galmorph will place all data
#         bands: the bands that will be downloaded. This defaults to 'r' band
#                if not set by the function call
# OUTPUTS: NONE
#
# PROGRAM CALLS: get_file.py (this is also included in this file)
#
# BY: Alan Meert
#    Department of Physics and Astronomy
#    University of Pennsylvania
#
# FOR: Mariangela Bernardi
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# DATE: 4 JAN 2011
#
#-----------------------------------
import os

def download_files(gal, data_stem, bands = 'r', data_release=12):
    """downloads the files of interest from SDSS3. locations of more files can be found 
at http://data.sdss3.org/datamodel/index-files.html"""
    psf_dir = data_stem+'/psField/'

    urlstem = "http://data.sdss3.org/sas/dr%d/boss" %data_release

    for gal_to_do in zip(gal['galcount'],gal['run'],gal['rerun'],gal['camCol'],gal['field']):        
        galcount, run, rerun, camCol, field = gal_to_do 
    
        # see if psField exists, if not get it from SDSS
        nm  = 'psField-%06d-%d-%04d.fit' %(run, camCol, field)
        str1 = '%s/photo/redux/%d/%d/objcs/%d/%s' %(urlstem, rerun, run, camCol, nm)
        if get_file(nm, str1, psf_dir):
            #zip the file to save space
            os.system('gzip %s/%s' %(psf_dir,nm))
    
        for band in bands:
            # see if frame file exists, if not, then get it from SDSS
            nm  = 'frame-%s-%06d-%d-%04d.fits.bz2' %(band, run, camCol, field)
            str1 = '%s/photoObj/frames/%d/%d/%d/%s' %(urlstem, rerun, run, camCol, nm)
            get_file(nm, str1, data_stem+band+'/')

    return

def download_files_old(gal, data_stem, bands = 'r'):
    """DEPRECATED!!!!!!
old version of the download script from dr7 and earlier from SDSS2"""
    for band in bands:
        psf_dir = data_stem+'/psField/'
        data_dir = data_stem + band + '/'
        for count in range(len(gal['galcount'])):
            run_tmp = gal['run'][count]

            # if we are looking at the coadd, we must adjust the run number
            if run_tmp == 106:
                run_tmp = 100006
            if run_tmp == 206:
                run_tmp = 200006

            rerun_tmp = gal['rerun'][count]
            camCol_tmp = gal['camCol'][count]
            field_tmp =  gal['field'][count]
            
            # see if psField exists, if not get it from SDSS
            nm  = 'psField-%06d-%d-%04d.fit' %(run_tmp, camCol_tmp, field_tmp)
            str1 = 'http://das.sdss.org/imaging/%d/%d/objcs/%d/%s' %(run_tmp, rerun_tmp, camCol_tmp, nm)
            get_file(nm, str1, psf_dir)

            # see if fpObjc exists, if not get it from SDSS
            #nm  = 'fpObjc-%06d-%d-%04d.fit' %(run_tmp, camCol_tmp, field_tmp)
            #str1 = 'http://das.sdss.org/imaging/%d/%d/objcs/%d/%s' %(run_tmp, rerun_tmp, camCol_tmp, nm)
            #get_file(nm, str1, data_dir)

            # see if fpC file exists, if not, then get it from SDSS
            nm  = 'fpC-%06d-%s%d-%04d.fit.gz' %(run_tmp, band, camCol_tmp, field_tmp)
            str1 = 'http://das.sdss.org/imaging/%d/%d/corr/%d/%s' %(run_tmp, rerun_tmp, camCol_tmp, nm)
            get_file(nm, str1, data_dir)

            ##### These files are currently commented out, because we aren't
            ##### currently using them
            
            # # see if fpM file exists, if not, then get it from SDSS
            # nm  = 'fpM-%06d-%s%d-%04d.fit' %(run_tmp, band, camCol_tmp, field_tmp)
            # str1 = 'http://das.sdss.org/imaging/%d/%d/objcs/%d/%s' %(run_tmp, rerun_tmp, camCol_tmp, nm)
            # get_file(nm, str1, data_dir)
            
    return

#++++++++++++++++++++++++++
#
# TITLE: get_file
#
# PURPOSE: This program checks for the file and
#          downloads the file if it doesn't exist
#
# INPUTS: nm:  string of file name
#         str1: string of url of file to be downloaded
#         download_dir: string path to directroy that
#                       galmorph will palce all data
#         
# OUTPUTS: NONE
#
# PROGRAM CALLS: uses os module 
#
# BY: Alan Meert
#    Department of Physics and Astronomy
#    University of Pennsylvania
#
# FOR: Mariangela Bernardi
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# DATE: 4 JAN 2011
#
#-----------------------------------

def get_file(nm, str1, download_dir):
    is_download = False
    if not os.path.isfile(download_dir + nm):
        if not os.path.isfile(download_dir + nm+'.gz'):
            if not os.path.isfile(download_dir + nm+'.bz2'):
                command = 'wget -P %s %s' %(download_dir, str1)
                os.system(command)
                is_download = True
                
    return is_download
