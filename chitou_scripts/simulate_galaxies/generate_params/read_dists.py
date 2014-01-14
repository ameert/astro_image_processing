#++++++++++++++++++++++++++
#
# TITLE: read_dists 
#
# PURPOSE: reads the cdf distributions
#          for observed magnitude, BT ratio,
#          rad bulge and disk in kpc, bulge
#          ellipticity, bulge sersic index,
#          redshift, zeropoint, kk and airmass
#          sdss parameters. Parameters are randomly
#          selected from this distribtuion.
#
# INPUTS: dist_path: path to the cdf profiles
#         dist_stem: the file stem for the distributions
#
# OUTPUTS: returns mag_dist, bt_dist, re_dist, rd_dist,
#          eb_dist, n_bulge_dist, z_dist, zp_dist, kk_dist,
#          airmass_dist. each of these is a list of arrays of the
#          parameter value and the corresponding cdf value.
#
# PROGRAM CALLS: relies only upon included and standard packages
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 20 FEB 2011
#
# NOTES:Files to be read MUST be of form below
#       1st line(headers): parameter name,cdf
#       2nd line and after: number,number
#      
#-----------------------------------

import numpy as n

def read_dists(dist_path, dist_stem):
    """ call method:
    mag_dist, bt_dist, re_dist, rd_dist, eb_dist, n_bulge_dist, z_dist, zp_dist, kk_dist, airmass_dist = read_dists(dist_path, dist_stem)

    INPUTS: dist_path: path to the cdf profiles
            dist_stem: the file stem for the distributions

    OUTPUTS: returns mag_dist, bt_dist, re_dist, rd_dist,
             eb_dist, n_bulge_dist, z_dist, zp_dist, kk_dist,
             airmass_dist. each of these is a list of arrays of the
             parameter value and the corresponding cdf value."""

    
    param_names = ['tot_mag_obs', 'BT', 're_kpc', 'rd_kpc', 'eb', 'n_bulge', 'z', 'zp', 'kk', 'airmass']

    vars = []

    for param_name in param_names:
        var_hold = []
        cdf_hold = []
        infile = open(dist_path + dist_stem + param_name+'.txt')
        infile.readline()
        for line in infile.readlines():
            line = line.strip()
            split_line = line.split(',')
            var_hold.append(float(split_line[0]))
            cdf_hold.append(float(split_line[1]))
        infile.close()
        var_hold = n.array(var_hold)
        cdf_hold = n.array(cdf_hold)
        vars.append([var_hold, cdf_hold])

    mag_dist =vars[0]
    bt_dist=vars[1]
    re_dist=vars[2]
    rd_dist=vars[3]
    eb_dist=vars[4]
    z_dist=vars[5]
    zp_dist=vars[6]
    kk_dist=vars[7]
    airmass_dist=vars[8]
    n_bulge_dist = vars[9]
    
    return mag_dist, bt_dist, re_dist, rd_dist, eb_dist, n_bulge_dist, z_dist, zp_dist, kk_dist, airmass_dist
