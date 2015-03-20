#truncate r_simard_best;
#insert into r_simard_best select a.* from r_simard_ser as a, r_simard_fit as b where a.galcount = b.galcount and b.Prob_pS>=0.32;

#insert into r_simard_best select a.* from r_simard_devexp as a, r_simard_fit as b where a.galcount = b.galcount and b.Prob_pS<0.32 and  b.Prob_n4>=0.32;

#insert into r_simard_best select a.* from r_simard_serexp as a, r_simard_fit as b where a.galcount = b.galcount and b.Prob_pS<0.32 and  b.Prob_n4<0.32;


#truncate r_mendel_best;
#insert into r_mendel_best select a.* from r_simard_ser as a, r_simard_fit as b where a.galcount = b.galcount and (b.ProfType=1 or b.ProfType=2);

#insert into r_mendel_best select a.* from r_simard_devexp as a, r_simard_fit as b where a.galcount = b.galcount and b.ProfType=3;


insert ignore into catalog.Flags_catalog (galcount,ftype, band, model) select galcount, 'u', 'g', 'best' from catalog.CAST; 
insert ignore into catalog.Flags_catalog (galcount,ftype, band, model) select galcount, 'r', 'g', 'best' from catalog.CAST; 

drop table IF EXISTS g_band_best;
create table g_band_best like g_band_serexp;
insert into g_band_best select a.* from g_band_serexp as a, catalog.Flags_catalog as b where a.galcount = b.galcount and b.model='serexp' and b.band='g' and b.ftype='u' and (b.flag&pow(2,10)>0 or b.flag&pow(2,14)>0 or b.flag&pow(2,20)>0);

update catalog.Flags_catalog as c, catalog.Flags_catalog as b set c.flag = b.flag  where c.galcount = b.galcount and b.model='serexp' and b.band='g' and b.ftype='u' and (b.flag&pow(2,10)>0 or b.flag&pow(2,14)>0  or b.flag&pow(2,20)>0) and c.model='best' and c.band='g' and c.ftype='u';

update catalog.Flags_catalog as c, catalog.Flags_catalog as b, catalog.Flags_catalog as a  set c.flag = a.flag  where c.galcount = b.galcount and b.model='serexp' and b.band='g' and b.ftype='u' and (b.flag&pow(2,10)>0 or b.flag&pow(2,14)>0 or b.flag&pow(2,20)>0) and  c.model='best' and c.band='g' and c.ftype='r' and  a.galcount = c.galcount and a.model='serexp' and a.band='g' and a.ftype='r';
 
insert into g_band_best select a.* from g_band_ser as a, catalog.Flags_catalog as b, catalog.Flags_catalog as c where a.galcount = b.galcount and b.model='serexp' and b.band='g' and b.ftype='u' and (b.flag&pow(2,10)=0 and b.flag&pow(2,14)=0 and b.flag&pow(2,20)=0) and (b.flag&pow(2,1)>0 or b.flag&pow(2,4)>0) and a.galcount = c.galcount and c.model='ser' and c.band='g' and c.ftype='u';

update catalog.Flags_catalog as c, catalog.Flags_catalog as b, catalog.Flags_catalog as a  set c.flag = a.flag  where c.galcount = b.galcount and b.model='serexp' and b.band='g' and b.ftype='u' and (b.flag&pow(2,10)=0 and b.flag&pow(2,14)=0 and b.flag&pow(2,20)=0)  and (b.flag&pow(2,1)>0 or b.flag&pow(2,4)>0) and c.model='best' and c.band='g' and c.ftype='u' and  a.galcount = c.galcount and a.model='ser' and a.band='g' and a.ftype='u';

update catalog.Flags_catalog as c, catalog.Flags_catalog as b, catalog.Flags_catalog as a  set c.flag = a.flag  where c.galcount = b.galcount and b.model='serexp' and b.band='g' and b.ftype='u' and (b.flag&pow(2,10)=0 and b.flag&pow(2,14)=0 and b.flag&pow(2,20)=0)  and (b.flag&pow(2,1)>0 or b.flag&pow(2,4)>0) and  c.model='best' and c.band='g' and c.ftype='r' and  a.galcount = c.galcount and a.model='ser' and a.band='g' and a.ftype='r';

insert ignore into catalog.Flags_catalog (galcount,ftype, band, model) select galcount, 'u', 'r', 'best' from catalog.CAST; 
insert ignore into catalog.Flags_catalog (galcount,ftype, band, model) select galcount, 'r', 'r', 'best' from catalog.CAST; 

drop table  IF EXISTS r_band_best;
create table r_band_best like r_band_serexp;
insert into r_band_best select a.* from r_band_serexp as a, catalog.Flags_catalog as b where a.galcount = b.galcount and b.model='serexp' and b.band='r' and b.ftype='u' and (b.flag&pow(2,10)>0 or b.flag&pow(2,14)>0 or b.flag&pow(2,20)>0);

update catalog.Flags_catalog as c, catalog.Flags_catalog as b set c.flag = b.flag  where c.galcount = b.galcount and b.model='serexp' and b.band='r' and b.ftype='u' and (b.flag&pow(2,10)>0 or b.flag&pow(2,14)>0  or b.flag&pow(2,20)>0) and c.model='best' and c.band='r' and c.ftype='u';

