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
DROP VIEW IF EXISTS r_sdss_model;
CREATE VIEW r_sdss_model AS SELECT galcount, ModelMag_r as m_tot, 1.0 as BT,  
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

DROP VIEW IF EXISTS g_sdss_model;
CREATE VIEW g_sdss_model AS SELECT galcount, ModelMag_g as m_tot, 1.0 as BT,  
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

DROP VIEW IF EXISTS i_sdss_model;
CREATE VIEW i_sdss_model AS SELECT galcount, ModelMag_i as m_tot, 1.0 as BT,  
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


-- best fits 
DROP VIEW IF EXISTS r_band_best;
CREATE VIEW r_band_best AS (SELECT a.* from r_band_ser as a, svm_probs as d where a.galcount = d.galcount and d.p_ser <= 0.5) UNION (SELECT a.* from r_band_serexp as a, svm_probs as d where a.galcount = d.galcount and d.p_ser > 0.5);

DROP VIEW IF EXISTS g_band_best;
CREATE VIEW g_band_best AS (SELECT a.* from g_band_ser as a, svm_probs as d where a.galcount = d.galcount and d.p_ser <= 0.5) UNION (SELECT a.* from g_band_serexp as a, svm_probs as d where a.galcount = d.galcount and d.p_ser > 0.5);

DROP VIEW IF EXISTS i_band_best;
CREATE VIEW i_band_best AS (SELECT a.* from i_band_ser as a, svm_probs as d where a.galcount = d.galcount and d.p_ser <= 0.5) UNION (SELECT a.* from i_band_serexp as a, svm_probs as d where a.galcount = d.galcount and d.p_ser > 0.5);

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
CREATE VIEW r_cmodel_serexp AS SELECT galcount, -2.5*log10(pow(10,-0.4*(devmag_r-0.0637))*fracdev_r + (1.0-fracdev_r)*pow(10,-0.4*(expmag_r-0.0103))) as m_tot, fracdev_r as BT,  
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
