'''

Module for plotting the ET

'''

import matplotlib.pyplot as plt

from sys import exit as exit
from .ternary import ternary_axes_subplot
from .coordsentropic import *
from random import choice

#Auxiliar functions

def get_cmap(number):

    """
    Used for generating a set of random colors in order to differenciate the coordinates of each variable in the diagram. 
    A series of color maps can be applied (It will be randomly selected)

    > colors_markers = get_cmap(len(df.index))

    Parameters
    ----------
    number : Number of colours (1 per variable)

    Returns
    ----------
    colors : Returns a set of colors for creating the scatter plot (matplotlib.colors.LinearSegmentedColormap)

    """
    #cmaps = list(['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds','YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu','GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'])
    cmaps = list(['spring','summer','autumn','winter','cool','Wistia'])
    cmaps = list(['Wistia'])
    return plt.cm.get_cmap(choice(cmaps) , number)



def markers(n) :
    
    #filled_markers = ('o', '*','+', 'x','D') ; mk = list()
    #filled_markers = ('o','D','h') ; mk = list()
    filled_markers = ('o') ; mk = list()
    for i in range(n) : mk.append(choice(filled_markers))
    return mk

def varnames (li):
    return dict((name,eval(name)) for name in li )
    
    
    
def entriangle (edf,names = None, scale = 100 , fonts = 30 ,s_mk = 200 
                     ,gridl = 20 , ticks_size = 15 , pltscale = 20, 
                     chart_title = ""):
    
    """
    Function for creating and plotting points of the entropy triangle, independentlly of the type of triangle (CBET, SMET or CMET)

    > entropytriangle(edf,names = None, scale = 100 , fonts = 30 ,s_mk = 200 
                     ,gridl = 20 , ticks_size = 15 , pltscale = 20, 
                     chart_title = ""):

    Parameters
    ----------
    edf : Dataframe with the entropic measures calculated
    names : Used for plotting a list of Daframes (Defalut = NONE) 
            In case of list: Names of the dataframes (if empty, some names will be provided for the plotting)
    scale : Scale for the entropy triangle
    fonts : Fontsize of the Labels
    s_mk : Size of the marks for the triangle
    gridl : Space between each gridline
    tick_size: size of the numbers for the ticks
    pltscale : Scale of the matplotlib window
    chart_title: Plot´s title
    

    Returns
    ----------
    points : painted points 
    Shows the triangle
    
    """

    if(not isinstance(edf,pd.DataFrame)):
            exit("Can only work with Data Frames or lists of DataFrames! (df it´s not a DataFrame)")
               
    points = entcoords(edf, scale)

    #SMET PLOT
    if(hasSplitSmetCoords(edf) or hasAggregateSmetCoords(edf) or hasDualAggregateSmetCoords(edf)):

        figure, tax = ternary_axes_subplot.figure(scale=scale,angle = -60)
        figure.set_size_inches(pltscale, pltscale)
        tax.boundary(linewidth=2.0)
        tax.gridlines(multiple = gridl, color="blue")
    
        colors = get_cmap(len(edf.index)) ; names = list(edf.index)
        mk = markers(1)*len(edf)
        
        for i in range(len(edf.index)):
            tax.scatter(points[i:i+1], s = s_mk, marker = mk[i], color = colors(i), label = names[i] ,edgecolor='black', linewidth='0.5')

        if (hasSplitSmetCoords(edf)):

            if(chart_title != ""):
                tax.set_title(chart_title, fontsize = fonts + 5)
            else:
                tax.set_title("Source Multivariate split entropies (SMET)", fontsize = fonts + 5)
            tax.left_axis_label(r"$\Delta H'_{P_{X_i}}$", fontsize=fonts)
            tax.right_axis_label(r"$ M'_{P_{X_i}}$", fontsize=fonts)
            tax.bottom_axis_label(r"$ H'_{P_{X_i|X_i^c}}$", fontsize=fonts)

        elif (hasAggregateSmetCoords(edf)):

            if(chart_title != ""):
                tax.set_title(chart_title, fontsize = fonts + 5)
            else:
                tax.set_title("Aggregate Source Multivariate entropies (SMET)", fontsize = fonts + 5)
            tax.left_axis_label(r"$\Delta H'_{Pi_{X}}$", fontsize=fonts)
            tax.right_axis_label(r"$ M'_{P_{X}}$", fontsize=fonts)
            tax.bottom_axis_label(r"$ VI'_{P_{X}}$", fontsize=fonts)

        elif (hasDualAggregateSmetCoords(edf)):

            if(chart_title != ""):
                tax.set_title(chart_title, fontsize = fonts + 5)
            else:
                tax.set_title("Dual Aggregate Source Multivariate entropies (SMET)", fontsize = fonts + 5)
            tax.left_axis_label(r"$\Delta H'_{P_{X}}$", fontsize=fonts)
            tax.right_axis_label(r"$ D'_{P_{X}}$", fontsize=fonts)
            tax.bottom_axis_label(r"$ VI'_{P_{X}}$", fontsize=fonts)
    
    elif(hasCbetEntropicCoords(edf)):

        figure, tax = ternary_axes_subplot.figure(scale=scale)
        figure.set_size_inches(pltscale, pltscale)
        tax.boundary(linewidth=2.0)
        tax.gridlines(multiple = gridl, color="blue")

        mk = markers(1)*len(edf.index) ; colors = get_cmap(len(edf.index)) ; names = list(edf.index)
        
        for i in range(len(edf.index)):
            tax.scatter(points[i:i+1], s = s_mk , marker = mk[i], color = colors(i), label = names[i] ,edgecolor='black', linewidth='0.1')

        if(chart_title != ""):
            tax.set_title(chart_title, fontsize = fonts + 5)
        else:
            tax.set_title("Channel Bivariate entropy triangle (CBET)", fontsize = fonts + 5)
        tax.left_axis_label(r"$ VI_{P_{XY}}$", fontsize=fonts)
        tax.right_axis_label(r"$ MI_{P_{XY}}  $", fontsize=fonts)
        tax.bottom_axis_label(r"$\Delta H_{P_{X}\cdot{P_{Y}}}$", fontsize=fonts)


    #CMET PLOT
    elif(hasCmetEntropicCoords(edf)):

        figure, tax = ternary_axes_subplot.figure(scale=scale)
        figure.set_size_inches(pltscale, pltscale)
        tax.boundary(linewidth=2.0)
        tax.gridlines(multiple = gridl, color="blue")

        mk = markers(len(edf.index)) ; colors = get_cmap(len(edf.index)) ; names = list(edf.index)
        for i in range(len(edf.index)):
            tax.scatter(points[i:i+1], s = s_mk , marker = mk[i], color = colors(i), label = names[i] ,edgecolor='black', linewidth='0.3')

        if(chart_title != ""):
            tax.set_title(chart_title, fontsize = fonts + 5)
        else:
            tax.set_title("Channel Multivariate entropies (CMET)", fontsize = fonts + 5)
        tax.left_axis_label(r"$ VI'_{P_\overline{XY}}$", fontsize=fonts)
        tax.right_axis_label(r"$ 2\cdot{I'_{P_\overline{XY}}}  $", fontsize=fonts)
        tax.bottom_axis_label(r"$\Delta H'_{P_\overline{XY}}$", fontsize=fonts)

    else: 
        
        exit("Entropic coordinates needed for the diagram plotting")

    tax.ticks(axis='lbr', linewidth=1, multiple = gridl , fontsize = ticks_size )
    tax.clear_matplotlib_ticks()
    tax.legend(title = 'Features' ,labelspacing = 1.5 , fontsize = 12)
    
    tax.show()
    
    return points

    
    
