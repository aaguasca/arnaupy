import numpy as np
import math
from astropy.table import Table

__all__=[
    "closest_distance",
    "normalization",
    "read_parameters_table",
    "significant_digits",
]

class significant_digits:
    """
    Script to round the input value using the rounding rules
    in experimental physics. The output value displays the number 
    of significant figures specified in the run method.    
    """
    
    def __init__(self,value,error_value=None):
        """
        Parameters
        ----------
        value: int, float
            Value to round
        error_value: int, float
            Value of the uncertainity of the value to round
        """
        self.value=value
        self.error_value=error_value
        self.add_zero=0
                                        
    def rounding_of_one(self, val, first_two_significant_figures):
        """
        If the first significant figure of the value is a one, 
        display the second significant figure as well.
        For some cases, a zero is added after rounding because of 
        the the first significant digit changes from 1 to 2 because
        the second significant digit has been rounded from 9 to 10.
        The zero from 10 is information needed.
        
        Parameters
        ----------
        val: int, float
            Value to round.
        first_two_significant_figures: float
            Value to round with the first and second significant figure
            divided by the decimal point
            
        Returns
        -------
        val: str
            Value of val rounded
        """
        # keep on more digit
        if self.n_zero_decimals!=0:
            self.n_zero_decimals=int(self.n_zero_decimals+np.sign(self.n_zero_decimals)*1)
        else:
            self.n_zero_decimals=self.n_zero_decimals+1
            self.add_zero=1
        self.precision+=1
        #keep the second significant figure
        round_val=round(first_two_significant_figures,1)

        #if the after rounding changes from 1 to 2, add 0 afterwards
        if int(first_two_significant_figures)!=int(round_val):
            # values higher than 1, e.g. 1, 10, 100, 1000, ...
            if self.n_zero_decimals>=1:
                val=10**self.n_zero_decimals*round(
                    val/10**self.n_zero_decimals,self.precision
                )

                #keep the digit after the decimal point for values ex 1.X
                if self.n_zero_decimals==1:
                    val=float(np.round(val,10))
                #the decimal point is not needed
                else:
                    val=int(np.round(val,10))
            #for the decimal values (< 1), add extra zero afterwards
            else:
                val=10**self.n_zero_decimals*round(val/10**self.n_zero_decimals)                                
                val=str(val)+"0"

        #round keeping the second significant figure
        else:
            val=10**self.n_zero_decimals*round(
                val/10**self.n_zero_decimals,self.precision
            )
            val=np.round(val,10)
            if self.n_zero_decimals>1:
                val=int(val)
        
        val = str(val)
        return val
    

    def rounding(self, val, first_two_significant_figures):
        """
        Rounding the value val using the first_two_significant_figures 
        variable, which is the value with the first and second 
        significant figure as a unit and a decimal, respectively.
        
        Rounding off is considered when the second digit is a 5 to avoid 
        the issue of rounding up for 5 or more. Then, if the first 
        significant figure is odd, the value is round up, else, round off.
        
        Also, the rounding from 9 to 10 keeps the 0 from the 10 since
        it is important information that cannot be excluded.
        
        Parameters
        ----------
        val: int, float
            Value to round.
        first_two_significant_figures: float
            Value to round with the first and second significant figure
            divided by the decimal point
            
        Returns
        -------
        val: str
            Value of val rounded        
        """        
        # keep the second significant figure it is a 9, 
        # since the round of 9 is not zero but ten!
        if int(first_two_significant_figures)==9 and \
            int(first_two_significant_figures)!=int(round(val*10**(-(self.digits-1)))):
            val=round(val,self.n_zero_decimals)
            val=str(val)+"0"

        #rounding off with a 5 as a second digit
        elif int(round(np.modf(first_two_significant_figures)[0],5)*10)==5:

            # if even the first significant figure, do not round
            if (int(np.modf(first_two_significant_figures)[1])%2)==0:
                #round last significant digit
                val=int(val*10**(-(self.digits-1))) * 10**(self.digits-1)
                val=np.round(val,10) 
                if self.precision == 2:
                    val=str(val)+"0"

            # if odd the first significant figure, round                
            else:                
                val=10**self.n_zero_decimals*round(
                    np.ceil(first_two_significant_figures) * \
                    10**self.n_zero_decimals/10**self.n_zero_decimals
                )
                val=np.round(val,10)
                if self.precision == 2:
                    val=str(val)+"0"  
                    
        #usual rounding
        else:
            val=10**self.n_zero_decimals*round(val/10**(self.n_zero_decimals))

            # for example, cases where the error value is 1.3 and you 
            # want the value of 200 to be "200.0" to match the error 
            # value digits
            if self.n_zero_decimals==1 and self.precision==2:
                val=float(np.round(val,10))
            else:
                val=np.round(val,10)

        val=str(val)
        return val
    
        
    def run(self,precision=1):
        """
        Run the script to round the value (and its uncertainty)
        using a certain precision.
        
        Parameters
        ----------
        precision: int
            Number of significant figures to display
            
        Returns
        -------
        value: str
            Value of value rounded     
        error_value: str
            Uncertainty value rounded     
        
        """
        
        #consider the significant figures of the error value
        if self.error_value!=None:
        
            if self.error_value!=0:
                self.digits = int( np.ceil( math.log10( abs( self.error_value ) ) ) )
            else:
                raise ErrorValue("Uncertainty is zero!")
                
            self.precision=precision
            self.n_zero_decimals=self.digits - self.precision

            #take the two first significant figures with the second as a decimal
            first_two_significant_err_figures=self.error_value*10**(-self.digits+1)
        
            #first significant digit is 1
            if int(first_two_significant_err_figures)==1:
                self.error_value = self.rounding_of_one(
                    self.error_value, first_two_significant_err_figures
                )
            else:
                self.error_value = self.rounding(
                    self.error_value, first_two_significant_err_figures
                )
                
            #round of the value
            #take the two first significant figures with the second as a decimal
            first_two_significant_value_figures = round(
                self.value*10**(-(self.n_zero_decimals-self.add_zero+self.precision-1)),
                10
            )
            self.value = self.rounding(self.value, first_two_significant_value_figures)
                            
        else:
            if self.value!=0:
                self.digits = int( np.ceil( math.log10( abs( self.value ) ) ) )
            else:
                raise ErrorValue("Uncertainty is zero!")
            
            self.precision = precision
            self.n_zero_decimals = self.digits - self.precision

            # values > 10 makes not sense to round
            if self.digits <= 1:
                #take the two first significant figures with the second as a decimal
                first_two_significant_value_figures = round(
                    self.value*10**(-(self.n_zero_decimals-self.add_zero+self.precision)),
                    10
                )

                #first significant digit is 1
                if int(first_two_significant_value_figures)==1:
                    self.value = self.rounding_of_one(
                        self.value, first_two_significant_value_figures
                    )
                else:
                    self.value = self.rounding(
                        self.value, first_two_significant_value_figures
                    )
            else:
                print("No rounding because the value is > 10")
                
        return self.value, self.error_value

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


