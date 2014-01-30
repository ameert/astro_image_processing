#!/sw/bin/python2.6
import os
os.system('ls 0*stamp.fits > file.list') #give filter 
f = open('sdss_r.cat', 'w') #give filter
f.writelines(['gal_id gimg wimg star\n'])
for l in open('file.list'):
 v = l.split()[0]
 wf = str(v.split('stamp')[0]) + '_r_W.fits' #give filter name
 gal_id = v.split('_stamp.fits')[0] #give filter name
 f.writelines([str(gal_id), ' ', str(v), ' ', str(wf), ' ', str(gal_id) + '_psf.fits\n']) #give filter name
f.close()
