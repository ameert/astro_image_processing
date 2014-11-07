import numpy as np
import pylab as pl
from scipy import ndimage
import matplotlib.cm as cm
import matplotlib.colors as col

#start_mysql -e "select a.r_bulge, b.r_bulge, a.n_bulge, b.n_bulge, c.gr15_hl, c.gr3_hl, d.g_mag, d.r_mag, e.g_mag, e.r_mag from g_band_ser as a, r_band_ser as b, COLOR_GRAD_ser as c, catalog.ser_color_HL as d, catalog.ser_color_HL as e where a.galcount = b.galcount and a.galcount = d.galcount and a.galcount = e.galcount and a.galcount = c.galcount and a.n_bulge>0 and b.n_bulge>0 and c.grColor_hl>-900 and gr15_hl > -900 and grtwo_hl >-900 and gr3_hl > -900 and gr90_hl>-900 and a.n_bulge<7.95 and b.n_bulge<7.95 and d.HL_rad_10=15 and e.HL_rad_10=30;" > color_grad_corr.txt

def plot_dense(x_dat, y_dat, xtext, ytext, xlim, ylim, bin_num,scale = False):
    
    H, xedges, yedges = np.histogram2d(x_dat, y_dat, range = [xlim,ylim], 
                                       bins = bin_num)

    Hpic = ndimage.rotate(H, 90.0)

    Hpic +=0.0000001
    if scale=='log':
        Hpic = np.log10(Hpic)
    elif scale == 'norm':
        Hpic = 100.0*Hpic/x_dat.size
    elif isinstance(scale, (long, int, float)):
        Hpic = Hpic*scale
    
    
    dense_high = np.max(Hpic)/2.0
    dense_low = 0.0
    color_start = 1.0/x_dat.size
    
    extent = [xlim[0], xlim[1], ylim[0], ylim[1]]
    
    if scale=='log':
        img = pl.imshow(Hpic,  interpolation='nearest', extent = extent,
                        vmax = np.log10(dense_high),vmin = np.log10(dense_low),
                        aspect = 'auto')
    else:
        img = pl.imshow(Hpic,  interpolation='nearest', extent = extent,
                        vmax = dense_high, vmin = dense_low,aspect = 'auto')

    pl.text(0.02, 7.5,'max: %2.2f' %np.max(Hpic), fontsize=6)
    pl.text(0.02, 7.2,'num: %d' %x_dat.size, fontsize=6)

    if scale=='log':
        color_scale_start = np.log(float(color_start))/np.log(dense_high)
    else:
        color_scale_start = float(color_start)/dense_high

    cdict = {'red': ((0.0, 1.0, 1.0),
                     (color_scale_start, 1.0,0.6),
                     (1.0, 0.0, 0.0)),
             'green': ((0.0, 1.0, 1.0),
                       (color_scale_start, 1.0,0.6),
                       (1.0, 0.0, 0.0)),
             'blue': ((0.0, 1.0, 1.0),
                      (color_scale_start, 1.0,0.6),
                      (1.0, 0.0, 0.0))}

    my_cmap = col.LinearSegmentedColormap('my_colormap',cdict,8192)
    img.set_cmap(my_cmap)

    pl.colorbar(img, shrink = .90)
    
    pl.xlabel(xtext)
    pl.ylabel(ytext)
    pl.xlim((extent[0],extent[1]))
    pl.ylim((extent[2],extent[3]))

    return H, xedges, yedges

r_g, r_r, n_g, n_r, gr_15, gr_30, g_15, r_15, g_30, r_30 = np.loadtxt('color_grad_corr.txt', unpack = True, skiprows =1)

print n_g.size

color_choice = ['r' if a>4.0 else 'b' for a in n_r]

if 1:
    pl.subplot(2,2,1)
    plot_dense(np.extract(n_r>=3.0,n_g-n_r), np.extract(n_r>=3.0,r_15), 'n_g-n_r', 'gr_15', (-2,2), (22.0,25.0), (100,100),scale = 'norm')
    pl.ylim(22.0,25.0)
    pl.xlim(-2,2)
    pl.title('n_r >= 3, gr grad to 1.5hl') 

    pl.subplot(2,2,2)
    plot_dense(np.extract(n_r>=3.0,n_g-n_r), np.extract(n_r>=3.0,r_30), 'n_g-n_r', 'gr_3', (-2,2), (22.0,25.0), (100,100),scale = 'norm')
    pl.ylim(22.0,25.0)
    pl.xlim(-2,2)
    pl.title('n_r >= 3, gr grad to 3hl') 

    pl.subplot(2,2,3)
    plot_dense(np.extract(n_r<3.0,n_g-n_r), np.extract(n_r<3.0,r_15), 'n_g-n_r', 'gr_15', (-2,2), (22.0,25.0), (100,100),scale = 'norm')
    pl.ylim(22.0,25.0)
    pl.xlim(-2,2)
    pl.title('n_r < 3, gr grad to 1.5hl') 

    pl.subplot(2,2,4)
    plot_dense(np.extract(n_r<3.0,n_g-n_r), np.extract(n_r<3.0,r_30), 'n_g-n_r', 'gr_3', (-2,2), (22.0,25.0), (100,100),scale = 'norm')
    pl.ylim(22.0,25.0)
    pl.xlim(-2,2)
    pl.title('n_r < 3, gr grad to 3hl') 
    pl.show() 

pl.subplot(2,2,1)
plot_dense(np.extract(n_r>=3.0,n_g-n_r), np.extract(n_r>=3.0,r_g/r_r), 'n_g-n_r', 'r_g/r_r', (-2,2), (0.75, 1.25), (100,100),scale = 'norm')
pl.ylim(0.75, 1.25)
pl.xlim(-2,2)
pl.title('n_r >= 3, g/r radius ratio') 

pl.subplot(2,2,2)
plot_dense(np.extract(n_r>=3.0,n_g-n_r), np.extract(n_r>=3.0,r_g/r_r), 'n_g-n_r', 'r_g/r_r', (-2,2), (0.75, 1.25), (100,100),scale = 'norm')
pl.ylim(0.75, 1.25)
pl.xlim(-2,2)
pl.title('n_r >= 3, g/r radius ratio') 

pl.subplot(2,2,3)
plot_dense(np.extract(n_r<3.0,n_g-n_r), np.extract(n_r<3.0,r_g/r_r), 'n_g-n_r', 'r_g/r_r', (-2,2), (0.75, 1.25), (100,100),scale = 'norm')
pl.ylim(0.75, 1.25)
pl.xlim(-2,2)
pl.title('n_r < 3, g/r radius ratio') 

pl.subplot(2,2,4)
plot_dense(np.extract(n_r<3.0,n_g-n_r), np.extract(n_r<3.0,r_g/r_r), 'n_g-n_r', 'r_g/r_r', (-2,2), (0.75, 1.25), (100,100),scale = 'norm')
pl.ylim(0.75, 1.25)
pl.xlim(-2,2)
pl.title('n_r < 3, g/r radius ratio') 
pl.show() 
