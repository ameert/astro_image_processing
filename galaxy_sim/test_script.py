#!/usr/bin/python

import simulate_galaxy
import pyfits as p
from mysql.mysql_connect import *
import numpy as n
import sys

num_gal = 5000
num_good = 2500

cursor = mysql_connect('catalog','ameert','al130568')

cmd = 'select a.galcount from dr7_r_dev as a, dr7_r_ser as b, dr7_r_devexp as c,dr7_r_serexp as d where a.galcount = b.galcount and a.galcount = c.galcount and a.galcount= d.galcount and c.Ie < 40.0 and c.Ie > 0.0 and d.Ie < 40.0 and d.Ie > 0.0 and  c.re_kpc < 40 and  b.re_kpc < 40 and  d.re_kpc < 40 and (c.re_kpc/c.rd_kpc < 1 or c.BT > .5) c.re_kpc/c.rd_kpc < 1 or c.BT > .5)order by RAND(2345) LIMIT %s;' %(num_gal)


infile = open('/media/ACTIVE/final_sim/list.txt', 'w')
infile.write('galcount, name, n, re, Ie, eb, rd, Id, ed, BT, zeropoint_pymorph, zeropoint_sdss_r, kk_r, airmass_r,bpa, dpa, z\n')
cursor.execute(cmd)



all_numbers = []
rows = cursor.fetchall()
rows = list(rows)
number_list = []
for row in rows:
    number_list.append(row[0])

#number_list = [2]

for model in ['devexp']:#['serexp','ser']:#, 'dev', 'serexp', 'devexp']:
    tot_good = 0
    for number in number_list:
        if tot_good == num_good:
            break
        cmd = 'select a.galcount, b.run, b.camcol, b.field,  a.n_%s, a.re_pix_%s, a.re_kpc_%s, a.Ie_%s, a.eb_%s,a.rd_pix_%s, a.Id_%s, a.ed_%s, a.BT_%s, a.zeropoint_pymorph, -1.0*b.aa_r, b.kk_r, b.airmass_r,a.bpa_%s, a.dpa_%s, a.z, b.petroR50_r from  r_full_detail as a, CAST as b where  a.galcount = %d and a.galcount = b.galcount;' %(model,model,model, model,model, model, model, model, model, 'devexp', 'devexp', number)

        
        
        cursor.execute(cmd)
        rows_new = cursor.fetchall()
        rows_new = list(rows_new)

        galcount = int(rows_new[0][0])
        run = int(rows_new[0][1])
        camcol = int(rows_new[0][2])
        field = int(rows_new[0][3])
        n_model = float(rows_new[0][4])
        re_model= float(rows_new[0][5])*0.396
        re_kpc = float(rows_new[0][6])
        Ie_model= float(rows_new[0][7])
        eb_model= 1 - float(rows_new[0][8])
        rd_model= float(rows_new[0][9])*0.396
        Id_model= float(rows_new[0][10])
        ed_model= 1-float(rows_new[0][11])
        BT_model= float(rows_new[0][12])
        zeropoint_pymorph= float(rows_new[0][13])
        zeropoint_sdss_r= float(rows_new[0][14])
        kk_r= float(rows_new[0][15])
        airmass_r = float(rows_new[0][16])
        bpa_model = float(rows_new[0][17])+90.0
        dpa_model = float(rows_new[0][18])+90.0
        z_model =  float(rows_new[0][19])
        half_rad = float(rows_new[0][20])/0.396

        if n_model > 8:
            continue
        if re_kpc > 40:
            continue
        if re_model/rd_model > 1:
            if BT_model < .5:
                continue

        tot_good += 1

        re_model = re_model * n.sqrt(1-eb_model)

        print "bpa dpa ", bpa_model, dpa_model 
        Ie_model = Ie_model - zeropoint_pymorph + zeropoint_sdss_r
        Id_model = Id_model - zeropoint_pymorph + zeropoint_sdss_r

        print Id_model, Ie_model
        
        if Id_model < -60:
            Id_model = -1.0* Id_model
        if Ie_model < -60:
            Ie_model = -1.0* Ie_model
        if rd_model < 0:
            rd_model = 1000

        print Id_model, Ie_model
        
        Ie_count = mag_to_counts(Ie_model, -1.0*zeropoint_sdss_r)#,kk= kk_r, airmass = airmass_r)
        Id_count = mag_to_counts(Id_model, -1.0*zeropoint_sdss_r)#, kk=kk_r, airmass=airmass_r)

        if ed_model < 0:
            ed_model = 0

        if dpa_model < -300:
            dpa_model = 0.0

        inc = n.arccos(1.0 - ed_model)
        
        name = '%06d_%s' %(galcount, model)
        psf_image = '/home/ameert/fit_catalog/sdss_sample/cutouts/r/%06d_r_psf.fits' %(galcount)
        background = '/media/BACKUP/sdss_sample/data/r/fpC-%06d-r%d-%04d.fit.gz' %(run, camcol, field)
        if 1:
        #try:
            print name, Ie_model, Id_model
            print magsum(Ie_model, Id_model), BT_model
            print counts_to_mag(Ie_count + Id_count, zeropoint_sdss_r)
            gal = simulate_galaxy.galaxy('/home/ameert/Desktop/final_sim/20/',name,psf_image, Ie_count+Id_count, BT_model, rd_model, inc, dpa_model, re_model, eb_model, bpa_model, n_model, bulge_mag = Ie_model, disk_mag = Id_model, kk = kk_r, zp = zeropoint_sdss_r, airmass = airmass_r, half_light = half_rad)
            gal.make_profile()
            gal.add_noise()
            gal.add_simulated_back()
            gal.add_real_back(back_im = background)
            infile.write('%d %s %f %f %f %f %f %f %f %f %f %f %f %f %f %f\n' %(galcount, name, n_model, re_model, Ie_model,
                                                                         eb_model, rd_model, Id_model, ed_model,
                                                                         BT_model, zeropoint_sdss_r, kk_r,
                                                                        airmass_r, bpa_model, dpa_model, z_model))
        #except:
            #pass

infile.close()

cursor.close()
