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
#         data_dir: string path to directroy that galmorph will palce all data
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

def download_files(gal, data_dir, bands = 'r'):
    for band in bands:
        for count in range(len(gal['galcount'])):
            run_tmp = gal['run'][count]
            rerun_tmp = gal['rerun'][count]
            camCol_tmp = gal['camCol'][count]
            field_tmp =  gal['field'][count]
            
            # see if psField exists, if not get it from SDSS
            nm  = 'psField-%06d-%d-%04d.fit' %(run_tmp, camCol_tmp, field_tmp)
            str = 'http://das.sdss.org/imaging/%d/%d/objcs/%d/%s' %(run_tmp, rerun_tmp, camCol_tmp, nm)
            get_file(nm, str, data_dir)

            # see if fpC file exists, if not, then get it from SDSS
            nm  = 'fpC-%06d-%s%d-%04d.fit.gz' %(run_tmp, band, camCol_tmp, field_tmp)
            str = 'http://das.sdss.org/imaging/%d/%d/corr/%d/%s' %(run_tmp, rerun_tmp, camCol_tmp, nm)
            get_file(nm, str, data_dir)

            ##### These files are currently commented out, because we aren't
            ##### currently using them
            
            # # see if fpM file exists, if not, then get it from SDSS
            # nm  = 'fpM-%06d-%s%d-%04d.fit' %(run_tmp, band, camCol_tmp, field_tmp)
            # str = 'http://das.sdss.org/imaging/%d/%d/objcs/%d/%s' %(run_tmp, rerun_tmp, camCol_tmp, nm)
            # get_file(nm, str, data_dir)
            
            # # see if tsObj file exists, if not, then get it from SDSS
            # nm  = 'tsObj-%06d-%d-%d-%04d.fit' %(run_tmp, camCol_tmp, rerun_tmp,field_tmp)
            # str = 'http://das.sdss.org/imaging/%d/%d/calibChunks/%d/%s' %(run_tmp, rerun_tmp, camCol_tmp, nm)
            # get_file(nm, str, data_dir)

            # # see if tsField file exists, if not, then get it from SDSS
            # nm  = 'tsField-%06d-%d-%d-%04d.fit' %(run_tmp, camCol_tmp, rerun_tmp,field_tmp)
            # str = 'http://das.sdss.org/imaging/%d/%d/calibChunks/%d/%s' %(run_tmp, rerun_tmp, camCol_tmp, nm)
            # get_file(nm, str, data_dir)
            
    return

#++++++++++++++++++++++++++
#
# TITLE: get_file
#
# PURPOSE: This program checks for the file and
#          downloads the file if it doesn't exist
#
# INPUTS: nm:  string of file name
#         str: string of url of file to be downloaded
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

def get_file(nm, str, download_dir):
    if not os.path.isfile(download_dir + nm):
        command = 'wget -P %s %s' %(download_dir, str)
        os.system(command)
    return
