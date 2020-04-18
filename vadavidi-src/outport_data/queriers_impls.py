"""
The implementations of the queriers.
"""

import math

from common.datas import Schema, Entry
from common.datas_util import  RowsMutableTable, ColsMutableTable, DatasUtil
from common.xlang import XLangParser
from outport_data.base_queriers import BaseQuerier
from numpy import deprecate
from pygments.lexers.textfmts import TodotxtLexer

################################################################################
"""
The source indicating that the source of the entry is computation and not actual 
input data
"""
COMPUTED = "(Computed)"


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
        x_axis_field = query.x_axis

        groupped = self.group(table, x_axis_field)
        new_table = self.prepare_new_table(schema, x_axis_field, groupped)

        result = ColsMutableTable(new_table)
        
        for y_axis_name in query.y_axis_specifiers.keys():
            y_axis_spec = query.y_axis_specifiers[y_axis_name]
            y_axis_xlang = self.xlang.parse(schema, y_axis_spec)
            self.add_y(result, schema, x_axis_field, y_axis_name, y_axis_xlang, groupped)

        return result.to_table()    
        
    def group(self, table, groupper_field):
        """ Groups the table, based on the groupper field to map 
        groupper_value -> list of entries with that groupper_value """
        
        result = {}
        for entry in table.list():
            groupper_val = entry[groupper_field]
            
            if groupper_val in result.keys():
                group = result.get(groupper_val)
                group.append(entry)
            else:
                group = [ entry ]
                result[groupper_val] = group
            
        return result
    
    def prepare_new_table(self, schema, x_axis_field, groupped):
        """ Constructs the new table with the only x_axis_field field, set to 
        each group's value of that field """
        
        x_axis_field_type = schema[x_axis_field]
        new_schema = Schema({x_axis_field: x_axis_field_type})
        result = RowsMutableTable(new_schema)
    
        for (ordnum, group_value) in enumerate(groupped.keys()):
            values = {x_axis_field: group_value}
            entry = Entry.create_new(new_schema, ordnum, COMPUTED, values)
            result += entry
            
        return result.to_table()


    def add_y(self, result, schema, x_axis, y_axis_name, y_axis_xlang, groupped):
        """ Computes and adds new y_axis_name with value computed by 
        y_axis_xlang on the groupped data to the result table """
        
        y_axis_type = self.type_of_agregation(schema, y_axis_xlang)

        y_axis_values = list(map(lambda g_v: self.compute_y(g_v, groupped, y_axis_name, y_axis_xlang),
                                 groupped.keys()))
        result.add_field_with_values(y_axis_name, y_axis_type, y_axis_values)
        
    def compute_y(self, group_value, groupped, y_axis_name, y_axis_xlang):
        """ Computes the y_axis_value of given group by given xlang """
        
        group = groupped[group_value]
        y_values = list(map(lambda e: self.evaluate(e, y_axis_xlang), group))
        agregator = y_axis_xlang.agregator
        
        return self.agregate(y_values, agregator)
        
    def evaluate(self, entry, xlang):
        """ Evaluates the given xlang entry for given entry """
        
        python_expr = xlang.to_python_str("_entry")
        return eval(python_expr, globals(),  {"_entry": entry} )
    
    #===========================================================================
    # @deprecate
    # def execute_y(self, schema, group_field, xle, groupped):
    #     """ Computes one value of the Y field specified by the xle of the given
    #     groupped values """
    #     
    #     # FIXME
    #     field_name = xle.items[0].field_name
    #     agregator = xle.items[0].operation
    #     
    #     new_schema = Schema({group_field: schema[group_field], \
    #                          field_name: schema[field_name]})
    #     
    #     result = RowsMutableTable(new_schema)
    #     for (ordnum, group_val) in enumerate(groupped.keys()):
    #         group_entries = groupped.get(group_val)
    #         group_values = list(map(lambda e: e.value(field_name), group_entries))
    #         group_value = self.agregate(group_values, agregator)
    #         
    #         values = {group_field: group_val, field_name: group_value}
    #         
    #         result.add(Entry.create_new(new_schema, ordnum, "(Computed)", values))
    #     return result.to_table()
    #===========================================================================
    
    def type_of_agregation(self, schema, xlang):
        """ Produces the type of the expression """
        #TODO type of agregation
        return "Some"
    
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
        
