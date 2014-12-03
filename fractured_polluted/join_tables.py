rename table i_band_fit to i_predeep_fit;
rename table i_band_dev to i_predeep_dev;
rename table i_band_ser to i_predeep_ser;
rename table i_band_devexp to i_predeep_devexp;
rename table i_band_serexp to i_predeep_serexp;

create table i_band_fit like i_predeep_fit;
create table i_band_dev like i_predeep_dev;
create table i_band_ser like i_predeep_ser;
create table i_band_devexp like i_predeep_devexp;
create table i_band_serexp like i_predeep_serexp;


select a.galcount from i_deep_badfits as a, i_band_badfits as b, i_deep_fits as x where x.galcount = a.galcount and a.galcount=b.galcount and a.is_polluted =0 and b.is_polluted = 1 and a.is_fractured=0  and b.is_fractured=0;

select a.galcount from i_deep_badfits as a, i_band_badfits as b where a.galcount=b.galcount and b.is_polluted =1 and b.is_fractured = 0 and (a.is_polluted = 1 or a.is_fractured=1);

select a.galcount from i_deep_badfits as a, i_band_badfits as b where a.galcount=b.galcount and b.is_polluted =0 and b.is_fractured = 1;


insert into i_band_fit select x.* from i_band_badfits as b, i_deep_fit as x where x.galcount = b.galcount and  b.is_polluted_deep =0 and b.is_polluted = 1 and b.is_fractured_deep=0  and b.is_fractured=0;

insert into i_band_dev select x.* from i_band_badfits as b, i_deep_dev as x where x.galcount = b.galcount and b.is_polluted_deep =0 and b.is_polluted = 1 and b.is_fractured_deep=0  and b.is_fractured=0;

insert into i_band_ser select x.* from i_band_badfits as b, i_deep_ser as x where x.galcount = b.galcount and b.is_polluted_deep =0 and b.is_polluted = 1 and b.is_fractured_deep=0  and b.is_fractured=0;

insert into i_band_devexp select x.* from i_band_badfits as b, i_deep_devexp as x where x.galcount = b.galcount and b.is_polluted_deep =0 and b.is_polluted = 1 and b.is_fractured_deep=0  and b.is_fractured=0;

insert into i_band_serexp select x.* from i_band_badfits as b, i_deep_serexp as x where x.galcount = b.galcount and b.is_polluted_deep =0 and b.is_polluted = 1 and b.is_fractured_deep=0  and b.is_fractured=0;


insert ignore into i_band_fit select * from i_predeep_fit;
insert ignore into i_band_ser select * from i_predeep_ser;
insert ignore into i_band_dev select * from i_predeep_dev;
insert ignore into i_band_devexp select * from i_predeep_devexp;
insert ignore into i_band_serexp select * from i_predeep_serexp;

delete from i_predeep_fit where galcount not in (select b.galcount from i_band_badfits as b, i_deep_fit as x where x.galcount = b.galcount and b.is_polluted_deep =0 and b.is_polluted = 1 and b.is_fractured_deep=0  and b.is_fractured=0);

delete from i_predeep_ser where galcount not in (select b.galcount from i_band_badfits as b, i_deep_ser as x where x.galcount = b.galcount and b.is_polluted_deep =0 and b.is_polluted = 1 and b.is_fractured_deep=0  and b.is_fractured=0);

delete from i_predeep_dev where galcount not in (select b.galcount from i_band_badfits as b, i_deep_dev as x where x.galcount = b.galcount and b.is_polluted_deep =0 and b.is_polluted = 1 and b.is_fractured_deep=0  and b.is_fractured=0);

delete from i_predeep_devexp where galcount not in (select b.galcount from i_band_badfits as b, i_deep_devexp as x where x.galcount = b.galcount and b.is_polluted_deep =0 and b.is_polluted = 1 and b.is_fractured_deep=0  and b.is_fractured=0);

delete from i_predeep_serexp where galcount not in (select b.galcount from i_band_badfits as b, i_deep_serexp as x where x.galcount = b.galcount and b.is_polluted_deep =0 and b.is_polluted = 1 and b.is_fractured_deep=0  and b.is_fractured=0);

