#++++++++++++++++++++++++++
#
# TITLE: match_query_functions 
#
# PURPOSE: This function makes the
#          casjobs query used to get
#          the necessary data from casjobs.
#          
# INPUTS: 
#         
#         
#
# OUTPUTS: The query string used by casjobs for correlated luminosity function
#
# PROGRAM CALLS: NONE
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 17 OCT 2014
#
#-----------------------------------
import traceback

def cone_search_query(job_info):
    """The cone serch query used in building the correlated luminostiy function"""
    cmd = """declare @thing_id int, @objid bigint, @ra float, @dec float, @zgal float;

DECLARE my_cursor cursor read_only
FOR
SELECT mt.thing_id, p.objid, p.ra, p.dec, mt.zspec FROM MYDB.{in_tablename} as mt, PhotoPrimary as p, specObj as s where mt.plate=s.plate and mt.fiber=s.fiberID and mt.mjd=s.mjd and s.bestObjID = p.objid
OPEN my_cursor

WHILE(1=1)
BEGIN
  FETCH NEXT from my_cursor into @thing_id, @objid, @ra, @dec, @zgal
  IF (@@fetch_status < 0) break
  INSERT MYDB.{tablename}
  SELECT  @thing_id, @objid, @zgal, N.distance, p.objid, p.petroMag_g, p.petroMag_r, p.petroMag_i, p.ModelMag_g, p.ModelMag_r, p.ModelMag_i, 
    p.CModelMag_g, p.CModelMag_r, p.CModelMag_i, p.fracdev_g, p.fracdev_r, p.fracdev_i, p.devmag_g, p.devmag_r, p.devmag_i, p.expmag_g, p.expmag_r, p.expmag_i,
    p.extinction_g, p.extinction_r, p.extinction_i
  FROM Galaxy as p,
dbo.fGetNearbyObjEq(@ra,@dec,3.0) as N where p.objid=N.objid
END

CLOSE my_cursor
  DEALLOCATE my_cursor""".format(**job_info)

    return cmd

def cone_search_blanksky_query(job_info):
    """The cone serch query used in building the correlated luminostiy function for searching blank sky"""
    cmd = """declare @thing_id int, @objid bigint, @ra float, @dec float, @zgal float;

DECLARE my_cursor cursor read_only
FOR
SELECT mt.thing_id, -999, mt.ra_gal, mt.dec_gal, mt.zspec FROM MYDB.{in_tablename} as mt
 OPEN my_cursor

WHILE(1=1)
BEGIN
  FETCH NEXT from my_cursor into @thing_id, @objid, @ra, @dec, @zgal
  IF (@@fetch_status < 0) break
  INSERT MYDB.{tablename}
  SELECT  @thing_id, @objid, @zgal, N.distance, p.objid, p.petroMag_g, p.petroMag_r, p.petroMag_i, p.ModelMag_g, p.ModelMag_r, p.ModelMag_i, 
    p.CModelMag_g, p.CModelMag_r, p.CModelMag_i, p.fracdev_g, p.fracdev_r, p.fracdev_i, p.devmag_g, p.devmag_r, p.devmag_i, p.expmag_g, p.expmag_r, p.expmag_i,
    p.extinction_g, p.extinction_r, p.extinction_i
  FROM Galaxy as p,
dbo.fGetNearbyObjEq(@ra,@dec,3.0) as N where p.objid=N.objid
END

CLOSE my_cursor
  DEALLOCATE my_cursor""".format(**job_info)

    return cmd


def create_table(tabname):
    """creates the table for cone search output"""
    cmd = """create table {tabname} (thing_id int, cmass_objid bigint, zgal float, distance float, objid bigint, 
petroMag_g float, petroMag_r float, petroMag_i float, 
ModelMag_g float,  ModelMag_r float, ModelMag_i float, 
CModelMag_g float, CModelMag_r float, CModelMag_i float, 
fracdev_g float, fracdev_r float, fracdev_i float, 
devmag_g float, devmag_r float, devmag_i float, 
expmag_g float, expmag_r float, expmag_i float,
extinction_g float, extinction_r float, extinction_i float);""".format(tabname=tabname)

    return cmd

def truncate_table(tabname):
    """truncates a table"""
    cmd = """truncate table {tabname};""".format(tabname=tabname)
    return cmd


def load_chunk(chunkdata, tabname):
    """creates a command to load data to a table denoted by tabname"""
    cmd = """insert into {tabname} VALUES {values};"""

    values = ','.join([str(a) for a in zip(chunkdata['thing_id'],chunkdata['plate'],chunkdata['mjd'],chunkdata['fiber'],chunkdata['zspec'])])
    return cmd.format(tabname=tabname, values=values)

def load_chunk_blanksky(chunkdata, tabname):
    """creates a command to load data to a table denoted by tabname"""
    cmd = """insert into {tabname} VALUES {values};"""

    values = ','.join([str(a) for a in zip(chunkdata['thing_id'],chunkdata['zspec'],chunkdata['ra_gal'],chunkdata['dec_gal'])])
    return cmd.format(tabname=tabname, values=values)


if __name__=="__main__":
    chunkdata ={'thing_id':[1,2,3], 'plate':[4,5,6], 'mjd':[7,8,9], 'fiber':[10,11,12], 'zspec':[0.2,0.3,0.4]}
    print load_chunk(chunkdata, 'hello')

