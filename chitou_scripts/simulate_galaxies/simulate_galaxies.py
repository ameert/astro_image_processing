mag, bt, rd_kpc, inc, dang, re_kpc, ell, bang, ser_bulge,z,zp,kk,airmass = g.generate_params(g.dist_path, g.dist_stem)


print mag, bt, rd_kpc, inc, dang, re_kpc, ell, bang, ser_bulge,z,zp,kk,airmass

out_dir = '/home/ameert/Desktop/'
in_dir = '/home/ameert/mgc_cat'
psf_dir = '/scratch/ameert/mgc_cat/'

source_list = open(out_dir +'source_list.txt', 'w')
source_list.write('filename inital_psf_file mag bt bar rd inc dang re ell bang ser rbar avg_background\n')

numpy.random.seed()
random.seed()

number_of_galaxies = 20 

z = [0.05, 0.5, 1.0]
Dl = [216.113, 2754.22, 6424.06]

psf_file = psf_dir + 'file_list.txt'
in_psf = open(psf_file)
psf_names = []
for line in in_psf.readlines():
    psf_names.append(line.strip())
in_psf.close()

models = ['SER', 'DEVEXP','SEREXP']
scale = .05 #arcsec/pixel
zeropoint = 24.59
exptime = 4000.0 #seconds

galaxies_to_simulate = []

for model_counter in range(0,3):
    in_params = in_dir+'r_%s_arcsec_mag.txt' %(models[model_counter])
    in_params_data = open(in_params)
    in_params_data.readline()

    myind = []
    mag = []
    bt = []
    rd = []
    inc = []
    dang = []
    re = []
    ell = []
    bang = []
    ser = []
    rowctr = []
    colctr = []

    for line in in_params_data.readlines():
        split_data = line.split()
        myind.append(int(split_data[0]))
        mag.append(float(split_data[1]))
        bt.append(float(split_data[2]))
        rd.append(float(split_data[3]))
        inc.append(float(split_data[4]))
        dang.append(float(split_data[5]))
        re.append(float(split_data[6]))
        ell.append(float(split_data[7]))
        bang.append(float(split_data[8]))
        ser.append(float(split_data[9]))
        rowctr.append(float(split_data[10]))
        colctr.append(float(split_data[11]))
    
    in_params_data.close()

    for z_counter in [1,2]:
        for counter in range(32,54):
            
            # now generate the image
            stamp_fn_base = '%06d_z%d_%s' %(myind[counter], z_counter, models[model_counter])
            
            
            # copy psf
            old_psf_fn = psf_names[random.randint(0,len(psf_names)-1)]
            psf_fn = '%s%s_psf.fits' %(out_dir, stamp_fn_base)
            command = 'cp %s%s %s' %(psf_dir, old_psf_fn, psf_fn)
            os.system(command)

            mag_dim = mag[counter]-5.0*math.log10(Dl[0]/Dl[z_counter])

            if bt[counter] < .4: 
                if re[counter] > 5.0:
                    re[counter] = 5.0
                if ser[counter] > 5.0:
                    ser[counter] = 4.0
            else:
                if bt[counter] > .8: 
                    if rd[counter] > 5.0:
                        rd[counter] = 5.0
            if ser[counter] > 8.0:
                ser[counter] = 8.0
            if rd[counter] == 0.0:
                rd[counter] = 1.0
            if inc[counter] == 0.0:
                inc[counter] = 1.0
	    if dang[counter] == 0.0:
                dang[counter] = bang[counter]
	    if ell[counter] > 0.6:
                ell[counter] = 0.6	 

            re_z = re[counter]*Dl[0]*((1.0 + z[z_counter])**2.0)/(Dl[z_counter]*((1.0+z[0])**2.0)) #arcsec
            rd_z = rd[counter]*Dl[0]*((1.0 + z[z_counter])**2.0)/(Dl[z_counter]*((1.0+z[0])**2.0)) #arcsec

            re_z_pixel = re_z/scale #now in pixels
            rd_z_pixel = rd_z/scale #now in pixels

            flx = 10**(-0.4*(mag_dim - zeropoint))*exptime

            gradient = random.uniform(5.0,20.0)
            for_or_back = random.choice([1,3])

            background_chip = numpy.random.poisson(lam=310.0, size = (200,200))

            grad_pixel = (for_or_back - 2)*gradient/200.0

            background_grad = numpy.zeros([1,200], float)

            for back_count in range(200):
                background_grad[0,back_count] = grad_pixel*(back_count - 100.0)

            background_chip = background_chip + background_grad

            avg_back = numpy.average(background_chip)

            str = '%s_image.fits %s %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f\n' %(stamp_fn_base, old_psf_fn, mag_dim, bt[counter], rd[counter],rd_z_pixel, inc[counter], dang[counter], re[counter], re_z_pixel, ell[counter], bang[counter], ser[counter], z[z_counter], flx, gradient, avg_back)
            source_list.write(str) 
            
            str = '/home/ameert/galmorph/bin/GALMORPH_make_image %f %f %f %f %f %f %f %f %f 100 100 0.0 0.0 0.1 0.1 0.6 200 200 %s %s%s_sim.fits NULL' %(flx, bt[counter], rd_z_pixel, inc[counter], dang[counter], re_z_pixel, ell[counter], bang[counter], ser[counter], psf_fn, out_dir, stamp_fn_base)
            
            os.system(str)

            
            file_str = '%s%s_sim.fits' %(out_dir, stamp_fn_base)
            clean_image = pyfits.open(file_str)
            clean_data = clean_image[0].data
            clean_image.close()
            
            new_image = clean_data + background_chip

            str = '%s%s_image.fits' %(out_dir, stamp_fn_base)
            ext = pyfits.PrimaryHDU(new_image)
            ext.writeto(str)

source_list.close()
