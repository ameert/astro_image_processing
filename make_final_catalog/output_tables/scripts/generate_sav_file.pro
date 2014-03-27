PRO GENERATE_SAV_FILE, choice

;First do the CAST table
if choice EQ 1 THEN BEGIN
readcol, 'CAST.txt', galcount,spec1_phot0,badflag,objid,run,rerun,camCol,field,obj,stripe,startmu,ra_gal,dec_gal,z,specobjid,plate,mjd,fiberid,veldisp,veldispErr,FORMAT = 'L,L,L,LL,L,L,L,L,L,L,L,F,F,F,LL,L,L,L,F,F'

readcol, 'CAST.txt', eclass,devRad_u,devRad_g,devRad_r,devRad_i,devRad_z,devab_u,devab_g,devab_r,devab_i,devab_z,devmag_u,devmag_g,devmag_r,devmag_i,devmag_z,dered_u,dered_g,dered_r,dered_i,FORMAT = 'X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'

readcol, 'CAST.txt',dered_z,fracdev_u,fracdev_g,fracdev_r,fracdev_i,fracdev_z,petroMag_u,petroMag_g,petroMag_r,petroMag_i,petroMag_z,petroR90_u,petroR90_g,petroR90_r,petroR90_i,petroR90_z,petroR50_u,petroR50_g,petroR50_r,petroR50_i,FORMAT = 'X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'

readcol, 'CAST.txt',petroR50_z,extinction_u,extinction_g,extinction_r,extinction_i,extinction_z,aa_u,aa_g,aa_r,aa_i,aa_z,kk_u,kk_g,kk_r,kk_i,kk_z,airmass_u,airmass_g,airmass_r,airmass_i,FORMAT = 'X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'

readcol, 'CAST.txt',airmass_z,p_el_debiased,p_cs_debiased,spiral,elliptical,uncertain,rowc_u,rowc_g,rowc_r,rowc_i,rowc_z,colc_u,colc_g,colc_r,colc_i,colc_z,FORMAT = 'X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,L,L,L,F,F,F,F,F,F,F,F,F,F'

save, /variables, filename = 'CAST.sav'

ENDIF ELSE IF choice EQ 2 THEN BEGIN
readcol, "M2010_ordered.txt", galcount,id_marc,specObjID_marc,ra_marc,dec_marc,z_marc,probaE,probaEll,probaS0,probaSab,probaScd,ask_class, FORMAT = 'L,L,LL,F,F,F,F,F,F,F,F,F'

save, /variables, filename = 'M2010.sav'

ENDIF ELSE IF choice EQ 3 THEN BEGIN
readcol, 'NYUT.txt',galcount,dis,Id_nyu,ra_nyu,dec_nyu,A_u,A_g,A_r,A_i,A_z,r0_u,r0_g,r0_r,r0_i,r0_z,n_ser_u,n_ser_g,n_ser_r,n_ser_i,n_ser_z, FORMAT = 'L,F,L,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'

save, /variables, /verbose, filename = 'NYUT.sav'

ENDIF ELSE IF choice EQ 4 THEN BEGIN
readcol, 'SSDR6_ordered.txt', galcount,plate_dr6,mjd_dr6,fiberID_dr6,ra_dr6,dec_dr6,kcorrNg,kcorrNr,BkLRGg,BkLRGr,Bkmu,Bkmg,Bkmr,Bkpu,Bkpg,Bkpr,z_dr6,gmr,gmrN,gmrpetro,FORMAT = 'L,L,L,L,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'

readcol, 'SSDR6_ordered.txt', umr,umrPetro,Vmaxwti,dr6vdisp,logS,logRedeV,logRedeV_g,regrad,logRePetro,absmagdev,absmagpetro,sdsslogMstar,logRetot,absmagtot,sdsslogMstartot,ab_dev_g,ab_dev_r,fracdev_r_dr6,cir,Ga50,FORMAT = 'X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'

readcol, 'SSDR6_ordered.txt',Ga50z0,Ga16,Ga84,Gz50,FORMAT = 'X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,F'

save, /variables, /verbose, filename = 'SSDR6.sav'

ENDIF ELSE IF choice EQ 5 THEN BEGIN
readcol, 'simard_sample_ordered.txt', galcount,objid,z_simard,SpecClass_simard,arcsec_per_kpc_simard,V_max_simard,f_test_ser,f_test_devexp,Ie_ser_simard,Ie_devexp_simard,Ie_serexp_simard,Ie_err_ser_simard,Ie_err_devexp_simard,Ie_err_serexp_simard,Id_ser_simard,Id_devexp_simard,Id_serexp_simard,Id_err_ser_simard,Id_err_devexp_simard,Id_err_serexp_simard,FORMAT = 'L,LL,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'

readcol, 'simard_sample_ordered.txt',BT_ser_simard,BT_devexp_simard,BT_serexp_simard,BT_err_ser_simard,BT_err_devexp_simard,BT_err_serexp_simard,re_kpc_ser_simard,re_kpc_devexp_simard,re_kpc_serexp_simard,re_err_kpc_ser_simard,re_err_kpc_devexp_simard,re_err_kpc_serexp_simard,eb_ser_simard,eb_devexp_simard,eb_serexp_simard,eb_err_ser_simard,eb_err_devexp_simard,eb_err_serexp_simard,rd_kpc_ser_simard,rd_kpc_devexp_simard,FORMAT = 'X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'

