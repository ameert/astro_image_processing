from datetime import date
import os
 
today = date.today()

def startfile(outfilename, inmodel, outmodel,xval, yval):
    outfile = open(outfilename, 'w')
    outfile.write("""###############################################
###############################################
# Name: {filename}
#
# Description: {description}
# 
# Creators: Alan Meert, 
#           Vinu Vikram,
#           Mariangela Bernardi
#           
#           Department of Physics and Astronomy
#           University of Pennsylvania
#
# Date Created: {date}
# 
###############################################
""".format(filename = outfilename.split('/')[-1], date = today.isoformat(), 
           description = get_description(inmodel, outmodel, xval, yval)))

    return outfile

def get_description(inmodel, outmodel, xval, yval):
    if xval == 'correlation' or yval ==  'correlation':
        des = """The correlation matrix of {inmodel} simulation
# fit with {outmodel}. Rows are bracketed together with
# opening and closing brackets around the full matrix.
# Values in row (or column) order are:
""".format(inmodel = inmodel, outmodel = outmodel)
        
        if (inmodel == 'ser') or (outmodel == 'ser'):
            if outmodel == inmodel:
                group_labels = ['m$_{tot}$','r$_{hl}$','n$_{sersic}$',
                                'sky$_{counts}$', 
                                'm$_{bulge}$','r$_{bulge}$', '(b/a)$_{bulge}$', 
                                '$\\phi_{bulge}$']
                fits_labels = ['total apparent magnitude',
                               'halflight radius (circularized) arcsec',
                               'sersic index', 'sky (background) level (in counts)',
                               'bulge apparent magnitude','bulge radius in arcsec',
                               'b/a of the bulge', 
                               'position angle of bulge in degrees']
            else:
                group_labels = ['m$_{tot}$', 'r$_{hl}$','sky']
                fits_labels = ['total apparent magnitude',
                               'halflight radius (circularized) arcsec',
                               'sky (background) level (in counts)'] 

        else:
            group_labels = ['m$_{tot}$', 'r$_{hl}$','n$_{sersic}$', 
                            'B/T', 'sky$_{counts}$', 
                            'm$_{bulge}$',  'r$_{bulge}$', '(b/a)$_{bulge}$', 
                            '$\\phi_{bulge}$',  'm$_{disk}$','r$_{disk}$',
                            '(b/a)$_{disk}$','$\\phi_{disk}$']

            fits_labels = ['total apparent magnitude ',
                           'halflight radius (circularized) arcsec',
                           'bulge sersic index', 'bulge-to-total light ratio',
                           'sky (background) level (in counts)', 
                           'bulge apparent magnitude','bulge radius in arcsec',
                           'b/a of the bulge', 
                           'position angle of bulge in degrees'
                           'disk apparent magnitude',
                           'disk scale radius in arcsec',
                           'b/a of the disk', 
                           'position angle of disk in degrees']
        des += '\n'.join([ "# %s -- %s" %(a,b) for a,b in zip(group_labels, fits_labels)])
            
            
    else:
        des = """The difference (output - input) of 
# paramter "{parameter}" of the "{outmodel}" fit of a simulated 
# "{inmodel}" galaxy vs the input "{xparam}" """.format(inmodel = inmodel, outmodel = outmodel, parameter = get_param(yval),
           xparam = get_param(xval))

    return des

def get_param(val):
    params = {'hrad': 'circularized halflight radius (arcsec)',
              'mtot': 'total apparent magnitude',
              'BT': 'bulge-to-total light ratio',
              'Id': 'disk apparent magnitude',
              'rd': 'disk scale radius (arcsec)',
              'Ie': 'bulge apparent magnitude',
              're': 'bulge halflight radius (arcsec)',
              'n': 'Sersic index of bulge or sersic component'
              }
    return params[val]

def copy_tabledata(outfile, infile):
    linestring = open(infile, 'r').read()
    outfile.write(linestring)

    return
    
infile_path = '/home/ameert/svn_stuff/letter_plot_scripts/sim_paper_plots/plots'
outfile_path = '/home/ameert/fit_catalog/output_tables/bias_tables'

params = ['mtot','hrad', 'BT','Id','rd','Ie','re','n']

for inmodel in ['Ser', 'deVExp', 'SerExp']:
    for outmodel in ['Ser', 'deVExp', 'SerExp']:
        for xp in params:
            for yp in params:
                infile = "%s/psf_%s_%s_%s_%s.tbl" %(infile_path, 
                          inmodel.lower(),outmodel.lower(), xp,yp)
                if not os.path.isfile(infile):
                    continue

                outfile = "%s/%s/%s/%s_%s_%s_%s.tbl" %(outfile_path, 
                          inmodel.lower(),outmodel.lower(),                                               inmodel.lower(),outmodel.lower(), xp,yp)
                ofile = startfile(outfile, inmodel.lower(), 
                                  outmodel.lower(),xp, yp)
                copy_tabledata(ofile, infile)

                ofile.close()
        infile = '/home/ameert/fit_catalog/scripts/%s_%s_correlation.txt' %(
            inmodel.lower(),outmodel.lower())
        outfile = "%s/%s/%s/%s_%s_correlation.tbl" %(outfile_path,
                                               inmodel.lower(),outmodel.lower(),
                                               inmodel.lower(),outmodel.lower())
        ofile = startfile(outfile, inmodel.lower(), 
                          outmodel.lower(),'correlation','correlation')
        copy_tabledata(ofile, infile)
        ofile.close()



        
