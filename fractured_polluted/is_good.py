from astro_image_processing.mysql.mysql_class import *
import numpy as np
import sys
cursor = mysql_connect('catalog','pymorph','pymorph')

def distance(xt, xn, yt, yn, ba, pa):
    cosa = np.cos(pa)
    sina = np.sin(pa)
        
    x_pix = cosa*(xn-xt) + (yn-yt)*sina
    y_pix = -sina*(xn-xt) + (yn-yt)*cosa
        
    rad_pix = np.sqrt(ba*(x_pix**2.0) + (y_pix**2)/ba)
    rad_pix = np.where(np.isnan(rad_pix), 999.0, rad_pix)
        
    return rad_pix*0.396 #in arcsec


def get_data(galcount, neighbor, isfit =True):
    if isfit:
        cmd = """select c.xctr_bulge,d.xctr_bulge, c.yctr_bulge,d.yctr_bulge, 
d.r_bulge*sqrt(d.ba_bulge), c.r_bulge,b.petroR50_i,
d.m_bulge, c.m_bulge, b.PetroMag_i,b.badflag, c.ba_bulge, c.pa_bulge
from  CAST as b, i_deep_ser as c, 
i_deep_neighbors_ser as d where  
b.galcount = c.galcount and 
c.galcount = d.galcount and c.galcount = %d
and d.neighbornum = %d;""" %(galcount, neighbor)
    else:
        cmd = """select  b.colc_i, a.colc_i, b.rowc_i,a.rowc_i, 
a.petroR50_i, c.r_bulge, b.petroR50_i, 
a.PetroMag_i, c.m_bulge, b.PetroMag_i, a.flags_i,c.ba_bulge, c.pa_bulge
from CAST_neighbors_i as a, CAST as b, i_deep_ser as c
where a.flags_i&70368744177664=0 and
a.galcount = b.galcount and a.galcount = c.galcount and 
b.galcount = %d and a.objid = %d;""" %(galcount, neighbor)
#flag condition prevents "nopeaks" from being considered
    data = np.array(cursor.get_data(cmd)).T[0]
        
    return data 
    
