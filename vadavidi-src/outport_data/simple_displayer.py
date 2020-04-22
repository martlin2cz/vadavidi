"""
The simple, testing displayer module
"""

import math
from time import sleep

from common.datas import Entry, Table, Schema, ID
from common.datas_util import DatasUtil
import matplotlib.pyplot as plt
from outport_data.base_displayers import SeriesStyle, LINE, SCATTER, BAR, PIE


################################################################################
class StylesBuilder:
    # the style built
    style: SeriesStyle
    
    def __init__(self):
        self.style = SeriesStyle(LINE, None, 1, "-", "o")
    
    def with_kind(self, kind):
        self.style.kind = kind
        return self
    
    def with_color(self, color):
        self.style.color = color
        return self
    
    def with_width(self, width):
        self.style.width = width
        return self
    
    def with_style(self, style):
        self.style.style = style
        return self
    
    def with_markers(self, markers):
        self.style.markers = markers
        return self
    
    def build(self):
        return self.style
    
    
    #TODO
    
################################################################################


class SimpleDisplayer(object):
    """ The simple displayer. Displays the table of two columns in simple 
    matplot window. """
        

 
    
    def show(self, dataset_name, result, x_axis_name, series_names, styles):
        """ Shows the given dataset """
        
        x_axis_values = DatasUtil.column(result, x_axis_name)
        
        for i, series_name in enumerate(series_names):
            series_values = DatasUtil.column(result, series_name)
            
            series_style = styles[series_name]
            ss = series_style
            
            if series_style.kind == LINE:
                plt.plot(x_axis_values, series_values, label = series_name, \
                         color = ss.color, linewidth = ss.width, \
                         linestyle = ss.style, marker = ss.markers)
            elif series_style.kind == BAR:
                x_axis_starts = list(map(lambda x: x + i * ss.width, x_axis_values))
                plt.bar(x_axis_starts, series_values, ss.width, \
                         label = series_name, color = ss.color, \
                         fill = True, hatch = ss.markers)        
            elif series_style.kind == SCATTER:
                datas = {"sizes": series_values }
                plt.scatter(x_axis_values, series_values, label = series_name, \
                         color = ss.color, s = "sizes", marker = ss.markers, data = datas)
                
            elif series_style.kind == PIE:
                labels = [series_name] + [""] * (len(series_values) - 1)
                plt.pie(series_values, radius = ss.width, labels = labels)

            
            else:
                raise ValueError("Unsupported kind")
            
            plt.title(dataset_name)
            if series_style.kind != PIE:
                plt.xlabel(x_axis_name)
                plt.ylabel(series_name)

        
        #plt.tight_layout()
        plt.legend()
        plt.show()
       
    
     
            
################################################################################
if __name__ == '__main__':
    print("Testing the simple displayer")
    
    disp = SimpleDisplayer()
    schema = Schema({"time":"int", "speed":"decimal"})
    entries = list((Entry.create_new(schema, i, "cmptd", \
            { "time": (i ** 1), "speed": math.e**i / 10, "age": math.cos(i) } )) \
                   for i in range(1, 7))
    
    table = Table(schema, entries)
    table.printit()
    
    series_names = [ID, "speed", "age"]

## various chart types:
#    styles = {ID: StylesBuilder().with_kind(LINE).build(), \
#              "speed": StylesBuilder().with_kind(BAR).build(), \
#              "age": StylesBuilder().with_kind(SCATTER).build() }

## various line chart styles:
#    styles = {ID: StylesBuilder().with_markers("x").build(), \
#              "speed": StylesBuilder().with_style("--").build(), \
#              "age": StylesBuilder().with_width(2).build() }

## various colors:
#    styles = {ID: StylesBuilder().with_color("y").build(), \
#              "speed": StylesBuilder().with_color("red").build(), \
#              "age": StylesBuilder().with_color("#906090").build() }

## various bar charts: 
#    styles = {ID: StylesBuilder().with_kind(BAR).with_width(4).build(), \
#              "speed": StylesBuilder().with_kind(BAR).with_color("red").build(), \
#              "age": StylesBuilder().with_kind(BAR).with_markers("/").build() }

## various scatter charts: 
#    styles = {ID: StylesBuilder().with_kind(SCATTER).with_width(14).build(), \
#              "speed": StylesBuilder().with_kind(SCATTER).with_color("red").build(), \
#              "age": StylesBuilder().with_kind(SCATTER).with_markers("*").build() }
   
    styles = {ID: StylesBuilder().with_kind(PIE).with_width(1.4).build(), \
              "speed": StylesBuilder().with_kind(PIE).with_color("red").build(), \
              "age": StylesBuilder().with_kind(PIE).with_width(0.5).build() }
   
        
    disp.show("Speeding up", table, "time", series_names, styles)
    
    sleep(20)
    
    