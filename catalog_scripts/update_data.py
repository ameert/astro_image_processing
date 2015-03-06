import os

for count in range(1300, 1700): #2684
    os.system('ls /data2/home/ameert/catalog/r/data/%04d/* > file.list' %count)
    infile = open('file.list')
    lines = len(infile.read())
    infile.close()

    if lines > 5:
        os.system('scp ameert@chitou.physics.upenn.edu:/media/SDSS2/fit_catalog/data/r/%04d/sdss_r_%d.cat /data2/home/ameert/catalog/r/data/%04d/' %(count, count, count))
        print 'scp ameert@chitou.physics.upenn.edu:/media/SDSS2/fit_catalog/data/r/%04d/sdss_r_%d.cat /data2/home/ameert/catalog/r/data/%04d/' %(count, count, count)
    else:
        os.system('scp ameert@chitou.physics.upenn.edu:/media/SDSS2/fit_catalog/data/r/%04d/* /data2/home/ameert/catalog/r/data/%04d/' %(count, count))
    
