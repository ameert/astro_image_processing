#++++++++++++++++++++++++++
#
# TITLE: query_functions 
#
# PURPOSE: This function makes the
#          casjobs query used to get
#          the necessary data from casjobs.
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# WITH: Joseph Clampitt, Charles Davis
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 11 NOV 2014
#
#-----------------------------------
import traceback
import numpy as np
from astro_image_processing.casjobs_query.casjobs_new_query import get_file_info, exec_cmd, get_filename, write_config

def truncate_table(tabname):
    """truncates a table"""
    cmd = """truncate table {tabname};""".format(tabname=tabname)
    return cmd

def get_chunk(chunksize, chunknum):
    """returns a chunk of objects for the cone search. This must be done in chuncks to aoid overfilling the casjobs mydb storage space"""
    
    data = np.loadtxt('test_file_100_objs.txt', unpack=True, skiprows=(chunknum-1)*chunksize)
    chunkdata = {}
    for a in zip(data,['id', 'ra_gal','dec_gal','zgal', 'theta', 'deltaz_photo', 'deltaz_spec'], [int, float, float, float, float, float, float]):
        chunkdata[a[1]] = np.array(a[0][:chunksize], dtype=a[2])
    return chunkdata


def cone_search_query(job_info, is_spec=False):
    """The cone serch query used in building the correlated luminostiy function"""
    cmd = """declare @id int, @ra float, @dec float, @zgal float, @theta float, @deltaz float;

DECLARE my_cursor cursor read_only
FOR
"""
    if is_spec:
        cmd +="""SELECT mt.id, mt.ra_gal, mt.dec_gal, mt.zgal, mt.theta, mt.deltaz_spec """
    else:
        cmd +="""SELECT mt.id, mt.ra_gal, mt.dec_gal, mt.zgal, mt.theta, mt.deltaz_photo""" 
    cmd +=""" FROM MYDB.{in_tablename} as mt
OPEN my_cursor

WHILE(1=1)
BEGIN
  FETCH NEXT from my_cursor into @id, @ra, @dec, @zgal, @theta, @deltaz
  IF (@@fetch_status < 0) break
  INSERT MYDB.{tablename}
  SELECT  @id, N.distance/(180.0*60.0)*PI(), p.objid, 
  p.petroMag_u,p.petroMag_g, p.petroMag_r, p.petroMag_i, p.petroMag_z,
  p.extinction_u,p.extinction_g, p.extinction_r,p.extinction_i,p.extinction_z,
"""
    if is_spec:
        cmd += """S.z, S.zErr,
"""
    else:
        cmd += """z.z, z.zErr,
"""

    cmd += """z.kcorrU,z.kcorrG, z.kcorrR, z.kcorrI, z.kcorrZ
  FROM Galaxy as p, Photoz as z, """
    if is_spec:
        cmd += """SpecObj as S,
"""

    cmd +="""dbo.fGetNearbyObjEq(@ra,@dec,@theta/PI()*180*60) as N 
WHERE 
p.objid=N.objid
and z.objid=p.objid
"""

    if is_spec:
        cmd += """and S.bestObjID=p.objid
and abs(S.z-@zgal)<= @deltaz+S.zErr
"""
    else:
        cmd += """and abs(z.z-@zgal)<= @deltaz+z.zErr
"""
    cmd +="""END

CLOSE my_cursor
  DEALLOCATE my_cursor"""

    return cmd.format(**job_info)

def create_table(tabname):
    """creates the table for cone search output"""
    cmd = """create table {tabname} (id int, distance float, objid bigint, 
petroMag_u float,petroMag_g float, petroMag_r float, petroMag_i float,petroMag_z float, 
extinction_u float,extinction_g float, extinction_r float, extinction_i float,extinction_z float, 
z float, zErr float, 
kcorrU float, kcorrG float, kcorrR float, kcorrI float, kcorrZ float
);""".format(tabname=tabname)

    return cmd

def load_chunk(chunkdata, tabname):
    """creates a command to load data to a table denoted by tabname"""
    cmd = """insert into {tabname} VALUES {values};"""
    values = ','.join([str(a) for a in zip(chunkdata['id'], chunkdata['ra_gal'],chunkdata['dec_gal'],chunkdata['zgal'], chunkdata['theta'], chunkdata['deltaz_photo'], chunkdata['deltaz_spec'])])
    return cmd.format(tabname=tabname, values=values)


if __name__=="__main__":
    chunkdata ={'id':[1,2,3], 'ra_gal':[4,5,6], 'dec_gal':[7,8,9], 'zspec':[0.2,0.3,0.4],'theta':[10,11,12],'deltaz_spec':[10,11,12],'deltaz_photo':[10,11,12]}
    print load_chunk(chunkdata, 'hello')

