"""
The implementations of the queriers.
"""

################################################################################

import math

from common.datas import Schema, Entry
from common.datas_util import  RowsMutableTable, ColsMutableTable, DatasUtil
from outport_data.base_queriers import BaseQuerier, BaseExpressionNativeRenderer

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
    renderer: BaseExpressionNativeRenderer
    
    def query(self, table, query):
        schema = table.schema
        x_axis_field = query.x_axis

        groupped = self.group(table, x_axis_field)
        new_table = self.prepare_new_table(schema, x_axis_field, groupped)

        result = ColsMutableTable(new_table)
        
        for y_axis_name in query.y_axis_specifiers.keys():
            y_axis_agrexp = query.y_axis_specifiers[y_axis_name]
            self.add_y(result, schema, x_axis_field, y_axis_name, y_axis_agrexp, groupped)

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


    def add_y(self, result, schema, x_axis, y_axis_name, y_axis_agrexp, groupped):
        """ Computes and adds new y_axis_name with value computed by 
        y_axis_agrexp on the groupped data to the result table """
        
        y_axis_type = y_axis_agrexp.result_type

        y_axis_values = list(map(
            lambda g_v: self.compute_y(g_v, groupped, y_axis_name, y_axis_agrexp),
            groupped.keys()))
        result.add_field_with_values(y_axis_name, y_axis_type, y_axis_values)
        
    def compute_y(self, group_value, groupped, y_axis_name, y_axis_agrexp):
        """ Computes the y_axis_value of given group by given expression """
        
        group = groupped[group_value]
        y_axis_enexp = y_axis_agrexp.expression
        agregator = y_axis_agrexp.aggregator
        
        y_values = list(map(lambda e: self.evaluate(e, y_axis_enexp), group))
        return self.agregate(y_values, agregator)
        
    def evaluate(self, entry, y_axis_enexp):
        """ Evaluates the given entry expression entry for given entry """
        
        python_expr = self.renderer.to_native(y_axis_enexp, self, "_entry_")
        return eval(python_expr, globals(),  {"_entry_": entry} )
    
    def agregate(self, values, aggregator):
        """ Calls the specified agregator on the given values """
        
        if aggregator is None:
            if len(values) == 1:
                return values[0]
            else:
                raise ValueError("Only single-valued can have no aggregator")
        
        if aggregator in ("first", "any"):
            return values[0]

        if aggregator in ("max", "maximum"):
            return max(values)
        
        if aggregator in ("min", "minimum"):
            return min(values)
        
        if aggregator in ("avg", "average"):
            return math.fsum(values) / len(values)
        
        if aggregator in ("count"):
            return len(values)
        
        raise ValueError("Unsupprted aggregator: " + aggregator)
################################################################################
        
