import os

def build_dirs(data_dir, cut_dir, bands):
    """checks for all the dirs and builds the dirs if possible"""

    good_dirs = True
    if not os.path.isdir(data_dir):
        print "Attempting to create data_dir: %s" %data_dir
        os.system('mkdir %s' %data_dir)
    
    if  os.path.isdir(data_dir):
        os.system('mkdir %s/psField' %data_dir)
        for band in bands:
            os.system('mkdir %s/%s' %(data_dir,band))
    else:
        print "data_dir has problems and can't be corrected!!!!"
        good_dirs=False

    if not os.path.isdir(cut_dir):
        print "Attempting to create cut_dir: %s" %cut_dir
        os.system('mkdir %s' %cut_dir)

    if  os.path.isdir(cut_dir):
        for band in bands:
            os.system('mkdir %s/%s' %(cut_dir,band))
    else:
        print "cut_dir has problems and can't be corrected!!!!"
        good_dirs=False

    return good_dirs
