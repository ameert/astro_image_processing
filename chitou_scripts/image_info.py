#++++++++++++++++++++++++++
#
# TITLE: image_info.py 
#
# PURPOSE: creates a class for calculation
#          of image moments and imae info
#
# INPUTS: image and mask used in calculation
#
# OUTPUTS: object holding image info
#
# PROGRAM CALLS: uses numpy 
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Mariangela Bernardi
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 23 March 2011
#
#-----------------------------------

import numpy as np
import pyfits

class image_info:
    """class used to calculate image info like ellipticity and radius
    must pass an image and binary mask (1 for valid pixel 0 for bad pixel"""

    def __init__(self, image, mask = "NULL", x_ctr = "NULL", y_ctr = "NULL",
                 ell = "NULL", pa = "NULL", zoom = 1):
        self.image = image
        if mask == "NULL":
            self.mask = np.ones_like(self.image)
        elif mask == "threshold":
            self.mask = self.make_mask()
        else:
            self.mask = mask

        #if zoom:
        #    zoom_data = image[x_ctr-5:x_ctr+5,y_ctr-5:y_ctr+5]
        #    zoom_mask = mask[x_ctr-5:x_ctr+5,y_ctr-5:y_ctr+5]
        #    mask[x_ctr-5:x_ctr+5,y_ctr-5:y_ctr+5] = 0
            
            #zyedges = np.arange(x_ctr-5:x_ctr+5)
            #zxedges = np.arange(np.shape(self.image)[1])
            #zxpos, zypos = np.meshgrid(xedges,yedges)
            
        yedges = np.arange(np.shape(self.image)[0])
        xedges = np.arange(np.shape(self.image)[1])
    
        self.xpos, self.ypos = np.meshgrid(xedges,yedges)

        self.x_flat = self.xpos.flatten()
        self.y_flat = self.ypos.flatten()
        self.mask_flat = self.mask.flatten()
        self.image_flat = self.image.flatten()

        self.sum_image = np.sum(self.mask_flat * self.image_flat)

        if x_ctr is "NULL":
            self.x_ctr = self.image_moment(1, 0)/self.sum_image
        else:
            self.x_ctr = x_ctr
            
        if y_ctr is "NULL":
            self.y_ctr = self.image_moment(0, 1)/self.sum_image
        else:
            self.y_ctr = y_ctr

        #edgemin = 1.0
        #edgestep = 1.5
        #edgenum  = (edgemax-edgemin)/edgestep;

        edgemin = 0.0
        edgemax = np.max(self.image.shape)
        edgestep = 2.0

        self.edges = np.arange(edgemin, edgemax, edgestep)

        if ell =="NULL" and pa =="NULL":
            self.imstats()
        else:
            self.ba = ell
            self.pa = pa

        cosa = np.cos(self.pa)
        sina = np.sin(self.pa)
        
        self.good_image = np.extract(self.mask_flat, self.image_flat)
        self.good_x = np.extract(self.mask_flat, self.x_flat)
        self.good_y = np.extract(self.mask_flat, self.y_flat)

        x_pix = cosa*(self.good_x-self.x_ctr) + (self.good_y-self.y_ctr)*sina
        y_pix = -sina*(self.good_x-self.x_ctr) + (self.good_y-self.y_ctr)*cosa
        
        self.rad_pix = np.sqrt(self.ba*(x_pix**2.0) + (y_pix**2)/self.ba)
        
        return

    def image_moment(self, x_mom, y_mom, x_ctr = 0.0, y_ctr = 0.0):

        m = (((self.x_flat - x_ctr)**x_mom)*((self.y_flat - y_ctr)**y_mom)*
             self.image_flat * self.mask_flat)

        return np.sum(m)

    def cov_mat(self):
        a = np.zeros((2,2))
        a[0][0] = self.image_moment(2,0,self.x_ctr, self.y_ctr)/self.sum_image
        a[1][1] = self.image_moment(0,2,self.x_ctr, self.y_ctr)/self.sum_image
        a[1][0] = self.image_moment(1,1,self.x_ctr, self.y_ctr)/self.sum_image
        a[0][1] = a[1][0]

        return a

    def calc_eigen(self, cov):
        lead_part = (cov[0][0] + cov[1][1])/2.0
        second_part = np.sqrt(4.0*cov[0][1]*cov[1][0]+(cov[0][0]-cov[1][1])**2.0)/2.0
        return lead_part + second_part, lead_part - second_part
    
    def imstats(self):
        cov = self.cov_mat()
        eigen_vals = self.calc_eigen(cov)

        ba = abs(eigen_vals[1]/eigen_vals[0])
        if ba > 1:
            ba = 1.0/ba
        
        self.ba = np.sqrt(ba) #as in b/a or ellipticity
        self.pa = ((0.5)*np.arctan2(2*cov[0][1],(cov[0][0]-cov[1][1]))) %  np.pi

        return
    

    def profile(self, outfile='NULL'):
                
        good_image = self.good_image        
        rad_pix = self.rad_pix
        
        self.rads, self.prof, self.proferr, self.aperflux, self.included_pix = self.running_ave(rad_pix, good_image, self.edges)

        if outfile != 'NULL':
            self.write_prof(self.rads, self.prof, self.proferr, self.aperflux, outfile)
        return


    def running_ave(self, rad_pix, good_image, edges):
        rad_out = []
        prof_out = []
        proferr_out = []
        aperflux = []
        included_pix = []

        for curr_edge in np.arange(len(edges)-1):
            tmp_im = np.extract(rad_pix < edges[curr_edge+1], good_image)
            tmp_rad = np.extract(rad_pix < edges[curr_edge+1], rad_pix)

            if len(tmp_rad)>0:
                aperflux.append(np.sum(tmp_im))
                included_pix.append(float(tmp_im.size))
            else:
                aperflux.append(0)
                included_pix.append(0)

            tmp_im = np.extract(tmp_rad >= edges[curr_edge], tmp_im)
            tmp_rad = np.extract(tmp_rad >= edges[curr_edge], tmp_rad)


            if len(tmp_rad) > 0:
                rad_out.append(np.mean(tmp_rad))
                prof_out.append(np.mean(tmp_im))
                proferr_out.append(np.std(tmp_im))
            else:
                rad_out.append(-999.0)
                prof_out.append(-999.0)
                proferr_out.append(-999.0)

        return rad_out, prof_out,proferr_out, aperflux, included_pix


    def write_prof(self, rads, prof, proferr, aperflux, outfile):
        file = open(outfile, 'w')
        file.write('# rad prof proferr aperflux\n')
        for r, p,perr, af in zip(rads, prof, proferr,aperflux):
            file.write('%f %e %e %e\n'  %(r,p,perr, af))

        file.close()
        return
   
    def halflight(self, ltot=0, inrad = 100.0):
        """returns halflight radius in pixels...You MUST use background subtracted image or this will not work correctly"""
        good_image = self.good_image[:]

        rad_pix = self.rad_pix[:]

        order = np.argsort(rad_pix)
        sort_image = good_image[order]
        sort_rad = rad_pix[order]

        running_total = np.cumsum(sort_image)
        if ltot > 0:
            h_light = ltot/2.0
        else:
            h_light = running_total[-1]/2.0
        #print "ltot is %f" %(ltot/2.0)
        for cur_rad, curtot in zip(sort_rad,running_total):
            if curtot >= h_light:
                half_rad = cur_rad
                break
        else:
            half_rad = -999

        inlight  = -999
        for cur_rad, curtot in zip(sort_rad,running_total):
            if cur_rad <= inrad:
                inlight = curtot
            else:
                break


        return half_rad, inlight
    
            
    def make_check_image(self):
        good_x = self.good_x
        good_y = self.good_y        
        rad_pix = self.rad_pix

        out_annuli = np.zeros_like(self.image)


        for x,y,radius in zip(good_x, good_y, rad_pix):
            count = 0

            while (radius > self.edges[count]):
                count += 1

                if (len(self.edges) - 1 == count):
                    count = -1
                    break
                
            out_annuli[y][x] = count

        ext = pyfits.PrimaryHDU(out_annuli)
        ext.writeto('test_annuli.fits', clobber = 1)

        return
    
            
    def make_mask(self):
        mask = np.where(self.image > np.median(self.image), 1, 0)
        return mask

        
    def make_halflight_mask(self, hrad = 1000):
        good_pix = np.where(self.rad_pix<= hrad, 1, 0)
        mask = good_pix.reshape(np.shape(self.image))

        return mask

    
    def get_noise(self, gain, dark_var, rad_lim):
        good_image = np.extract(self.rad_pix< rad_lim, self.good_image)
        
        noise = good_image/gain + dark_var

        print "noise ", np.sum(noise)
        tot_noise = np.sqrt(np.sum(noise))
        
        return tot_noise


        
