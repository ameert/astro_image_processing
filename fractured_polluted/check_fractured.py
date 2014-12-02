from mysql.mysql_class import *
import numpy as np
import sys

cursor = mysql_connect('catalog','pymorph','pymorph')

mult = int(sys.argv[1])

cmd = """select galcount from r_band_badfits where is_fractured =1 and galcount between 0 and 700000;""" 
#cmd = """select galcount from r_band_badfits where is_fractured =1 and galcount between %d and %d;""" %(mult*10000+1, (mult+1)*10000+1)
#cmd = """select galcount from r_band_badfits where is_fractured =1;""" 
data, = cursor.get_data(cmd)
print cmd
gals = data
gals = [213009]
print gals
print len(gals)
#sys.exit()
def distance(xt, xn, yt, yn):
    dx = np.array(xt)-np.array(xn)
    dy = np.array(yt)-np.array(yn)

    return np.sqrt(dx**2+ dy**2)*0.396 #in arcsec


def get_data(galcount, neighbor, isfit =True):
    if isfit:
        cmd = """select c.xctr_bulge,d.xctr_bulge, c.yctr_bulge,d.yctr_bulge, 
d.r_bulge*sqrt(d.ba_bulge), c.r_bulge*sqrt(c.ba_bulge),b.petroR50_r,
d.m_bulge, c.m_bulge, b.PetroMag_r,b.badflag
from  CAST as b, r_band_ser as c, 
r_neighbors_ser as d where  
b.galcount = c.galcount and 
c.galcount = d.galcount and c.galcount = %d
and d.neighbornum = %d;""" %(galcount, neighbor)
    else:
        cmd = """select  b.colc_r, a.colc_r, b.rowc_r,a.rowc_r, 
a.petroR50_r, c.r_bulge*sqrt(c.ba_bulge), b.petroR50_r, 
a.PetroMag_r, c.m_bulge, b.PetroMag_r, a.flags_r
from CAST_neighbors as a, CAST as b, r_band_ser as c
where (a.flags_r&70368744177664=0 or a.flags_r<0) and
a.galcount = b.galcount and a.galcount = c.galcount and 
b.galcount = %d and a.objid = %d;""" %(galcount, neighbor)
#flag condition prevents "nopeaks" from being considered
    data = np.array(cursor.get_data(cmd)).T[0]
        
    return data 
    
fractured = []
polluted = []


for galcount in gals:
    print "searching gal ", galcount
    
    cmd = """select IFNULL(a.objid,-999), IFNULL(d.neighbornum,-999), 
IFNULL(c.xctr_bulge,-999),IFNULL(d.xctr_bulge,-888), 
IFNULL(c.yctr_bulge,-999),IFNULL(d.yctr_bulge,-888), 
IFNULL(b.rowc_r,-777), IFNULL(b.colc_r,-777), 
IFNULL(a.rowc_r,-666), IFNULL(a.colc_r,-666), 
IFNULL(a.petroR50_r,-999), IFNULL(d.ismatched,-999), 
IFNULL(b.run,-999), IFNULL(a.run,-999), 
IFNULL(b.petroR50_r,-999), 
IFNULL(c.r_bulge*sqrt(c.ba_bulge), -999), IFNULL(a.distance*60.0, -999)
from  ((CAST as b left join CAST_neighbors as a on a.galcount = b.galcount) left join r_band_ser as c on b.galcount = c.galcount) left join r_neighbors_ser as d on b.galcount = d.galcount where b.galcount = %d;""" %galcount

    matches = []
    nomatches = []

    try:
        data = cursor.get_data(cmd)
        
        objid_n = np.array(data[0], dtype=np.int64)
        neighbornum = np.array(data[1], dtype=int)
        x_t = np.array(data[2])
        x_n = np.array(data[3])
        y_t = np.array(data[4])
        y_n = np.array(data[5])
        row_t = np.array(data[6])
        col_t = np.array(data[7])
        row_n = np.array(data[8])
        col_n = np.array(data[9])
        r_n = np.array(data[10])
        ismatched = np.array(data[11], dtype=int)
        rundiff = np.array(data[12], dtype=int)-np.array(data[13], dtype=int)
        r_t = np.array(data[14])
        r_f = np.array(data[15])
        castDistance = np.array(data[16])

        # adjust r_n to scale with petrorad unless r_n bigger than 1.5 arcsec
        #r_n = np.where(r_n<1.5, r_n, 1.5)
        r_n = np.where(rundiff==0, 1.5, 1.5)
        #r_n = np.where(r_n<1.5, r_n, 1.5)

        dp = distance(x_t, x_n, y_t, y_n)
        dr = distance(row_t, row_n, col_t, col_n)

        ddr = distance(x_t-col_t, x_n-col_n, y_t-row_t, y_n-row_n)
        print x_t, x_n, y_t, y_n
        print row_t, row_n, col_t, col_n
        print dp
        print dr
        print ddr
        #calculate a best distance, based on whether they are the same run
        best_dist = np.copy(ddr)
        best_dist = np.where(rundiff==0, best_dist, abs(dp-castDistance))
        for a in zip(objid_n,neighbornum,ismatched,rundiff,r_t, r_f,
                     best_dist,r_n):
            #print a
            if abs(a[-2])<a[-1]:
                matches.append(a)
            else:
                nomatches.append(a)
        
        print "matches "
        if galcount%1000 ==0:
            print "gal ", galcount
        for a in matches:
            print a[0:2],' %.2f, %.2f, %.2f, %.2f'%tuple(a[-4:])
            #cmd = 'update CAST_neighbors set neighbornum = %d, neighborfit = 1 where objid = %d;' %(a[1],a[0])
            #print cmd
            #cursor.execute(cmd)
        print "nomatches"
        for a in nomatches:
            print a[0:2],' %.2f, %.2f, %.2f, %.2f'%tuple(a[-4:])
        #continue
        # prune matches if there is a duplicate better match (highly unlikely
        # but lets check)
        nnums = np.array([b[1] for b in matches], dtype=int)
        objnum = np.array([b[0] for b in matches], dtype=int)

        #if len(set(nnums)) != len(nnums):
            #do something!
        #    print "repeats of nnum found"
        #if len(set(objnum)) != len(objnum):
        #    #do something!
        #    print "repeats of objnum found"

        extra_cas = []
        extra_source = []
        for a in nomatches:
            if a[0] not in objnum:
                extra_cas.append(a[0])
            if a[1] not in nnums:
                extra_source.append(a[1])
    
        print 'extra cas '
        print set(extra_cas)
        print 'extra nums '
        print set(extra_source)


        #do the extra sources matter?
        checknums = set(extra_source)
        for num in checknums:
            if num == -999:
                continue
            xt,xn, yt,yn, rn, rf,rcas,mn, mf, mcas,flag=get_data(galcount, num, isfit =True)
            dis = distance(xt, xn, yt, yn)
            print "dis ", dis
            if dis < 3.0*rcas and mn-mf < 3.0-dis/rcas and dis<9.0:
                print 'dis ', dis, rcas
                print 'mags ',mn, mf, mn-mf, 4.0-dis/rcas
                print "OHNO Fractured! ", num
                fractured.append(galcount)
