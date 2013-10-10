import os
import sys

def clean_dir(targetdir = './', do_all = 0):
    """This function removes files typically produced by PyMorph. You can choose between most or all PyMorph files."""
    to_remove = ['OEM_*.fits', 'SO_*.fits', 'R_*.html', 'seg.fits',
                     'SegCat.cat', 'index.html', 'restart.cat', 'P_*.png',
                     'pymorph.html', 'E_*.txt', 'OE_*.txt', 'BackMask.fits',
                     'check.fits','config.pyc','O_*.fits']
    
    if do_all:
        to_remove += ['agm_result_with_radius.csv', '*.sex', 'EM_*.fits',
                      '*.log', 'G_*', 'M_*.fits', '*.con', 'result.csv',
                      '*_out.cat', '*.cat.Shallow']
    
    thisdir = os.getcwd()

    os.chdir(targetdir)
    for del_file in to_remove:
        os.system('rm %s' %del_file)

    os.chdir(thisdir)

    return

if __name__ == '__main__':
    print "Running clean_dir"
    try:
        targetdir = sys.argv[1]
        do_all = int(sys.argv[2])
    except:
        print """To run clean_dir at the command line, you must provide two arguments:
        1: the target directory,
        2: 0(partial clean) or 1(full_clean)
        """
        sys.exit()

    clean_dir(targetdir = targetdir, do_all = do_all)
    
