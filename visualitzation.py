import numpy as np
import matplotlib.pyplot as plt
from .utils import significant_digits
from matplotlib.transforms import Bbox
import matplotlib

def update_2cool_rcParams(**kwargs):
    """
    Parameters
    ----------
    kwargs: dict
    Dictionary with addition parameters to add to the rcParams, or change any
    parameter already in the dict.
    """
    dict_rcParams={
        'font.weight': "normal", #
        'font.size': 16,
    #     "font.family": "Helvetica",    
    #     "font.family": {"serif": 'Computer Modern'},    
        'text.usetex': False,              # use latex for all text handling
        'figure.titlesize': 16,            # size of the figure title
        'axes.linewidth' : 1.5,            # edge line width
        'axes.labelweight': "normal",      # weight of the x and y labels
        'axes.titlesize': 16,              # font size of the axes title
        'axes.labelsize': 16,              # font size of the x and y labels
        'axes.grid': True,                 # display grid or not
        'axes.grid.axis': "both",          # which axis the grid should apply to
        'axes.grid.which': "major",        # grid lines at {major, minor, both} ticks
        'xtick.top': True,                 # draw x ticks on the top side
        'xtick.bottom': True,              # draw x ticks on the bottom side
        'ytick.right': True,               # draw y ticks on the right side
        'ytick.left': True,                # draw y ticks on the right side
        'xtick.direction': "in",           # x ticks direction: {in, out, inout} 
        'ytick.direction': "in",           # y ticks direction: {in, out, inout} 
        'xtick.major.width': 1.5,          # x major tick width in points
        'ytick.major.width': 1.5,          # y major tick width in points
        'xtick.minor.width': 1.5,          # x minor tick width in points    
        'ytick.minor.width': 1.5,          # y minor tick width in points
        'xtick.major.size': 8,             # x major tick size in points
        'ytick.major.size': 8,             # y major tick size in points    
        'xtick.minor.size': 5,             # x minor tick size in points
        'ytick.minor.size': 5,             # y minor tick size in points    
        'xtick.major.pad': 7.5,            # distance to x major tick label in points
        'ytick.major.pad': 7.5,            # distance to y major tick label in points
        'xtick.minor.pad': 7.5,            # distance to the x minor tick label in points    
        'ytick.minor.pad': 7.5,            # distance to the y minor tick label in points
        'xtick.labelsize': 16,             # font size of the x tick labels
        'ytick.labelsize': 16,             # font size of the y tick labels
        'lines.linewidth': 2,              # line width in points
    }
    
    for k,v in zip(kwargs.keys(),kwargs.values()):
        dict_rcParams[k]=v    
    
    #solve bug legend fontsize not updated
    fig,ax=plt.subplots()
    plt.close()

    matplotlib.rcParams.update(dict_rcParams)
    

def plot_parameter_value(fig,ax,latex_symbol,value,loc="lower left",value_error=None):
    """
    Plot the equation showing the value of given mathematical symbol in a plot.
    
    Parameters
    ----------
    fig: matplotlib.pyplot.figure
        Figure
    ax: matplotlib.pyplot.axis
        Axis used to store the figure
    latex_symbol: string
        Latex mathetmatical name of a symbol (\ is not required)
    value: float
        Value of the latex_symbol.
    loc: string
        Location of the equation in the plot.
    value_erorr: float or None
        If None, the error is not showed. Else, the value and the error
        are rounded to show only significant decimals.
    
    Returns
    -------
    ax:
        Axis
    """
    
    text_kwargs={
        "size":20,
        "horizontalalignment":'center',
        "verticalalignment":'center',
        "zorder":1000,
    }
    
    if value_error!=None:
        value,value_error,n_decimals=significant_digits(value,value_error)
        text_print=r"$\{} = {:1.{}f} \pm {:1.{}f}$".format(latex_symbol,
                                                           value,n_decimals,
                                                           value_error,n_decimals)
    else:
        text_print=r"$\{} = {:1.3}$".format(latex_symbol,value)

    xmin,xmax=ax.get_xlim()
    ymin,ymax=ax.get_ylim()

    dx=xmax-xmin
    dy=ymax-ymin
    
    t=ax.text(0.1,0.1,text_print,**text_kwargs)
    r = fig.canvas.get_renderer()
    
    bbox_text=t.get_window_extent(r)
    bbox_ax=ax.get_window_extent(r)
    
    frac_hor_size_t=bbox_text.width/bbox_ax.width
    frac_ver_size_t=bbox_text.height/bbox_ax.height

    x_interval=1/20
    y_interval=1/20
    
    if frac_hor_size_t/2>x_interval:
        x_interval=frac_hor_size_t/2+x_interval
    if frac_ver_size_t/2>y_interval:
        y_interval=frac_ver_size_t/2+y_interval
        
    if loc=="lower left":
        if ax.get_xscale()=="linear":
            pos_x=xmin+dx*(x_interval)
        if ax.get_xscale()=="log":
            pos_x=np.exp(np.log(xmin)+(x_interval)*(np.log(xmax)-np.log(xmin)))
            
        if ax.get_yscale()=="linear":
            pos_y=ymin+dy*(y_interval)
        if ax.get_yscale()=="log":
            pos_y=np.exp(np.log(ymin)+(y_interval)*(np.log(ymax)-np.log(ymin)))
            
    elif loc=="lower right":
        if ax.get_xscale()=="linear":       
            pos_x=xmax-dx*(x_interval)
        if ax.get_xscale()=="log":
            pos_x=np.exp(np.log(xmax)-(x_interval)*(np.log(xmax)-np.log(xmin)))
        
        if ax.get_yscale()=="linear":       
            pos_y=ymin+dy*(y_interval)
        if ax.get_yscale()=="log":
            pos_y=np.exp(np.log(ymin)+(y_interval)*(np.log(ymax)-np.log(ymin)))
            
    elif loc=="upper left":
        if ax.get_xscale()=="linear":
            pos_x=xmin+dx*(x_interval)
        if ax.get_xscale()=="log":
            pos_x=np.exp(np.log(xmin)+(x_interval)*(np.log(xmax)-np.log(xmin)))
            
        if ax.get_yscale()=="linear":        
            pos_y=ymax-dy*(y_interval)
        if ax.get_yscale()=="log":     
            pos_y=np.exp(np.log(ymax)-(y_interval)*(np.log(ymax)-np.log(ymin)))
            
    elif loc=="upper right":
        if ax.get_xscale()=="linear":
            pos_x=xmax-dx*(x_interval)
        if ax.get_xscale()=="log":
            pos_x=np.exp(np.log(xmax)-(x_interval)*(np.log(xmax)-np.log(xmin)))
            
        if ax.get_yscale()=="linear":        
            pos_y=ymax-dy*(y_interval)
        if ax.get_yscale()=="log": 
            pos_y=np.exp(np.log(ymax)-(y_interval)*(np.log(ymax)-np.log(ymin)))        
            
    else:
        raise ValueError("Error, available values or loc are: lower left,"+\
                         " lower right, upper left, upper right")

    t.set_position((pos_x,pos_y))
       
    return ax


