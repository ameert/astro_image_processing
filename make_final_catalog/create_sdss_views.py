-- petro mags 
DROP VIEW IF EXISTS r_sdss_petro;
CREATE VIEW r_sdss_petro AS SELECT galcount, petroMag_r as m_tot, 1.0 as BT,  
petroR50_r as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
petroMag_r as m_bulge , petroMagErr_r as m_bulge_err ,
petroR50_r as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_r as Galsky , skyErr_r as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;

DROP VIEW IF EXISTS g_sdss_petro;
CREATE VIEW g_sdss_petro AS SELECT galcount, petroMag_g as m_tot, 1.0 as BT,  
petroR50_g as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
petroMag_g as m_bulge , petroMagErr_g as m_bulge_err ,
petroR50_g as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_g as Galsky , skyErr_g as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;

DROP VIEW IF EXISTS i_sdss_petro;
CREATE VIEW i_sdss_petro AS SELECT galcount, petroMag_i as m_tot, 1.0 as BT,  
petroR50_i as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
petroMag_i as m_bulge , petroMagErr_i as m_bulge_err ,
petroR50_i as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_i as Galsky , skyErr_i as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;


-- model mags
DROP VIEW IF EXISTS r_sdssmodel_dev;
CREATE VIEW r_sdssmodel_dev AS SELECT galcount, ModelMag_r as m_tot, 1.0 as BT,  
-999.0 as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
ModelMag_r as m_bulge , ModelMagErr_r as m_bulge_err ,
-999.0 as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_r as Galsky , skyErr_r as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;

DROP VIEW IF EXISTS g_sdssmodel_dev;
CREATE VIEW g_sdssmodel_dev AS SELECT galcount, ModelMag_g as m_tot, 1.0 as BT,  
-999.0 as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
ModelMag_g as m_bulge , ModelMagErr_g as m_bulge_err ,
-999.0 as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_g as Galsky , skyErr_g as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;

DROP VIEW IF EXISTS i_sdssmodel_dev;
CREATE VIEW i_sdssmodel_dev AS SELECT galcount, ModelMag_i as m_tot, 1.0 as BT,  
-999.0 as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
ModelMag_i as m_bulge , ModelMagErr_i as m_bulge_err ,
-999.0 as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_i as Galsky , skyErr_i as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;




DROP VIEW IF EXISTS r_sdssmodel_ser;
CREATE VIEW r_sdssmodel_ser AS SELECT galcount, ModelMag_r as m_tot, 1.0 as BT,  
-999.0 as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
ModelMag_r as m_bulge , ModelMagErr_r as m_bulge_err ,
-999.0 as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_r as Galsky , skyErr_r as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;

DROP VIEW IF EXISTS g_sdssmodel_ser;
CREATE VIEW g_sdssmodel_ser AS SELECT galcount, ModelMag_g as m_tot, 1.0 as BT,  
-999.0 as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
ModelMag_g as m_bulge , ModelMagErr_g as m_bulge_err ,
-999.0 as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_g as Galsky , skyErr_g as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;

DROP VIEW IF EXISTS i_sdssmodel_ser;
CREATE VIEW i_sdssmodel_ser AS SELECT galcount, ModelMag_i as m_tot, 1.0 as BT,  
-999.0 as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
ModelMag_i as m_bulge , ModelMagErr_i as m_bulge_err ,
-999.0 as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_i as Galsky , skyErr_i as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;


DROP VIEW IF EXISTS r_sdssmodel_devexp;
CREATE VIEW r_sdssmodel_devexp AS SELECT galcount, ModelMag_r as m_tot, 1.0 as BT,  
-999.0 as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
ModelMag_r as m_bulge , ModelMagErr_r as m_bulge_err ,
-999.0 as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_r as Galsky , skyErr_r as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;

DROP VIEW IF EXISTS g_sdssmodel_devexp;
CREATE VIEW g_sdssmodel_devexp AS SELECT galcount, ModelMag_g as m_tot, 1.0 as BT,  
-999.0 as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
ModelMag_g as m_bulge , ModelMagErr_g as m_bulge_err ,
-999.0 as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_g as Galsky , skyErr_g as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;

