# the queriers impl module

import math

from common.datas import Schema, Entry
from common.datas_util import MutableTable
from common.xlang import XLangParser
from outport_data.base_queriers import BaseQuerier


################################################################################
class DefaultQuerier(BaseQuerier):
    xlang = XLangParser()
    
    def query(self, table, query):
        schema = table.schema
        
        xAxis = query.xAxisSpecifier
        groupped = self.group(table, xAxis)
        
        #result = MutableTable(schema)
        #FIXME
        #for yAxisName in query.yAxisSpecifiers.keys():
            #yAxisSpec = query.yAxisSpecifiers.get(yAxisName)
        yAxisSpec = query.yAxisSpecifiers.get(list(query.yAxisSpecifiers.keys())[0])
        xle = self.xlang.parse(schema, yAxisSpec)
        return self.executeY(schema, xAxis, xle, groupped)
        
        #return result.toTable()    
        
        
    def group(self, table, groupper):
        result = {}
        for entry in table.list():
            val = entry.value(groupper)
            if val in result.keys():
                group = result.get(val)
                group.append(entry)
            else:
                group = [ entry ]
                result[val] = group
            
        return result
    
    def executeY(self, schema, groupField, xle, groupped):
        #FIXME
        fieldName = xle.items[0].fieldName
        agregator = xle.items[0].operation
        
        newSchema = Schema({groupField: schema.typeOf(groupField), fieldName: schema.typeOf(fieldName)})
        result = MutableTable(newSchema)
        for (ordnum, groupVal) in enumerate(groupped.keys()):
            groupEntries = groupped.get(groupVal)
            groupValues = list(map(lambda e: e.value(fieldName), groupEntries))
            groupValue = self.agregate(groupValues, agregator)
            
            values = {groupField: groupVal, fieldName: groupValue}
            
            result.add(Entry(ordnum, values))
        return result.toTable()
        
    def agregate(self, values, agregator):
        if agregator == "first":
            return values[0]

        if agregator == "max":
            return max(values)
        
        if agregator == "min":
            return min(values)
        
        if agregator == "avg":
            return math.avg(values)
        
        if agregator == "count":
            return len(values)
        
        raise ValueError("Unsupprted agragator: " + agregator)
################################################################################
        