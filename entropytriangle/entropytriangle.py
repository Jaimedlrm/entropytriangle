'''

Module for plotting the ET

'''


from sys import exit as exit
from .inverted_ternary import inverted_ternary
from .ternary import ternary_axes_subplot
from .coordsentropic import *





def etplotjoint(lis, names, scale = 100, fonts = 30, s_mk = 200, gridl = 20, ticks_size = 15, pltscale = 20):
    
    
    """
    Function for creating and showing the plots of the entropy triangle, independentlly of the type of triangle (Only for SMET).
    This function works with list of DataFrames for plotting the split or the aggregate entropies measures of multiple databases

    > etplotjoint(lis,names, scale = x)

    Parameters
    ----------
    lis : List of Dataframes to be plotted
    names : Names of the dataframes (if empty, some names will be provided for the plotting)
    scale : Scale for the entropy triangle
    fonts : Fontsize of the Labels
    s_mk : Size of the marks for the triangle
    gridl : Space between each gridline
    tick_size: size of the numbers for the ticks

    Returns
    ----------
    points : painted points 
    Shows the triangle without returning anything
    
    """

    
    if(not isinstance(lis, list)):
        exit('This function only works with LISTS of Dataframes, maybe you can try the etplot function for an individual DataFrame plot')
    
    if(not all(isinstance(lis[x],pd.DataFrame) for x in range(len(lis)))):
        exit('All values must be instances of DataFrames for entropy calculations')
        
    if(not names):
        warning('No names founded, Providing Dummy names')
        names = list(map(lambda x: "x"+str(x), range(len(lis))))
    
    if(hasSplitSmetCoords(lis[0]) or hasAggregateSmetCoords(lis[0]) or hasDualAggregateSmetCoords(lis[0])):
        
        figure, tax = inverted_ternary.figure(scale=scale)
        figure.set_size_inches(pltscale,pltscale)
        tax.boundary(linewidth=2.0)
        tax.gridlines(multiple = gridl, color="blue")
        
        for j in range(len(lis)):
            aux = lis[j]
            points = entcoords(aux, scale)
            colors = get_cmap(len(aux.index)) ; mk = markers(1)*len(list(aux.index))
            name = list ()
            for na in range(len(aux.index)) : name.append(names[j] + str('-') +aux.index[na])
            
            for i in range(len(aux.index)):
                tax.scatter(points[i:i+1], s = s_mk, marker = mk[i], color = colors(i), label = name[i] ,edgecolor='black', linewidth='0.5')
         
        if (hasSplitSmetCoords(lis[0])):
            
            tax.set_title("Source Multivariate split entropies (SMET)", fontsize = fonts + 5)
            tax.left_axis_label(r"$\Delta H'_{P_{X_i}}$", fontsize=fonts)
            tax.right_axis_label(r"$ M'_{P_{X_i}}$", fontsize=fonts)
            tax.bottom_axis_label(r"$ H'_{P_{X_i|X_i^c}}$", fontsize=fonts)

        elif (hasAggregateSmetCoords(lis[0])):

            tax.set_title("Aggregate Source Multivariate entropies (SMET)", fontsize = fonts + 5)
            tax.left_axis_label(r"$\Delta H'_{Pi_{X}}$", fontsize=fonts)
            tax.right_axis_label(r"$ M'_{P_{X}}$", fontsize=fonts)
            tax.bottom_axis_label(r"$ VI'_{P_{X}}$", fontsize=fonts)

        elif (hasDualAggregateSmetCoords(lis[0])):

            tax.set_title("Dual Aggregate Source Multivariate entropies (SMET)", fontsize = fonts + 5)
            tax.left_axis_label(r"$\Delta H'_{P_{X}}$", fontsize=fonts)
            tax.right_axis_label(r"$ D'_{P_{X}}$", fontsize=fonts)
            tax.bottom_axis_label(r"$ VI'_{P_{X}}$", fontsize=fonts)
        
        tax.ticks(axis='lbr', linewidth=1, multiple = gridl , fontsize = ticks_size )
        tax.clear_matplotlib_ticks()
        tax.legend(title = 'Features' ,labelspacing = 1.5 , fontsize = 12)

        tax.show()

        return None
        
        
    else:
        exit('Only works for SMET cases')




