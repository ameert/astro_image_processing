#col = 'zmodel,Ie,Ie_err,re_pix,re_err_pix,re_kpc,re_err_kpc,n,n_err,eb,GalSky'
col = 'GalSky,Ie,Ie_err,re_pix,re_err_pix,re_kpc,re_err_kpc,n,n_err,eb,Id,Id_err,rd_pix,rd_err_pix,rd_kpc,rd_err_kpc,ed,BT,chi2nu,GalSky'
m = 'Ser'
n = 'SerExp'
col = col.split(',')
for i in range(len(col) - 1):
 cmd = 'alter table s0_test add column ' + col[i+1] + '_' + str(m) + ' float after ' + col[i] + '_' + str(n) + ';'
 #cmd = 'alter table s0_test change column ' + col[i] +' ' + col[i] + '_' + str(m) + ' float;'
# print cmd
col = 'Ie,Ie_err,re_pix,re_err_pix,re_kpc,re_err_kpc,n,n_err,eb,Id,Id_err,rd_pix,rd_err_pix,rd_kpc,rd_err_kpc,ed,BT,GalSky,chi2nu'
col = col.split(',')
l = "update s0_test as a, s0_ser as b set "
for i in range(len(col)):
 l +=  'a.'+col[i] + '_' + str(m) + "=  b."+col[i]+ ', '
l += " where Name = b.Name"
print l
col = 'Morphology,ObsID,Date,Version,Filter,Total_Run,rootname,Name,ra_,dec_,z,mag_auto,magerr_auto,AvgIe,AvgIe_err,eb_err,bboxy,bboxy_err,ed_err,dboxy,dboxy_err,Point,Point_err,Pfwhm,Pfwhm_kpc,Goodness,run,C,C_err,A,A_err,S,S_err,G,M,SexSky,dis_modu,distance,fit,flag,Manual_flag,MorphType,Comments'
col = col.split(',')
l = "insert into s0_test("+col[0]
for i in range(1,len(col)):
    l += ','+col[i]
l += ") select "+col[0]
for i in range(1,len(col)):
    l += ","+col[i]
l += " from s0_ser UNION ALL select  "+col[0]
for i in range(1,len(col)):
    l += "," + col[i]
l+= " from s0_dev_exp UNION ALL select "+col[0]
for i in range(1,len(col)):
    l += "," + col[i]
l+= " from s0_ser_exp;" 


#    l += ', '+ col[i]
#l += ')\nVALUES (s0_ser_exp.'+col[0]
#for i in range(1,len(col)):
#    l += ', s0_ser_exp.'+col[i]
#l += ');\n'

#print l