update catalog.Flags_catalog as c, catalog.Flags_catalog as b, catalog.Flags_catalog as a  set c.flag = a.flag  where c.galcount = b.galcount and b.model='serexp' and b.band='r' and b.ftype='u' and (b.flag&pow(2,10)>0 or b.flag&pow(2,14)>0 or b.flag&pow(2,20)>0) and  c.model='best' and c.band='r' and c.ftype='r' and  a.galcount = c.galcount and a.model='serexp' and a.band='r' and a.ftype='r';
 
insert into r_band_best select a.* from r_band_ser as a, catalog.Flags_catalog as b, catalog.Flags_catalog as c where a.galcount = b.galcount and b.model='serexp' and b.band='r' and b.ftype='u' and (b.flag&pow(2,10)=0 and b.flag&pow(2,14)=0 and b.flag&pow(2,20)=0) and (b.flag&pow(2,1)>0 or b.flag&pow(2,4)>0) and a.galcount = c.galcount and c.model='ser' and c.band='r' and c.ftype='u';

update catalog.Flags_catalog as c, catalog.Flags_catalog as b, catalog.Flags_catalog as a  set c.flag = a.flag  where c.galcount = b.galcount and b.model='serexp' and b.band='r' and b.ftype='u' and (b.flag&pow(2,10)=0 and b.flag&pow(2,14)=0 and b.flag&pow(2,20)=0)  and (b.flag&pow(2,1)>0 or b.flag&pow(2,4)>0) and c.model='best' and c.band='r' and c.ftype='u' and  a.galcount = c.galcount and a.model='ser' and a.band='r' and a.ftype='u';

update catalog.Flags_catalog as c, catalog.Flags_catalog as b, catalog.Flags_catalog as a  set c.flag = a.flag  where c.galcount = b.galcount and b.model='serexp' and b.band='r' and b.ftype='u' and (b.flag&pow(2,10)=0 and b.flag&pow(2,14)=0 and b.flag&pow(2,20)=0)  and (b.flag&pow(2,1)>0 or b.flag&pow(2,4)>0) and  c.model='best' and c.band='r' and c.ftype='r' and  a.galcount = c.galcount and a.model='ser' and a.band='r' and a.ftype='r';

insert ignore into catalog.Flags_catalog (galcount,ftype, band, model) select galcount, 'u', 'i', 'best' from catalog.CAST; 
insert ignore into catalog.Flags_catalog (galcount,ftype, band, model) select galcount, 'r', 'i', 'best' from catalog.CAST; 

drop table  IF EXISTS i_band_best;
create table i_band_best like i_band_serexp;
insert into i_band_best select a.* from i_band_serexp as a, catalog.Flags_catalog as b where a.galcount = b.galcount and b.model='serexp' and b.band='i' and b.ftype='u' and (b.flag&pow(2,10)>0 or b.flag&pow(2,14)>0 or b.flag&pow(2,20)>0);

update catalog.Flags_catalog as c, catalog.Flags_catalog as b set c.flag = b.flag  where c.galcount = b.galcount and b.model='serexp' and b.band='i' and b.ftype='u' and (b.flag&pow(2,10)>0 or b.flag&pow(2,14)>0  or b.flag&pow(2,20)>0) and c.model='best' and c.band='i' and c.ftype='u';

update catalog.Flags_catalog as c, catalog.Flags_catalog as b, catalog.Flags_catalog as a  set c.flag = a.flag  where c.galcount = b.galcount and b.model='serexp' and b.band='i' and b.ftype='u' and (b.flag&pow(2,10)>0 or b.flag&pow(2,14)>0 or b.flag&pow(2,20)>0) and  c.model='best' and c.band='i' and c.ftype='r' and  a.galcount = c.galcount and a.model='serexp' and a.band='i' and a.ftype='r';
 
insert into i_band_best select a.* from i_band_ser as a, catalog.Flags_catalog as b, catalog.Flags_catalog as c where a.galcount = b.galcount and b.model='serexp' and b.band='i' and b.ftype='u' and (b.flag&pow(2,10)=0 and b.flag&pow(2,14)=0 and b.flag&pow(2,20)=0) and (b.flag&pow(2,1)>0 or b.flag&pow(2,4)>0) and a.galcount = c.galcount and c.model='ser' and c.band='i' and c.ftype='u';

update catalog.Flags_catalog as c, catalog.Flags_catalog as b, catalog.Flags_catalog as a  set c.flag = a.flag  where c.galcount = b.galcount and b.model='serexp' and b.band='i' and b.ftype='u' and (b.flag&pow(2,10)=0 and b.flag&pow(2,14)=0 and b.flag&pow(2,20)=0)  and (b.flag&pow(2,1)>0 or b.flag&pow(2,4)>0) and c.model='best' and c.band='i' and c.ftype='u' and  a.galcount = c.galcount and a.model='ser' and a.band='i' and a.ftype='u';

update catalog.Flags_catalog as c, catalog.Flags_catalog as b, catalog.Flags_catalog as a  set c.flag = a.flag  where c.galcount = b.galcount and b.model='serexp' and b.band='i' and b.ftype='u' and (b.flag&pow(2,10)=0 and b.flag&pow(2,14)=0 and b.flag&pow(2,20)=0)  and (b.flag&pow(2,1)>0 or b.flag&pow(2,4)>0) and  c.model='best' and c.band='i' and c.ftype='r' and  a.galcount = c.galcount and a.model='ser' and a.band='i' and a.ftype='r';