def etplot (edf,names = None, scale = 100 , fonts = 30 ,s_mk = 200 , gridl = 20 , ticks_size = 15 , pltscale = 20):
    
    """
    Function for creating and showing the plots of the entropy triangle, independentlly of the type of triangle (SMET or CMET)

    > etplot(edf, scale = x)

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

    Returns
    ----------
    points : painted points 
    Shows the triangle
    
    """

    if(not isinstance(edf,pd.DataFrame)):
        if(isinstance(edf,list)):
            if(not all(isinstance(x,pd.DataFrame) for x in edf)):
                exit("Can only work with Data Frames or lists of DataFrames! (df it´s not a DataFrame)")
            else:
                etplotjoint(edf, names = names, scale = scale, fonts = fonts, s_mk = s_mk, gridl = gridl, ticks_size = ticks_size, pltscale = pltscale)
                return None
        else: 
            exit("Can only work with Data Frames or lists of DataFrames! (df it´s not a DataFrame)")
               

    points = entcoords(edf, scale)

    #SMET PLOT
    if(hasSplitSmetCoords(edf) or hasAggregateSmetCoords(edf) or hasDualAggregateSmetCoords(edf)):

        figure, tax = inverted_ternary.figure(scale=scale)
        figure.set_size_inches(pltscale, pltscale)
        tax.boundary(linewidth=2.0)
        tax.gridlines(multiple = gridl, color="blue")
    
        colors = get_cmap(len(edf.index)) ; names = list(edf.index)

        if(any(edf.index == 'AGGREGATE')):
            mk = markers(1)*len(edf)
            for i in range(len(edf.index)):
                tax.scatter(points[i:i+1], s = s_mk, marker = mk[i], color = colors(i), label = names[i] ,edgecolor='black', linewidth='0.5')
        else:
            mk = markers(len(edf.index))
            for i in range(len(edf.index)):
                tax.scatter(points[i:i+1], s = s_mk, marker = mk[i], color = colors(i), label = names[i] ,edgecolor='black', linewidth='0.5')

        if (hasSplitSmetCoords(edf)):

            tax.set_title("Source Multivariate split entropies (SMET)", fontsize = fonts + 5)
            tax.left_axis_label(r"$\Delta H'_{P_{X_i}}$", fontsize=fonts)
            tax.right_axis_label(r"$ M'_{P_{X_i}}$", fontsize=fonts)
            tax.bottom_axis_label(r"$ H'_{P_{X_i|X_i^c}}$", fontsize=fonts)

        elif (hasAggregateSmetCoords(edf)):

            tax.set_title("Aggregate Source Multivariate entropies (SMET)", fontsize = fonts + 5)
            tax.left_axis_label(r"$\Delta H'_{Pi_{X}}$", fontsize=fonts)
            tax.right_axis_label(r"$ M'_{P_{X}}$", fontsize=fonts)
            tax.bottom_axis_label(r"$ VI'_{P_{X}}$", fontsize=fonts)

        elif (hasDualAggregateSmetCoords(edf)):

            tax.set_title("Dual Aggregate Source Multivariate entropies (SMET)", fontsize = fonts + 5)
            tax.left_axis_label(r"$\Delta H'_{P_{X}}$", fontsize=fonts)
            tax.right_axis_label(r"$ D'_{P_{X}}$", fontsize=fonts)
            tax.bottom_axis_label(r"$ VI'_{P_{X}}$", fontsize=fonts)

    #CMET PLOT
    elif(hasCmetEntropicCoords(edf)):

        figure, tax = ternary_axes_subplot.figure(scale=scale)
        figure.set_size_inches(pltscale, pltscale)
        tax.boundary(linewidth=2.0)
        tax.gridlines(multiple = gridl, color="blue")

        mk = markers(len(edf.index)) ; colors = get_cmap(len(edf.index)) ; names = list(edf.index)
        for i in range(len(edf.index)):
            tax.scatter(points[i:i+1], s = s_mk , marker = mk[i], color = colors(i), label = names[i] ,edgecolor='black', linewidth='0.3')

        tax.set_title("Aggregate Channel Multivariate entropies (CMET)", fontsize = fonts + 5)
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





