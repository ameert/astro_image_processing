

def sql_query(model, number,choice):
    if choice == 1:
#        cmd = "select Name_r, galcount, n_%s, re_pix_%s, Ie_%s, eb_%s,rd_pix_%s, Id_%s, ed_%s, BT_%s, GalSky_avg, chi2nu_%s, fit_%s,  probaE,zeropoint_pymorph, zeropoint_sdss_r, kk_r, airmass_r, sex_halflight_%s,bpa_%s, dpa_%s,bxc_%s, byc_%s,dxc_%s, dyc_%s  from  r_full where  Name_r = '%06d_r_stamp' and  probaE > -1;" %(model,model,model,model, model, model, model, model, model, model, model, model, model, model, model, model, model, number)
        cmd = "select Name_r, galcount, n_%s, re_pix_%s, Ie_%s, eb_%s,rd_pix_%s, Id_%s, ed_%s, BT_%s, GalSky_%s, chi2nu_%s, fit_%s,  probaE,zeropoint_pymorph, zeropoint_sdss_r, kk_r, airmass_r, sex_halflight_%s,bpa_%s, dpa_%s,bxc_%s, byc_%s,dxc_%s, dyc_%s, GalSky_%s - GalSky_DevExp   from  r_full where  Name_r = '%06d_r_stamp' and  probaE > -1;" %(model,model,model,model, model, model, model, model, model, model, model, model, model, model, model, model, model, model, model, number)
        # cmd = "select Name_r, galcount, n_%s, re_pix_%s, Ie_%s, eb_%s,rd_pix_%s, Id_%s, ed_%s, BT_%s, GalSky_%s, chi2nu_%s, fit_%s,  probaE,zeropoint_pymorph, zeropoint_sdss_r, kk_r, airmass_r, petroR50_r  from  r_full where  Name_r = '%06d_r_stamp' and  probaE > -1;" %(model, model, model, model, model, model, model, model, model, model, model, number)

    elif choice == 2:
        cmd = "select Name, galcount, n_%s, re_pix_%s, Ie_%s, eb_%s,rd_pix_%s, Id_%s, ed_%s, BT_%s, GalSky_%s, chi2nu_%s, fit_%s from  old_fit.r_full where  Name = '%06d_r_stamp' and  probaE > -1;"  %(model, model, model, model, model, model, model, model, model, model, model, number)

    elif choice == 3:
        cmd = "select Name_r, galcount, nyc_A_r, nyc_r0_r, nyc_n_ser_r from  sdss_sample.r_full where  Name_r = '%06d_r_stamp' and  probaE > -1 and  nyc_dist < 3.0;" %(number)


    elif choice == 4:
        model = '45'
        cmd = "select Name, galcount, n_%s, re_pix_%s, Ie_%s, eb_%s,rd_pix_%s, Id_%s, ed_%s, BT_%s, GalSky_%s, chi2nu_%s, fit_%s from  test_fixed.combined2 where  galcount = '%d';"  %(model, model, model, model, model, model, model, model, model, model, model, number)

    return cmd

