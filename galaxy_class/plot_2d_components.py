from MatplotRc import *
import pylab
import numpy as n


def plot_2d_components(save_path, number, model_type, plot_name_info, data, pymodel, resid, total_model, add_string = ''):

    adj_data = n.abs(data - n.max(pymodel))/n.max(n.abs(pymodel - n.max(pymodel)))
    adj_pymodel = n.abs(pymodel - n.max(pymodel))/n.max(n.abs(pymodel - n.max(pymodel)))
    adj_total_model = n.abs(total_model - n.max(pymodel))/n.max(n.abs(pymodel - n.max(pymodel)))

    cb_labels = ['%4.2f'%(n.max(pymodel)),'%4.2f'%(n.max(pymodel)-.2*(n.max(pymodel) -n.min(pymodel))),'%4.2f'%(n.max(pymodel)-.4*(n.max(pymodel) -n.min(pymodel))),'%4.2f'%(n.max(pymodel)-.6*(n.max(pymodel) -n.min(pymodel))),'%4.2f'%(n.max(pymodel)-.8*(n.max(pymodel) -n.min(pymodel))),'%4.2f'%(n.min(pymodel))]
    matrc6()
    pylab.suptitle(plot_name_info+' Fit Decomposition', fontsize = 14)
    pylab.suptitle(add_string, y = .96)
    pylab.suptitle('Note: all measurements are in magnitude/arcsec$^2$', y = .05)
    
    ax = pylab.subplot(3,2,1)
    pylab.title('Original Image')
    pylab.pcolor(adj_data)
    pylab.clim(0,1)
    cbar=pylab.colorbar(ticks=[0,.2,.4,.6,.8,1])
    cbar.ax.set_yticklabels(cb_labels)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticklabels('')
    ax.yaxis.set_ticklabels('')
    
    ax = pylab.subplot(3,2,2)
    pylab.title('Pymorph Fit - Data')
    pylab.pcolor(resid)
    pylab.clim(-0.25, 0.25)
    pylab.colorbar()
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticklabels('')
    ax.yaxis.set_ticklabels('')

    ax =pylab.subplot(3,2,3)
    pylab.title('Pymorph Fit')
    pylab.pcolor(adj_pymodel)
    cbar=pylab.colorbar(ticks=[0,.2,.4,.6,.8,1])
    cbar.ax.set_yticklabels(cb_labels)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticklabels('')
    ax.yaxis.set_ticklabels('')

    ax = pylab.subplot(3,2,4)
    pylab.title('(Pymorph fit - Component Sum) in units of $10^{-6}$')
    pylab.pcolor((pymodel - total_model)*10**6)
    pylab.colorbar()
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticklabels('')
    ax.yaxis.set_ticklabels('')

    ax = pylab.subplot(3,2,5)
    pylab.title('Component Sum')
    pylab.pcolor(adj_total_model)
    cbar=pylab.colorbar(ticks=[0,.2,.4,.6,.8,1])
    cbar.ax.set_yticklabels(cb_labels)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticklabels('')
    ax.yaxis.set_ticklabels('')
            
    ax = pylab.subplot(3,2,6)
    pylab.title('Component Sum - Data')
    pylab.pcolor(total_model - data)
    pylab.clim(-0.25, 0.25)
    pylab.colorbar()
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticklabels('')
    ax.yaxis.set_ticklabels('')
            
            
    pylab.savefig(save_path + '%06d_fits_comp_%s.png' %(number,model_type), format = 'png')
    pylab.clf()
