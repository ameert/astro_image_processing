import subprocess as sub
import os
import datetime

def exec_cmd(job_str):
    print job_str
    p1=sub.Popen(job_str, shell=True, stdout = sub.PIPE)
    output = p1.communicate()[0]
    output = output.strip()
    return output

class query_class(object):
    """This class is a parent class for running sdss queries"""
    def __init__(self, gal_cat, casjobs_info):
        """Initialize the gal_cat and casjobs_info dictionaries, which hold all relevant info"""
        self.gal_cat = gal_cat
        self.casjobs_info = casjobs_info
        
        os.system('rm {data_dir}{filename}'.format(**self.gal_cat))

        self.thisdir = os.getcwd()
        self.casjobs_jar='java -jar %s ' %self.casjobs_info['cas_jar_path']

        self.write_config()

        full_jobname = "%s_%s" %(self.casjobs_info['jobname'],str(datetime.date.today()).replace('-','_'))
        self.job_info = {'full_jobname':full_jobname,
                         'table_count':0,
                         'lastnum':'-99',
                         'tablename':full_jobname,
                         'in_tablename':"in_"+full_jobname,
                         'chunknum':0,
                         'chunk':self.gal_cat['chunksize'],
                         'casjobs_jar':self.casjobs_jar
                    }
    
        return


    def prep_output_table(self):
        print 'CUT PIPE: Preparing mydb output tables'
        exec_cmd('{casjobs_jar} execute -t "MyDB" -n "drop output table" "drop table {tablename}"'.format(**self.job_info))
        exec_cmd('{casjobs_jar} -j '.format(**self.job_info))

        exec_cmd('{casjobs_jar} execute -t "MyDB" -n "create output table" "{cmd}"'.format(cmd=self.create_table_output()))
        exec_cmd('{casjobs_jar} -j '.format(**self.job_info))
        return

    def prep_input_table(self):

        print 'CUT PIPE: Preparing MyDB input tables'
        exec_cmd('{casjobs_jar} execute -t "MyDB" -n "drop input table" "drop table {in_tablename}"'.format(**self.job_info))
        exec_cmd('{casjobs_jar} -j '.format(**self.job_info))
        
        exec_cmd('{casjobs_jar} execute -t "MyDB" -n "create input table" "{cmd}";'.format(cmd=self.create_table_intput()))
        exec_cmd('{casjobs_jar} -j '.format(**self.job_info))
        return



    def prep_next_job(self):
        self.job_info['table_count']+=1
        self.job_info['jobname']='{full_jobname}_{table_count}'.format(**self.job_info)
        self.job_info['query_name']='query_{jobname}.txt'.format(**self.job_info)
        self.job_info['tablename'] = self.job_info['jobname']

        print 'CUT PIPE: Preparing MyDB input/output tables'
        exec_cmd('{casjobs_jar} execute -t "MyDB" -n "drop output table" "drop table {tablename}"'.format(**self.job_info))
        exec_cmd('{casjobs_jar} -j '.format(**self.job_info))
        print 'NOTICE:It is OK if it said error just then.'

        
        return True

    def get_job_output(self):
        self.get_filename()
        cmd = 'cat %s >> %s' %(self.filename, 
                               self.gal_cat['data_dir']+self.gal_cat['filename'])
        os.system(cmd)
        num_out, lastline = self.get_file_info()
        self.job_info['lastnum'] = lastline.split(',')[0]
        os.system('rm %s' %self.filename)
       
        if num_out<self.job_info['chunk']:
            return False #because we must be at the end of the list
        else:
            return True


    def build_query(self):
        fid = open(self.job_info['query_name'],'w')
        fid.write(self.catalog_query())
        fid.close()
        return

    def run_full_query(self):
        while True:
            self.prep_next_job()

            self.build_query()

            print 'CUT PIPE: Running Query'
            self.job_info['cmd']='{casjobs_jar} run -n "{jobname}" -f {query_name}'.format(**self.job_info)
            print self.job_info['cmd']
            exec_cmd(self.job_info['cmd'])

            print 'GALMORPH: Downloading Results'
            self.job_info['cmd']='{casjobs_jar} extract -force -type "csv" -download {jobname} -table {tablename}'.format(**self.job_info)
            print self.job_info['cmd']
            self.casjobs_out = exec_cmd(self.job_info['cmd'])
            print self.casjobs_out

            if not self.get_job_output():
                # This loop exits when prep_next_job returns false. ie there is not a next job
                break
        return

    def write_config(self):
        """writes the casjobs configuration info to the Casjobs.config file used by the jar file"""
        config_str = """wsid={wsid}
password={password}
default_target={search_target}
default_queue=1
default_days=1
verbose=true
debug=false
jobs_location={casjobs_url}
""".format(**self.casjobs_info)
    
        config_file = open('CasJobs.config','w')
        config_file.write(config_str)
        config_file.close()
        return



    def get_filename(self):
        casjobs_out = self.casjobs_out.split('Saved as: ')[1]
        self.filename = casjobs_out.split()[0]
        return 
    
    def get_file_info(self):
        """returns the last line of the file and the number of lines in the file."""
        
        infile = open(self.filename)
        lines = infile.readlines()
        infile.close()

        numlines = len(lines)
        lastline = lines[-1]

        return numlines, lastline
