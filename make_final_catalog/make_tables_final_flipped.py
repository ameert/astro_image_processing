DROP TABLE IF EXISTS final_cat.g_band_ser;
create table final_cat.g_band_ser like catalog.g_band_ser;
insert into final_cat.g_band_ser select * from catalog.g_band_ser;
alter table final_cat.g_band_ser add column n_disk_err float default -999 after r_bulge; 
alter table final_cat.g_band_ser add column n_disk float default -999 after r_bulge; 

DROP TABLE IF EXISTS final_cat.g_band_dev;
create table final_cat.g_band_dev like catalog.g_band_dev;
insert into final_cat.g_band_dev select * from catalog.g_band_dev;
alter table final_cat.g_band_dev add column n_disk_err float default -999 after r_bulge; 
alter table final_cat.g_band_dev add column n_disk float default -999 after r_bulge; 

DROP TABLE IF EXISTS final_cat.g_band_serexp;
create table final_cat.g_band_serexp like catalog.g_band_serexp;
insert into final_cat.g_band_serexp select * from catalog.g_band_serexp;
alter table final_cat.g_band_serexp add column n_disk_err float default -999 after r_bulge; 
alter table final_cat.g_band_serexp add column n_disk float default -999 after r_bulge; 
update final_cat.g_band_serexp set n_disk = 1.0, r_disk = 1.678*r_disk, 
r_disk_err = 1.678*r_disk_err where m_disk between 1 and 35;

update final_cat.g_band_serexp as a, catalog.Flags_catalog as b set 
a.BT = 1.0-a.BT, 
a.xctr_bulge =a.xctr_disk, a.xctr_bulge_err =a.xctr_disk_err,
a.yctr_bulge =a.yctr_disk, a.yctr_bulge_err =a.yctr_disk_err,
a.m_bulge = a.m_disk, a.m_bulge_err = a.m_disk_err, 
a.r_bulge = a.r_disk, a.r_bulge_err = a.r_disk_err, 
a.n_bulge = a.n_disk, a.n_bulge_err = a.n_disk_err, 
a.ba_bulge = a.ba_disk, a.ba_bulge_err = a.ba_disk_err, 
a.pa_bulge = a.pa_disk, a.pa_bulge_err = a.pa_disk_err, 
a.xctr_disk =a.xctr_bulge, a.xctr_disk_err =a.xctr_bulge_err,
a.yctr_disk =a.yctr_bulge, a.yctr_disk_err =a.yctr_bulge_err,
a.m_disk = a.m_bulge, a.m_disk_err = a.m_bulge_err, 
a.r_disk = a.r_bulge, a.r_disk_err = a.r_bulge_err, 
a.n_disk = a.n_bulge, a.n_disk_err = a.n_bulge_err, 
a.ba_disk = a.ba_bulge, a.ba_disk_err = a.ba_bulge_err, 
a.pa_disk = a.pa_bulge, a.pa_disk_err = a.pa_bulge_err
where
a.galcount=b.galcount and b.ftype = 'u' and b.band='g'
and b.model='serexp' and  (b.flag&pow(2,6)>0 or b.flag&pow(2,7) or 
b.flag&pow(2,13) ); 


DROP TABLE IF EXISTS final_cat.g_band_devexp;
create table final_cat.g_band_devexp like catalog.g_band_devexp;
insert into final_cat.g_band_devexp select * from catalog.g_band_devexp;
alter table final_cat.g_band_devexp add column n_disk_err float default -999 after r_bulge; 
alter table final_cat.g_band_devexp add column n_disk float default -999 after r_bulge; 
update final_cat.g_band_devexp set n_disk = 1.0, r_disk = 1.678*r_disk, 
r_disk_err = 1.678*r_disk_err where m_disk between 1 and 35;