def cbetplot(edf, scale = 100 , fonts = 30 ,s_mk = 200 , gridl = 20 , ticks_size = 15 , pltscale = 17):
    
    if(not isinstance(edf,pd.DataFrame)):
        exit("Can only work with Data Frames or lists of DataFrames! (df it´s not a DataFrame)")
    
    points = entcoords(edf, scale)
    
    if(hasCmetEntropicCoords(edf)):
        
        figure, tax = ternary_axes_subplot.figure(scale=scale)
        figure.set_size_inches(pltscale, pltscale)
        tax.boundary(linewidth=2.0)
        tax.gridlines(multiple = gridl, color="blue")

        mk = markers(len(edf.index))
        colors = get_cmap(len(edf.index)) 
        names = list([r"$K$",r"$\hat{K}}$",r"$ K\hat{X}}$"])

        for i in range(len(edf.index)):
            tax.scatter(points[i:i+1], s = s_mk , marker = mk[0], color = colors(i), label = names[i] ,edgecolor='black', linewidth='0.3')

        tax.set_title("Channel Bivariate Entropy Triangle (CBET)", fontsize = fonts + 5)
        tax.left_axis_label(r"$ VI_{P_{XY}}$", fontsize=fonts)
        tax.right_axis_label(r"$ MI_{P_{XY}}  $", fontsize=fonts)
        tax.bottom_axis_label(r"$\Delta H_{P_{X}\cdot{P_{Y}}}$", fontsize=fonts)

    else: 
        
        exit("Entropic coordinates needed for the diagram plotting")

    tax.ticks(axis='lbr', linewidth=1, multiple = gridl , fontsize = ticks_size )
    tax.clear_matplotlib_ticks()
    tax.legend(title = 'Features' ,labelspacing = 1.5 , fontsize = 12)
    
    tax.show()
    
    
    
    
    
def cmetplot(edf, names = None, scale = 100 , fonts = 30 ,s_mk = 200 , gridl = 20 , ticks_size = 15 , pltscale = 17):

    if(not isinstance(edf, list)):
        exit('This function only works with LISTS of Dataframes, maybe you can try the etplot function for an individual DataFrame plot')
    
    if(not all(isinstance(edf[x],pd.DataFrame) for x in range(len(edf)))):
        exit('All values must be instances of DataFrames for entropy calculations')
        
    if(not names):
        warning('No names founded, Providing Dummy names')
        names = list(map(lambda x: "Features"+str(len(edf)-x)+"PC", range(len(edf))))
             
    
    if(all(hasCmetEntropicCoords(edf[l]) for l in range(len(edf)))):

        figure, tax = ternary_axes_subplot.figure(scale=scale)
        figure.set_size_inches(pltscale, pltscale)
        tax.boundary(linewidth=2.0)
        tax.gridlines(multiple = gridl, color="blue")
        
        
        colors = get_cmap(len(edf[0].index))
        for i in range(len(edf)):
            
            points = entcoords(edf[i], scale)
            mk = markers(1)*len(edf[i].index) ; names = list(edf[i].index+'-FT-'+str(len(edf)-i)+'-PC')
            for j in range(len(edf[i].index)):
                tax.scatter(points[j:j+1], s = s_mk , marker = mk[j], color = colors(j), label = names[j] ,edgecolor='black', linewidth='0.3')

        tax.set_title("Aggregate Channel Multivariate entropies (CMET)", fontsize = fonts + 5)
        tax.left_axis_label(r"$ VI'_{P_\overline{XY}}$", fontsize=fonts)
        tax.right_axis_label(r"$ 2\cdot{I'_{P_\overline{XY}}}  $", fontsize=fonts)
        tax.bottom_axis_label(r"$\Delta H'_{P_\overline{XY}}$", fontsize=fonts)

    else: 
        
        exit("Entropic coordinates needed for the diagram plotting")

    tax.ticks(axis='lbr', linewidth=1, multiple = gridl , fontsize = ticks_size )
    tax.clear_matplotlib_ticks()
    tax.legend(title = 'Features' ,labelspacing = 1.5 , fontsize = 12)
    
    tax.show()