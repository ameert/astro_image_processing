

cmd_str = 'qsub -V '
exe_str = '/data2/home/ameert/serial_pipeline/trunk/pymorph.py'
basedir = '/data2/home/ameert'

models = ['dev', 'ser', 'devexp', 'serexp']
#models = ['serexp']

max_folder = 27

ofile = open(basedir + 'run_pymorph.txt', 'w')

for model in models:
    for num in range(1, max_folder +1):
        str_out = '%s -o %s/job_output/%s -e %s/job_output/%s -N %s -wd %s/sdss_sample/fits_ser_detailed/serexp/%d %s \n' %(cmd_str, basedir, 'pymorph_'+model+'_'+str(num)+'.out', basedir, 'pymorph_'+model+'_'+str(num)+'.err', model+'_'+str(num), basedir, num  , exe_str)
        ofile.write(str_out)

ofile.write("python2.5 monitor_jobs.py\n")

ofile.close()

