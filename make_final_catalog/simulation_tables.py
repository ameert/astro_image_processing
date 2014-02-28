#these commands are to be executed in the simulation database in order to 
#produce a data structure that is parallel to the true data structure such 
#that we can operate on these tables in the same way as the real data

# i.e. these commands create CAST, DERT, and M2010 tables for the simulated galaxies with galcount now referring to the simulation count

# the true galcount that maps back to the original data is shown in the 
# new "true_galcount" column


create table CAST like catalog.CAST;
alter table CAST change column galcount true_galcount int;
alter table CAST drop primary key;
alter table CAST drop key objid;
alter table CAST drop key specobjid;
alter table CAST drop key plate;
alter table CAST add column galcount int primary key first;
insert into CAST select a.simcount, b.*  from sim_input as a, catalog.CAST as b where a.galcount = b.galcount;

create table DERT like catalog.DERT;
alter table DERT change column galcount true_galcount int;
alter table DERT drop primary key;
alter table DERT add column galcount int primary key first;
insert into DERT select a.simcount, b.*  from sim_input as a, catalog.DERT as b where a.galcount = b.galcount;

create table M2010 like catalog.M2010;
alter table M2010 change column galcount true_galcount int;
alter table M2010 drop primary key;
alter table M2010 add column galcount int primary key first;
insert into M2010 select a.simcount, b.*  from sim_input as a, catalog.M2010 as b where a.galcount = b.galcount;