#                cmd = 'update r_neighbors_ser set is_fracture=1 where neighbornum = %d and galcount = %d;' %(num, galcount)
#                print cmd
#                cursor.execute(cmd)#print dis, rcas, mn, mf,mn-mf,4.0-dis/rcas 
            else:
                cmd = 'update r_neighbors_ser set is_fracture=0 where neighbornum = %d and galcount = %d;' %(num, galcount)
                print cmd
                cursor.execute(cmd)               
                #pass
                #print "NOWORRIES! ", num
                #print dis, rcas, mn, mf,mn-mf,4.0-dis/rcas 
        checkcas = set(extra_cas)
        for num in checkcas:
            if num == -999:
                continue
            xt,xn, yt,yn, rn, rf,rcas,mn, mf, mcas,flag=get_data(galcount, num, isfit =False)
            dis = distance(xt, xn, yt, yn)
            if dis < 4.0*rcas and mn-mf < 4.0-dis/rcas and dis<9.0:
                #print "OHNO polluted! ", num
                polluted.append(galcount)
                #print dis, rcas, mn, mf,mn-mf,4.0-dis/rcas,int(flag)&70368744177664 
            else:
                pass
                #cmd = 'update CAST_neighbors set neighbornum = 999, neighborfit = 0 where objid = %d;' %(num)
                #print cmd
                #cursor.execute(cmd)
                #print "NOWORRIES! ", num
                #print dis, rcas, mn, mf,mn-mf,4.0-dis/rcas,int(flag)&70368744177664
                
        #for a in matches:
        #    if 
        
    except IndexError:
        pass
    #if galcount > 100000:
    #    break

fractured = set(fractured)
for count in fractured:
    cmd = 'update r_band_badfits set is_fractured = 1 where galcount = %d;' %count
    cursor.execute(cmd)
polluted = set(polluted)
#for count in polluted:
#    cmd = 'update r_band_badfits set is_polluted = 1 where galcount = %d;' %count
#    cursor.execute(cmd)



ok = []

for a in gals:
    if a not in fractured:
        cmd = 'update r_band_badfits set is_fractured = 0 where galcount = %d;' %a
        cursor.execute(cmd)
        if a not in polluted:
            ok.append(a)

#ok = set(ok)
#for count in fractured:


print "fractured"
print fractured
#print zip(fractured, [human_class[a][0] for a in fractured]) 
print "polluted"
print polluted 
#print zip(polluted, [human_class[a][0] for a in polluted]) 
print "OK"
print ok
#print zip(ok, [human_class[a][0] for a in ok]) 
