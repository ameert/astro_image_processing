#from profile_to_arcsec_mag import *
from sersic_classes import im_obj
import pyfits as pf
import numpy as np
from mysql.mysql_class import *

bands = 'gri'
table_name = 'CAST'
dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'

def corner_im(rowc, colc, petro_half_light):
    image_size = petro_half_light * 20.0 * 2.0/.396
            
    if image_size < 80:
        image_size = 80

    # print shape(data)
    row_low = np.round(rowc - .5 - .5*image_size)
    row_high = np.round(rowc - .5 + .5*image_size)
    col_low = np.round(colc - .5 - .5*image_size)
    col_high = np.round(colc - .5 + .5*image_size)
    # -.5 accounts for sdss convention of first pixel being at (.5,.5)

    rowc_f = np.floor(rowc-0.5)
    colc_f = np.floor(colc-0.5)

    if row_low < 0.0:
        row_low = 0.0
        row_high = np.round(2*(rowc - .5))
    if row_high > 1488.0:
        row_high = 1488.0
        row_low = np.round(1488.0 - 2*(1488.0 - rowc + .5))
    if col_low < 0.0:
        col_low = 0.0
        col_high = np.round(2*(colc - .5))
    if col_high > 2047.0:
        col_high = 2047.0
        col_low = np.round(2047.0 - 2*(2047.0 - colc + .5))

    return (rowc_f - row_low, row_high-rowc_f, colc_f- col_low, col_high-colc_f)

def resize_images(galcount, ims):
    cursor = mysql_connect(dba, usr, pwd, '')

    cmd = 'select rowc_g, rowc_r, rowc_i, colc_g, colc_r, colc_i, petroR50_r from CAST where galcount = %d;' %galcount
    data =cursor.get_data(cmd)
    
    petro_half_light = data[6][0]
    locs = [(data[count][0], data[count+3][0]) for count in [0,1,2]]
    shapes = np.array([ corner_im(rowc, colc, petro_half_light) for rowc, colc in locs], dtype=int)
    
    pref_size = np.array(np.ma.min(shapes,0), dtype = int)

    coords =  pref_size - shapes
    
    new_im = []
    for im, row in zip(ims,[a for a in coords ]):
        row = row * np.array([-1, 1, -1, 1], dtype=int)
        row = list(row)
        if row[1]==0:
            row[1] = None
        if row[3]==0:
            row[3] = None
        print row
        new_im.append(im[row[0]:row[1], row[2]:row[3]])

    return new_im

def get_images(im_files, mask_files):
    """return the three images as an image cube with the 4th image as the sum"""
    ims = []
    sims = []
    masks = []

    for im_file, mask_file  in zip(im_files, mask_files):
        tmp_im = pf.open(im_file)
        
        sims.append(tmp_im[4].data)
        ims.append(tmp_im[1].data-tmp_im[5].data)
        tmp_im.close()
        
        tmp_im = pf.open(mask_file)
        masks.append(tmp_im[0].data)
        tmp_im.close()
        
    return ims,sims, masks
