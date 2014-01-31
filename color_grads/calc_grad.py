"""create table %s_colorgrad_%srad (galcount int primary key, centerrad_arcsec float default -999,
grCenter float default -999,  giCenter float default -999,  riCenter float default -999,
gr05_hl float default -999,  gi05_hl float default -999,  ri05_hl float default -999,
gr10_hl float default -999,  gi10_hl float default -999,  ri10_hl float default -999,
gr15_hl float default -999,  gi15_hl float default -999,  ri15_hl float default -999,
gr20_hl float default -999,  gi20_hl float default -999,  ri20_hl float default -999,
gr25_hl float default -999,  gi25_hl float default -999,  ri25_hl float default -999,
gr30_hl float default -999,  gi30_hl float default -999,  ri30_hl float default -999,
gr40_hl float default -999,  gi40_hl float default -999,  ri40_hl float default -999,
gr90_hl float default -999,  gi90_hl float default -999,  ri90_hl float default -999);
"""

bands = 'gr'
table_name = 'CAST'
dba = 'catalog'
usr = 'pymorph'
pwd = 'pymorph'
lhost = ''

cursor = mysql_connect(dba, usr, pwd, lhost)

folder_num = int(sys.argv[1])
path = '/home/ameert/color_grad/data/%04d' %folder_num
model = 'ser'

cmd = """select a.galcount, x.r50_r_arcsec,x.r90_r_arcsec from CAST as a, 
%s_hrad_90_est as x
where a.galcount = x.galcount and a.galcount between %d and %d 
order by galcount;""" %(model, (folder_num-1)*250, folder_num*250)

data = cursor.get_data(cmd)

galcount = np.array(data[0], dtype = int)
profiles = {'g':{}, 'r':{}, 'i':{}, 'gr':[], 'gi':[], 'ri':[] }

for gc, dat in zip(galcount,np.array(data[1:]).transpose()):
    radlim = 3.0*dat[0]
    try:
        rads = np.extract(profiles['log_rad_arcsec']< np.log10(radlim), profiles['log_rad_arcsec'])
        
        for tcount,tb in enumerate(['gr']):#,'gi','ri']):
            try:
                color = np.extract(profiles['log_rad_arcsec']< np.log10(radlim), profiles[tb])
                cerr = np.extract(profiles['log_rad_arcsec']< np.log10(radlim), profiles[tb+'_err'])
            

                
            except:
                #print "skipping gc:%d band:%s" %(gc, tb)
                pass
        if 0:
            cmd = """update %s_colorgrad_%srad set centerrad_arcsec = %f,
        grCenter = %f,  giCenter = %f,  riCenter = %f,
        gr05_hl = %f,  gi05_hl = %f,  ri05_hl = %f,
        gr10_hl = %f,  gi10_hl = %f,  ri10_hl = %f,
        gr15_hl = %f,  gi15_hl = %f,  ri15_hl = %f,
        gr20_hl = %f,  gi20_hl = %f,  ri20_hl = %f,
        gr25_hl = %f,  gi25_hl = %f,  ri25_hl = %f,
        gr30_hl = %f,  gi30_hl = %f,  ri30_hl = %f,
        gr40_hl = %f,  gi40_hl = %f,  ri40_hl = %f,
        gr90_hl = %f,  gi90_hl = %f,  ri90_hl = %f
        where galcount = %d;""" %(model, model, innerrad,
                                  rad_vals[0],rad_vals[1],rad_vals[2],
                                  rad_vals[3],rad_vals[4],rad_vals[5],
                                  rad_vals[6],rad_vals[7],rad_vals[8],
                                  rad_vals[9],rad_vals[10],rad_vals[11],
                                  rad_vals[12],rad_vals[13],rad_vals[14],
                                  rad_vals[15],rad_vals[16],rad_vals[17],
                                  rad_vals[18],rad_vals[19],rad_vals[20],
                                  rad_vals[21],rad_vals[22],rad_vals[23],
                                  rad_vals[24],rad_vals[25],rad_vals[26],
                                  gc)
        
        cmd = cmd.replace('nan', '-999.0')
        #print gc
        #print r50, r90
        #print cmd
        cursor.execute(cmd)
    except IOError:
        print IOError
