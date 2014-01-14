### taken from http://zulko.wordpress.com/2012/09/29/animate-your-3d-plots-with-pythons-matplotlib/ ###



import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
import os, sys
import numpy as np
import pylab as pl
import pyfits as pf
from MatplotRc import *
from pylab import rcParams
 
##### TO CREATE A SERIES OF PICTURES
 
def make_views(ax,angles,elevation=None, width=4, height = 3,
                prefix='tmprot_',**kwargs):
    """
    Makes jpeg pictures of the given 3d ax, with different angles.
    Args:
        ax (3D axis): te ax
        angles (list): the list of angles (in degree) under which to
                       take the picture.
        width,height (float): size, in inches, of the output images.
        prefix (str): prefix for the files created. 
     
    Returns: the list of files created (for later removal)
    """
     
    files = []
    ax.figure.set_size_inches(width,height)
     
    for i,angle in enumerate(angles):
     
        ax.view_init(elev = elevation, azim=angle)
        fname = '%s%03d.png'%(prefix,i)
        ax.figure.savefig(fname)
        files.append(fname)
     
    return files

def make_panels(fig,datafiles, width=4, height = 3,
                prefix='tmprot_',**kwargs):
    """
    Makes png pictures of the given plot, with different angles.
    Args:
        ax (3D axis): te ax
        angles (list): the list of angles (in degree) under which to
                       take the picture.
        width,height (float): size, in inches, of the output images.
        prefix (str): prefix for the files created. 
     
    Returns: the list of files created (for later removal)
    """
     
    files = []
    
    for i,df in enumerate(datafiles):
        pl.clf()
        fig.set_size_inches(width,height)
        ticks = pub_plots(xmaj = 1000, xmin = 50, xstr = '%d', ymaj = 1000, ymin = 50, ystr = '%d')
        MatPlotParams = {'xtick.major.size': 4, 'ytick.major.size' : 4, 
                         'xtick.minor.size': 4, 'ytick.minor.size': 4,
                         'axes.labelsize': 6, 'xtick.labelsize': 10, 
                         'ytick.labelsize': 8}
        rcParams.update(MatPlotParams)

        pl.subplots_adjust(wspace = 0.35,hspace = 0.35)
        pl.figtext(.5,.95, 'Iteration:%d' %i, ha='center')
        
        indat = pf.open(df)
        data = indat[1].data
        model = indat[2].data
        residual = indat[3].data
        header = indat[2].header
        indat.close()
        
        zoom_min = data.shape[0]/2 - 100
        zoom_max = data.shape[0]/2 + 100
        
        fig.add_subplot(2,2,1)
        pl.title('data')
        pl.imshow(-2.5*np.log10(data[zoom_min:zoom_max,zoom_min:zoom_max])+25.256, cmap = cm.jet_r)
        pl.colorbar()
        ticks.set_plot(pl.gca())
        pl.gca().axes.get_xaxis().set_ticks([])
        pl.gca().axes.get_yaxis().set_ticks([])
        vmin, vmax = pl.gci().get_clim()

        fig.add_subplot(2,2,2)
        pl.title('model')
        pl.imshow(-2.5*np.log10(model[zoom_min:zoom_max,zoom_min:zoom_max])+25.256, cmap = cm.jet_r, vmin=vmin, vmax=vmax)
        ticks.set_plot(pl.gca())
        pl.text(0.1, 0.95,'$m_{total}$: %4.2f, $r_e$: %4.1f' %(float(header['1_MAG'].split()[0]),float(header['1_RE'].split()[0])),
             horizontalalignment='left',
             verticalalignment='center',
             fontsize=6, color = 'white',
             transform = pl.gca().transAxes)
        if i==17:
            pl.text(0.1, 0.05,'$n$: %3.2f, $\chi^2_{DOF}$: %.2f' %(float(header['1_N'].split()[0]),header['CHI2NU']),
             horizontalalignment='left',
             verticalalignment='center',
             fontsize=6, color = 'white',
             transform = pl.gca().transAxes)
        else:
            pl.text(0.1, 0.05,'$n$: %3.2f' %(float(header['1_N'].split()[0])),
             horizontalalignment='left',
             verticalalignment='center',
             fontsize=6, color = 'white',
             transform = pl.gca().transAxes)
        pl.gca().axes.get_xaxis().set_ticks([])
        pl.gca().axes.get_yaxis().set_ticks([])
        
        pl.colorbar()

        zoom_resid = -2.5*np.log10(data[zoom_min:zoom_max,zoom_min:zoom_max])+2.5*np.log10(model[zoom_min:zoom_max,zoom_min:zoom_max])
        
        fig.add_subplot(2,2,4)
        pl.title('residual')
        pl.imshow(zoom_resid, cmap = cm.jet)
        #pl.text(0.5, 0.9,'$\chi^2_{DOF}$: %.2f' %header['CHI2NU'],
        #     horizontalalignment='center',
        #     verticalalignment='center',
        #     fontsize=10, color = 'black',
        #     transform = pl.gca().transAxes)
        pl.colorbar()
        vmin, vmax = pl.gci().get_clim()
        ticks.set_plot(pl.gca())
        pl.gca().axes.get_xaxis().set_ticks([])
        pl.gca().axes.get_yaxis().set_ticks([])
        
        fig.add_subplot(2,2,3)
        pl.title('full frame')
        pl.imshow(-2.5*np.log10(data)+2.5*np.log10(model), cmap = cm.jet, vmin = vmin, vmax = vmax)
        
        cbar = pl.colorbar()
        ticks.set_plot(pl.gca())
        pl.gca().axes.get_xaxis().set_ticks([])
        pl.gca().axes.get_yaxis().set_ticks([])

        fname = '%s%03d.png'%(prefix,i)
        pl.savefig(fname)
        pl.savefig('%s_%d.eps'%('my_epsfiles',i))
        files.append(fname)
     
    return files
 
 
 
