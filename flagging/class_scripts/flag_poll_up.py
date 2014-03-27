for model in ['ser','dev','serexp','devexp']:

    print "update Flags_optimize as x, r_band_badfits as a, r_deep_badfits as z set x.flag= x.flag+pow(2,25) where z.galcount =x.galcount and a.galcount =x.galcount and x.band='r' and x.model = '%s' and x.ftype='r' and x.flag&pow(2,0)>=0 and a.is_fractured = 1;" %model

    print "update Flags_optimize as x, r_band_badfits as a, r_deep_badfits as z set x.flag= x.flag+pow(2,24) where z.galcount =x.galcount and a.galcount =x.galcount and x.band='r' and x.model = '%s' and x.ftype='r' and x.flag&pow(2,0)>=0 and a.is_fractured = 1 and a.is_polluted = 1;" %model

    print "update Flags_optimize as x, r_band_badfits as a, r_deep_badfits as z set x.flag= x.flag+pow(2,24) where z.galcount =x.galcount and a.galcount =x.galcount and x.band='r' and x.model = '%s' and x.ftype='r' and x.flag&pow(2,0)>=0 and a.is_polluted = 1 and a.is_fractured = 0 and (z.is_polluted = 1 or z.is_fractured =1);" %model


for model in ['ser','dev','serexp','devexp']:

    print "update Flags_optimize as x, Flags_optimize as y set y.flag= pow(2,25)+pow(2,19) where y.galcount =x.galcount and x.band='r' and x.model = '%s' and x.ftype='r' and  y.band=x.band and y.model = x.model and y.ftype='u' and x.flag&(pow(2,24)+pow(2,25))>0 and y.flag&pow(2,24)=0;" %(model)
    #print "select x.galcount from  Flags_optimize as x, Flags_optimize as y where y.galcount =x.galcount and x.band='r' and x.model = '%s' and x.ftype='r' and  y.band=x.band and y.model = x.model and y.ftype='u' and x.flag&(pow(2,24)+pow(2,25))>0 and y.flag&pow(2,24)=0;" %(model)

    

for model in ['dev','ser','serexp','devexp']:

    #print "select a.galcount, a.r_bulge, a.BT from Flags_optimize as x,r_band_%s as a where a.r_bulge/0.396*sqrt(a.ba_bulge) between 0.0 and 1.0 and a.galcount =x.galcount and x.band='r' and x.model = '%s' and x.ftype='r';" %(model, model)
    print "Update Flags_optimize as x,r_band_%s as a set x.flag= x.flag+pow(2,26) where a.r_bulge/0.396*sqrt(a.ba_bulge) between 0.0 and 0.5 and a.galcount =x.galcount and x.band='r' and x.model = '%s' and x.ftype='r';" %(model, model)

for model in ['dev','ser','serexp','devexp']:

    #print "select a.galcount, y.flag&pow(2,10), ((y.flag^(pow(2,10)+pow(2,11)+pow(2,12)))|(pow(2,14)+pow(2,26)))&pow(2,10) as newflag from  Flags_optimize as x,Flags_optimize as y, r_band_%s as a  where a.galcount =x.galcount and a.galcount =y.galcount and x.band='r' and x.model = '%s' and x.ftype='r' and y.band='r' and y.model = '%s' and y.ftype='u' and x.flag&pow(2,26)>0 and (y.flag&pow(2,11)>0 or y.flag&pow(2,12)>0 );" %(model, model,model)
    print "Update Flags_optimize as x,Flags_optimize as y, r_band_%s as a set y.flag = (y.flag^(pow(2,10)+pow(2,11)+pow(2,12)))|(pow(2,14)+pow(2,26)) where a.galcount =x.galcount and a.galcount =y.galcount and x.band='r' and x.model = '%s' and x.ftype='r' and y.band='r' and y.model = '%s' and y.ftype='u' and x.flag&pow(2,26)>0 and (y.flag&pow(2,11)>0 or y.flag&pow(2,12)>0 );" %(model, model,model)

