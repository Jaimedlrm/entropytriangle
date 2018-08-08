import sys
from .inverted_ternary import inverted_ternary
from .ternary import ternary_axes_subplot

from .coordsentropic import *

def etplot (edf, scale = 100 , fonts = 30 , multiple = 5 ,s_mk = 150 , offset = 0.08 , gridl = 5 , ticks_size = 15):

    if(not isinstance(edf,pd.DataFrame)):
        sys.exit("Can only work with Data Frames! (df it´s not a DataFrame)")

    points = entcoords(edf, scale)

    #SMET PLOT
    if(hasSplitSmetCoords(edf) or hasAggregateSmetCoords(edf) or hasDualAggregateSmetCoords(edf)):

        figure, tax = inverted_ternary.figure(scale=scale)
        figure.set_size_inches(25, 25)
        tax.boundary(linewidth=2.0)
        tax.gridlines(multiple = gridl, color="blue")

        mk = markers(len(edf.index)) ; colors = get_cmap(len(edf.index)) ; names = list(edf.index)

        for i in range(len(edf.index)):
            tax.scatter(points[i:i+1], s = s_mk, marker = mk[i], color = colors(i), label = names[i] ,edgecolor='black', linewidth='0.5')

        if (hasSplitSmetCoords(edf)):

            tax.set_title("Source Multivariate split entropies (SMET)", fontsize = fonts + 10)
            tax.left_axis_label(r"$\Delta H'_{P_{X_i}}$", fontsize=fonts)
            tax.right_axis_label(r"$ M'_{P_{X_i}}$", fontsize=fonts)
            tax.bottom_axis_label(r"$ H'_{P_{X_i|X_i^c}}$", fontsize=fonts)

        elif (hasAggregateSmetCoords(edf)):

            tax.set_title("Aggregate Source Multivariate entropies (SMET)", fontsize = fonts + 10)
            tax.left_axis_label(r"$\Delta H'_{Pi_{X}}$", fontsize=fonts)
            tax.right_axis_label(r"$ M'_{P_{X}}$", fontsize=fonts)
            tax.bottom_axis_label(r"$ VI'_{P_{X}}$", fontsize=fonts)

        elif (hasDualAggregateSmetCoords(edf)):

            tax.set_title("Dual Aggregate Source Multivariate entropies (SMET)", fontsize = fonts + 10)
            tax.left_axis_label(r"$\Delta H'_{P_{X}}$", fontsize=fonts)
            tax.right_axis_label(r"$ D'_{P_{X}}$", fontsize=fonts)
            tax.bottom_axis_label(r"$ VI'_{P_{X}}$", fontsize=fonts)

    #CMET PLOT
    elif(hasCmetEntropicCoords(edf)):

        figure, tax = ternary_axes_subplot.figure(scale=scale)
        figure.set_size_inches(25, 25)
        tax.boundary(linewidth=2.0)
        tax.gridlines(multiple = gridl, color="blue")

        mk = markers(len(edf.index)) ; colors = get_cmap(len(edf.index)) ; names = list(edf.index)

        for i in range(len(edf.index)):
            tax.scatter(points[i:i+1], s = s_mk , marker = mk[i], color = colors(i), label = names[i] ,edgecolor='black', linewidth='0.3')

        tax.set_title("Aggregate Channel Multivariate entropies (CMET)", fontsize = fonts + 10)
        tax.left_axis_label(r"$ VI'_{P_\overline{XY}}$", fontsize=fonts)
        tax.right_axis_label(r"$ 2\cdot{I'_{P_\overline{XY}}}  $", fontsize=fonts)
        tax.bottom_axis_label(r"$\Delta H'_{P_\overline{XY}}$", fontsize=fonts)

    else: 
        
        sys.exit("Entropic coordinates needed for the diagram plotting")

    tax.ticks(axis='lbr', linewidth=1, multiple = gridl , fontsize = ticks_size )
    tax.clear_matplotlib_ticks()
    tax.legend(title = 'Features' ,labelspacing = 1.5 , fontsize = 12)

    tax.show()
    
    return None

