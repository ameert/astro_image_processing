#!/usr/bin/python

import pyfits as pf
import numpy as np
import scipy as s
import os
import sys
from numpy.random import shuffle
import random as ran
from mysql.mysql_class import *
import time
import pylab as pl
import scipy.signal as signal

seed_val = int(time.time())
s.random.seed(seed_val)
main_path = '/home/ameert/RESEARCH/clusters/data/sims/'
exptime =53.907456
def insert_im(data_gal, back_dat, rowc, colc):
    rowc = int(rowc)
    colc = int(colc)
    shape = np.array(back_dat.shape).astype(int)
    inshape = np.array(data_gal.shape).astype(int)
    # trim the inserted image
    inctr = (inshape/2.0).astype(int)
    
    backrange = np.array([[rowc, colc],[rowc, colc]])
    backrange[0,:] = np.round(backrange[0,:]-inctr)
    backrange[1,:] = np.round(backrange[1,:]+inctr)
    
    print 'inctr ',inctr
    print 'backrange'
    print backrange
    print shape
    print inshape

    back_lims = backrange[:,:]
    imlims = np.zeros_like(backrange)
    for a in [0,1]:
        if back_lims[0,a]<0:
            imlims[0,a]=-1.0*back_lims[0,a]
    for a in [0,1]:
        if back_lims[1,a]>shape[a]:
            imlims[1,a]=inshape[a]-1-(back_lims[1,a]-shape[a])
        else:
            imlims[1,a]=inshape[a]
    for a in [0,1]:
        if back_lims[0,a]<0:
            back_lims[0,a]=0
    for a in [0,1]:
        if back_lims[1,a]>shape[a]:
            back_lims[1,a]=shape[a]

    back_lims=back_lims
    imlims=imlims

    print 'backlims'
    print back_lims
    print 'imlims'
    print imlims
    print 'shape'
    print shape

    outim =back_dat[:,:] 
    outim[back_lims[0,0]:back_lims[1,0],back_lims[0,1]:back_lims[1,1]] += data_gal[imlims[0,0]:imlims[1,0],imlims[0,1]:imlims[1,1]]
    #pl.subplot(121)
    #pl.imshow(trim_im)
    #pl.subplot(122)
    #pl.imshow(trim_back)
    #pl.show()
    
    return outim

def combine_head(header, back_head, rowc, colc, icl=False):
    new_head = back_head
    if icl:
        stem='I_'
    else:
        stem='G_'

    new_head.update(stem+"rowc", rowc, "rowc of object upon insertion")
    new_head.update(stem+"colc", colc, "colc of object upon insertion")
    
    for key in header.keys():
        if key in ['IE', 'ID','N_SER','BT','RD','RE','ED','EB','BANG','DANG']:
            new_head.update(stem+key, header[key], header.comments[key])
        else:
            new_head.update(key, header[key], header.comments[key])

    return new_head

def cut_im(new_dat, rowc, colc, petrorad_pix, 
           cut_size = 20.0, min_size = 80.0):
    image_size = petrorad_pix * cut_size * 2.0
            
    if image_size < min_size:
        image_size = min_size

    row_low = np.round(rowc - .5 - .5*image_size)
    row_high = np.round(rowc - .5 + .5*image_size)
    col_low = np.round(colc - .5 - .5*image_size)
    col_high = np.round(colc - .5 + .5*image_size)

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
                
    trim_data = new_dat[row_low:row_high,col_low:col_high]

    return trim_data


def add_real_back(main_path, nm_stm, gal_im, ICL_im, useICL,back_im,
                  rowc, colc, petrorad_pix):

    
    back_image = pf.open(main_path+back_im)
    back_head = back_image[0].header 
    back_data = back_image[0].data
    back_image.close()
            
    data_image = pf.open(main_path+gal_im)
    data = data_image[0].data
    header = data_image[0].header
    data_image.close()

    new_dat= insert_im(data,back_data,rowc,colc)
    new_head = combine_head(header, back_head,rowc,colc, icl=False)
    if useICL:
        ICL_image = pf.open(main_path+ICL_im)
        ICL = ICL_image[0].data
        ICLheader = ICL_image[0].header
        ICL_image.close()
    
        new_dat = insert_im(ICL,new_dat,rowc,colc)
        new_head = combine_head(ICLheader, new_head, rowc,colc,icl=True)

    new_dat = cut_im(new_dat, rowc, colc, petrorad_pix)


    ext = pf.PrimaryHDU(new_dat, new_head)
    ext.writeto(main_path+nm_stm+"chipflat.fits", clobber = 1)
            
    return new_dat, new_head

