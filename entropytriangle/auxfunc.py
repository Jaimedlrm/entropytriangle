'''

Auxiliar functions used in the calculation of the Measures

'''

import numpy as np                  
import pandas as pd
import operator

from sys import exit as exit
from warnings import warn as warning
from scipy.stats import entropy as entropy
from sklearn.preprocessing import LabelEncoder   #' Used for discretization
from functools import reduce


def discretization (df , nbins = 1):

    """
    Function created for the discretization of a dataframe in #nbins equalwidth bins

    > comprobation = discretization(df,nbins)

    Parameters
    ----------
    df : raw DataFrame 
    nbins : number of bins 

    Returns
    ----------
    df : Discretized Dataframe

    """


    if(not isinstance(df,pd.DataFrame)):
        exit("Can only work with Data Frames!")
    #' Rows or columns equal to zero?
    if (len(df.columns) == 0 or len(df.index) == 0): 
        exit("Can only work with non-empty Data Frames!")
    
    if(nbins == 1):
        nbins = int(len(df.index)**(1/3))

    if (not isinstance(nbins,np.int)):
        nbins = int(nbins)
    
    #Object -> String 
    #Numeric -> (Float o int)
    warning("Discretizing data!")
    lb = LabelEncoder()
    
    df.update(df.select_dtypes(exclude = ['float64',np.int]).apply((lambda x : lb.fit_transform(x)), axis = 0))
    df.update(df.select_dtypes(include = ['float64',np.int]).apply((lambda x : pd.cut(x, bins = nbins , labels = list(range(nbins))))).astype('object'))

    disc = df.astype('category')

    return disc


def sjoin(df,lis,sep=''):

    """
    Function created for merge all the colums of a DataFrame in one column

    > odf = sjoin(df,df.columns,'')

    Parameters
    ----------
    df : Raw DataFrame 
    lis: Columns to merge
    sep : Separator
    Returns
    ----------
    odf : Merged DataFrame

    """

    return reduce(lambda x, y: x.astype(str).str.cat(y.astype(str), sep=sep),[df[col] for col in lis])


def ent(data , base = 2):
    
    """
    Function created for calculating the entropy of a pandas Series

    > entropy = ent(df,base = 2)

    Parameters
    ----------
    df : Raw DataFrame 
    base : Logarithm base used for the entropy calculation (Default value equal 2)
    ----------
    entropy : Value (float)

    """
   
    if(isinstance(data, pd.DataFrame)):
        data = sjoin(data,lis = data.columns)

    p_data = data.value_counts()/len(data) # calculates the probabilities
    entr = np.nan_to_num(entropy(p_data , base = base))  # input probabilities to get the entropy 
    
    return entr



def condentropy(X,Y = None, base = 2):

    """
    Function created for calculating the conditional entropy of two dataframes
    Formula used from the R function condentropy
    https://rdrr.io/cran/infotheo/man/condentropy.html
    
    H(X|Y) = H(Y,X)-H(Y)
    
    > entropy_value = condentropy(X,Y,base)

    Parameters
    ----------
    X : DataFrame 
    Y : DataFrame
    base : Logarithm base used for the entropy calculation (Default value equal 2)
    ----------
    entropy_value : Value (float)

    """
    
    if(isinstance(Y, type(None))):
        Hres = ent(X,base = base)
        
    else:
        
        if(isinstance(Y, pd.Series)):
            Y = Y.to_frame(name = None)
        if(isinstance(X, pd.Series)):
            X = X.to_frame(name = None)
        
        joint = pd.merge(Y,X, left_index = True, right_index = True)
        Hyx = ent(joint,base = base)
        Hy = ent(Y,base = base) 
        
        Hres = Hyx - Hy
        
    return Hres

