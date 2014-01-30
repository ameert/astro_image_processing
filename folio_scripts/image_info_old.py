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

import numpy as n
import pyfits

class image_info:
    """class used to calculate image info like ellipticity and radius
    must pass and image and binary mask (1 for valid pixel 0 for bad pixel"""

    def __init__(self, image, mask = "NULL", x_ctr = "NULL", y_ctr = "NULL"):
        self.image = image
        if mask == "NULL":
            self.mask = n.ones_like(self.image)
        else:
            self.mask = mask
        yedges = n.arange(n.shape(self.image)[0])
        xedges = n.arange(n.shape(self.image)[1])
    
        self.xpos, self.ypos = n.meshgrid(xedges,yedges)

        self.x_flat = self.xpos.flatten()
        self.y_flat = self.ypos.flatten()

        self.mask_flat = self.mask.flatten()
        self.image_flat = self.image.flatten()

        self.sum_image = n.sum(self.mask_flat * self.image_flat)
        if x_ctr is "NULL":
            self.x_ctr = self.image_moment(1, 0)/self.sum_image
        else:
            self.x_ctr = x_ctr
            
        if y_ctr is "NULL":
            self.y_ctr = self.image_moment(0, 1)/self.sum_image
        else:
            self.y_ctr = y_ctr
            
        
    def image_moment(self, x_mom, y_mom, x_ctr = 0, y_ctr = 0):

        m = (((self.x_flat - x_ctr)**x_mom)*((self.y_flat - y_ctr)**y_mom)*
             self.image_flat * self.mask_flat)

        return n.sum(m)

    def cov_mat(self):
        a = n.zeros((2,2))
        a[0][0] = self.image_moment(0,2,self.x_ctr, self.y_ctr)/self.sum_image
        a[1][1] = self.image_moment(2,0,self.x_ctr, self.y_ctr)/self.sum_image
        a[1][0] = self.image_moment(1,1,self.x_ctr, self.y_ctr)/self.sum_image
        a[0][1] = a[1][0]

        return a

    def imstats(self):
        cov = self.cov_mat()
        eigen_vals = n.linalg.linalg.eigvals(cov)
        
        self.ba = n.sqrt(eigen_vals[1]/eigen_vals[0]) #as in b/a or ellipticity
        self.pa = ((0.5)*n.arctan2(2*cov[0][1],(cov[0][0]-cov[1][1]))) %  n.pi

        return
    

    def profile(self, outfile='NULL'):
        edgemin = 0.5
        edgemax = n.shape(self.image)[0] + n.shape(self.image)[1]
        edgestep = 1.5
        edgenum  = (edgemax-edgemin)/edgestep;

        edges = n.arange(edgemin, edgemax, edgestep)
        
        rads =[]
        prof = []
        proferr = []
        cosa = n.cos(self.pa)
        sina = n.sin(self.pa)

        good_image = n.extract(self.mask_flat, self.image_flat)
        good_x = n.extract(self.mask_flat, self.x_flat)
        good_y = n.extract(self.mask_flat, self.y_flat)
        
        x_pix = cosa*(good_x-self.x_ctr) + (good_y-self.y_ctr)*sina
        y_pix = -sina*(good_x-self.x_ctr) + (good_y-self.y_ctr)*cosa
        
        rad_pix = n.sqrt(self.ba*(x_pix**2.0) + (y_pix**2)/self.ba)
        

        self.rads, self.prof, self.proferr = self.running_ave(rad_pix, good_image, edges)

        if outfile != 'NULL':
            self.write_prof(self.rads, self.prof, self.proferr, outfile)
        return


    def running_ave(self, rad_pix, good_image, edges):
        rad_out = []
        prof_out = []
        proferr_out = []
        
        for curr_edge in n.arange(len(edges)-1):
            tmp_im = n.extract(rad_pix >= edges[curr_edge],good_image)
            tmp_rad = n.extract(rad_pix >= edges[curr_edge],rad_pix)
            
            tmp_im = n.extract(tmp_rad < edges[curr_edge+1], tmp_im)
            tmp_rad = n.extract(tmp_rad < edges[curr_edge+1], tmp_rad)
            
            
            if len(tmp_rad) > 0:
                rad_out.append(n.mean(tmp_rad))
                prof_out.append(n.mean(tmp_im))
                proferr_out.append(n.std(tmp_im)/len(tmp_rad))
        return rad_out, prof_out,proferr_out

    def write_prof(self, rads, prof, proferr, outfile):
        file = open(outfile, 'w')
        file.write('# rad prof proferr\n')
        for r, p,perr in zip(rads, prof, proferr):
            file.write('%f %e %e\n'  %(r,p,perr))

        file.close()
        return
    
    def make_check_image(self):
        good_x = n.extract(self.mask_flat, self.x_flat)
        good_y = n.extract(self.mask_flat, self.y_flat)
        
        cosa = n.cos(self.pa)#n.cos(self.pa)
        sina = n.sin(self.pa)#n.sin(self.pa)

        x_pix = cosa*(good_x-self.x_ctr) + (good_y-self.y_ctr)*sina
        y_pix = -sina*(good_x-self.x_ctr) + (good_y-self.y_ctr)*cosa
        
        rad_pix = n.sqrt(self.ba*(x_pix**2.0) + (y_pix**2)/self.ba)

        out_annuli = n.zeros_like(self.image)

        edgemin = 0.5
        edgemax = n.shape(self.image)[0] + n.shape(self.image)[1]
        edgestep = 1.5
        edgenum  = (edgemax-edgemin)/edgestep

        edges = n.arange(edgemin, edgemax, edgestep)

        for x,y,radius in zip(good_x, good_y, rad_pix):
            count = 0

            while (radius > edges[count]):
                count += 1

                if (len(edges) - 1 == count):
                    count = -1
                    break
                
            out_annuli[y][x] = count

        ext = pyfits.PrimaryHDU(out_annuli)
        ext.writeto('test_annuli.fits', clobber = 1)

        return
    
            
        
        