update final_cat.g_band_devexp as a, catalog.Flags_catalog as b set 
a.BT = 1.0-a.BT, 
a.xctr_bulge =a.xctr_disk, a.xctr_bulge_err =a.xctr_disk_err,
a.yctr_bulge =a.yctr_disk, a.yctr_bulge_err =a.yctr_disk_err,
a.m_bulge = a.m_disk, a.m_bulge_err = a.m_disk_err, 
a.r_bulge = a.r_disk, a.r_bulge_err = a.r_disk_err, 
a.n_bulge = a.n_disk, a.n_bulge_err = a.n_disk_err, 
a.ba_bulge = a.ba_disk, a.ba_bulge_err = a.ba_disk_err, 
a.pa_bulge = a.pa_disk, a.pa_bulge_err = a.pa_disk_err, 
a.xctr_disk =a.xctr_bulge, a.xctr_disk_err =a.xctr_bulge_err,
a.yctr_disk =a.yctr_bulge, a.yctr_disk_err =a.yctr_bulge_err,
a.m_disk = a.m_bulge, a.m_disk_err = a.m_bulge_err, 
a.r_disk = a.r_bulge, a.r_disk_err = a.r_bulge_err, 
a.n_disk = a.n_bulge, a.n_disk_err = a.n_bulge_err, 
a.ba_disk = a.ba_bulge, a.ba_disk_err = a.ba_bulge_err, 
a.pa_disk = a.pa_bulge, a.pa_disk_err = a.pa_bulge_err
where
a.galcount=b.galcount and b.ftype = 'u' and b.band='g'
and b.model='devexp' and  (b.flag&pow(2,6)>0 or b.flag&pow(2,7) or 
b.flag&pow(2,13) ); 

DROP TABLE IF EXISTS final_cat.r_band_ser;
create table final_cat.r_band_ser like catalog.r_band_ser;
insert into final_cat.r_band_ser select * from catalog.r_band_ser;
alter table final_cat.r_band_ser add column n_disk_err float default -999 after r_bulge; 
alter table final_cat.r_band_ser add column n_disk float default -999 after r_bulge; 

DROP TABLE IF EXISTS final_cat.r_band_dev;
create table final_cat.r_band_dev like catalog.r_band_dev;
insert into final_cat.r_band_dev select * from catalog.r_band_dev;
alter table final_cat.r_band_dev add column n_disk_err float default -999 after r_bulge; 
alter table final_cat.r_band_dev add column n_disk float default -999 after r_bulge; 

DROP TABLE IF EXISTS final_cat.r_band_serexp;
create table final_cat.r_band_serexp like catalog.r_band_serexp;
insert into final_cat.r_band_serexp select * from catalog.r_band_serexp;
alter table final_cat.r_band_serexp add column n_disk_err float default -999 after r_bulge; 
alter table final_cat.r_band_serexp add column n_disk float default -999 after r_bulge; 
update final_cat.r_band_serexp set n_disk = 1.0, r_disk = 1.678*r_disk, 
r_disk_err = 1.678*r_disk_err where m_disk between 1 and 35;

update final_cat.r_band_serexp as a, catalog.Flags_catalog as b set 
a.BT = 1.0-a.BT, 
a.xctr_bulge =a.xctr_disk, a.xctr_bulge_err =a.xctr_disk_err,
a.yctr_bulge =a.yctr_disk, a.yctr_bulge_err =a.yctr_disk_err,
a.m_bulge = a.m_disk, a.m_bulge_err = a.m_disk_err, 
a.r_bulge = a.r_disk, a.r_bulge_err = a.r_disk_err, 
a.n_bulge = a.n_disk, a.n_bulge_err = a.n_disk_err, 
a.ba_bulge = a.ba_disk, a.ba_bulge_err = a.ba_disk_err, 
a.pa_bulge = a.pa_disk, a.pa_bulge_err = a.pa_disk_err, 
a.xctr_disk =a.xctr_bulge, a.xctr_disk_err =a.xctr_bulge_err,
a.yctr_disk =a.yctr_bulge, a.yctr_disk_err =a.yctr_bulge_err,
a.m_disk = a.m_bulge, a.m_disk_err = a.m_bulge_err, 
a.r_disk = a.r_bulge, a.r_disk_err = a.r_bulge_err, 
a.n_disk = a.n_bulge, a.n_disk_err = a.n_bulge_err, 
a.ba_disk = a.ba_bulge, a.ba_disk_err = a.ba_bulge_err, 
a.pa_disk = a.pa_bulge, a.pa_disk_err = a.pa_bulge_err
where
a.galcount=b.galcount and b.ftype = 'u' and b.band='r'
and b.model='serexp' and  (b.flag&pow(2,6)>0 or b.flag&pow(2,7) or 
b.flag&pow(2,13) ); 


