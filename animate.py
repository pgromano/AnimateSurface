from warnings import warn
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from matplotlib import animation, gridspec, style
style.use('seaborn-whitegrid')
font = {'family' : 'sans-serf',
        'weight' : 'light',
        'size'   : 20}

def surface(surf,filename=None,x=None,y=None,x_labels=None,y_labels=None, fps=20):
    if surf.shape[0] != surf.shape[1]:
        warn("""Input surfaces must be a square matrix!""")

    # If no x-axis is set default to 0 to 1
    if x is None:
        x = np.linspace(0,1,surf.shape[0])
    # If no y-axis is set default to 0 to 1
    if y is None:
        y = np.linspace(0,1,surf.shape[1])
    X,Y = np.meshgrid(x,y)

    #Close any pre-existing figures and create new figure
    plt.close()
    fig = plt.figure(1, figsize=(15, 15))
    # Create ROYGBIV color scheme
    colors = cm.rainbow(np.linspace(0,1,7))
    gs = gridspec.GridSpec(4,4)

    # Create plot figures,
    axPLOT2D = fig.add_subplot(gs[1:4,0:3])
    axPLOTx = fig.add_subplot(gs[0,0:3])
    axPLOTy = fig.add_subplot(gs[1:4,3])

    if x_labels is not None:
        axPLOT2D.set_xlabel(x_labels,fontsize=35)
    if y_labels is not None:
        axPLOT2D.set_ylabel(y_labels,fontsize=35)

    # Prepare axes for Surface
    axPLOT2D.set_xlim(x.min(),x.max())
    axPLOT2D.set_ylim(y.min(),y.max())
    axPLOT2D.tick_params(labelsize=20)

    # Prepare axes for X cross section
    axPLOTx.set_xlim([x.min(),x.max()])
    axPLOTx.set_ylim([surf.min(),surf.max()])
    axPLOTx.get_xaxis().set_ticks([])
    axPLOTx.get_yaxis().set_ticks([])

    # Prepare axes for Y cross section
    axPLOTy.set_xlim([surf.min(),surf.max()])
    axPLOTy.set_ylim([y.min(),y.max()])
    axPLOTy.get_xaxis().set_ticks([])
    axPLOTy.get_yaxis().set_ticks([])

    line1, = axPLOTx.plot([],[],linewidth=6,alpha=0.5,color=colors[1])
    line2, = axPLOTy.plot([],[],linewidth=6,alpha=0.5,color=colors[-1])

    line3 = axPLOT2D.contourf(X,Y,surf,20,cmap=cm.Spectral_r)
    line3x, = axPLOT2D.plot([],[],linewidth=5,alpha=0.5,color=colors[1])
    line3y, = axPLOT2D.plot([],[],linewidth=5,alpha=0.5,color=colors[-1])

    def animate(n):
        line1.set_data(x,surf[n,:])
        line2.set_data(surf[:,n],y)
        line3x.set_data([x.min(),x.max()],[y[n],y[n]])
        line3y.set_data([x[n],x[n]],[y.min(),y.max()])
        return line1,line2

    anim = animation.FuncAnimation(fig,animate,frames=surf.shape[0])
    if filename is None:
        anim.save('AnimatedSurface.mpg',writer='mencoder',fps=fps)
    else:
        if filename.lower().endswitch('.mpg'):
            anim.save(filename,writer='mencoder',fps=fps)
        else:
            anim.save(filename+'.mpg',writer='mencoder',fps=fps)

    plt.close()