def plot_preliminary_text(fig,ax):
    """
    Plot the word PRELIMINARY diagonally in the plot
    
    Parameters
    ----------
    fig: matplotlib.pyplot.figure
        Figure
    ax: matplotlib.pyplot.axis
        Axis used to store the figure
        
    Returns
    -------
    ax: matplotlib.pyplot.axis
        Axis used to store the figure    
    """
    
    rotation_angle=np.rad2deg(np.arctan(ax.bbox.height/ax.bbox.width))
    text_kwargs={
        "rotation":rotation_angle,
        "alpha":0.5,
        "color":"gray",
        "wrap":True,
        "size":50,
        "horizontalalignment":'center',
        "verticalalignment":'center',
        "zorder":1000,
    }

    xmin,xmax=ax.get_xlim()
    ymin,ymax=ax.get_ylim()

    text="PRELIMINARY"
    
    if ax.get_xscale()=="log":
        xmidpoint=(xmin*xmax)**0.5        
    elif ax.get_xscale()=="linear":
        xmidpoint=(xmin+xmax)/2
    else:
        print("The specified xscale is not an option...")

    if ax.get_yscale()=="log":
        ymidpoint=(ymin*ymax)**0.5        
    elif ax.get_yscale()=="linear":
        ymidpoint=(ymin+ymax)/2
    else:
        print("The specified yscale is not an option...")
        
    t=ax.text(xmidpoint,ymidpoint,text,**text_kwargs)

    r = fig.canvas.get_renderer()
    bb_ax=ax.get_tightbbox(r)    
    bb = t.get_window_extent(renderer=r)
    #transform to axis coordinates, 
    #(0, 0) is bottom left of the figure, 
    #and (1, 1) is top right of the figure.
    bb = Bbox(ax.transAxes.inverted().transform(bb))
    print(bb.width,bb.height)

#     while bb.width>bb_ax.width or bb.height>bb_ax.height:
    while bb.width>0.9 or bb.height>0.9:
        old_size=t.get_size()
        t.set_size(old_size-5)
        bb = t.get_window_extent(renderer=r)    
        bb = Bbox(ax.transAxes.inverted().transform(bb))
        
#     while bb.width<0.75*bb_ax.width or bb.height<0.75*bb_ax.height:
    while bb.width<0.8 or bb.height<0.8:
        old_size=t.get_size()
        t.set_size(old_size+5)
        bb = t.get_window_extent(renderer=r)
        bb = Bbox(ax.transAxes.inverted().transform(bb))

    print(bb.width,bb.height)
    return ax


def manage_number_axes(data_shape,figsize=None,nrows=None,ncols=None):

    """
    data_shape
        shape: 0-> plot ax
        shape: 1-> x or y
        shape: 2-> date in x or y    
    """
    
    if ncols==None and nrows==None:
        ncols=data_shape.shape[0]%2+data_shape.shape[0]//2
        nrows=data_shape.shape[0]%2+data_shape.shape[0]//2
        
        if data_shape.shape[0]==2:
            ncols=ncols+1
            nrows=nrows+1
            
    elif ncols!=None and nrows==None:
        nrows=data_shape.shape[0]%2+data_shape.shape[0]//2 + 1
        
        
    elif ncols==None and nrows!=None:
        ncols=data_shape.shape[0]%2+data_shape.shape[0]//2 + 1
        
    else:
        if nrows*ncols<data_shape.shape[0]:
            raise ValueError("number of rows and columns is lower than the data strings")

    print(nrows,ncols)
    if figsize==None:
        fig,axs=plt.subplots(nrows=nrows,ncols=ncols)
    else:
        fig,axs=plt.subplots(figsize=figsize,nrows=nrows,ncols=ncols)

    
    if data_shape.shape[0]==1:
        axs.plot(data_shape[0,0,:],data_shape[0,1,:],"X")
    else:
        naxes=0
        for ax_row in axs:
            if isinstance(ax_row,np.ndarray):
                for ax_col in ax_row:
                    if naxes>=data_shape.shape[0]:
                        ax_col.remove()
                    else:
                        ax_col.plot(data_shape[naxes,0,:],data_shape[naxes,1,:],"X")
                    naxes=naxes+1
            else:
                ax_row.plot(data_shape[i,0,:],data_shape[i,1,:],"X")
    
    return axs
    
