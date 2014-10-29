from astro_image_processing.statistics.convex_hull import *
import pylab as pl
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

def run_hull(x,y): 
    
    x_out = np.array([])
    y_out = np.array([])
    enclosed = np.array([])
    tot_points = float(len(x))

    while len(x) > 5:

        list1 = np.array([x,y])
        hull_pts, interior_points = convex_hull(list1, graphic=False)
        
        b = n.reshape(interior_points, (-1,2)) 
    
        x = b[:,0]
        y = b[:,1]

        
        x_hull = hull_pts[:,0]
        y_hull = hull_pts[:,1]

        x_out = np.append(x_out, x_hull)
        y_out = np.append(y_out, y_hull)

        enc_tmp = np.ones_like(x_hull) * len(x)/tot_points
        enclosed = np.append(enclosed, enc_tmp)
        print len(x_out)/tot_points

    return x_out, y_out, enclosed


def plot_data(x_in, y_in, sample_size, num_sample, xmin, xmax, xbin,ymin, ymax, ybin, color = 'r'):
    indicies = np.arange(len(x_in))

    # Set up a regular grid of interpolation points
    xi, yi = np.linspace(xmin, xmax, xbin), np.linspace(ymin, ymax, ybin)
    xi, yi = np.meshgrid(xi, yi)

    z_full = np.zeros_like(xi)

    for count in np.arange(num_sample):
        np.random.shuffle(indicies)
        xsample = x_in[:sample_size]
        ysample = y_in[:sample_size]
        x,y,enc = run_hull(xsample, ysample)

        # Interpolate
        # rbf = scipy.interpolate.Rbf(x, y, enc, function='linear')
        # zi = rbf(xi, yi)
        zi = scipy.interpolate.griddata((x, y), enc, (xi, yi), method='linear')

        zi = np.where(np.isnan(zi),1.0,zi)
        z_full += zi


    z_full = z_full/num_sample
    print xi, yi
    print z_full
    # plt.imshow(zi, vmin=0, vmax=1, origin='lower',
    #           extent=[x.min(), x.max(), y.min(), y.max()])
    #pl.scatter(points[0], points[1], s = 4, edgecolor = 'none')
    pl.contour(xi,yi,z_full, (0.0,0.25, 0.5, 0.75,1.0),linewidths = 3, colors = [color]*4, linestyles = ['-','-','--',':'])

    #plt.colorbar()
    return

   