DROP VIEW IF EXISTS i_sdssmodel_devexp;
CREATE VIEW i_sdssmodel_devexp AS SELECT galcount, ModelMag_i as m_tot, 1.0 as BT,  
-999.0 as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
ModelMag_i as m_bulge , ModelMagErr_i as m_bulge_err ,
-999.0 as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_i as Galsky , skyErr_i as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;



DROP VIEW IF EXISTS r_sdssmodel_serexp;
CREATE VIEW r_sdssmodel_serexp AS SELECT galcount, ModelMag_r as m_tot, 1.0 as BT,  
-999.0 as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
ModelMag_r as m_bulge , ModelMagErr_r as m_bulge_err ,
-999.0 as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_r as Galsky , skyErr_r as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;

DROP VIEW IF EXISTS g_sdssmodel_serexp;
CREATE VIEW g_sdssmodel_serexp AS SELECT galcount, ModelMag_g as m_tot, 1.0 as BT,  
-999.0 as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
ModelMag_g as m_bulge , ModelMagErr_g as m_bulge_err ,
-999.0 as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_g as Galsky , skyErr_g as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;

DROP VIEW IF EXISTS i_sdssmodel_serexp;
CREATE VIEW i_sdssmodel_serexp AS SELECT galcount, ModelMag_i as m_tot, 1.0 as BT,  
-999.0 as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
ModelMag_i as m_bulge , ModelMagErr_i as m_bulge_err ,
-999.0 as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_i as Galsky , skyErr_i as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;



-- dev mags
DROP VIEW IF EXISTS r_sdss_dev;
CREATE VIEW r_sdss_dev AS SELECT galcount, DevMag_r as m_tot, 1.0 as BT,  
ifNull(devRad_r*sqrt(devab_r), -999.0) as Hrad_corr ,devab_r as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
DevMag_r as m_bulge , -999.0 as m_bulge_err ,
devRad_r as r_bulge , -999.0 as r_bulge_err ,
4.0 as n_bulge , -999.0 as n_bulge_err ,
devab_r as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_r as Galsky , skyErr_r as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;

DROP VIEW IF EXISTS g_sdss_dev;
CREATE VIEW g_sdss_dev AS SELECT galcount, DevMag_g as m_tot, 1.0 as BT,  
ifNull(devRad_g*sqrt(devab_g), -999.0) as Hrad_corr ,devab_g as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
DevMag_g as m_bulge , -999.0 as m_bulge_err ,
devRad_g as r_bulge , -999.0 as r_bulge_err ,
4.0 as n_bulge , -999.0 as n_bulge_err ,
devab_g as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_g as Galsky , skyErr_g as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;

DROP VIEW IF EXISTS i_sdss_dev;
CREATE VIEW i_sdss_dev AS SELECT galcount, DevMag_i as m_tot, 1.0 as BT,  
ifNull(devRad_i*sqrt(devab_i), -999.0) as Hrad_corr ,devab_i as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
DevMag_i as m_bulge , -999.0 as m_bulge_err ,
devRad_i as r_bulge , -999.0 as r_bulge_err ,
4.0 as n_bulge , -999.0 as n_bulge_err ,
devab_i as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_i as Galsky , skyErr_i as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;

--lackner mappings
DROP VIEW IF EXISTS i_lackner_dev;
CREATE VIEW i_lackner_dev AS SELECT * from i_lackner_dvc;

DROP VIEW IF EXISTS i_lackner_devexp;
CREATE VIEW i_lackner_devexp AS SELECT * from i_lackner_nb4;

DROP VIEW IF EXISTS g_lackner_dev;
CREATE VIEW g_lackner_dev AS SELECT * from g_lackner_dvc;

DROP VIEW IF EXISTS g_lackner_devexp;
CREATE VIEW g_lackner_devexp AS SELECT * from g_lackner_nb4;

