import numpy as np
from matplotlib import pyplot as plt
from matplotlib import gridspec
from scipy.stats import gaussian_kde

from cmap import get_cmap

def kde_2d(x, y, xlim, ylim):
    
    xmin, xmax = xlim if xlim else (x.min(), x.max())
    ymin, ymax = ylim if ylim else (y.min(), y.max())
    
    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([x, y])
    
    kernel = gaussian_kde(values)
    Z = np.reshape(kernel(positions).T, X.shape)

    return Z

def kde_1d(a, alim):
    
    amin, amax = alim if alim else (a.min(), a.max())
    
    kdea=gaussian_kde(a)
    a = np.linspace(amin - (amax-amin)*0.05, amax + (amax-amin)*0.05,400)
    da = kdea(a)

    return a, da

def jointplot_kde(x, y, data=None, figsize=(8, 8), ratio=(5, 5), xlim=None, ylim=None, 
                  color="orange", fontsize=16, title_fontsize=20, **kwargs):
    
    if data is not None:
        assert isinstance(x, str) and isinstance(y, str)
        x = data[x]
        y = data[y]

    xmin, xmax = xlim if xlim else (x.min(), x.max())
    ymin, ymax = ylim if ylim else (y.min(), y.max())

    # Define grid for subplots
    gs = gridspec.GridSpec(2, 2, width_ratios=[ratio[0], 1], height_ratios = [1, ratio[1]])

    ## Create kde 2d plot
    fig = plt.figure(facecolor='white', figsize=figsize)
    ax = plt.subplot(gs[1, 0], frameon=True, zorder=3)
    
    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    Z = kde_2d(x, y, xlim, ylim)
    cfset = ax.contourf(X, Y, Z, cmap=get_cmap(color))
    
    scale_factor = figsize[0] / figsize[1]
    ax.set_xlim(xmin - 0.05*(xmax-xmin), xmax + 0.05*(xmax-xmin))
    ax.set_ylim(ymin - 0.05*scale_factor*(ymax-ymin), ymax + 0.05*scale_factor*(ymax-ymin))

    # Create Y-marginal (right)
    axr = plt.subplot(gs[1, 1], sharey=ax, frameon=False, xticks=[], zorder=2 ) 

    # Create X-marginal (top)
    axt = plt.subplot(gs[0, 0], sharex=ax, frameon=False, yticks=[], zorder=1)
    
    if 'title' in kwargs.keys():
        ax.set_title(kwargs['title'], x=0.95, y=1.05, fontsize=title_fontsize)
    if 'xlabel' in kwargs.keys():
        ax.set_xlabel(kwargs['xlabel'], fontsize=fontsize)
    if 'ylabel' in kwargs.keys():
        ax.set_ylabel(kwargs['ylabel'], fontsize=fontsize)
    
    ## Create x distribution
    x, dx = kde_1d(x, xlim)
    
    axt.plot(x, dx, color=color)
    axt.fill_between(x, dx, color=color, alpha=0.2)
    
    axt.set_xlim(xmin - 0.05*(xmax-xmin), xmax + 0.05*(xmax-xmin))
    axt.axis("off")
    axt.set_ylim(0)
    
    ## Create y distribution
    y, dy = kde_1d(y, ylim)

    axr.plot(dy, y, color=color)
    axr.fill_betweenx(y, dy, color=color, alpha=0.2)

    axr.set_ylim(ymin - 0.05*scale_factor*(ymax-ymin), ymax + 0.05*scale_factor*(ymax-ymin))
    axr.axis("off")
    axr.set_xlim(0)
                 
    ### Final settings
    plt.subplots_adjust(wspace=0, hspace=0)
    
    secax = ax.secondary_xaxis('top')
    secax.tick_params(axis="x",direction="in", pad=-15, labelsize=0, labelcolor="white")
    secax.set_xticklabels([])
    
    secax = ax.secondary_yaxis('right')
    secax.tick_params(axis="y",direction="in", pad=-15, labelsize=0, labelcolor="white")
    secax.set_xticklabels([])
                               
    ax.patch.set_edgecolor('black')  
    ax.patch.set_linewidth('1')

    ax.patch.set_facecolor('white')
    
    if "save" in kwargs.keys():
        plt.savefig(kwargs["save"])
    plt.show()
    