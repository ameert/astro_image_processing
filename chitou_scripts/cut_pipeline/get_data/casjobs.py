#++++++++++++++++++++++++++
#
# TITLE: casjobs
#
# PURPOSE: queries casjobs for a list of
#          objects using either ra/dec or
#          objID. I hope to add functionality
#          for UKIDDS
#
# INPUTS: gal_cat :  a dictionary containing the keys: 'filename'
#                    names the file that downloaded data will
#                    be saved in and either 'ra'/'dec'
#                    or 'sdssobjid' used for the search
#         data_dir:  the directory where all data will be stored
#         username:  string! username used for making queries
#         wsid:      string! id number used by casjobs
#         password:  string! the password for casjobs
#         search_82: set to 1 if searching 
# OUTPUTS: NONE, but does create the data file
#          named by 'filename'
#
# PROGRAM CALLS: make_query (this is imported)
#                also uses the 'os' module and
#                'datetime' module
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 5 JAN 2011
#
# NOTES: For now, casjobs program must be in the directory
#        that you are executing the python code from. I intend
#        to change this.
#
#-----------------------------------

import os
import datetime

def casjobs(gal_cat, data_dir, username = 'upenn_pymorph', wsid = '396840617', password='pymorph_upenn', search_82 = 0, telescope = 'sdss'):
    """PURPOSE: queries casjobs for a list of
                objects using either ra/dec or
                objID. I hope to add functionality
                for galex and UKIDDS

    INPUTS: gal_cat :  a dictionary containing the keys: 'filename'
                       names the file that downloaded data will
                       be saved in and either 'ra'/'dec'
                       or 'sdssobjid' used for the search
            data_dir:  the directory where all data will be stored
            username:  string! username used for making queries
            wsid:      string! id number used by casjobs
            password:  string! the password for casjobs
            search_82: set to 1 if searching stripe 82 coadd
            
    OUTPUTS: NONE, but does create the data file
             named by 'filename'

    PROGRAM CALLS: make_query (this is imported with the module)
                   also uses the 'os' module and
                   'datetime' module"""

    if telescope not in ['sdss','galex']:
        print 'Error in casjobs.py:'
        print '-------------------------------------------------'
        print 'You selected a telescope that is not currently supported!!!'
        print 'Please choose an acceptable telescope'
        print '-------------------------------------------------'
        return 1
    
    if gal_cat.has_key('ra') and gal_cat.has_key('dec'):
        # Search is performed using ra/dec
        ra = gal_cat['ra']
        dec = gal_cat['dec']
        do_pos = 1
        gal_num = len(ra)
        # checks to make sure that every galaxy has both an ra and dec component
        # if it doesn't then it kills the program
        if len(ra) != len(dec):
            print 'Error in casjobs.py:'
            print '-------------------------------------------------'
            print 'Every entry DOES NOT have an ra and dec component'
            print 'Please examine your catalog!!!!'
            print 'Terminating program!!!!!'
            print '-------------------------------------------------'
            return 1
    elif gal_cat.has_key('sdssobjid'):
        if telescope == 'galex':
            print 'Error in casjobs.py:'
            print '-------------------------------------------------'
            print 'Casjobs cannot use sdss objid in Galex!'
            print 'Please examine your catalog!!!!'
            print 'Terminating program!!!!!'
            print '-------------------------------------------------'
            return 1
        # Search is performed using sdss objid
        sdssobjid = gal_cat['sdssobjid']
        do_pos = 0 # tells make query to use 
        gal_num = len(sdssobjid)
    
    else:
        # this kills program if neither ra/dec or sdssobjid were found
        print 'Error in casjobs.py:'
        print '--------------------------------------------------'
        print 'You must have either sdssobjid or ra/dec to execute'
        print 'an object search!!!'
        print 'Exiting casjobs search!!!!!!!!!!!!'
        print '--------------------------------------------------'
        return 1

    thisdir = os.getcwd()
    # Uses the version of casjobs installed with galmorph for now.
    os.chdir(casjobs_path)
    casjobs='java -jar casjobs.jar '

    # write config file used by casjobs
    config_file = open('CasJobs.config','w')
    if telescope == 'sdss':      
        if search_82:
            config_file.write('wsid=' + wsid + '\n' +
                              'password=' + password + '\n' +
                              'default_target=Stripe82\n' +
                              'default_queue=1\n' +
                              'default_days=1\n' +
                              'verbose=true\n' +
                              'debug=false\n' +
                              'jobs_location=http://casjobs.sdss.org/casjobs/services/jobs.asmx\n')
        else:    
            config_file.write('wsid=' + wsid + '\n' +
                              'password=' + password + '\n' +
                              'default_target=DR7\n' +
                              'default_queue=1\n' +
                              'default_days=1\n' +
                              'verbose=true\n' +
                              'debug=false\n' +
                              'jobs_location=http://casjobs.sdss.org/casjobs/services/jobs.asmx\n')
    elif telescope == 'galex':
        config_file.write('wsid=' + wsid +'\n' +
                          'password=' + password + '\n' +
                          'default_target=GALEXGR4Plus5\n'+
                          'default_queue=1\n'+
                          'default_days=1\n'+
                          'verbose=true\n'+
                          'debug=false\n'+
                          'jobs_location=http://galex.stsci.edu/casjobs/services/jobs.asmx\n')

    config_file.close()

    # name that will appear in the users casjobs query list. This is the current date
    jn = datetime.date.today()

    print 'GALMORPH: Preparing mydb input/output tables'
    os.system(casjobs + 'execute -t "mydb" -n "drop output table" "drop table cl_out"')
    print 'GALMORPH: It is ok if it said error just then. -JBH'

    os.system(casjobs +'execute -t "mydb" -n "drop input table" "drop table cl_in"')
    print 'GALMORPH: It is ok if it said error just then. -JBH'

    if do_pos:
        os.system(casjobs + 'execute -t "mydb" -n "create input table" "create table cl_in (ra float, dec float, myind int)"')
    else:
        os.system(casjobs + 'execute -t "mydb" -n "create input table" "create table cl_in (sdssobjid bigint, myind int)"')

    print 'GALMORPH: Importing data into casjobs'

    count = 0;
    chunklen = 50;
    while (chunklen*count <= gal_num):
        sqlstr = 'execute -t "mydb" "'
        for i in range(chunklen*count, min(gal_num,(chunklen*(count+1)))):      
            if do_pos:
                sqlstr += 'insert into cl_in (ra, dec, myind) values (%f,%f,%i) ' %(ra[i],dec[i],i+1)
            else:
                sqlstr += 'insert into cl_in (sdssobjid, myind) values (%s,%i) ' %(sdssobjid[i],i+1)
        sqlstr += '"'
        os.system(casjobs + sqlstr)
        count= count + 1

    print 'GALMORPH: Done Importing data into casjobs'

    fid = open('query.txt', 'w')
    if telescope == 'sdss':
        fid.write(make_query_sdss(do_ra_dec = do_pos, stripe_82 = search_82))
    elif telescope == 'galex':
        fid.write(make_query_galex())
    else:
        print 'currently this program does not support other telescopes'
    fid.close()

    
    print 'GALMORPH: Running Query'
    str = 'run -n "%s" -f query.txt' %(jn)
    os.system(casjobs + str)
    print 'GALMORPH: Downloading Results'
    str = 'extract -force -type "csv" -download %s -table cl_out' %(jn)
    print casjobs + str 
    os.system(casjobs + str)
    str = 'mv %scl_out*.csv %s' %(jn,data_dir + gal_cat['filename'])
    os.system(str)
    # os.system('rm CasJobs.config')
    # os.system('rm query.txt')
    os.chdir(thisdir)
    return 0
