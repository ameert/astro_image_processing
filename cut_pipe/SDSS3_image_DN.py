import numpy as np
import pyfits as pf
import os
from scipy import interpolate

class frame_img():
    """class for opening and converting sdss3 images to counts"""
    def __init__(self, filename=None):
        self.filename=filename
        if self.filename is not None:
            self.load_img()
        return

    def load_img(self):
        """loads sky-subtracted image, calibration image, and sky image 
all in nanomaggies"""
        if os.path.isfile(self.filename):
            image = pf.open(self.filename)

            #read in the FITS image from HDU0; the resulting image will be
            #sky-subtracted as well as calibrated in nanomaggies/pixel
            self.data_nosky = image[0].data

            #read in sky, and interpolate to full image size; this returns a
            #sky image the same size as the frame image, in units of counts
            allsky, xinterp, yinterp = image[2].data[0]
            x = np.arange(allsky.shape[0])
            y = np.arange(allsky.shape[1])
            f = interpolate.interp2d(y,x, allsky, kind='linear')

            simg = f(yinterp,xinterp).T

            #read in calibration, and expand to full image size; this returns
            #a calibration image the same size as the frame image, in units of
            # nanomaggies per count
            calib= image[1].data
            self.cimg= calib*np.ones(self.data_nosky.shape)

            self.simg = simg*self.cimg
        else:
            print "File '%s' not found!!!!" %self.filename
            print "File not loaded!!!"

        return

    def DN(self,sky=False):
        """returns an image in DN following the prescription at
http://data.sdss3.org/datamodel/files/BOSS_PHOTOOBJ/frames/RERUN/RUN/CAMCOL/frame.html with or without sky based on the setting of the sky keyword""" 
        if sky:
            return (self.data_nosky+self.simg)/self.cimg
        else:
            return self.data_nosky/self.cimg

    def NM(self, sky=False):
        """returns an image in nanomaggies with or without sky based on the setting of the sky keyword""" 
        if sky:
            return self.data_nosky+self.simg
        else:
            return self.data_nosky
        
    def diagnostic_plot(self):
        import matplotlib.pyplot as plt
        plt.subplot(2,2,1)
        plt.imshow(self.simg, interpolation='none')
        plt.colorbar()
        plt.title('sky image in nanomaggies', fontsize=8)

        plt.subplot(2,2,2)
        plt.imshow(self.cimg, interpolation='none')
        plt.colorbar()
        plt.title('calibration image in  nanomaggies/count', fontsize=8)

        plt.subplot(2,2,3)
        plt.imshow(np.log10(self.data_nosky), interpolation='none')
        plt.colorbar()
        plt.title('sky-subtracted image in log10(nmgy)', fontsize=8)

        plt.subplot(2,2,4)
        plt.imshow(np.log10(self.NM(sky=True)), interpolation='none')
        plt.colorbar()
        plt.title('full image in log10(nmgy)', fontsize=8)
        plt.show()
        return 

if __name__ == "__main__":
    nm  = '/home/ameert/Desktop/frame-i-001009-4-0144.fits' 
    image = frame_img(nm)

    image.diagnostic_plot()

