select count(*) from yang.ModelGroupsC where member_count =1;
select count(*) from yang.ModelGroupsC where member_count =2;
select count(*) from yang.ModelGroupsC where member_count =3;
select count(*) from yang.ModelGroupsC where member_count >3;
select count(*) from yang.ModelGroupsC where member_count >1;

select count(*) from yang.ModelGroupsC where member_count =1 and z<=0.09;
select count(*) from yang.ModelGroupsC where member_count =2 and z<=0.09;
select count(*) from yang.ModelGroupsC where member_count =3 and z<=0.09;
select count(*) from yang.ModelGroupsC where member_count >3 and z<=0.09;

select count(*) from yang.ModelGroupsC where member_count >1 and z<=0.09;
select count(*) from yang.ModelGroupsC where member_count >1 and z>0.09;

select count(*) from yang.ModelGroupsC where member_count >1 and z<=0.09 and fedge >=0.6;