DROP VIEW IF EXISTS r_lackner_dev;
CREATE VIEW r_lackner_dev AS SELECT * from r_lackner_dvc;

DROP VIEW IF EXISTS r_lackner_devexp;
CREATE VIEW r_lackner_devexp AS SELECT * from r_lackner_nb4;


-- cmodel mags
DROP VIEW IF EXISTS r_cmodel_serexp;
CREATE VIEW r_cmodel_serexp AS SELECT galcount, -2.5*log10(pow(10,-0.4*(c.devmag_r-0.0637))*fracdev_r + (1.0-fracdev_r)*pow(10,-0.4*(expmag_r-0.0103))) as m_tot, fracdev_r as BT,  
-999.0 as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
-999.0 as m_bulge , -999.0 as m_bulge_err ,
-999.0 as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_r as Galsky , skyErr_r as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;


DROP VIEW IF EXISTS g_cmodel_serexp;
CREATE VIEW g_cmodel_serexp AS SELECT galcount, -2.5*log10(pow(10,-0.4*(abs(devmag_g)-0.0637))*fracdev_g + (1.0-fracdev_g)*pow(10,-0.4*(abs(expmag_g)-0.0103))) as m_tot, fracdev_g as BT,  
-999.0 as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
-999.0 as m_bulge , -999.0 as m_bulge_err ,
-999.0 as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_g as Galsky , skyErr_g as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;

DROP VIEW IF EXISTS g_sdss_cmodel;
CREATE VIEW g_sdss_cmodel AS SELECT galcount, -2.5*log10(pow(10,-0.4*(abs(devmag_g)-0.0637))*fracdev_g + (1.0-fracdev_g)*pow(10,-0.4*(abs(expmag_g)-0.0103))) as m_tot, fracdev_g as BT,  
-999.0 as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
-999.0 as m_bulge , -999.0 as m_bulge_err ,
-999.0 as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_g as Galsky , skyErr_g as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;



DROP VIEW IF EXISTS i_sdss_cmodel;
CREATE VIEW i_sdss_cmodel AS SELECT galcount, -2.5*log10(pow(10,-0.4*(abs(devmag_i)-0.0637))*fracdev_i + (1.0-fracdev_i)*pow(10,-0.4*(abs(expmag_i)-0.0103))) as m_tot, fracdev_i as BT,  
-999.0 as Hrad_corr , -999.0 as ba_tot_corr ,
-999.0 as xctr_bulge , -999.0 as xctr_bulge_err ,  
-999.0 as yctr_bulge , -999.0 as yctr_bulge_err ,  
-999.0 as m_bulge , -999.0 as m_bulge_err ,
-999.0 as r_bulge , -999.0 as r_bulge_err ,
-999.0 as n_bulge , -999.0 as n_bulge_err ,
-999.0 as ba_bulge , -999.0 as ba_bulge_err ,
-999.0 as pa_bulge , -999.0 as pa_bulge_err ,
-999.0 as xctr_disk , -999.0 as xctr_disk_err ,  
-999.0 as yctr_disk , -999.0 as yctr_disk_err ,  
-999.0 as m_disk , -999.0 as m_disk_err ,
-999.0 as r_disk , -999.0 as r_disk_err ,
-999.0 as ba_disk , -999.0 as ba_disk_err ,
-999.0 as pa_disk , -999.0 as pa_disk_err ,
-999.0 as chi2nu , -999.0 as Goodness ,
sky_i as Galsky , skyErr_i as Galsky_err , 
-999 as fit , -999 as FitFlag,
-999 as flag, -999 as Manual_flag,
-999 as FinalFlag, '-999' as Comments
FROM CAST;


create table r_band_best like r_band_dev;
create table r_lackner_best like r_band_dev;
create table r_simard_best like r_band_dev;
create table r_mendel_best like r_band_dev;



