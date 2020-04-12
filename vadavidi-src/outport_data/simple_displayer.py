# The simple, testing displayer module

import matplotlib.pyplot as plt
from common.datas import Entry, Table, Schema
import math
from time import sleep

################################################################################
#
class SimpleDisplayer(object):
    
    def show(self, datasetName, result):
        schema = result.schema
        fieldNames = schema.listFieldNames()
        if len(fieldNames) > 2:
            raise ValueError("Result has more than X and Y")
            
        xAxisName = fieldNames[0]
        yAxisName = fieldNames[1]
        
        xAxis = list(map(
            lambda e: e.value(xAxisName), 
            result.list()))
        
        yAxis = list(map(
            lambda e: e.value(yAxisName), 
            result.list()))
        
        plt.plot(xAxis,yAxis)
        plt.title(datasetName)
        plt.xlabel(xAxisName)
        plt.ylabel(yAxisName)
        plt.show()
        
################################################################################
if __name__ == '__main__':
    print("Testing the simple displayer")
    
    disp = SimpleDisplayer()
    schema = Schema({"time":"int", "speed":"decimal"})
    entries = list((Entry(i, {"time": i, "speed": math.e**i}) for i in range(1, 7)))
    
    table = Table(schema, entries)
    table.printit()
     
    disp.show("Speeding up", table)
    
    sleep(20)
    
    