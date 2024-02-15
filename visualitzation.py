import numpy as np
import matplotlib.pyplot as plt
from .utils import significant_digits
from matplotlib.transforms import Bbox
import matplotlib
import string
import astropy.units as u

__all__=[
    "update_2cool_rcParams",
    "plot_parameter_value",
    "add_panel_labels",
    "plot_preliminary_text",
    "manage_number_axes",
]

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
    

def plot_parameter_value(fig,ax,latex_symbol,value,loc="lower left",value_error=None, **kwargs):
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
    kwargs
        Kwargs passed to ax.text
    
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
    
    text_kwargs.update(kwargs)
    
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


def add_panel_labels(fig,label_style="alphabet",loc="lower left", **kwargs):
    """
    Plot the label of the plots in a panel.
    
    Parameters
    ----------
    fig: matplotlib.pyplot.figure
        Figure
    label_style: str
        Style of the label of the pannels: options; alphabet: use alphabetical order.
        numbers: use numbers. Else, specify yourself the labels.
    loc: string
        Location of the equation in the plot.
    kwargs
        Kwargs passed to ax.text
    
    """
    
    axs_list = fig.axes
    
    if label_style=="alphabet":
        alphabet = list(string.ascii_lowercase)
        label_list = alphabet[:len(axs_list)]
    elif label_style=="numbers":
        label_list = np.arange(len(axs_list))
    else:
        try:
            if len(label_style) == len(axs_list):
                label_list=label_style
        except:
            raise ValueError("The dimension of label_style is not the same to the number of plots.")
                               
    text_kwargs={
        "horizontalalignment":'center',
        "verticalalignment":'center',
        "zorder":1000,
    }    
                               
    text_kwargs.update(kwargs)
                               
                               
    for text_print,ax in zip(label_list,axs_list):
    
        xmin,xmax=ax.get_xlim()
        ymin,ymax=ax.get_ylim()

        dx=xmax-xmin
        dy=ymax-ymin

        t=ax.text(0.1,0.1,text_print, **text_kwargs)
        r = fig.canvas.get_renderer()

        bbox_text=t.get_window_extent(r)
        bbox_ax=ax.get_window_extent(r)

        frac_hor_size_t=bbox_text.width/bbox_ax.width
        frac_ver_size_t=bbox_text.height/bbox_ax.height

        x_interval=1/10
        y_interval=1/10


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
        "zorder":0,
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
        shape: 0-> array with the dimension equal to the number of axes to plot
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

    naxes=0
    for ax_row in axs:
        if isinstance(ax_row,np.ndarray):
            for ax_col in ax_row:
                if naxes>=data_shape.shape[0]:
                    ax_col.remove()
                naxes=naxes+1
        
    axs=axs.flatten()
    return fig, axs    

def correct_display_flux_units(flux_units):
    """
    Function to return units of an integral or differential flux in
    The usual way the units of the flux are defined: energy per cm-2 s-1.

    Parameters
    ----------
    flux_units: astropy.unit
        Units of the flux

    Returns
    -------
    units_string: str
        Units in latex_inline format of the flux

    """

    units_string=flux_units.to_string("latex_inline")

    # split the string to get a list with the units (ex in one index: s^{-1})
    split_units=units_string.split("\\mathrm{")[1].split("}$")[0].split("\,")

    #obtain the power of the energy
    for iunit,ipow in zip(split_units,flux_units.powers):
        if u.Unit(iunit.split("^")[0]).is_equivalent("erg"):
            energy_power=ipow

    if flux_units.is_equivalent(u.Unit(f"erg{energy_power} cm-2 s-1")):

        if energy_power!=0:
            units_to_check_order=[f"erg{energy_power}","cm-2", "s-1"]
        else:
            units_to_check_order=["cm-2", "s-1"]

        # fill a list with the order we want
        correct_unit_order=[]
        for i_u in units_to_check_order:
            for iunit,ipow in zip(split_units,flux_units.powers):
                new_iunit=u.Unit(iunit.split("^")[0])**ipow
                if u.Unit(f"{new_iunit}").is_equivalent(f"{i_u}"):
                    correct_unit_order.append(iunit)

        # write again the string with the correct order
        if energy_power!=0:
            units_string="$\\mathrm{"+correct_unit_order[-3]+"\\,"+correct_unit_order[-2]+"\\,"+correct_unit_order[-1]+"}$"
        else:
            units_string="$\\mathrm{"+correct_unit_order[-2]+"\\,"+correct_unit_order[-1]+"}$"

        return units_string

    else:
        raise Exception("The units provided are not equivalent to E^power cm-2 s-1")
