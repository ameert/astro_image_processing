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
            self.imhead = image[0].header

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
            
            #read in run, rerun, camcol, field, filter data for default
            # gain and dark_var
            self.run = image[3].data['run'][0]
            self.rerun = image[3].data['rerun'][0]
            self.camcol = image[3].data['camcol'][0]
            self.band = image[3].data['filter'][0]
            self.field = image[3].data['field'][0]
            
            # set the default dark_var and gain
            self.default_gain()
            self.default_dark_var()
            image.close()
        else:
            print "File '%s' not found!!!!" %self.filename
            print "File not loaded!!!"

        return

    def default_gain(self):
        """sets default gain"""
        gains = {'u':{1:1.62, 2:1.595 if self.run<1100 else 1.825, 
                      3:1.59, 4:1.6, 5:1.47, 6:2.17},
                 'g':{1:3.32, 2:3.855, 3:3.845, 4:3.995, 5:4.05, 6:4.035},
                 'r':{1:4.71, 2:4.6, 3:4.72, 4:4.76, 5:4.725, 6:4.895},
                 'i':{1:5.165, 2:4.6, 3:4.86, 4:4.885, 5:4.64, 6:4.76},
                 'z':{1:4.745, 2:5.155, 3:4.885, 4:4.775, 5:3.48, 6:4.69},
                 }
        self.gain = gains[self.band][self.camcol]
        return

    def default_dark_var(self):
        """sets default dark_var"""
        dark_var = {'u':{1:9.61, 2:12.6025, 3:8.7025, 
                         4:12.6025, 5:9.3025, 6:7.0225},
                    'g':{1:15.6025, 2:1.44, 3:1.3225, 
                         4:1.96, 5:1.1025, 6:1.8225},
                    'r':{1:1.8225, 2:1.00, 3:1.3225, 
                         4:1.3225, 5:0.81, 6:0.9025},
                    'i':{1:7.84, 2:5.76 if self.run<1500 else 6.25,
                         3:4.6225, 4:6.25 if self.run<1500 else 7.5625,
                         5:7.84, 6:5.0625},
                    'z':{1:0.81, 2:1.0, 3:1.0, 
                         4:9.61 if self.run<1500 else 12.6025,
                         5:1.8225 if self.run<1500 else 2.1025, 6:1.21},
                    }
        self.dark_var = dark_var[self.band][self.camcol]
        
        return

    def DN(self,sky=True):
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
        
    def weight_im(self, unit='NM', gain=None, dark_var=None):
        if gain!=None:
            self.gain = gain
        elif self.gain==None:
            self.default_gain()
        
        if dark_var!=None:
            self.dark_var = dark_var
        elif self.dark_var==None:
            self.default_dark_var()
        
        #poisson noise is in photo-electrons
        dn_err= np.sqrt(self.DN(sky=True)/self.gain+self.dark_var)
        
        if unit=='DN':
            self.weight=dn_err
        elif unit=='NM':
            self.weight = dn_err*self.cimg
        else:
            print "Units not recognized!\nNo weight image created"
        
        return self.weight

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
    nm  = '/home/jofis/Galaxy_Evo/frame-i-001009-4-0144.fits' 
    image = frame_img(nm)

    image.diagnostic_plot()