insert into r_band_best (galcount, m_tot) select a.galcount, a.m_tot from r_band_serexp as a, Flags_catalog as x where a.galcount = x.galcount  and x.band = 'r' and x.ftype = 'u' and x.model = 'serexp'  and ( x.flag&pow(2,19)=0 ) ;
insert into r_lackner_best (galcount, m_tot) select a.galcount, a.m_tot-0.071648 from r_lackner_dev as a, r_lackner_fit as b where a.galcount = b.galcount and b.model ='dvc';
insert into r_lackner_best (galcount, m_tot) select a.galcount, a.m_tot-0.0103 from r_lackner_exp as a, r_lackner_fit as b where a.galcount = b.galcount and b.model ='exp';
insert into r_lackner_best (galcount, m_tot) select a.galcount, a.m_tot from r_lackner_ser as a, r_lackner_fit as b where a.galcount = b.galcount and b.model ='ser';
insert into r_lackner_best (galcount, m_tot) select a.galcount, a.m_tot-0.0103 from r_lackner_nb1 as a, r_lackner_fit as b where a.galcount = b.galcount and b.model ='nb1';
insert into r_lackner_best (galcount, m_tot) select a.galcount, -2.5*log10(pow(10,-0.4*(a.m_bulge-0.0637)) + pow(10,-0.4*(a.m_disk-0.0103))) from r_lackner_devexp as a, r_lackner_fit as b where a.galcount = b.galcount and b.model ='nb4';
insert into r_simard_best (galcount, m_tot) select a.galcount, a.m_tot from r_simard_ser as a, r_simard_fit as x where a.galcount = x.galcount  and  x.Prob_Ps > 0.32 ;
insert into r_simard_best (galcount, m_tot) select a.galcount, a.m_tot from r_simard_devexp as a, r_simard_fit as x where a.galcount = x.galcount  and  x.Prob_Ps <= 0.32 and x.Prob_n4>0.32;
insert into r_simard_best (galcount, m_tot) select a.galcount, a.m_tot from r_simard_serexp as a, r_simard_fit as x where a.galcount = x.galcount  and  x.Prob_Ps <= 0.32 and x.Prob_n4<=0.32;

insert into r_mendel_best (galcount, m_tot) select a.galcount, a.m_tot from r_simard_ser as a, r_simard_fit as x where a.galcount = x.galcount  and  x.ProfType <=2 ;
insert into r_mendel_best (galcount, m_tot) select a.galcount, a.m_tot from r_simard_devexp as a, r_simard_fit as x where a.galcount = x.galcount  and  x.ProfType =3 ;



create table g_band_best like g_band_dev;
create table g_lackner_best like g_band_dev;
create table g_simard_best like g_band_dev;
create table g_mendel_best like g_band_dev;



insert into g_band_best (galcount, m_tot) select a.galcount, a.m_tot from g_band_serexp as a, Flags_catalog as x where a.galcount = x.galcount  and x.band = 'g' and x.ftype = 'u' and x.model = 'serexp'  and ( x.flag&pow(2,19)=0 ) ;
insert into g_lackner_best (galcount, m_tot) select a.galcount, a.m_tot-0.071648 from g_lackner_dev as a, g_lackner_fit as b where a.galcount = b.galcount and b.model ='dvc';
insert into g_lackner_best (galcount, m_tot) select a.galcount, a.m_tot-0.0103 from g_lackner_exp as a, g_lackner_fit as b where a.galcount = b.galcount and b.model ='exp';
insert into g_lackner_best (galcount, m_tot) select a.galcount, a.m_tot from g_lackner_ser as a, g_lackner_fit as b where a.galcount = b.galcount and b.model ='ser';
insert into g_lackner_best (galcount, m_tot) select a.galcount, a.m_tot-0.0103 from g_lackner_nb1 as a, g_lackner_fit as b where a.galcount = b.galcount and b.model ='nb1';
insert into g_lackner_best (galcount, m_tot) select a.galcount, -2.5*log10(pow(10,-0.4*(a.m_bulge-0.0637)) + pow(10,-0.4*(a.m_disk-0.0103))) from g_lackner_devexp as a, g_lackner_fit as b where a.galcount = b.galcount and b.model ='nb4';
insert into g_simard_best (galcount, m_tot) select a.galcount, a.m_tot from g_simard_ser as a, r_simard_fit as x where a.galcount = x.galcount  and  x.Prob_Ps > 0.32 ;
insert into g_simard_best (galcount, m_tot) select a.galcount, a.m_tot from g_simard_devexp as a, g_simard_fit as x where a.galcount = x.galcount  and  x.Prob_Ps <= 0.32 and x.Prob_n4>0.32;
insert into g_simard_best (galcount, m_tot) select a.galcount, a.m_tot from g_simard_serexp as a, g_simard_fit as x where a.galcount = x.galcount  and  x.Prob_Ps <= 0.32 and x.Prob_n4<=0.32;

