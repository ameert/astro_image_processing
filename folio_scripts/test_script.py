#!/usr/bin/python

import simulate_galaxy
import pyfits as p
from mysql_connect import *
import numpy as n

def mag_to_counts( mag, aa, kk = 0 , airmass = 0):
    exptime = 53.907456 #in seconds, taken from SDSS website www.sdss.org/dr3/algorithms/fluxcal.html
    return exptime * (10**(-.4*mag)) / (10**(0.4*(aa + kk*airmass)))

num_gal = 2000

cursor = mysql_connect('sdss_sample','pymorph','pymorph')

cmd = 'select galcount from r_full where fit_ser = 1 and fit_dev = 1 and fit_serexp = 1 and fit_devexp = 1 and z<.12 and z>.08 order by RAND(36459) LIMIT %s;' %(num_gal)

file = open('/home/ameert/Desktop/sim_image/list.txt', 'w')
file.write('galcount, name, n, re, Ie, eb, rd, Id, ed, BT, zeropoint_pymorph, zeropoint_sdss_r, kk_r, airmass_r,bpa, dpa, z\n')
cursor.execute(cmd)

all_numbers = []
rows = cursor.fetchall()
rows = list(rows)
number_list = []
for row in rows:
    number_list.append(row[0])

#number_list = [2]
for number in number_list:
    for model in ['devexp']:#['ser', 'dev', 'serexp', 'devexp']:
        cmd = 'select galcount, run, camcol, field,  n_%s, re_pix_%s, Ie_%s, eb_%s,rd_pix_%s, Id_%s, ed_%s, BT_%s, zeropoint_pymorph, zeropoint_sdss_r, kk_r, airmass_r,bpa_%s, dpa_%s, z, sex_halflight_%s from  r_full where  galcount = %d;' %(model,model,model,model, model, model, model, model, model, model, model, number)

        
        cursor.execute(cmd)
        rows_new = cursor.fetchall()
        rows_new = list(rows_new)

        galcount = int(rows_new[0][0])
        run = int(rows_new[0][1])
        camcol = int(rows_new[0][2])
        field = int(rows_new[0][3])
        n_model = float(rows_new[0][4])
        re_model= float(rows_new[0][5])*0.396
        Ie_model= float(rows_new[0][6])
        eb_model= 1 - float(rows_new[0][7])
        rd_model= float(rows_new[0][8])*0.396
        Id_model= float(rows_new[0][9])
        ed_model= 1-float(rows_new[0][10])
        BT_model= float(rows_new[0][11])
        zeropoint_pymorph= float(rows_new[0][12])
        zeropoint_sdss_r= float(rows_new[0][13])
        kk_r= float(rows_new[0][14])
        airmass_r = float(rows_new[0][15])
        bpa_model = float(rows_new[0][16])+90.0
        dpa_model = float(rows_new[0][17])+90.0
        z_model =  float(rows_new[0][18])
        half_rad = float(rows_new[0][19])
        
        Ie_model = Ie_model - zeropoint_pymorph + zeropoint_sdss_r
        Id_model = Id_model - zeropoint_pymorph + zeropoint_sdss_r

        if Id_model < -60:
            Id_model = -1.0* Id_model
        if Ie_model < -60:
            Ie_model = -1.0* Ie_model
        if rd_model < 0:
            rd_model = 1000
    
        Ie_count = mag_to_counts(Ie_model, -1.0*zeropoint_sdss_r,kk= kk_r, airmass = airmass_r)
        Id_count = mag_to_counts(Id_model, -1.0*zeropoint_sdss_r, kk=kk_r, airmass=airmass_r)

        if ed_model < 0:
            ed_model = 0

        if dpa_model < -300:
            dpa_model = 0.0

        inc = n.arccos(1.0 - ed_model)
        
        name = '%06d_%s' %(galcount, model)
        psf_image = '/home/ameert/sdss_sample/cutouts/r/%06d_r_psf.fits' %(galcount)
        background = '/media/BACKUP/sdss_sample/data_dir/fpC-%06d-r%d-%04d.fit.gz' %(run, camcol, field)
        try:
            print name
            gal = simulate_galaxy.galaxy('/home/ameert/Desktop',name,psf_image, Ie_count+Id_count, BT_model, rd_model, inc, dpa_model, re_model, eb_model, bpa_model, n_model, bulge_mag = Ie_model, disk_mag = Id_model, kk = kk_r, zp = zeropoint_sdss_r, airmass = airmass_r, half_light = half_rad)
            gal.make_profile()
            gal.add_noise()
            gal.add_simulated_back()
            gal.add_real_back(back_im = background)
            file.write('%d %s %f %f %f %f %f %f %f %f %f %f %f %f %f %f\n' %(galcount, name, n_model, re_model, Ie_model,
                                                                          eb_model, rd_model, Id_model, ed_model,
                                                                          BT_model, zeropoint_sdss_r, kk_r,
                                                                          airmass_r, bpa_model, dpa_model, z_model))
        except:
            pass

file.close()

for step_back in ['flat', 'noise', 'realback', 'simsky']:
    file = open('/home/ameert/Desktop/sim_image/sdss_%s.cat' %(step_back), 'w')
    file.write('gal_id gimg star\n')
    for number in number_list:
        for model in ['ser', 'dev', 'serexp', 'devexp']:
            name = '%08d_%s' %(galcount, model)
            psf_image = '%08d_r_psf.fits' %(galcount)
            gimg = '%08d_%s_%s.fits' %(galcount, model, step_back)

            file.write('%s %s %s\n' %(name, gimg, psf_image))

    file.close()
    

cursor.close()