if __name__=="__main__":
    if 0:
        cmd =  'UPDATE i_deep_neighbors_ser set is_fracture=0, ismatched = 0;'
        print cmd
        cursor.execute(cmd)

        cmd = 'UPDATE CAST_neighbors_i set neighbornum_deep = 999, neighborfit_deep = 0, is_polluter_deep=0, is_masked_deep = 0;'
        print cmd
        cursor.execute(cmd)

        cmd = 'update i_band_badfits set is_polluted_deep=0, is_fractured_deep=0;'
        print cmd
        cursor.execute(cmd)

    #sys.exit()


    #gals = [29, 55650, 87030, 122899, 152158, 188196, 206773, 251863, 307713, 354375, 385152, 488123, 525891, 531338, 574397, 588738, 597065, 601737, 647330, 652989]
    mult = int(sys.argv[1])

    #cmd = """select galcount from r_band_badfits where is_polluted >0 and galcount between %d and %d;""" %(mult*10000+1, (mult+1)*10000+1)
    #cmd = """select galcount from r_band_badfits where is_polluted >0 and galcount between 1250 and 1500;""" 
    #data, = cursor.get_data(cmd)

    #gals = data
    #gals = [7946]
    gals = range(mult*100000+1,(mult+1)*100000+1)
    #print gals

    #false is fake source, True is real source
    human_class = {29:[False,True,False],
                   55650:[True, False], 
                   87030:[True, True, True], 
                   122899:[True], 152158:[False], 
                   188196:[True,True], 206773:[True], 
                   251863:[False,True,True], 
                   307713:[False], 354375:[True], 
                   385152:[True,True, True, True], 488123:[True, True], 
                   525891:[False], 531338:[False], 
                   574397:[True,True, True], 588738:[True], 
                   597065:[True,True,True], 601737:[False,True, False], 
                   647330:[False], 652989:[True]}


    fractured = []
    polluted = []


    for galcount in gals:
        #print "searching gal ", galcount
        #print "Alan class ", human_class[galcount]

        cmd = """select IFNULL(a.objid,-999), IFNULL(d.neighbornum,-999), 
    IFNULL(c.xctr_bulge,-999),IFNULL(d.xctr_bulge,-888), 
    IFNULL(c.yctr_bulge,-999),IFNULL(d.yctr_bulge,-888), 
    IFNULL(b.rowc_i,-777), IFNULL(b.colc_i,-777), 
    IFNULL(a.rowc_i,-666), IFNULL(a.colc_i,-666), 
    IFNULL(a.petroR50_i,-999), IFNULL(d.ismatched,-999), 
    IFNULL(b.run,-999), IFNULL(a.run,-999), 
    IFNULL(b.petroR50_i,-999), 
    IFNULL(c.r_bulge*sqrt(c.ba_bulge), -999), IFNULL(a.distance*60.0, 999)
    from  ((CAST as b left join CAST_neighbors_i as a on a.galcount = b.galcount) left join i_deep_ser as c on b.galcount = c.galcount) left join i_deep_neighbors_ser as d on b.galcount = d.galcount where b.galcount = %d and c.galcount is not null;""" %galcount

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

            dp = distance(x_t, x_n, y_t, y_n,1.0,0.0)
            dr = distance(row_t, row_n, col_t, col_n,1.0,0.0)

            ddr = distance(x_t-col_t, x_n-col_n, y_t-row_t, y_n-row_n,1.0,0.0)

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

            #print "matches "
            if galcount%1000 ==0:
                print "gal ", galcount
            for a in matches:
                #print a[0:2],' %.2f, %.2f, %.2f, %.2f'%tuple(a[-4:])
                cmd = 'update CAST_neighbors_i set neighbornum_deep = %d, neighborfit_deep = 1 where objid = %d;' %(a[1],a[0])
                #print cmd
                cursor.execute(cmd)
                cmd = 'update i_deep_neighbors_ser set ismatched=1 where galcount = %d and neighbornum = %d;' %(galcount,a[1])
                #print cmd
                cursor.execute(cmd)

            #print "nomatches"
            #for a in nomatches:
            #    print a[0:2],' %.2f, %.2f, %.2f, %.2f'%tuple(a[-4:])
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

            #print 'extra cas '
            #print set(extra_cas)
            #print 'extra nums '
            #print set(extra_source)


            #do the extra sources matter?
            checknums = set(extra_source)
            for num in checknums:
                if num == -999:
                    continue
                xt,xn, yt,yn, rn, rf,rcas,mn, mf, mcas,flag, ba_t, pa_t=get_data(galcount, num, isfit =True)
                dis = distance(xt, xn, yt, yn, 1.0, 0.0) 
                # use ba=1 and rcas because we want to find sources that should be
                # together, so in this case the target fit is wrong
                if dis < 3.0*rcas and mn-mf < 3.0-dis/rcas and dis<9.0 and mf-mcas>0.5:
                    #print "OHNO Fractured! ", num
                    fractured.append(galcount)
                    cmd = 'update i_deep_neighbors_ser set is_fracture=1, ismatched=0 where neighbornum = %d and galcount = %d;' %(num, galcount)
                    cursor.execute(cmd) 
                else:
                    cmd = 'update i_deep_neighbors_ser set is_fracture=0, ismatched=0 where neighbornum = %d and galcount = %d;' %(num, galcount)
                    cursor.execute(cmd) 
            checkcas = set(extra_cas)
            for num in checkcas:
                if num == -999:
                    continue
                xt,xn, yt,yn, rn, rf,rcas,mn, mf, mcas,flag, ba_t, pa_t=get_data(galcount, num, isfit =False)
    #            print xt,xn, yt,yn, rn, rf,rcas,mn, mf, mcas,flag, ba_t, pa_t
                dis = distance(xt, xn, yt, yn, ba_t, pa_t)
                userad = np.max([rf,rcas])
                if dis < 3.0*userad and mn-mf < 4.0-dis/userad:
    #                print "OHNO polluted! ", num
                    polluted.append(galcount)
                    cmd = 'update CAST_neighbors_i set is_polluter_deep = 1, neighbornum_deep = -999, neighborfit_deep = 0 where objid = %d;' %(num)
                    #print cmd
                    cursor.execute(cmd)
                else:
                    cmd = 'update CAST_neighbors_i set is_polluter_deep = 0 , neighbornum_deep = 999, neighborfit_deep = 0 where objid = %d;' %(num)
                    #print cmd
                    cursor.execute(cmd)
                    #print "NOWORRIES! ", num
                    #print dis, rf, rcas, mn, mf,mn-mf,4.0-dis/rf,rn 

            #for a in matches:
            #    if 

        except IndexError:
            pass
        #if galcount > 100000:
        #    break


    fractured = list(set(fractured))
    fractured.sort()
    #for count in fractured:
    #    cmd = 'update r_band_badfits set is_fractured = 1 where galcount = %d;' %count
        #cursor.execute(cmd)
    polluted = list(set(polluted))
    polluted.sort()
    #for count in polluted:
    #    cmd = 'update r_band_badfits set is_polluted = 1 where galcount = %d;' %count
        #cursor.execute(cmd)
    ok = []

    cmd = 'update i_band_badfits set is_polluted_deep={pollute}, is_fractured_deep={frac} where galcount = {galcount};'
    for a in gals:
        frac = 0
        pollute=0
        if a in polluted:
             pollute = 1
        if a in fractured:
            frac=1
        if pollute+frac==0:
            ok.append(a)
        else:
            cursor.execute(cmd.format(frac=frac, pollute=pollute, galcount = a))

    print "fractured"
    #print zip(fractured, [human_class[a][0] for a in fractured]) 
    print fractured 
    print "polluted"
    #print zip(polluted, [human_class[a][0] for a in polluted]) 
    print polluted
    #print "OK"
    #print ok
    #print zip(ok, [human_class[a][0] for a in ok]) 
