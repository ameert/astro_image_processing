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

update CAST as a, catalog.CAST as c set a.gain_r = c.gain_r, a.gain_g = c.gain_g, a.gain_i = c.gain_i where a.true_galcount = c.galcount;
update CAST as a, CAST as c set a.gain_r = c.gain_r, a.gain_g = c.gain_g, a.gain_i = c.gain_i  where a.galcount >61 and a.cluster_num=c.cluster_num;

update CAST as a, catalog.CAST as c set a.run = c.run, a.rerun = c.rerun, 
a.camcol = c.camcol,a.field = c.field where a.true_galcount = c.galcount;
update CAST as a, CAST as c set a.run = c.run, a.rerun = c.rerun, 
a.camcol = c.camcol,a.field = c.field  where a.galcount >61 and a.cluster_num=c.cluster_num;

update CAST as a, z_sims_g as b set a.aa_g = -1.0*b.zeropoint where a.galcount = b.simcount;
update CAST as a, z_sims_g as b set a.z = b.z where a.galcount = b.simcount;
update CAST as a, z_sims_r as b set a.aa_r = -1.0*b.zeropoint where a.galcount = b.simcount;

update DERT as a,  z_sims_r as b set a.kcorr_r = b.kcorr where a.galcount = b.simcount;
update DERT as a, z_sims_g as b set a.kcorr_g = b.kcorr where a.galcount = b.simcount;
update DERT as a,  z_sims_g as b set a.dismod = b.dismod where a.galcount = b.simcount;
update DERT as a, z_sims_g as b set a.kpc_per_arcsec = b.kpc_per_arcsec where a.galcount = b.simcount;

update CAST as a, CAST as c set a.run = c.run, a.rerun = c.rerun, 
a.camcol = c.camcol,a.field = c.field  where a.galcount >61 and a.cluster_num=c.cluster_num;
