'''

Functions used for calculating entropic measures (CMET Triangle)

'''

from sys import exit as exit
from warnings import warn as warning
from scipy.stats import entropy as entropy

from .auxfunc import * 


def jentropies(X,Y , base = 2 , nbins = 1):

    """
    Channel Entropy decomposition of two dataframes X and Y

    > edf = jentropies_df (X,Y, base = 2)

    Parameters
    ----------
    X, Y : DataFrame for calculating the channel entropies
    base : The logarithm to be used in working out the sentropies (Default base = 2 -> "log2")

    Returns
    ----------
    edf : Pandas DataFrame containing the entropic values of input Frames

    """

    dimx = X.shape ; dimy = Y.shape
    
    if(not isinstance(X,pd.DataFrame)):
        exit("Can only work with Data Frames! (X it´s not a DataFrame)")
    
    if(not isinstance(Y,pd.DataFrame)):
        exit("Can only work with Data Frames! (Y it´s not a DataFrame)")   
    
    if (dimx[0] == 0 or dimx[1] == 0):
        exit("Can only work with non-empty data.frames X!")

    if (dimy[0] == 0 or dimy[1] == 0):
        exit("Can only condition on non-empty data.frame Y!")

    if (dimx[0] != dimy[0]):	
        exit("Can only condition on variable lists with the same number of instances!")

    if (not(all(X.dtypes)=='category')):
        warning("Discretizing data from X DataFrame before entropy calculation!") #' Throwing a Warning for communicating a discretization of data
        X = discretization(X , nbins)

    if (not(all(Y.dtypes)=='category')):
        warning("Discretizing data from X DataFrame before entropy calculation!") #' Throwing a Warning for communicating a discretization of data
        Y = discretization(Y , nbins)

    H_U = np.array([np.sum(X.apply((lambda x : np.log2(len(pd.unique(x)))), axis = 0).values) , np.sum(Y.apply((lambda x : np.log2(len(pd.unique(x)))), axis = 0).values)])
    H_P = np.array([ent(sjoin(X,lis = X.columns)),ent(sjoin(Y,lis = Y.columns))])
    
    #Calculation of Conditional Entropies of the Random Vectors
    VI_P = np.array([condentropy(X,Y,base = base),condentropy(Y,X,base = base)])
    
    edf = pd.DataFrame({'Type' : ['X','Y'], 'H_U': H_U , 'H_P': H_P , 'DeltaH_P' : H_U - H_P, }, columns = ['Type','H_U','H_P','DeltaH_P'])
    edf['M_P'] = H_P - VI_P
    edf['VI_P'] = VI_P
    edf = edf.set_index('Type')
    edf.loc['XY'] = edf.sum(axis = 0)

    return edf


def jentropies_binary(Nxy, base = 2):

    """
    Joint Entropy decomposition of a 2d contingency matrix due to a channel transmission

    > edf = jentropies_binary (Nxy, base = 2)

    Parameters
    ----------
    Nxy : Contingency matrix for calculating the channel entropies
    base : The logarithm to be used in working out the sentropies (Default base = 2 -> "log2")

    Returns
    ----------
    edf : Pandas DataFrame containing the entropic values of input Frames

    """

    dims = Nxy.shape # dim is a tuple wiht dim[0] rows  and dim[1] columns

    if(len(dims) != 2):
        exit("It must be a 2 dimensions array")

    Nx = Nxy.sum(axis = 1) ; Ny = Nxy.sum(axis = 0) 
    Hx = entropy(Nx , base = base) ; Hy = entropy(Ny , base = base)
    Ux = np.log2(dims[0]) ; Uy = np.log2(dims[1])
    Hxy = entropy(np.ravel(Nxy),base = base)
    VI_P = [(Hxy-Hy),(Hxy-Hx)]

    edf = pd.DataFrame({'Type':['X','Y'],'H_P2':[Hx,Hy] , 'H_U2' : [Ux,Uy] ,'DeltaH_P2':[(Ux - Hx) , (Uy - Hy)] , 'M_P2': [Hx - VI_P[0] , Hy - VI_P[1]] , 'VI_P2': VI_P }, columns = ['Type','H_U2','H_P2','DeltaH_P2','M_P2','VI_P2'])
    edf = edf.append(edf.apply(lambda x: np.sum(x,axis=0),axis = 0), ignore_index=True)
    #edf.loc['All'] = edf.sum(axis = 0)
    edf = edf.set_index('Type')

    return edf