def entriangle_list(edf, names = None, scale = 100 , fonts = 30 ,s_mk = 200 , gridl = 20 , ticks_size = 15 , pltscale = 17, chart_title = ""):
    
    '''
    You can only pass list of aggregated entropies values.
    '''

    if(not isinstance(edf, list)):
        exit('This function only works with LISTS of Dataframes, maybe you can try the etplot function for an individual DataFrame plot')
    
    if(not all(isinstance(edf[x],pd.DataFrame) for x in range(len(edf)))):
        exit('All values must be instances of DataFrames for entropy calculations')
        
    if(not names):
        warning('No names founded, Providing Dummy names')
        names = list(map(lambda x: "Knn"+str(len(edf)-x)+"PC", range(len(edf))))
     
    if(all(hasCbetEntropicCoords(edf[l]) for l in range(len(edf)))):
        
        figure, tax = ternary_axes_subplot.figure(scale=scale)
        figure.set_size_inches(pltscale, pltscale)
        tax.boundary(linewidth=2.0)
        tax.gridlines(multiple = gridl, color="blue")
        
        name = names
        colors = get_cmap(len(edf)); mk = markers(1)*len(edf) #mk = markers(1)*len(edf[i].index)
        for i in range(len(edf)):
            points = entcoords(edf[i], scale)
            #mk = markers(1)*len(edf[i].index) ; 
            name = str(names[i])
            for j in range(len(edf[i].index)):
                tax.scatter(points[j:j+1], s = s_mk , marker = mk[j], color = colors(i), label = name ,edgecolor='black', linewidth='0.3')

        if(chart_title != ""):
            tax.set_title(chart_title, fontsize = fonts + 5)
        else:
            tax.set_title("Channel Bivariate entropy triangle (CBET)", fontsize = fonts + 5)
        tax.left_axis_label(r"$ VI_{P_{XY}}$", fontsize=fonts)
        tax.right_axis_label(r"$ MI_{P_{XY}}  $", fontsize=fonts)
        tax.bottom_axis_label(r"$\Delta H_{P_{X}\cdot{P_{Y}}}$", fontsize=fonts)
    
    elif(all(hasCmetEntropicCoords(edf[l]) for l in range(len(edf)))):

        figure, tax = ternary_axes_subplot.figure(scale=scale)
        figure.set_size_inches(pltscale, pltscale)
        tax.boundary(linewidth=2.0)
        tax.gridlines(multiple = gridl, color="blue")
        
        marker = list(['o','h','D', 's','d','v','^'])
        #marker = list(['v','^', '<','>'])
        colors = get_cmap(len(edf[0].index))
        
        for i in range(len(edf)): 
            points = entcoords(edf[i], scale)
            mk = marker[i]*len(edf[i].index) ; names = list(edf[i].index+'-FT-'+str(len(edf)-i)+'-PC')
            
            for j in range(len(edf[i].index)):
                tax.scatter(points[j:j+1], s = s_mk , marker = mk[j], color = colors(j), label = names[j] ,edgecolor='black', linewidth='0.4')

        if(chart_title == ""):
            tax.set_title("Aggregate Channel Multivariate entropies (CMET)", fontsize = fonts + 5)
        else:
            tax.set_title(chart_title, fontsize = fonts + 5)
            
        tax.left_axis_label(r"$ VI'_{P_\overline{XY}}$", fontsize=fonts)
        tax.right_axis_label(r"$ 2\cdot{I'_{P_\overline{XY}}}  $", fontsize=fonts)
        tax.bottom_axis_label(r"$\Delta H'_{P_\overline{XY}}$", fontsize=fonts)


    tax.ticks(axis='lbr', linewidth=1, multiple = gridl , fontsize = ticks_size )
    tax.clear_matplotlib_ticks()
    tax.legend(title = 'Features' ,labelspacing = 1.5 , fontsize = 12)
    
    tax.show()