def read_parameters_table(path,n):
    """
    Read table with several parameters required to compute
    the last n columns of the table.
    
    The parameters are ordered from shorter parameter values
    to longer ones.
    
    Parameters
    ----------
    path: string
        Path to table.
    n: int
        Number of columns that are the results of using the parameters 
        in the columns 0,..,n-1 of the table.
        
    Returns
    -------
    axes_values: list
        List with the variables values ordered from shorter parameter
        values to longer ones.
    final_data: list
        List with the n column parameters. The dimension of the returned
        list is as follows:
        - first dimension: the n column values
        - second to n-1 dimension: the rehsaped parameter values size
          with unrepeated parameter values.
          
    example 1:
    variables: x,y,z. x,y,z=np.arange(10)
    parametrization of the results: r=\sum_i,j,k x_i+y_j+z_k for all i,j,k
    axes_values=[x,y,z]
    final_data dimension: (1,10,10,10)
    example 2:
    variables: x,y,z. x,y,z=np.arange(10)
    parametrization of the results: r1=\sum_i x_i+y_i+z_i and r2=\sum_i x_i*y_i*z_i for all i
    axes_values=[x,y,z]
    final_data dimension: (2,10)
    """
    
    tab=Table.read(path, format='ascii')

    #dict with colname and unique values of the parameter variables
    col_values={}
    #size unique values for each colname of the parameter variables
    col_n_values=[]
    
    print(tab.colnames)
    #get the parameter values
    for col in tab.colnames[:-n]:
        unique_val=np.unique(tab[col])
        col_values[col]=unique_val
        col_n_values.append(len(unique_val))

    #sort size to have ascendent order
    arg_order_size=np.argsort(col_n_values)
    print(col_n_values)
    
    #obtain the names in sorted order
    axis_name_array=[]
    for i in arg_order_size:
        axis_name_array.append(list(col_values.keys())[i])

    #reshape the results to the shape based on the colname order
    data=[]
    for col in tab.colnames[-n:]:
        if len(tab[col].value)==np.prod(col_n_values):
            data.append(tab[col].value.reshape(col_n_values)*tab[col].unit)
        else:
            data.append(tab[col].value*tab[col].unit)
        
    #list with the sorted dim
    new_shape=[]
    #list with the values of each parameter, sorted order
    axes_values=[]
    for name in axis_name_array:
        new_shape.append(len(col_values[name]))
        axes_values.append(col_values[name])
        
    #arg of the name to exclude. To avoid swaping again
    skip_arg_name=1000
    
    print("old",col_values.keys())
    print("new",axis_name_array)
    print("new shape",new_shape)

    #swap the axes that are not ordered in the colname order
    new=new_shape
    
    #swap for all results
    for kk,dat in enumerate(data):    
        old=np.shape(dat) 
#         print(f"old shape {kk}",np.shape(dat))
        for i in range(len(old)):
            if old[i]!=new[i]:
                #avoid repeating the same swap
                if i!=skip_arg_name:
                    arg_name=np.argwhere(np.array(new)==old[i])[0][0]
#                     print(i,arg_name)
                    data[kk]=np.swapaxes(dat,i,arg_name)
                    skip_arg_name=arg_name

    final_data=data
    print("final shape",np.shape(final_data))
    return axes_values,final_data
