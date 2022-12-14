import numpy as np
import math

def significant_digits(value,error_value):
    """
    Return the significant digits of value and error_value
    depending on the value and decimals of the error_value.
    
    Parameters
    ----------
    value: float
        Quantity one wants to represent showing only significant decimals based
        on the associated error value.
    value_error: float
        Error value associated to the quantity value.

    Returns
    -------
    value: float
        Rounded quantity value up to the significant decimal.
    error_value: float
        Rounded error associated to value up to the significant decimal.
    n_zero_decimals: int
        Number of decimals after zero.
    """    
    
    log_val=math.log10(error_value)
    digits=int(np.sign(log_val)*int(np.abs(log_val)))

    #for errors <=-0.1
    if digits<0:
#         print("A",(digits-1),np.sign(log_val),error_value*10**(-(digits-1)))

        #number of zeros to reach the first significant digit
        n_zero_decimals=np.abs((digits-1))
        
        #first significant digit is 1
        if int(error_value*10**(-(digits-1)))==1:
            error_value=round(error_value,n_zero_decimals+1)
        else:
            error_value=round(error_value,n_zero_decimals)
        
        #round last significant digit
        value=float(round(value,n_zero_decimals))


    elif int(digits)==0:

        #for errors between -0.1<x<0
        if np.sign(log_val)<0:
#             print("B1",(digits-1),np.sign(log_val),error_value*10**(-(digits-1)))

            #number of zeros to reach the first significant digit            
            n_zero_decimals=np.abs(int((digits-1)))

            #first significant digit is 1
            if int(error_value*10**(-(digits-1)))==1:
                error_value=round(error_value,n_zero_decimals+1)
            else:
                error_value=round(error_value,n_zero_decimals)

            #round last significant digit
            value=float(round(value,n_zero_decimals))

       #for errors between 0<=x<10
        else:
#             print("B2",(digits-1),np.sign(log_val),error_value,value)

            #number of zeros to reach the first significant digit            
            n_zero_decimals=0

            #round last significant digit
            value=round(value*10**(-(digits-1)-1),0)*10**((digits-1)+1)    
            value=int(value) 
            
            #first significant digit is 1
            if int(error_value)==1:
                error_value=round(error_value,1)

            else:  
                error_value=round(error_value,0)
                error_value=int(error_value)                

    #for errors x>10
    else:
#         print("C",(digits-1),np.sign(log_val),error_value*10**(-(digits-1)-1))
        
        #number of zeros to reach the first significant digit        
        n_zero_decimals=0
        
        #round last significant digit
        value=round(value*10**(-(digits-1)-1),0)*10**((digits-1)+1)  
        value=int(value)        
        
        #first significant digit is 1
        if int(error_value*10**(-(digits-1)-1))==1:
            error_value=round(error_value*10**(-(digits-1)),0)*10**((digits-1))
        else:
            error_value=round(error_value*10**(-(digits-1)-1),0)*10**((digits-1)+1)
        error_value=int(error_value)
          
    return value,error_value,n_zero_decimals


def normalization(x):
    """
    Normalize between 0 and 1 an array.
    
    Parameters
    ----------
    x: np.array
        Array to normalize between 0 and 1.

    Returns
    -------
    norm_x: np.array
        Normalized array.
    """
    
    x = np.array(x)
    norm_x = (x - np.min(x)) / (np.max(x) - np.min(x))
    
    return norm_x


def closest_distance(x,y,xo,yo,n):
    """
    search the closest non-repitiong points to xo and yo.
    
    Parameters
    ----------
    xo: float
        Value of the central point in the x axis.
    yo: float
        Value of the central point in the y axis.
    x: np.array
        list of values in the x axis to compare with xo.
    y: np.array
        list of values in the x axis to compare with yo.  
    n: int
        The number of n closest (x,y) points we are interested in.
    
    Returns
    -------
    bool_selected_node: np.array
        Boolean array with the "n" closest nodes as True
    """
    
    epsilon=1e-6
    for i in range(len(x)):
        for ii in range(len(x)):
            if np.abs(x[ii]-x[i])<epsilon and np.abs(y[ii]-y[i])<epsilon and ii!=i:
                x[ii]=None
                y[ii]=None  
    
    dist2_to_xoyo=np.zeros(shape=(len(x),len(xo)))
    arg_closer_node=np.zeros(shape=(n,len(xo)),dtype=int)
    bool_selected_node=np.zeros(shape=(len(x),len(xo)),dtype=bool)

    for i in range(len(xo)):
        dist2_to_xoyo[:,i]=((x-xo[i])**2+(y-yo[i])**2)
        arg_closer_node[:,i]=np.argsort(dist2_to_xoyo[:,i])[:n]
    
        for j in range(n):
            bool_selected_node[arg_closer_node[j,i],i]=True
            
    return bool_selected_node