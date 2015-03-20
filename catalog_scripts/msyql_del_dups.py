create table tmp_table (galcount int, date varchar(30));

truncate tmp_table;

alter table full_dr7_r_dev add column galcount int first;
Update full_dr7_r_dev set galcount = SUBSTRING(Name,locate('0', Name), 8);

insert into tmp_table select galcount, Date from full_dr7_r_serexp group by galcount having count(*) > 1;

select galcount, Date from full_dr7_r_serexp group by galcount having count(*) > 1;

delete from full_dr7_r_serexp where galcount in (select galcount from tmp_table) and date = '2012.7.2';

alter table full_dr7_r_serexp add primary key (galcount);
