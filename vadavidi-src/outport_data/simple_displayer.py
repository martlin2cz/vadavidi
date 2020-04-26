"""
The simple, testing displayer module
"""

from builtins import str
import numpy as np
from dataclasses import dataclass, replace
import math
from time import sleep

from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

from common.datas import Entry, Table, Schema, ID
from common.datas_util import DatasUtil
import matplotlib.pyplot as plt
from outport_data.base_displayers import BaseSeriesStyle


################################################################################
@dataclass(init=False)
class LineChartSeriesStyle(BaseSeriesStyle):
    color: str = None
    line_width: float = None
    line_style: str = "-"
    marker_size: float = None
    marker_style: str = None

################################################################################
@dataclass(init=False)
class BarChartSeriesStyle(BaseSeriesStyle):
    color: str = None
    bar_width: float = 2
    hatch_style: str = None
    space_after: float = 0.5

################################################################################
@dataclass(init=False)
class ScatterChartSeriesStyle(BaseSeriesStyle):
    color: str = None
    marker_base_size: float = None
    marker_sizes_field: str = None
    marker_style: str = None
    
################################################################################
@dataclass(init=False)
class PieChartSeriesStyle(BaseSeriesStyle):
    first_color: str = None
    last_color: str = "black"
    radius: float = 1.0
    explode: float = 0.0

################################################################################


class SimpleDisplayer(object):
    """ The simple displayer. Displays the table of two columns in simple 
    matplot window. """
        
    def show_line(self, x_values, name, values, style):
        plt.plot(x_values, values, \
                 label = name, \
                 color = style.color, \
                 linewidth = style.line_width, \
                 linestyle = style.line_style, \
                 marker = style.marker_style, \
                 markersize = style.marker_size)
        
    def relativise(self, current_style, styles, x_step):
        total_width = sum(map(lambda x: x.bar_width + x.space_after, styles.values()))
        ratio = (x_step / total_width)
        
        subsum = 0.0
        for style in styles.values():
            if style is current_style:
                
                left = subsum * ratio 
                width = current_style.bar_width * ratio
                return (left, width)
            
            subsum += (style.bar_width + style.space_after)
            
        return None
        
    def show_bar(self, x_values, name, values, style, styles):
        x_step = abs(x_values[0] - x_values[1])
        (x_offset, relative_width) = self.relativise(style, styles, x_step)
        x_values_shiffted = list(map(lambda x: (x + x_offset), x_values))
        
        plt.bar(x_values_shiffted, values, relative_width, \
             label = name, \
             color = style.color, \
             fill = True, \
             hatch = style.hatch_style)     
        
    def show_scatter(self, table, x_values, name, values, style):
        if style.marker_sizes_field:
            sizes_values = DatasUtil.column(table, style.marker_sizes_field)
        else:
            sizes_values = style.marker_base_size
            
        datas = {"sizes": sizes_values }
        plt.scatter(x_values, values, \
                    label = name, \
                    color = style.color, \
                    marker = style.marker_style, 
                    s = "sizes", \
                    data = datas)
        
    def show_pie(self, x_values, name, values, style):
        colors = None
        if style.first_color:
            cmap = LinearSegmentedColormap.from_list("REV " + name, \
                    [style.first_color, style.last_color]) \
                    .reversed(name)
            #suma = sum(values)
            colors = cmap(np.linspace(0,1, num = len(values)))
            
        explodes = list(map(lambda y: style.explode, values))
        plt.pie(values, \
                #labels = values, \
                colors = colors, \
                radius = style.radius, \
                explode = explodes)
    
    def show(self, dataset_name, result, x_axis_name, series_names, styles):
        """ Shows the given dataset """
        
        x_axis_values = DatasUtil.column(result, x_axis_name)
        
        for i, series_name in enumerate(series_names):
            series_values = DatasUtil.column(result, series_name)
            
            series_style = styles[series_name]
            
            if isinstance(series_style, LineChartSeriesStyle):
                self.show_line(x_axis_values, series_name, series_values, series_style)

            elif isinstance(series_style, BarChartSeriesStyle):
                self.show_bar(x_axis_values, series_name, series_values, series_style, styles)
                
            elif isinstance(series_style, ScatterChartSeriesStyle):
                self.show_scatter(result, x_axis_values, series_name, series_values, series_style)
            
            elif isinstance(series_style, PieChartSeriesStyle):
                self.show_pie(x_axis_values, series_name, series_values, series_style)
                    
            else:
                raise ValueError("Unsupported kind")
            
            plt.title(dataset_name)

            if not isinstance(series_style, PieChartSeriesStyle):
                plt.xlabel(x_axis_name)
                plt.ylabel(series_name)
        
        #plt.tight_layout()
        if not isinstance(series_style, PieChartSeriesStyle):
            plt.legend()
            
        plt.show()
       
      
            
################################################################################
if __name__ == '__main__':
    print("See the displayers_test module")
    

    
    