ofile = open('hrad_job', 'w')

for count in range(1,270):
    ofile.write('qsub -V -h -o /data2/home/ameert/catalog/short_sample/r/job_output/de_%04d.out -e /data2/home/ameert/catalog/short_sample/r/job_output/de_%04d.err -N hde%d -wd /data2/home/ameert/catalog/short_sample/r/fits/devexp/%04d /data2/home/ameert/catalog/short_sample/scripts/measure_and_clean2.py full_dr7_r_devexp \n' %(count,count,count,count))


ofile.close()





               
