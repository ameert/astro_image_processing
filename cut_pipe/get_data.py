### Now import configuration variables ###
from cutout_config import *
import astro_image_processing.user_settings as user_settings
from astro_image_processing.mysql import *


### the first entry is the name in mysql, the second in the name for my program

def get_cut_data(start_num, end_num):
    """gets data from SQL table for fitting"""

    cursor = mysql_connect(user_settings.mysql_params['dba'],
                           user_settings.mysql_params['user'],
                           user_settings.mysql_params['pwd'],
                           user_settings.mysql_params['host'])

    table_prefix ='a'
    gal = {}
    cmd = 'select '+table_prefix+'.'+ (', '+table_prefix + '.').join(params)
    for bp in band_params:
        for band in bands:
            cmd += ", %s.%s_%s" %(table_prefix, bp, band)

    cmd += ' from %s as %s where %s.galcount >= %d and %s.galcount <= %d order by %s.galcount;' %(table_name, table_prefix, table_prefix, start_num, table_prefix, end_num, table_prefix)


    ### fetch data
    print cmd
    data  =  cursor.get_data(cmd)

    for tmp_data, name in zip(data, params+['%s_%s' %(tmp_param, band) for tmp_param in band_params for band in bands]):
        gal[name] = tmp_data


    ### group the output into directories for easier handling
    gal['dir_end'] = [ folder_fmt %a for a in ((np.array(gal['galcount'])-1)/folder_size +1)]

    return gal


if __name__=="__main__":
    gal= get_cut_data(1,10)

    print gal
