from mysql.mysql_class import *
import pyfits as pf

cursor = mysql_connect('catalog','pymorph','pymorph')

infile = pf.open('./zoo2MainSpecz.fits')
data = infile[1].data
infile.close()

cols=['deVPhi_u','deVPhi_g','deVPhi_r','deVPhi_i','deVPhi_z','expPhi_u',
      'expPhi_g','expPhi_r','expPhi_i','expPhi_z','expab_u','expab_g',
      'expab_r','expab_i','expab_z',
      'exprad_u','exprad_g','exprad_r','exprad_i','exprad_z',
      'expmag_u','expmag_g','expmag_r','expmag_i','expmag_z']

incols = ['dr7objid','ra','dec','specobjid','gz2class',
't01_smooth_or_features_a01_smooth_flag',
't01_smooth_or_features_a02_features_or_disk_flag',
't02_edgeon_a04_yes_flag','t02_edgeon_a05_no_flag','t03_bar_a06_bar_flag',
't03_bar_a07_no_bar_flag','t05_bulge_prominence_a10_no_bulge_flag',
't05_bulge_prominence_a11_just_noticeable_flag',
't05_bulge_prominence_a12_obvious_flag',
't05_bulge_prominence_a13_dominant_flag',
't07_rounded_a16_completely_round_flag', 
't07_rounded_a17_in_between_flag','t07_rounded_a18_cigar_shaped_flag',
 't08_odd_feature_a19_ring_flag','t08_odd_feature_a21_disturbed_flag',
't08_odd_feature_a22_irregular_flag','t08_odd_feature_a24_merger_flag',
't08_odd_feature_a38_dust_lane_flag','t09_bulge_shape_a25_rounded_flag',
't09_bulge_shape_a26_boxy_flag' ,'t09_bulge_shape_a27_no_bulge_flag']

cols = ['objid','ra_gal','dec_gal','specobjid','gz2class',
't01_smooth','t01_features_disk','t02_edgeon_yes','t02_edgeon_no','t03_bar','t03_no_bar','t05_no_bulge','t05_just_noticeable','t05_obvious','t05_dominant','t07_completely_round_E', 't07_in_between_E','t07_cigar_shaped_E','t08_ring','t08_disturbed','t08_irregular','t08_merger','t08_dust_lane','t09_bulge_rounded','t09_bulge_boxy' ,'t09_no_bulge']

cmd = "insert ignore into gz2_flags (%s) values ({vals});" %','.join(cols)
for row in data[6430:]:
    rowdata = [str(row[a]) for a in incols]
    rowdata[4] = "'%s'" %rowdata[4].replace('-9999', 'NULL')
    rowstr = ','.join(rowdata)
    cursor.execute(cmd.format(vals=rowstr))

    


