create table simulations.svm_probs (galcount int primary key, p_ser float default -999, p_serexp float default -999, ser_serexp_choice int default -999);
insert into simulations.svm_probs (galcount) select simcount from simulations.sim_input;

create table catalog.svm_probs (galcount int primary key, p_ser float default -999, p_serexp float default -999, ser_serexp_choice int default -999);
insert into catalog.svm_probs (galcount) select galcount from catalog.CAST;

