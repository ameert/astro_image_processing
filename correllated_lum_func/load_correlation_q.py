import os


cmd = 'mysql -u pymorph -ppymorph catalog < cmdfile.txt'

tablename = "corr_lum_func_galaxy_blanks"
infile = '/home/ameert/claudia/data/correlated_sample_raw_blanks_galaxy.cat'

create_table_cmd = """CREATE TABLE {tablename} (thing_id int, objid_thing bigint, zgal float, distance float, objid_n bigint, petroMag_g float, petroMag_r float , petroMag_i float, ModelMag_g float, ModelMag_r float, ModelMag_i float, CModelMag_g float, CModelMag_r float, CModelMag_i float, fracdev_g float, fracdev_r float, fracdev_i float, devmag_g float, devmag_r float, devmag_i float, expmag_g float, expmag_r float, expmag_i float, extinction_g float, extinction_r float, extinction_i float, dismod float default 0.0, kpc_per_arcsec float default -999);
ALTER TABLE {tablename} ADD UNIQUE KEY (thing_id, objid_thing, objid_n);
""".format(tablename=tablename)

print create_table_cmd


cmdfilecmd = """LOAD DATA INFILE '{infile}' IGNORE INTO TABLE {tablename}
FIELDS TERMINATED BY ',' IGNORE 1 LINES;""".format(infile=infile, tablename=tablename)
print cmdfilecmd


cmd2 = """update {tablename} as a, claudia_values as b set a.dismod=b.dismod, a.kpc_per_arcsec = b.kpc_per_arcsec where a.thing_id=b.thing_id;
""".format(tablename=tablename)
print cmd2