readcol, 'simard_sample_ordered.txt',rd_kpc_serexp_simard,rd_err_kpc_ser_simard,rd_err_kpc_devexp_simard,rd_err_kpc_serexp_simard,n_ser_simard,n_devexp_simard,n_serexp_simard,n_err_ser_simard,n_err_devexp_simard,n_err_serexp_simard,ed_ser,ed_devexp,ed_serexp,colc_40,rowc_40,colc_60,rowc_60,true_x, true_y, absmag_r_tot_ser_simard, absmag_r_tot_ser_simard_err, FORMAT = 'X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'

save, /variables, filename = 'simard_sample.sav'

ENDIF ELSE IF choice EQ 6 THEN BEGIN
readcol, 'r_full_detail.txt',galcount,Name_r,Date,Filter,z,dis_modu,MorphType,SexSky,mag_auto,mag_err_auto,sex_halflight_pix,zeropoint_pymorph,C,C_err,A,A_err,S,S_err,G,M, FORMAT = 'L,A,A,A,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'


readcol, 'r_full_detail.txt',Comments,Ie_Dev,Ie_DevExp,Ie_Ser,Ie_SerExp,Ie_err_Dev,Ie_err_DevExp,Ie_err_Ser,Ie_err_SerExp,AbsMagBulge_Dev,AbsMagBulge_DevExp,AbsMagBulge_Ser,AbsMagBulge_SerExp,re_pix_Dev,re_pix_DevExp,re_pix_Ser,re_pix_SerExp,re_err_pix_Dev,re_err_pix_DevExp,re_err_pix_Ser,FORMAT = 'X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,A,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'

readcol, 'r_full_detail.txt',re_err_pix_SerExp,re_kpc_Dev,re_kpc_DevExp,re_kpc_Ser,re_kpc_SerExp,re_err_kpc_Dev,re_err_kpc_DevExp,re_err_kpc_Ser,re_err_kpc_SerExp,n_Dev,n_DevExp,n_Ser,n_SerExp,n_err_Dev,n_err_DevExp,n_err_Ser,n_err_SerExp,eb_Dev,eb_DevExp,eb_Ser,FORMAT = 'X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'

readcol, 'r_full_detail.txt',eb_SerExp,eb_err_Dev,eb_err_DevExp,eb_err_Ser,eb_err_SerExp,bboxy_Dev,bboxy_DevExp,bboxy_Ser,bboxy_SerExp,bboxy_err_Dev,bboxy_err_DevExp,bboxy_err_Ser,bboxy_err_SerExp,Id_Dev,Id_DevExp,Id_Ser,Id_SerExp,Id_err_Dev,Id_err_DevExp,Id_err_Ser,FORMAT = 'X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'
;
readcol, 'r_full_detail.txt',Id_err_SerExp,AbsMagDisk_Dev,AbsMagDisk_DevExp,AbsMagDisk_Ser,AbsMagDisk_SerExp,rd_pix_Dev,rd_pix_DevExp,rd_pix_Ser,rd_pix_SerExp,rd_err_pix_Dev,rd_err_pix_DevExp,rd_err_pix_Ser,rd_err_pix_SerExp,rd_kpc_Dev,rd_kpc_DevExp,rd_kpc_Ser,rd_kpc_SerExp,rd_err_kpc_Dev,rd_err_kpc_DevExp,rd_err_kpc_Ser,FORMAT = 'X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'

readcol, 'r_full_detail.txt',rd_err_kpc_SerExp,ed_Dev,ed_DevExp,ed_Ser,ed_SerExp,ed_err_Dev,ed_err_DevExp,ed_err_Ser,ed_err_SerExp,dboxy_Dev,dboxy_DevExp,dboxy_Ser,dboxy_SerExp,dboxy_err_Dev,dboxy_err_DevExp,dboxy_err_Ser,dboxy_err_SerExp,BT_Dev,BT_DevExp,BT_Ser,FORMAT = 'X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'


readcol, 'r_full_detail.txt',BT_SerExp,BT_err_Dev,BT_err_DevExp,BT_err_Ser,BT_err_SerExp,BD_Dev,BD_DevExp,BD_Ser,BD_SerExp,BD_err_Dev,BD_err_DevExp,BD_err_Ser,BD_err_SerExp,fit_Dev,fit_DevExp,fit_Ser,fit_SerExp,flag_Dev,flag_DevExp,flag_Ser,FORMAT = 'X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'


readcol, 'r_full_detail.txt',flag_SerExp,chi2nu_Dev,chi2nu_DevExp,chi2nu_Ser,chi2nu_Serexp,GalSky_Dev,GalSky_DevExp,GalSky_Ser,GalSky_SerExp,bpa_Dev,bpa_DevExp,bpa_Ser,bpa_Serexp,dpa_Dev,dpa_DevExp,dpa_Ser,dpa_SerExp,bxc_Dev,bxc_DevExp,bxc_Ser,FORMAT = 'X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F,F'


readcol, 'r_full_detail.txt',bxc_SerExp,byc_Dev,byc_DevExp,byc_Ser,byc_SerExp,dxc_Dev,dxc_DevExp,dxc_Ser,dxc_SerExp,dyc_Dev,dyc_DevExp,dyc_Ser,dyc_SerExp,FORMAT = 'X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,F,F,F,F,F,F,F,F,F,F,F,F,F'


save, /variables, filename = 'r_full_detail.sav'


ENDIF




END
