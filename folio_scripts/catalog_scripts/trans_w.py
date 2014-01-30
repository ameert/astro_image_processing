import os

for count in range(1, 2684):
    print 'scp ameert@chitou.physics.upenn.edu:/media/SDSS2/fit_catalog/data/r/%04d/*_W.fits /data2/home/ameert/catalog/r/data/%04d/' %(count, count)
    os.system('scp ameert@chitou.physics.upenn.edu:/media/SDSS2/fit_catalog/data/r/%04d/*_W.fits /data2/home/ameert/catalog/r/data/%04d/' %(count, count))
