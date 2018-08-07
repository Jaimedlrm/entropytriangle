import sys                          #' Sys.Exit 
import warnings                     #' Warnings 

import numpy as np                  #' Numpy 
import pandas as pd
import scipy as sc                #' DataFrames manipulation
import operator
#import itertools

from itertools import product
from random import choice 
from sklearn.preprocessing import LabelEncoder   #' Used for discretization

from functools import reduce


def discretization (df , nbins = 1):


    if(not isinstance(df,pd.DataFrame)):
        sys.exit("Can only work with Data Frames!")
    #' Rows or columns equal to zero?
    if (len(df.columns) == 0 or len(df.index) == 0): 
        sys.exit("Can only work with non-empty Data Frames!")
    
    if(nbins == 1):
        nbins = int(len(df.index)*(1/3))
    print(nbins)
    lb = LabelEncoder()

    if (isinstance(nbins,np.int)):

        #Object -> String 
        #Numeric -> (Float o int)
        warnings.warn("Discretizing data!")

        df.update(df.select_dtypes(exclude = ['float64',np.int]).apply((lambda x : lb.fit_transform(x)), axis = 0))
        df.update(df.select_dtypes(include = ['float64',np.int]).apply((lambda x : pd.cut(x, bins = nbins , labels = list(range(nbins))))).astype('object'))

        disc = df.astype('category')

    else: 

        ##warning
        sys.exit("Number of bins for discretizing must be integer")

    return disc


def df2matrix(df, nb = 5):

    df = discretization(df,nb)
    li = list() ; dims = list() 

    df.apply((lambda x : dims.append(len(pd.unique(x)))))
    for i in range(len(df.columns)):li.append(pd.Series(df[df.columns[i]]))

    m = pd.crosstab(index = li[0:len(li)-1], columns = li[len(li)-1], dropna= False)
    matrix = m.as_matrix().reshape(dims)

    return matrix 



def expand_grid(data_dict):

    rows = product(*data_dict.values())
    return pd.DataFrame.from_records(rows, columns=data_dict.keys())

## d = {c: sorted(list(df[c].unique())) for c in df.columns} 


# Input a pandas series 
def ent(data , base = 2):
    
    p_data = data.value_counts()/len(data) # calculates the probabilities
    entropy = np.nan_to_num(sc.stats.entropy(p_data , base = base))  # input probabilities to get the entropy 
    
    return entropy


def sjoin(df,lis,sep=''):

    return reduce(lambda x, y: x.astype(str).str.cat(y.astype(str), sep=sep),[df[col] for col in lis])


def condentropies(df, base = 2):


    cond = list() ; ncol = df.columns
    total = ent(sjoin(df,lis = ncol),base = base)
    for i in range(len(df.columns)): 
        cond.append(total - ent(sjoin(df, lis = ncol[ncol != ncol[i]])))

    return cond 

"""
def condentropy_df(X,Y,base = 2):

    cond = list(); 
    joint = pd.merge(X, Y, left_index = True, right_index = True) ; ncol = joint.columns
    ejoint = ent(sjoin(joint,lis = joint.columns),base = base)
    for i in range(len(X.columns)): 
        cond.append(ejoint - ent(sjoin(joint, lis = ncol[ncol != ncol[i]])))
    return cond
"""

def condentropy_df(X,Y,base = 2):

    joint = pd.merge(X, Y, left_index = True, right_index = True)
    cond = ent(sjoin(joint,lis = joint.columns),base = base) - ent(sjoin(Y,lis = Y.columns),base = base)
    
    return cond


    