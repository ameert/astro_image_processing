truncate r_simard_best;
insert into r_simard_best select a.* from r_simard_ser as a, r_simard_fit as b where a.galcount = b.galcount and b.Prob_pS>=0.32;

insert into r_simard_best select a.* from r_simard_devexp as a, r_simard_fit as b where a.galcount = b.galcount and b.Prob_pS<0.32 and  b.Prob_n4>=0.32;

insert into r_simard_best select a.* from r_simard_serexp as a, r_simard_fit as b where a.galcount = b.galcount and b.Prob_pS<0.32 and  b.Prob_n4<0.32;


truncate r_mendel_best;
insert into r_mendel_best select a.* from r_simard_ser as a, r_simard_fit as b where a.galcount = b.galcount and (b.ProfType=1 or b.ProfType=2);

insert into r_mendel_best select a.* from r_simard_devexp as a, r_simard_fit as b where a.galcount = b.galcount and b.ProfType=3;


#insert into Flags_optimize (galcount,ftype, band, model) select galcount, 'u', 'r', 'best' from CAST; 
#insert into Flags_optimize (galcount,ftype, band, model) select galcount, 'r', 'r', 'best' from CAST; 

truncate r_band_best;
insert into r_band_best select a.* from r_band_serexp as a, Flags_optimize as b where a.galcount = b.galcount and b.model='serexp' and b.band='r' and b.ftype='u' and (b.flag&pow(2,10)>0 or b.flag&pow(2,14)>0 or b.flag&pow(2,19)>0);

update Flags_optimize as c, Flags_optimize as b set c.flag = b.flag  where c.galcount = b.galcount and b.model='serexp' and b.band='r' and b.ftype='u' and (b.flag&pow(2,10)>0 or b.flag&pow(2,14)>0  or b.flag&pow(2,19)>0) and c.model='best' and c.band='r' and c.ftype='u';

update Flags_optimize as c, Flags_optimize as b, Flags_optimize as a  set c.flag = a.flag  where c.galcount = b.galcount and b.model='serexp' and b.band='r' and b.ftype='u' and (b.flag&pow(2,10)>0 or b.flag&pow(2,14)>0 or b.flag&pow(2,19)>0) and  c.model='best' and c.band='r' and c.ftype='r' and  a.galcount = c.galcount and a.model='serexp' and a.band='r' and a.ftype='r';
 
insert into r_band_best select a.* from r_band_ser as a, Flags_optimize as b, Flags_optimize as c where a.galcount = b.galcount and b.model='serexp' and b.band='r' and b.ftype='u' and (b.flag&pow(2,10)=0 and b.flag&pow(2,14)=0 and b.flag&pow(2,19)=0) and (b.flag&pow(2,1)>0 or b.flag&pow(2,4)>0) and a.galcount = c.galcount and c.model='ser' and c.band='r' and c.ftype='u';

update Flags_optimize as c, Flags_optimize as b, Flags_optimize as a  set c.flag = a.flag  where c.galcount = b.galcount and b.model='serexp' and b.band='r' and b.ftype='u' and (b.flag&pow(2,10)=0 and b.flag&pow(2,14)=0 and b.flag&pow(2,19)=0)  and (b.flag&pow(2,1)>0 or b.flag&pow(2,4)>0) and c.model='best' and c.band='r' and c.ftype='u' and  a.galcount = c.galcount and a.model='ser' and a.band='r' and a.ftype='u';

update Flags_optimize as c, Flags_optimize as b, Flags_optimize as a  set c.flag = a.flag  where c.galcount = b.galcount and b.model='serexp' and b.band='r' and b.ftype='u' and (b.flag&pow(2,10)=0 and b.flag&pow(2,14)=0 and b.flag&pow(2,19)=0)  and (b.flag&pow(2,1)>0 or b.flag&pow(2,4)>0) and  c.model='best' and c.band='r' and c.ftype='r' and  a.galcount = c.galcount and a.model='ser' and a.band='r' and a.ftype='r';
