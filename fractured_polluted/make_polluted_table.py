from mysql.mysql_class import *
import numpy as np
import sys

band = 'g'

cursor = mysql_connect('catalog','pymorph','pymorph')

cmd = "select a.galcount, a.objid, a.colc_{band}-b.colc_{band}+c.xctr_bulge, a.rowc_{band}-b.rowc_{band}+c.yctr_bulge,a.petroR50_{band}/0.396 from CAST_neighbors_{band} as a, CAST as b, {band}_band_ser as c where a.galcount = b.galcount and a.galcount = c.galcount  and a.is_polluter=1;"


print cmd.format(band=band)

# we should techinically include this, but there are only 2 sources that don't satisfy this and they are definitely problems.
#a.run=b.run and a.rerun=b.rerun and a.camcol=b.camcol and a.field=b.field

#galcount, objid, xpix, ypix, rpix = cursor.get_data(cmd)