insert into g_mendel_best (galcount, m_tot) select a.galcount, a.m_tot from g_simard_ser as a, g_simard_fit as x where a.galcount = x.galcount  and  x.ProfType <=2 ;
insert into g_mendel_best (galcount, m_tot) select a.galcount, a.m_tot from g_simard_devexp as a, g_simard_fit as x where a.galcount = x.galcount  and  x.ProfType =3 ;


create table i_band_best like i_band_dev;
create table i_lackner_best like i_band_dev;
create table i_simard_best like i_band_dev;
create table i_mendel_best like i_band_dev;



insert into i_band_best select a.* from i_band_serexp as a, Flags_catalog as x where a.galcount = x.galcount  and x.band = 'i' and x.ftype = 'u' and x.model = 'serexp'  and ( x.flag&pow(2,19)=0 ) ;
insert into i_band_best (galcount, m_tot) select a.galcount, a.m_tot from i_band_serexp as a, Flags_catalog as x where a.galcount = x.galcount  and x.band = 'i' and x.ftype = 'u' and x.model = 'serexp'  and ( x.flag&pow(2,19)=0 ) ;

insert into i_lackner_best (galcount, m_tot) select a.galcount, a.m_tot-0.071648 from i_lackner_dev as a, i_lackner_fit as b where a.galcount = b.galcount and b.model ='dvc';
insert into i_lackner_best (galcount, m_tot) select a.galcount, a.m_tot-0.0103 from i_lackner_exp as a, i_lackner_fit as b where a.galcount = b.galcount and b.model ='exp';
insert into i_lackner_best (galcount, m_tot) select a.galcount, a.m_tot from i_lackner_ser as a, i_lackner_fit as b where a.galcount = b.galcount and b.model ='ser';
insert into i_lackner_best (galcount, m_tot) select a.galcount, a.m_tot-0.0103 from i_lackner_nb1 as a, i_lackner_fit as b where a.galcount = b.galcount and b.model ='nb1';
insert into i_lackner_best (galcount, m_tot) select a.galcount, -2.5*log10(pow(10,-0.4*(a.m_bulge-0.0637)) + pow(10,-0.4*(a.m_disk-0.0103))) from i_lackner_devexp as a, i_lackner_fit as b where a.galcount = b.galcount and b.model ='nb4';
insert into i_simard_best (galcount, m_tot) select a.galcount, a.m_tot from i_simard_ser as a, r_simard_fit as x where a.galcount = x.galcount  and  x.Prob_Ps > 0.32 ;
insert into i_simard_best (galcount, m_tot) select a.galcount, a.m_tot from i_simard_devexp as a, i_simard_fit as x where a.galcount = x.galcount  and  x.Prob_Ps <= 0.32 and x.Prob_n4>0.32;
insert into i_simard_best (galcount, m_tot) select a.galcount, a.m_tot from i_simard_serexp as a, i_simard_fit as x where a.galcount = x.galcount  and  x.Prob_Ps <= 0.32 and x.Prob_n4<=0.32;

insert into i_mendel_best (galcount, m_tot) select a.galcount, a.m_tot from i_simard_ser as a, i_simard_fit as x where a.galcount = x.galcount  and  x.ProfType <=2 ;
insert into i_mendel_best (galcount, m_tot) select a.galcount, a.m_tot from i_simard_devexp as a, i_simard_fit as x where a.galcount = x.galcount  and  x.ProfType =3 ;





