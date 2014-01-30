

cmd_str = 'qsub -V '
exe_str = '/data2/home/ameert/serial_pipeline/trunk/pymorph.py /data2/home/ameert/sdss_sample/fits'
basedir = '/data2/home/ameert'

models = ['dev', 'ser', 'devexp', 'serexp']
#models = ['serexp']

max_folder = 27

ofile = open('run_pymorph.txt', 'w')

for model in models:
    for num in range(1, max_folder +1):
        str_out = '%s -o %s/job_output/%s -e %s/job_output/%s -N %s %s/%s/%d/ \n' %(cmd_str, basedir, 'pymorph_'+model+'_'+str(num)+'.out', basedir, 'pymorph_'+model+'_'+str(num)+'.err', model+'_'+str(num), exe_str, model, num)  
        ofile.write(str_out)


ofile.write("python2.5 monitor_jobs.py\n")

ofile.close()

