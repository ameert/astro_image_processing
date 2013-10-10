#++++++++++++++++++++++++++
#
# TITLE: prep_job.py
#
# PURPOSE: contains the job_creator class 
#          used to create jobs for the cluster
#
# INPUTS: NONE
#
# OUTPUTS: NONE
#
# PROGRAM CALLS: NONE
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: FOLIO cluster
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: updated 16 OCT 2012
#
#-----------------------------------

import os
import sys

class job_creator():
    """handles job creation ... like the US Congress ...supposedly"""
    def __init__(self, incat_stem = '', outcat = '', path_stem = '',
                 pymorph_loc = '', hrad_script_loc = '',
                 mysql_table_stem = '', band = '', UN = 8.0, fit_sky = 1,
                 cas_model = 'dev', models = ['dev'], jobs_to_run = [1],
                 job_prefix = ''):
        self.incat_stem = incat_stem
        self.outcat = outcat
        self.path_stem = path_stem
        self.pymorph_loc =pymorph_loc
        self.hrad_script_loc = hrad_script_loc
        self.mysql_table_stem = mysql_table_stem
        self.band = band
        self.UN = UN
        self.fit_sky = fit_sky
        self.cas_model = cas_model
        self.models = models
        self.jobs_to_run= jobs_to_run
        self.job_prefix = job_prefix
        return

    
    def fill_job_dict(self, running_jobs, completed_jobs):
        """populate the dictionary of jobs that we want to run"""
        jobs = {}
        name_dict = {'dev':'d', 'ser':'s', 'devexp':'de', 'serexp':'se'}
        for job_count in self.jobs_to_run:
            for model in self.models:
                job_name = "%s%s%04d" %(self.job_prefix, name_dict[model],
                                        job_count)
                if job_name not in running_jobs.keys() and \
                       job_name not in completed_jobs.keys():

                    jobs[job_name] = self.make_job_dict(job_name, job_count,  
                                                        model)
                    job_maker.make_config(jobs[job_name])

        print jobs.keys()
        return jobs
    
    def make_job_dict(self, job_name, count, model):
        """makes the job dictionary used by the scheduler for a single job"""
        a = {}
        a['incat'] = '%s_%s_%04d.cat' %(self.incat_stem,self.band,count)
        a['outcat'] = self.outcat
        a['data_loc'] = '%s/%s/data/%04d/' %(self.path_stem,self.band, count)
        a['job_loc'] = '%s/%s/job_output' %(self.path_stem,self.band)
        a['out_loc'] = '%s/%s/fits/%s/%04d' %(self.path_stem,self.band, model, count)
        a['qsub'] = self.make_job_pymorph(job_name, a) 
        a['tablename'] = '%s_%s_%s' %(self.mysql_table_stem,self.band,model)
        a['model'] = model
        a['count'] = count
        a['band'] = self.band
        a['hrad_qsub'] = self.make_job_hrad(job_name, a)
        a['timestamp'] = ''
        a['istransferred'] = 0
        return a
        
    
    def make_job_pymorph(self, job_name, job_dict):
        """construct job names"""
        job = self.make_job(job_name, job_dict['out_loc'],job_dict['job_loc'], self.pymorph_loc)
        job = job.replace('NAME_BLANK', job_name)
        return job

    def make_job_hrad(self, job_name, job_dict):
        job = self.make_job(job_name, job_dict['out_loc'],job_dict['job_loc'], self.hrad_script_loc, hold = 0)
        job = job.replace('NAME_BLANK', 'hrad')
        # now add additional arguments
        job += ' %s %s %d ' %(job_dict['tablename'], job_dict['model'], job_dict['count'])
        return job
    
    def make_job(self,job_name, outdir, jobdir, script_name, hold = 1):
        job = "qsub -V -h -l h_vmem=2G -o %s/%s.out -e %s/%s.err -N NAME_BLANK -wd %s %s" %(jobdir, job_name, jobdir, job_name, outdir, script_name)

        if hold == 0:
            job = job.replace('-h', '')
    
        return job
    
    def make_config(self, job_dict):
        """generates the output directory and builds the configuration file there"""
        if not os.path.isdir(job_dict['out_loc']):
            os.mkdir(job_dict['out_loc'])
        if not os.path.isdir(job_dict['data_loc']):
            os.mkdir(job_dict['data_loc'])
              
        config_dict = {'clus_cata': "'%s'" %job_dict['incat'],
                       'datadir':"'%s'" %job_dict['data_loc'],
                       'rootname':"'%s'" %self.band,
                       'outdir':"'%s'" %job_dict['out_loc'],
                       'LN':'0.1', 'UN':self.UN,
                       'fitting':'[1, 1, %d]' %self.fit_sky,
                       'host':"'shredder'",'database':"'pymorph'",
                       'table':"'%s'" %job_dict['tablename'], 'usr':"'pymorph'",
                       'pword':"'pymorph9455'",
                       'dbparams':"['Morphology:%s', 'ObsID:1:int']" %job_dict['model']
                       }

        if job_dict['model'] == self.cas_model:
            config_dict['cas']='True'
        else:
            config_dict['cas']='False'

        if job_dict['model'] in ['dev', 'devexp']:
            config_dict['devauc']='True'
        else:
            config_dict['devauc']='False'

        if job_dict['model'] in ['serexp', 'devexp']:
            config_dict['components']="['bulge', 'disk']"
        else:
            config_dict['components']="['bulge']"
        
        self.complete_job_config_dict(config_dict)

        self.write_config('%s/config.py' %(job_dict['out_loc']), config_dict)

        return

    def complete_job_config_dict(self,config_dict):
        """makes a dictionary that is used to generate the configuration file for PyMorph"""
        default_cat = {'imagefile':"'j8f643-1-1_drz_sci.fits'",
                       'whtfile':"'j8f643-1-1_drz_rms.fits'",  
                       'sex_cata':"'sdss_sex.cat'",
                       'clus_cata':"'input.cat'",'datadir':"'./'",
                       'out_cata':"'sdss_r_out.cat'",'rootname':"'r'",  
                       'outdir':"'./'",'psfselect':'0',                         
                       'starsize':'20','psflist':"'@psflist.list'",
                       'mag_zero':'25.256','manual_mask':'0',
                       'mask_reg':'2.0','thresh_area':'0.2',
                       'threshold':'3.0','size':'[0, 1, 9, 1, 120]',              
                       'searchrad':"'0.3arc'",'pixelscale':'0.396',       
                       'H0':'71.0','WM':'0.27','WV':'0.73',                   
                       'back_extraction_radius':'15.0','angle':'180.0',
                       'repeat':'False','galcut':'True',                        
                       'decompose':'True','detail':'False',
                       'galfit':'True', 'cas':'False',
                       'findandfit':'0','maglim':'[22, 15]', 
                       'stargal':'0.8',  'crashhandler':'0',
                       'components':"['bulge']",'devauc':'True',
                       'LN':'0.1', 'UN':'8.0',
                       'fitting':'[1, 1, 1]',
                       'GALFIT_PATH':"'/data2/home/ameert/galfit/galfit'",
                       'SEX_PATH':"'/data2/home/ameert/sextractor-2.5.0/sex/bin/sex'",
                       'PYMORPH_PATH':"'/data2/home/ameert/new_pymorph/serial_pipeline/trunk/pymorph/'",
                       'galfitv':"'2.0'",'chi2sq':'2.5',
                       'Goodness':'0.60', 'center_deviation':'3.0',                
                       'center_constrain':'2.0',              
                       'host':"'shredder'",'database':"'pymorph'",
                       'table':"'test'",'usr':"'pymorph'",
                       'pword':"'pymorph9455'",'dbparams':'[]'
                       }

        for key in default_cat:
            if key not in config_dict:
                config_dict[key] = default_cat[key]


        return config_dict


    def write_config(self, filename, config_dict):
        """uses the configuration dictionary to write a config file for PyMorph"""
        f = open(filename, 'w')
        f.write('###----Specify the input images and Catalogues----###\n')
        self.write_keywords(f, config_dict, ['imagefile','whtfile','sex_cata','clus_cata','datadir'])

        f.write('###----Specify the output names of images and catalogues----###\n')
        self.write_keywords(f, config_dict, ['out_cata','rootname','outdir'])

        f.write('###----Psf list----###\n')
        self.write_keywords(f,config_dict,['psfselect','starsize','psflist','mag_zero'])

        f.write('###----Conditions for Masking----###\n')
        self.write_keywords(f,config_dict,['manual_mask','mask_reg','thresh_area','threshold'])

        f.write('###---Size of the cut out and search conditions---###\n')
        f.write('###---size = [resize?, varsize?, fracrad, square?, fixsize]---###\n')
        self.write_keywords(f,config_dict,['size','searchrad'])  

        f.write('###----Parameters for calculating the physical parameters of galaxy----###\n')
        self.write_keywords(f,config_dict,['pixelscale', 'H0','WM','WV'])

        f.write('###----Parameters to be set for calculating the CASGM----###\n')
        self.write_keywords(f,config_dict, ['back_extraction_radius','angle'])

        f.write('###----Fitting modes----###\n')
        self.write_keywords(f,config_dict,['repeat','galcut','decompose','detail',
                                      'galfit','cas','findandfit','maglim',
                                      'stargal','crashhandler'])

        f.write('###---Galfit Controls---###\n')
        self.write_keywords(f,config_dict,['components','devauc', 'LN','UN'])

        f.write('###---fixing = [bulge_center, disk_center, sky]\n')
        self.write_keywords(f,config_dict,['fitting'])

        f.write('###----Set the SExtractor and GALFIT path here----###\n')
        self.write_keywords(f,config_dict,['GALFIT_PATH','SEX_PATH','PYMORPH_PATH','galfitv'])

        f.write('###----The following conditions are used to classify fit goo/bad----###\n')
        self.write_keywords(f,config_dict,['chi2sq','Goodness','center_deviation','center_constrain'])

        f.write('###----Database Informations----###\n')
        self.write_keywords(f,config_dict,['host','database','table','usr','pword','dbparams'])

        f.close()

        return

    def write_keywords(self, outfile, config_dict, keywords):
        """used by write_config to write groups of keywords"""
        for keyword in keywords:
            if keyword in config_dict.keys():
                outfile.write('%s = %s\n' %(keyword, config_dict[keyword]))
        return