DROP VIEW IF EXISTS g_fiber_ser;
CREATE VIEW g_fiber_ser AS SELECT a.galcount,  IFNULL(a.m_tot-2.5*log10(b.fiber),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
a.m_bulge , a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
a.m_disk , a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM g_band_ser as a, cir_model_g_ser as b where a.galcount=b.galcount;

DROP VIEW IF EXISTS r_fiber_ser;
CREATE VIEW r_fiber_ser AS SELECT a.galcount,  IFNULL(a.m_tot-2.5*log10(b.fiber),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
a.m_bulge , a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
a.m_disk , a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM r_band_ser as a, cir_model_r_ser as b where a.galcount=b.galcount;

DROP VIEW IF EXISTS i_fiber_ser;
CREATE VIEW i_fiber_ser AS SELECT a.galcount,  IFNULL(a.m_tot-2.5*log10(b.fiber),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
a.m_bulge , a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
a.m_disk , a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM i_band_ser as a, cir_model_i_ser as b where a.galcount=b.galcount;


DROP VIEW IF EXISTS g_petroR50_ser;
CREATE VIEW g_petroR50_ser AS SELECT a.galcount,  IFNULL(a.m_tot-2.5*log10(b.petro50),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
a.m_bulge , a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
a.m_disk , a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM g_band_ser as a, cir_model_g_ser as b where a.galcount=b.galcount;

DROP VIEW IF EXISTS r_petroR50_ser;
CREATE VIEW r_petroR50_ser AS SELECT a.galcount,  IFNULL(a.m_tot-2.5*log10(b.petro50),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
a.m_bulge , a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
a.m_disk , a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM r_band_ser as a, cir_model_r_ser as b where a.galcount=b.galcount;

DROP VIEW IF EXISTS i_petroR50_ser;
CREATE VIEW i_petroR50_ser AS SELECT a.galcount,  IFNULL(a.m_tot-2.5*log10(b.petro50),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
a.m_bulge , a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
a.m_disk , a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM i_band_ser as a, cir_model_i_ser as b where a.galcount=b.galcount;





DROP VIEW IF EXISTS i_model_ser;
CREATE VIEW i_model_ser AS SELECT a.galcount,  IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8),a.m_tot-2.5*log10(b.exprad4)),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
a.m_bulge , a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
a.m_disk , a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM i_band_ser as a, modelcolor_i_ser as b , CAST as c where a.galcount = c.galcount and  a.galcount=b.galcount;

DROP VIEW IF EXISTS i_model_serexp;
CREATE VIEW i_model_serexp AS SELECT a.galcount,  IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8),a.m_tot-2.5*log10(b.exprad4)),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8)-2.5*log10(b.devrad8_BT),a.m_tot-2.5*log10(b.exprad4)-2.5*log10(b.exprad4_BT)),-999) as m_bulge , 
a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8)-2.5*log10(1.0-b.devrad8_BT),a.m_tot-2.5*log10(b.exprad4)-2.5*log10(1.0-b.exprad4_BT)),-999) as m_disk  , 
a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM i_band_serexp as a, modelcolor_i_serexp as b, CAST as c where 
a.galcount=b.galcount and a.galcount=c.galcount;


DROP VIEW IF EXISTS i_model_devexp;
CREATE VIEW i_model_devexp AS SELECT a.galcount,  IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8),a.m_tot-2.5*log10(b.exprad4)),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8)-2.5*log10(b.devrad8_BT),a.m_tot-2.5*log10(b.exprad4)-2.5*log10(b.exprad4_BT)),-999) as m_bulge , 
a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8)-2.5*log10(1.0-b.devrad8_BT),a.m_tot-2.5*log10(b.exprad4)-2.5*log10(1.0-b.exprad4_BT)),-999) as m_disk  , 
a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM i_band_devexp as a, modelcolor_i_devexp as b , CAST as c where a.galcount = c.galcount and  a.galcount=b.galcount;