DROP TABLE IF EXISTS final_cat.r_band_devexp;
create table final_cat.r_band_devexp like catalog.r_band_devexp;
insert into final_cat.r_band_devexp select * from catalog.r_band_devexp;
alter table final_cat.r_band_devexp add column n_disk_err float default -999 after r_bulge; 
alter table final_cat.r_band_devexp add column n_disk float default -999 after r_bulge; 
update final_cat.r_band_devexp set n_disk = 1.0, r_disk = 1.678*r_disk, 
r_disk_err = 1.678*r_disk_err where m_disk between 1 and 35;

update final_cat.r_band_devexp as a, catalog.Flags_catalog as b set 
a.BT = 1.0-a.BT, 
a.xctr_bulge =a.xctr_disk, a.xctr_bulge_err =a.xctr_disk_err,
a.yctr_bulge =a.yctr_disk, a.yctr_bulge_err =a.yctr_disk_err,
a.m_bulge = a.m_disk, a.m_bulge_err = a.m_disk_err, 
a.r_bulge = a.r_disk, a.r_bulge_err = a.r_disk_err, 
a.n_bulge = a.n_disk, a.n_bulge_err = a.n_disk_err, 
a.ba_bulge = a.ba_disk, a.ba_bulge_err = a.ba_disk_err, 
a.pa_bulge = a.pa_disk, a.pa_bulge_err = a.pa_disk_err, 
a.xctr_disk =a.xctr_bulge, a.xctr_disk_err =a.xctr_bulge_err,
a.yctr_disk =a.yctr_bulge, a.yctr_disk_err =a.yctr_bulge_err,
a.m_disk = a.m_bulge, a.m_disk_err = a.m_bulge_err, 
a.r_disk = a.r_bulge, a.r_disk_err = a.r_bulge_err, 
a.n_disk = a.n_bulge, a.n_disk_err = a.n_bulge_err, 
a.ba_disk = a.ba_bulge, a.ba_disk_err = a.ba_bulge_err, 
a.pa_disk = a.pa_bulge, a.pa_disk_err = a.pa_bulge_err
where
a.galcount=b.galcount and b.ftype = 'u' and b.band='r'
and b.model='devexp' and  (b.flag&pow(2,6)>0 or b.flag&pow(2,7) or 
b.flag&pow(2,13) ); 

DROP TABLE IF EXISTS final_cat.i_band_ser;
create table final_cat.i_band_ser like catalog.i_band_ser;
insert into final_cat.i_band_ser select * from catalog.i_band_ser;
alter table final_cat.i_band_ser add column n_disk_err float default -999 after r_bulge; 
alter table final_cat.i_band_ser add column n_disk float default -999 after r_bulge; 

DROP TABLE IF EXISTS final_cat.i_band_dev;
create table final_cat.i_band_dev like catalog.i_band_dev;
insert into final_cat.i_band_dev select * from catalog.i_band_dev;
alter table final_cat.i_band_dev add column n_disk_err float default -999 after r_bulge; 
alter table final_cat.i_band_dev add column n_disk float default -999 after r_bulge; 

DROP TABLE IF EXISTS final_cat.i_band_serexp;
create table final_cat.i_band_serexp like catalog.i_band_serexp;
insert into final_cat.i_band_serexp select * from catalog.i_band_serexp;
alter table final_cat.i_band_serexp add column n_disk_err float default -999 after r_bulge; 
alter table final_cat.i_band_serexp add column n_disk float default -999 after r_bulge; 
update final_cat.i_band_serexp set n_disk = 1.0, r_disk = 1.678*r_disk, 
r_disk_err = 1.678*r_disk_err where m_disk between 1 and 35;

