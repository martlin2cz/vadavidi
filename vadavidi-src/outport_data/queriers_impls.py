"""
The implementations of the queriers.
"""

import math

from common.datas import Schema, Entry
from common.datas_util import  RowsMutableTable
from common.xlang import XLangParser
from outport_data.base_queriers import BaseQuerier


################################################################################
class DefaultQuerier(BaseQuerier):
    """
    The default querier. Query is executed by normal python code with no 
    optimalisations.
    """
    
    # the xlang impl
    xlang = XLangParser()
    
    def query(self, table, query):
        schema = table.schema
        
        x_axis = query.x_axis_specifier
        groupped = self.group(table, x_axis)
        
        #result = MutableTable(schema)
        #FIXME
        #for yAxisName in query.yAxisSpecifiers.keys():
            #yAxisSpec = query.yAxisSpecifiers.get(yAxisName)
        y_axis_spec = query.y_axis_specifiers.get(list(query.y_axis_specifiers.keys())[0])
        xle = self.xlang.parse(schema, y_axis_spec)
        return self.execute_y(schema, x_axis, xle, groupped)
        
        #return result.toTable()    
        
        
    def group(self, table, groupper):
        """ Groups the table, based on the groupper field to map 
        groupper_value -> list of entries with that groupper_value """
        
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
    
    def execute_y(self, schema, group_field, xle, groupped):
        """ Computes one value of the Y field specified by the xle of the given
        groupped values """
        
        #FIXME
        field_name = xle.items[0].field_name
        agregator = xle.items[0].operation
        
        new_schema = Schema({group_field: schema[group_field], \
                             field_name: schema[field_name]})
        
        result = RowsMutableTable(new_schema)
        for (ordnum, group_val) in enumerate(groupped.keys()):
            group_entries = groupped.get(group_val)
            group_values = list(map(lambda e: e.value(field_name), group_entries))
            group_value = self.agregate(group_values, agregator)
            
            values = {group_field: group_val, field_name: group_value}
            
            result.add(Entry.create_new(new_schema, ordnum, "(Computed)", values))
        return result.to_table()
        
    def agregate(self, values, agregator):
        """ Calls the specified agregator on the given values """
        
        if agregator == "first":
            return values[0]

        if agregator == "max":
            return max(values)
        
        if agregator == "min":
            return min(values)
        
        if agregator == "avg":
            return math.fsum(values) / len(values)
        
        if agregator == "count":
            return len(values)
        
        raise ValueError("Unsupprted agragator: " + agregator)
################################################################################
        