DROP VIEW IF EXISTS i_model_dev;
CREATE VIEW i_model_dev AS SELECT a.galcount,  IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8),a.m_tot-2.5*log10(b.exprad4)),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
a.m_bulge , a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
a.m_disk , a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM i_band_dev as a, modelcolor_i_dev as b , CAST as c where a.galcount = c.galcount and  a.galcount=b.galcount;









DROP VIEW IF EXISTS r_model_ser;
CREATE VIEW r_model_ser AS SELECT a.galcount,  IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8),a.m_tot-2.5*log10(b.exprad4)),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
a.m_bulge , a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
a.m_disk , a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM r_band_ser as a, modelcolor_r_ser as b , CAST as c where a.galcount = c.galcount and  a.galcount=b.galcount;

DROP VIEW IF EXISTS r_model_serexp;
CREATE VIEW r_model_serexp AS SELECT a.galcount,  IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8),a.m_tot-2.5*log10(b.exprad4)),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8)-2.5*log10(b.devrad8_BT),a.m_tot-2.5*log10(b.exprad4)-2.5*log10(b.exprad4_BT)),-999) as m_bulge , 
a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8)-2.5*log10(1.0-b.devrad8_BT),a.m_tot-2.5*log10(b.exprad4)-2.5*log10(1.0-b.exprad4_BT)),-999) as m_disk , a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM r_band_serexp as a, modelcolor_r_serexp as b , CAST as c where a.galcount = c.galcount and  a.galcount=b.galcount;

DROP VIEW IF EXISTS r_model_dev;
CREATE VIEW r_model_dev AS SELECT a.galcount,  IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8),a.m_tot-2.5*log10(b.exprad4)),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
a.m_bulge , a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
a.m_disk , a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM r_band_dev as a, modelcolor_r_dev as b , CAST as c where a.galcount = c.galcount and  a.galcount=b.galcount;

DROP VIEW IF EXISTS r_model_devexp;
CREATE VIEW r_model_devexp AS SELECT a.galcount,  IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8),a.m_tot-2.5*log10(b.exprad4)),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8)-2.5*log10(b.devrad8_BT),a.m_tot-2.5*log10(b.exprad4)-2.5*log10(b.exprad4_BT)),-999) as m_bulge , 
 , a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8)-2.5*log10(1.0-b.devrad8_BT),a.m_tot-2.5*log10(b.exprad4)-2.5*log10(1.0-b.exprad4_BT)),-999) as m_disk , a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM r_band_devexp as a, modelcolor_r_devexp as b , CAST as c where a.galcount = c.galcount and  a.galcount=b.galcount;






DROP VIEW IF EXISTS g_model_ser;
CREATE VIEW g_model_ser AS SELECT a.galcount,  IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8),a.m_tot-2.5*log10(b.exprad4)),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
a.m_bulge , a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
a.m_disk , a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM g_band_ser as a, modelcolor_g_ser as b , CAST as c where a.galcount = c.galcount and  a.galcount=b.galcount;

DROP VIEW IF EXISTS g_model_serexp;
CREATE VIEW g_model_serexp AS SELECT a.galcount,  IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8),a.m_tot-2.5*log10(b.exprad4)),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8)-2.5*log10(b.devrad8_BT),a.m_tot-2.5*log10(b.exprad4)-2.5*log10(b.exprad4_BT)),-999) as m_bulge , 
 a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8)-2.5*log10(1.0-b.devrad8_BT),a.m_tot-2.5*log10(b.exprad4)-2.5*log10(1.0-b.exprad4_BT)),-999) as m_disk , a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM g_band_serexp as a, modelcolor_g_serexp as b , CAST as c where a.galcount = c.galcount and  a.galcount=b.galcount;

DROP VIEW IF EXISTS g_model_dev;
CREATE VIEW g_model_dev AS SELECT a.galcount,  IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8),a.m_tot-2.5*log10(b.exprad4)),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
a.m_bulge , a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
a.m_disk , a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM g_band_dev as a, modelcolor_g_dev as b, CAST as c where a.galcount = c.galcount and a.galcount=b.galcount;

