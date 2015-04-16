from mysql_class import *
import numpy as np
import os
import pickle

band = 'r'
pymorph_loc = '/data2/home/ameert/new_pymorph/serial_pipeline/trunk/pymorph.py'
model = 'serexp'
path_stem ='/data2/home/ameert/catalog/'
jobs_to_run = range(1,801)


np.set_printoptions(threshold='nan')
name_dict = {'dev':'d', 'ser':'s', 'devexp':'de', 'serexp':'se'}

cursor = mysql_connect('pymorph', 'pymorph', 'pymorph9455', 'shredder')


counts, hrad = cursor.get_data('select galcount, alan_hrad_pix from full_dr7_r_%s where alan_hrad_pix < 0 order by galcount;' %model)

counts = np.array(counts)/250 +1
groups = {}

bad_keys = list(set(counts))

for a in bad_keys:
    name = '%s%04d' %(name_dict[model],a) 
    groups[name] =  len(np.extract(counts == a, counts))
    
print groups

def un_pickle_data(filename):
    a = open(filename)
    data = pickle.load(a)
    a.close()
    return data

# construct job names
def make_job(job_name, outdir, jobdir, pymorph_loc, hrad = 0):
    job = "qsub -V -h -l h_vmem=1G -o %s/%s.out -e %s/%s.err -N NAME_BLANK -wd %s " %(jobdir, job_name, jobdir, job_name, outdir)

    if hrad:
        job = job.replace('-h', '')
        job = job.replace('NAME_BLANK', 'hrad')
        job += " /data2/home/ameert/catalog/scripts/measure_and_clean.py "        
    else:
        job = job.replace('NAME_BLANK', job_name)
        job += " %s\n"  %pymorph_loc
    
    return job

# construct job info dictionary
def make_job_dict(job_name, count, model, band, pymorph_loc):
    a = {}
    a['incat'] = 'sdss_%s_%d.cat' %(band, count)
    a['outcat'] = 'result.csv'
    a['data_loc'] = '%s/%s/data/%04d/' %(path_stem,band, count)
    a['job_loc'] = '%s/%s/job_output' %(path_stem,band)
    a['out_loc'] = '%s/%s/fits/%s/%04d' %(path_stem,band, model, count)
    a['qsub'] = make_job(job_name, a['out_loc'],a['job_loc'], pymorph_loc) 
    a['tablename'] = 'full_dr7_%s_%s' %(band, model)
    a['model'] = model
    a['count'] = count
    a['band'] = band
    a['hrad_qsub'] = make_job(job_name, a['out_loc'],a['job_loc'], pymorph_loc, hrad=1) + a['tablename']
    a['timestamp'] = ''
    a['istransferred'] = 0
    return a

completed_jobs = {}

for job_count in jobs_to_run:
    job_name = '%s%04d' %(name_dict[model],job_count) 
    completed_jobs[job_name] = make_job_dict(job_name, job_count,  model, band, pymorph_loc)

for key in groups.keys():
    os.system(completed_jobs[key]['hrad_qsub'])
    if groups[key] > 10:
        print groups[key]
        print completed_jobs[key]['hrad_qsub']

print len(groups.keys())

