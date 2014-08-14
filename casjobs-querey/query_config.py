from astro_image_processing.user_settings import casjobs_info

gal_cat = {'filename':'spectro_sample_raw.cat',
           'data_dir':'/home/ameert/new_cut_pipe/',
           'out_file':'spectro_sample.cat'
           }

casjobs_info.update({ 'cas_jar_path':'casjobs.jar',
                 'jobname':'test_name',
                 'search_target':'DR8'})