DROP VIEW IF EXISTS g_model_devexp;
CREATE VIEW g_model_devexp AS SELECT a.galcount,  IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8),a.m_tot-2.5*log10(b.exprad4)),-999) as m_tot, a.BT,  
a.Hrad_corr , a.ba_tot_corr ,
a.xctr_bulge , a.xctr_bulge_err ,  
a.yctr_bulge , a.yctr_bulge_err ,  
IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8)-2.5*log10(b.devrad8_BT),a.m_tot-2.5*log10(b.exprad4)-2.5*log10(b.exprad4_BT)),-999) as m_bulge , 
 a.m_bulge_err ,
a.r_bulge , a.r_bulge_err ,
a.n_bulge , a.n_bulge_err ,
a.ba_bulge , a.ba_bulge_err ,
a.pa_bulge , a.pa_bulge_err ,
a.xctr_disk , a.xctr_disk_err ,  
a.yctr_disk , a.yctr_disk_err ,  
IFNULL(IF(abs(c.modelmag_r-c.devmag_r)<=abs(c.modelmag_r-c.expmag_r), a.m_tot-2.5*log10(b.devrad8)-2.5*log10(1.0-b.devrad8_BT),a.m_tot-2.5*log10(b.exprad4)-2.5*log10(1.0-b.exprad4_BT)),-999) as m_disk , a.m_disk_err ,
a.r_disk , a.r_disk_err ,
a.ba_disk , a.ba_disk_err ,
a.pa_disk , a.pa_disk_err ,
a.chi2nu , a.Goodness ,
a.Galsky , a.Galsky_err , 
a.fit , a.FitFlag,
a.flag, a.Manual_flag,
a.FinalFlag, a.Comments
FROM g_band_devexp as a, modelcolor_g_devexp as b , CAST as c where a.galcount = c.galcount and  a.galcount=b.galcount;


update modelcolor_g_devexp as a, g_band_devexp as b set a.devrad8_BT = b.BT where a.devrad8>0.99 and a.galcount=b.galcount;
update modelcolor_g_devexp as a, g_band_devexp as b set a.exprad4_BT = b.BT where a.exprad4>0.99 and a.galcount=b.galcount;
update modelcolor_g_serexp as a, g_band_serexp as b set a.devrad8_BT = b.BT where a.devrad8>0.99 and a.galcount=b.galcount;
update modelcolor_g_serexp as a, g_band_serexp as b set a.exprad4_BT = b.BT where a.exprad4>0.99 and a.galcount=b.galcount;

update modelcolor_r_devexp as a, r_band_devexp as b set a.devrad8_BT = b.BT where a.devrad8>0.99 and a.galcount=b.galcount;
update modelcolor_r_devexp as a, r_band_devexp as b set a.exprad4_BT = b.BT where a.exprad4>0.99 and a.galcount=b.galcount;
update modelcolor_r_serexp as a, r_band_serexp as b set a.devrad8_BT = b.BT where a.devrad8>0.99 and a.galcount=b.galcount;
update modelcolor_r_serexp as a, r_band_serexp as b set a.exprad4_BT = b.BT where a.exprad4>0.99 and a.galcount=b.galcount;

update modelcolor_i_devexp as a, i_band_devexp as b set a.devrad8_BT = b.BT where a.devrad8>0.99 and a.galcount=b.galcount;
update modelcolor_i_devexp as a, i_band_devexp as b set a.exprad4_BT = b.BT where a.exprad4>0.99 and a.galcount=b.galcount;
update modelcolor_i_serexp as a, i_band_serexp as b set a.devrad8_BT = b.BT where a.devrad8>0.99 and a.galcount=b.galcount;
update modelcolor_i_serexp as a, i_band_serexp as b set a.exprad4_BT = b.BT where a.exprad4>0.99 and a.galcount=b.galcount;
