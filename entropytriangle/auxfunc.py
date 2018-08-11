'''

Auxiliar functions used in the calculation of the Measures

'''

import numpy as np                  
import pandas as pd
import operator

from sys import exit as exit
from warnings import warn as warning
from scipy.stats import entropy as entropy
from itertools import product
from random import choice 
from sklearn.preprocessing import LabelEncoder   #' Used for discretization
from functools import reduce


def discretization (df , nbins = 1):


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


def df2matrix(df, nb = 1):

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
    entr = np.nan_to_num(entropy(p_data , base = base))  # input probabilities to get the entropy 
    
    return entr


def sjoin(df,lis,sep=''):

    return reduce(lambda x, y: x.astype(str).str.cat(y.astype(str), sep=sep),[df[col] for col in lis])



def condentropy(df, base = 2):


    cond = list() ; ncol = df.columns
    total = ent(sjoin(df,lis = ncol),base = base)
    for i in range(len(df.columns)): 
        cond.append(total - ent(sjoin(df, lis = ncol[ncol != ncol[i]]),base = base))

    return cond 


def condentropy_joint(X,Y,base = 2):
    
    joint = pd.merge(X, Y, left_index = True, right_index = True)
    cond = ent(sjoin(joint,lis = joint.columns),base = base) - ent(sjoin(Y,lis = Y.columns),base = base)
    
    return cond

#VARIATION WITH MERGING IN EVERY CONDENTROPY CALCULATION

'''
def condentropy(df, base = 2):


    cond = list() ; ncol = df.columns
    #total = ent(sjoin(df,lis = ncol),base = base)
    for i in range(len(df.columns)): 
        new = pd.merge(df[ncol[ncol != ncol[i]]],pd.DataFrame(df[ncol[i]]),left_index=True , right_index= True)
        total = ent(sjoin(new, lis = new.columns),base =2)
        cond.append(total - ent(sjoin(df, lis = ncol[ncol != ncol[i]]),base = base))

    return cond 

'''


#Deprecated

'''

def condentropy_df(X,Y,base = 2):

    cond = list(); 
    joint = pd.merge(X, Y, left_index = True, right_index = True) ; ncol = joint.columns
    ejoint = ent(sjoin(joint,lis = joint.columns),base = base)
    for i in range(len(X.columns)): 
        cond.append(ejoint - ent(sjoin(joint, lis = ncol[ncol != ncol[i]])))
    return cond

'''