def add_noise(image,header, Name,gain, dark_var, exptime = 53.907456):
    x_size, y_size  = np.shape(image)
    a = s.random.standard_normal((x_size, y_size))
    data = np.abs(image)

    new_image = data/exptime + a * s.sqrt(data/gain + dark_var)/exptime
    header.update("GAIN", gain, "Gain used in chip sim")
    header.update('RDNOISE', dark_var, "Dark Var in chip")
    header.update('EXPTIME', 1.0, "Exposure time (Sec)")

    ext = pf.PrimaryHDU(new_image, header)
    
    ext.writeto(Name + "chip.fits", clobber = 1)
        
    return


def mkwgt(Name, gain, dark_var, exptime = 53.907456):
    image = pf.open(Name + "chip.fits")
    head = image[0].header 
    data = image[0].data*exptime
    image.close()

    wz =  np.sqrt(data / gain+dark_var) / exptime

    hdu = pf.PrimaryHDU(wz.astype(np.float32))
    hdu.writeto(Name + "chip_r_W.fits", clobber = 1)

    return

if __name__=="__main__":

    gal_cat = {'galcount':(138529,142447,149162,558387,561842), 
               'run':(2583,2662,2738,3325,3325),
               'rerun':(40,40,40,41,41),
               'camcol':(4,3,4,1,4), 
               'field':(130,210,201,212,133),
               'rowc':{'g':(501.419,505.145,662.795,748.299,544.346),
                       'r':(490.855,494.561,652.493,735.198,534.715)},
               'colc':{'g':(881.964,1717.7,1070.83,1255.06,1789.28),
                       'r':(879.202,1716.55,1071.73,1256.36,1791.83)},
               'gain':{'g':(3.995,3.845,3.995,3.32,3.995),
                       'r':(4.76,4.72,4.76,4.71,4.76)},
               'darkvar':{'g':(1.96,1.3225,1.96,15.6025,1.96),
                          'r':(1.3225,1.3225,1.3225,1.8225,1.3225)},
               'petror50_kpc':[17.61,14.35,16.94,7.22,5.87],
               'new_kpc_per_arc': [1.6307,2.02872,2.42283,2.81298,3.19917,
                                   3.58137,3.95959,4.3338,4.704],}

    sim_to_choice =  np.array([1,8,15,22,29,36,43,50,57], dtype=int)
    choice = 0
    zchoice = 0

    gal_num = int(sys.argv[1])
    band = sys.argv[2]
    try:
        useICL = sys.argv[3]
        if useICL=='icl':
            useICL = True
        else:
            useICL = False
    except:
        useICL = False

    while(choice<6):
        if gal_num in sim_to_choice+choice:
            break
        else:
            choice+=1
    while(zchoice<len(sim_to_choice-1)):
        if gal_num >= sim_to_choice[zchoice+1]:
            zchoice+=1
        else:
            break
    print zchoice

    gal_cat['petror50_arcsec'] = np.array(gal_cat['petror50_kpc'])/gal_cat['new_kpc_per_arc'][zchoice]

    ICL_num = gal_num +63

    nm_stm = '%08d_%s_' %(gal_num, band)
    if useICL:
        nm_stm +="ICL_"
    else:
        nm_stm +="noICL_"

    print 'galaxy ',gal_num
    if useICL:
        print "adding ICL"
    else:
        print "NOT adding ICL"
    print 'ICL ',ICL_num

    gal_im = '%08d_%s_flat.fits' %(gal_num, band)
    ICL_im = '%08d_%s_flat.fits' %(ICL_num, band)
    back_im = 'bkrd_%s_%d.fits' %(band,gal_cat['galcount'][choice])
    image, header = add_real_back(main_path, nm_stm, gal_im, ICL_im, useICL,
                                  back_im,gal_cat['rowc'][band][choice], 
                                  gal_cat['colc'][band][choice],
                                  gal_cat['petror50_arcsec'][choice])

    add_noise(image, header, main_path+nm_stm,gal_cat['gain'][band][choice], gal_cat['darkvar'][band][choice])
    mkwgt(main_path +nm_stm, gal_cat['gain'][band][choice], gal_cat['darkvar'][band][choice])
