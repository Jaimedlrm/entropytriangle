'''

Functions used for calculating entropic measures (SMET Triangle)

'''

from sys import exit as exit
from warnings import warn as warning
from scipy.stats import entropy as entropy

from .auxfunc import * 


def sentropies(df, type = "total" , base = 2 , nbins = 1 ):

    """
    Source Entropy decomposition of a dataframe
    Given a dataframe, provide the dual or the aggregate entropy decomposition of the dataframe

    > edf = sentropies_df(df, type = 'total, base = 2, nbins = 1)

    Parameters
    ----------
    df : DataFrame for calculating the source entropies
    base : The logarithm to be used in working out the sentropies (Default base = 2 -> "log2")

    Returns
    ----------
    edf : Pandas DataFrame containing the values of the entropies calculated

    if the type = "total" then the function calculates the Total Decomposition & Aggregates
    else if  type = "dual" then it will calculate the dual Decomposition & Aggregates

    """

    dims = df.shape

    if(not isinstance(df,pd.DataFrame)):
        exit("Can only work with Data Frames!")

    if(dims[1] == 0 or dims[0] == 0): 
        exit("Can only work with non-empty DataFrames!")
    
    if (not(all(df.dtypes=='category'))):
        warning("Discretizing data from X DataFrame before entropy calculation!")
        df = discretization(df , nbins)

    H_Uxi = df.apply((lambda x : np.log2(len(pd.unique(x)))), axis = 0).values
    H_Pxi = df.apply(ent,axis=0).values

    if (dims[1]==1):

        warnings.warn("Single variable: providing only entropy")
        VI_Pxi = H_Pxi

    else:
        
        VI_Pxi = list()
        for i in range(len(df.columns)):
            VI_Pxi.append(condentropy(df[df.columns[i]],df[df.columns.drop(df.columns[i])]))
        
        
    if (type == "total") : # TOTAL decomposition & Aggregates

        if (any(df.columns.isnull())):
            #' Delete names and append new ones
            warning("No names for columns: providing variable names!")
            #Apply dummy names 
            df.columns = list(map(lambda x: "x"+str(x), range(len(df.columns))))

        #DataFrame Creation
        edf = pd.DataFrame({'Name': list(df.columns) , 'H_Uxi': H_Uxi , 'H_Pxi':H_Pxi ,'DeltaH_Pxi': H_Uxi - H_Pxi ,'M_Pxi': H_Pxi - VI_Pxi , 'VI_Pxi': VI_Pxi}, columns = ['Name','H_Uxi','H_Pxi','DeltaH_Pxi','M_Pxi','VI_Pxi'])
        edf = edf.set_index('Name')
        edf.loc['AGGREGATE'] = edf.sum(axis = 0)


    else :  #return only an aggregate with the DUAL total correlation D_Px

        H_Ux = np.sum(H_Uxi)
        H_Px = ent(sjoin(df,lis = df.columns))
        VI_Px = np.sum(VI_Pxi)

        edf = pd.DataFrame({'Name' : ['AGGREGATE'] , 'H_Ux' : H_Ux , 'H_Px'  : H_Px , 'DeltaH_Px' : (H_Ux - H_Px) ,'D_Px' : H_Px - VI_Px , 'VI_Px' : VI_Px }, columns = ['Name','H_Ux','H_Px','DeltaH_Px','D_Px','VI_Px'])
        edf = edf.set_index('Name')

    return edf