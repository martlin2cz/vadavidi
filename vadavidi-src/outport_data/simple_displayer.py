"""
The simple, testing displayer module
"""

import matplotlib.pyplot as plt
from common.datas import Entry, Table, Schema
import math
from time import sleep

################################################################################
class SimpleDisplayer(object):
    """ The simple displayer. Displays the table of two columns in simple 
    matplot window. """
        
    def show(self, dataset_name, result):
        """ Shows the given dataset """
        
        schema = result.schema
        field_names = schema.list_raw()
        if len(field_names) > 2:
            raise ValueError("Result has more than X and Y")
            
        x_axis_name = field_names[0]
        y_axis_name = field_names[1]
        
        # TODO table.get_column(field_name)
        x_axis = list(map(
            lambda e: e.value(x_axis_name), 
            result.list()))
        
        y_axis = list(map(
            lambda e: e.value(y_axis_name), 
            result.list()))
        
        plt.plot(x_axis,y_axis)
        plt.title(dataset_name)
        plt.xlabel(x_axis_name)
        plt.ylabel(y_axis_name)
        plt.show()
        
################################################################################
if __name__ == '__main__':
    print("Testing the simple displayer")
    
    disp = SimpleDisplayer()
    schema = Schema({"time":"int", "speed":"decimal"})
    entries = list((Entry.create_new(schema, i, "cmt", {"time": i, "speed": math.e**i})) \
                   for i in range(1, 7))
    
    table = Table(schema, entries)
    table.printit()
     
    disp.show("Speeding up", table)
    
    sleep(20)
    
    