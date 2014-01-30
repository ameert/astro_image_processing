#!/data2/home/ameert/python/bin/python2.5
import os
a = 'E*fits E*txt G_* I*fits *.pl *.con M_* O*fits O*txt P*png R*html error.log  index.html galfit.* W*fits fit2.log fit.log Tmp* SO* agm_r* restart* BMask.fits MaskedGalaxy.fits MRotated.fits CRASH.CAT restart.cat B.fits GalEllFit.fits AResidual.fits ellip err BackMask.fits'
#a = 'E*fits G_* I*fits *.pl *.con M_* O*fits error.log galfit.* W*fits fit2.log fit.log Tmp* SO* agm_r* restart* BMask.fits MaskedGalaxy.fits MRotated.fits CRASH.CAT restart.cat B.fits GalEllFit.fits AResidual.fits ellip err BackMask.fits'

v = a.split()
for v1 in v:
 try:
  os.system('rm -f ' + str(v1))
 except:
  pass

