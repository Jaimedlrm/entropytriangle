import sys                          #' Sys.Exit 
import warnings                     #' Warnings 

import numpy as np                  #' Numpy 
import pandas as pd
import scipy as sc                #' DataFrames manipulation

from .auxfunc import * 



def sentropies_table(Nxy,base = 2):

    """
    Source Entropy decomposition of a contingency matrix

    Given a contingency matrix, provide one row of entropy coordinates.

    Parameters
    ----------
    Nxy : Contingency matrix of the database for calculating the source entropies

    Base : The logarithm to be used in working out the sentropies (Default "log2")

     Returns
    -------
    edf : Pandas DataFrame containing the values of the entropies calculated

          For 2d contingency tables it will provide a single row
          For nd contingency tables (n>2) it will provide a set of rows of the Entropies calculated per dimension (x = rows , y = columns)

    """

    dims = Nxy.shape # dim is a tuple wiht dim[0] rows  and dim[1] columns

    if(len(dims) < 2 ): # dim less than 2
        sys.exit("Cannot process tables with less/more than 2 dimensions.")
    #'stop('Cannot process tables with less/more than 2 dimensions.')

    if(dims[0] < 2 | dims[1] < 2):
        sys.exit("Sentropies are not defined for distributions with a singleton domain.")
    #'stop('Sentropies are not defined for distributions with a singleton domain.')

    if (len(dims) == 2):

        Nx = Nxy.sum(axis = 1) ; Ny = Nxy.sum(axis = 0)
        Hx = sc.stats.entropy(Nx , base = base) ; Hy = sc.stats.entropy(Ny , base = base)
        Ux = np.log2(dims[0]) ; Uy = np.log2(dims[1])
        Hxy = sc.stats.entropy( Nxy.reshape(np.prod(dims)), base  = base)

        df = pd.DataFrame({'Name': ['XY'],'Ux': Ux,'Uy': Uy,'Hx': Hx,'Hy': Hy, 'Hxy': Hxy})
        df = df.set_index('Name')

    else:

        #axis  = 0 columns , axis = 1 rows 
        #When n dimensions ->>>> (n,n-1,n-2,....,0,1)

        dims = Nxy.shape
        Nx = Nxy.sum(axis = len(dims)-1)
        Ny = Nxy.sum(axis = len(dims)-2)
        Hx = np.nan_to_num(np.apply_along_axis(sc.stats.entropy,axis = len(Nx.shape)-1,arr = Nx))
        Hy = np.nan_to_num(np.apply_along_axis(sc.stats.entropy,axis = len(Nx.shape)-1,arr = Ny))
        Hx = np.append(Hx,[]) ; Hy = np.append(Hy,[])
        Ux = np.array([np.log2(dims[0])]*len(Hx)) ; Uy = np.array([np.log2(dims[0])]*len(Hy))
        Hxy = np.apply_along_axis(sc.stats.entropy,axis = 1, arr = Nxy.reshape(np.product(dims[0:-2]),np.product([dims[-2],dims[-1]])) )

        #DataFrame creation

        df = pd.DataFrame({'Ux': Ux,'Uy': Uy,'Hx': Hx,'Hy': Hy, 'Hxy': np.nan_to_num(Hxy)} , columns = ['Ux','Hx','Uy','Hy','Hxy'])
        df['Name'] = list(range(len(Hxy)))
        df = df.set_index('Name')


    return df




def sentropies_df(df, type = "total" , base = 2 , nbins = 1 ):

    """
    Source Entropy decomposition of a dataframe
    Given a dataframe, provide the dual or the aggregate entropy decomposition of the dataframe

    > edf = sentropies_table(df, base = 2)

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
        sys.exit("Can only work with Data Frames!")

    if(dims[1] == 0 or dims[0] == 0): 
        sys.exit("Can only work with non-empty DataFrames!")

    if (not(all(df.dtypes)=='category')):
        warnings.warn("Discretizing data from X DataFrame before entropy calculation!")
        df = discretization(df , nbins)

    H_Uxi = df.apply((lambda x : np.log2(len(pd.unique(x)))), axis = 0).values
    H_Pxi = df.apply(ent,axis=0).values

    if (dims[1]==1):

        warnings.warn("Single variable: providing only entropy")
        VI_Pxi = H_Pxi

    else:

        VI_Pxi = condentropies(df)

    if (type == "total") : # TOTAL decomposition & Aggregates

        if (any(df.columns.isnull())):
            #' Delete names and append new ones
            warnings.warn("No names for columns: providing variable names!")
            #Apply dummy names 
            df.columns = list(map(lambda x: "x"+str(x), range(len(df.columns))))

        #DataFrame Creation
        edf = pd.DataFrame({'Name': list(df.columns) , 'H_Uxi': H_Uxi , 'H_Pxi':H_Pxi ,'DeltaH_Pxi': H_Uxi - H_Pxi ,'M_Pxi': H_Pxi - VI_Pxi , 'VI_Pxi': VI_Pxi}, columns = ['Name','H_Uxi','H_Pxi','DeltaH_Pxi','M_Pxi','VI_Pxi'])
        edf = edf.set_index('Name')
        edf.loc['All'] = edf.sum(axis = 0)


    else :  #return only an aggregate with the DUAL total correlation D_Px

        H_Ux = np.sum(H_Uxi)
        H_Px = ent(sjoin(df,lis = df.columns))
        VI_Px = np.sum(VI_Pxi)

        edf = pd.DataFrame({'Name' : ['All'] , 'H_Ux' : H_Ux , 'H_Px'  : H_Px , 'DeltaH_Px' : (H_Ux - H_Px) ,'D_Px' : H_Px - VI_Px , 'VI_Px' : VI_Px }, columns = ['Name','H_Ux','H_Px','DeltaH_Px','D_Px','VI_Px'])
        edf = edf.set_index('Name')

    return edf