update final_cat.i_band_serexp as a, catalog.Flags_catalog as b set 
a.BT = 1.0-a.BT, 
a.xctr_bulge =a.xctr_disk, a.xctr_bulge_err =a.xctr_disk_err,
a.yctr_bulge =a.yctr_disk, a.yctr_bulge_err =a.yctr_disk_err,
a.m_bulge = a.m_disk, a.m_bulge_err = a.m_disk_err, 
a.r_bulge = a.r_disk, a.r_bulge_err = a.r_disk_err, 
a.n_bulge = a.n_disk, a.n_bulge_err = a.n_disk_err, 
a.ba_bulge = a.ba_disk, a.ba_bulge_err = a.ba_disk_err, 
a.pa_bulge = a.pa_disk, a.pa_bulge_err = a.pa_disk_err, 
a.xctr_disk =a.xctr_bulge, a.xctr_disk_err =a.xctr_bulge_err,
a.yctr_disk =a.yctr_bulge, a.yctr_disk_err =a.yctr_bulge_err,
a.m_disk = a.m_bulge, a.m_disk_err = a.m_bulge_err, 
a.r_disk = a.r_bulge, a.r_disk_err = a.r_bulge_err, 
a.n_disk = a.n_bulge, a.n_disk_err = a.n_bulge_err, 
a.ba_disk = a.ba_bulge, a.ba_disk_err = a.ba_bulge_err, 
a.pa_disk = a.pa_bulge, a.pa_disk_err = a.pa_bulge_err
where
a.galcount=b.galcount and b.ftype = 'u' and b.band='i'
and b.model='serexp' and  (b.flag&pow(2,6)>0 or b.flag&pow(2,7) or 
b.flag&pow(2,13) ); 


DROP TABLE IF EXISTS final_cat.i_band_devexp;
create table final_cat.i_band_devexp like catalog.i_band_devexp;
insert into final_cat.i_band_devexp select * from catalog.i_band_devexp;
alter table final_cat.i_band_devexp add column n_disk_err float default -999 after r_bulge; 
alter table final_cat.i_band_devexp add column n_disk float default -999 after r_bulge; 
update final_cat.i_band_devexp set n_disk = 1.0, r_disk = 1.678*r_disk, 
r_disk_err = 1.678*r_disk_err where m_disk between 1 and 35;

update final_cat.i_band_devexp as a, catalog.Flags_catalog as b set 
a.BT = 1.0-a.BT, 
a.xctr_bulge =a.xctr_disk, a.xctr_bulge_err =a.xctr_disk_err,
a.yctr_bulge =a.yctr_disk, a.yctr_bulge_err =a.yctr_disk_err,
a.m_bulge = a.m_disk, a.m_bulge_err = a.m_disk_err, 
a.r_bulge = a.r_disk, a.r_bulge_err = a.r_disk_err, 
a.n_bulge = a.n_disk, a.n_bulge_err = a.n_disk_err, 
a.ba_bulge = a.ba_disk, a.ba_bulge_err = a.ba_disk_err, 
a.pa_bulge = a.pa_disk, a.pa_bulge_err = a.pa_disk_err, 
a.xctr_disk =a.xctr_bulge, a.xctr_disk_err =a.xctr_bulge_err,
a.yctr_disk =a.yctr_bulge, a.yctr_disk_err =a.yctr_bulge_err,
a.m_disk = a.m_bulge, a.m_disk_err = a.m_bulge_err, 
a.r_disk = a.r_bulge, a.r_disk_err = a.r_bulge_err, 
a.n_disk = a.n_bulge, a.n_disk_err = a.n_bulge_err, 
a.ba_disk = a.ba_bulge, a.ba_disk_err = a.ba_bulge_err, 
a.pa_disk = a.pa_bulge, a.pa_disk_err = a.pa_bulge_err
where
a.galcount=b.galcount and b.ftype = 'u' and b.band='i'
and b.model='devexp' and  (b.flag&pow(2,6)>0 or b.flag&pow(2,7) or 
b.flag&pow(2,13) ); 