##### TO TRANSFORM THE SERIES OF PICTURE INTO AN ANIMATION
 
def make_movie(files,output, fps=10,bitrate=1800,**kwargs):
    """
    Uses mencoder, produces a .mp4/.ogv/... movie from a list of
    picture files.
    """
     
    output_name, output_ext = os.path.splitext(output)
    command = { '.mp4' : 'mencoder "mf://%s" -mf fps=%d -o %s.mp4 -ovc lavc\
                         -lavcopts vcodec=msmpeg4v2:vbitrate=%d'
                         %(",".join(files),fps,output_name,bitrate)}
                          
    command['.ogv'] = command['.mp4'] + '; ffmpeg -i %s.mp4 -r %d %s'%(output_name,fps,output)
     
    print command[output_ext]
    output_ext = os.path.splitext(output)[1]
    os.system(command[output_ext])
 
 
 
def make_gif(files,output,delay=100, repeat=True,**kwargs):
    """
    Uses imageMagick to produce an animated .gif from a list of
    picture files.
    """
     
    loop = -1 if repeat else 0
    os.system('convert -delay %d -loop %d %s %s'
              %(delay,loop," ".join(files),output))
 
 
 
 
def make_strip(files,output,**kwargs):
    """
    Uses imageMagick to produce a .jpeg strip from a list of
    picture files.
    """
     
    os.system('montage -tile 1x -geometry +0+0 %s %s'%(" ".join(files),output))
     
     
     
##### MAIN FUNCTION
 
def rotanimate(ax, angles, output, **kwargs):
    """
    Produces an animation (.mp4,.ogv,.gif,.jpeg,.png) from a 3D plot on
    a 3D ax
     
    Args:
        ax (3D axis): the ax containing the plot of interest
        angles (list): the list of angles (in degree) under which to
                       show the plot.
        output : name of the output file. The extension determines the
                 kind of animation used.
        **kwargs:
            - width : in inches
            - heigth: in inches
            - framerate : frames per second
            - delay : delay between frames in milliseconds
            - repeat : True or False (.gif only)
    """
         
    output_ext = os.path.splitext(output)[1]
 
    files = make_views(ax,angles, **kwargs)
     
    D = { '.mp4' : make_movie,
          '.ogv' : make_movie,
          '.gif': make_gif ,
          '.jpeg': make_strip,
          '.png':make_strip}
           
    D[output_ext](files,output,**kwargs)
     
    for f in files:
        os.remove(f)
     

def panelanimate(fig, infiles, output, **kwargs):
    """
    Produces an animation (.gif) from a set of panels
     
    Args:
        fig: the figure containing the plots of interest
        output : name of the output file. The extension determines the
                 kind of animation used.
        **kwargs:
            - width : in inches
            - heigth: in inches
            - framerate : frames per second
            - delay : delay between frames in milliseconds
            - repeat : True or False (.gif only)
    """
         
    output_ext = os.path.splitext(output)[1]
 
    files = make_panels(fig, infiles, **kwargs)
     
    D = { '.mp4' : make_movie,
          '.ogv' : make_movie,
          '.gif': make_gif ,
          '.jpeg': make_strip,
          '.png':make_strip}
           
    D[output_ext](files,output,**kwargs)
     
    #for f in files:
    #    os.remove(f)
     
 
##### EXAMPLE
 
if __name__ == '__mainold__':
 
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    X, Y, Z = axes3d.get_test_data(0.05)
    s = ax.plot_surface(X, Y, Z, cmap=cm.jet)
    plt.axis('off') # remove axes for visual appeal
     
    angles = np.linspace(0,360,21)[:-1] # Take 20 angles between 0 and 360
 
    # create an animated gif (20ms between frames)
    rotanimate(ax, angles,'movie.gif',delay=20) 
 
    # create a movie with 10 frames per seconds and 'quality' 2000
    #rotanimate(ax, angles,'movie.mp4',fps=10,bitrate=2000)
 
    # create an ogv movie
    #rotanimate(ax, angles, 'movie.ogv',fps=10) 

if __name__ == '__main__':
 
    fig = plt.figure()
    
    # create an animated gif (20ms between frames)
    files = ['O_r_00521117_r_stamp_step_0.fits',
             'O_r_00521117_r_stamp_step_1.fits', 
             'O_r_00521117_r_stamp_step_2.fits',
             'O_r_00521117_r_stamp_step_3.fits',
             'O_r_00521117_r_stamp_step_4.fits',
             'O_r_00521117_r_stamp_step_5.fits',
             'O_r_00521117_r_stamp_step_6.fits',
             'O_r_00521117_r_stamp_step_7.fits',
             'O_r_00521117_r_stamp_step_8.fits',
             'O_r_00521117_r_stamp_step_9.fits',
             'O_r_00521117_r_stamp_step_10.fits',  
             'O_r_00521117_r_stamp_step_11.fits',  
             'O_r_00521117_r_stamp_step_12.fits',  
             'O_r_00521117_r_stamp_step_13.fits',  
             'O_r_00521117_r_stamp_step_14.fits',  
             'O_r_00521117_r_stamp_step_15.fits',  
             'O_r_00521117_r_stamp_step_16.fits',  
             'O_r_00521117_r_stamp.fits' ]
    panelanimate(fig, files, 'movie.gif',delay=50) 
