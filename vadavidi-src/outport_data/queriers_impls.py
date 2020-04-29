"""
The implementations of the queriers.
"""

################################################################################

"""
The source indicating that the source of the entry is computation and not actual 
input data
"""

import math

from common.datas import Schema, Entry, Table, ID, SOURCE
from common.datas_util import  RowsMutableTable, ColsMutableTable, DatasUtil
from outport_data.base_queriers import BaseQuerier, BaseExpressionNativeRenderer, \
    Query


COMPUTED = "(Computed)"

################################################################################
class DefaultQuerier(BaseQuerier):
    """
    The default querier. Query is executed by normal python code with no 
    optimalisations.
    """
    renderer: BaseExpressionNativeRenderer

    def query(self, table:Table, query:Query):
        values_map = query.values_map
        computed = self.compute(table, values_map)
        
        grouppers_names = list(filter(lambda gn: (query.groups_map[gn] is None), \
                             query.groups_map.keys()))
        groupped = self.group(computed, grouppers_names)
        
        groups = query.groups_map
        agregated = self.agregate(groupped, groups)

        return agregated

################################################################################       

    def compute(self, table, values_map):
        """ Computes the brand new table containing the given values (evaluated 
        named expressions) """
        
        new_schema = self.schema_of_computed(values_map)
        result = RowsMutableTable(new_schema)
        
        for entry in table:
            new_entry = self.compute_entry(new_schema, entry, values_map)
            result += new_entry
            
        return result.to_table()
        
    def schema_of_computed(self, values):
        values_names = values.keys()
        values_typed = dict(map(lambda vn: (vn, COMPUTED), values_names))
        return Schema(values_typed)
    
    def compute_entry(self, schema, entry, values_map):
        values = dict(map(lambda vn: \
                          (vn, self.compute_value(entry, vn, values_map[vn])), \
                          values_map.keys()))
        
        return Entry.create_new(schema, entry[ID], entry[SOURCE], values)
    
    def compute_value(self, entry, value_name, value_expression):
        ENTRY_IDENTIFIER = "_entry_"
        python_expr = self.renderer.to_native(value_expression, self, None, ENTRY_IDENTIFIER)
        
        try:
            return eval(python_expr, globals(),  { ENTRY_IDENTIFIER: entry } )
        except:
            print("The expression evaluation failed: the " + \
                  str(value_expression) + " of " + str(entry))
            #TODO handle error properly
            return None
        
        
################################################################################       
    def group(self, table, grouppers_names):
        """ Groups the table, based on the grouppers to map 
        (grouppers) -> list of entries with that groupper_value """
        
        table_groups = self.compute_groups(table, grouppers_names)
        
        schema = table.schema
        return self.group_table(schema, table_groups, grouppers_names)
    
    def compute_groups(self, table, grouppers_names):
        result = {}
        for entry in table:
            groupper_vals_dict = DatasUtil.extract(entry, grouppers_names)
            grouppers_vals = tuple(groupper_vals_dict.items())
            
            if grouppers_vals in result.keys():
                group = result.get(grouppers_vals)
                group.append(entry)
            else:
                group = [ entry ]
                result[grouppers_vals] = group
            
        return result
    
    def group_table(self, schema, table_groups, grouppers_names):
        new_schema = self.schema_of_groupped(schema, grouppers_names)
        
        result = RowsMutableTable(new_schema)
    
        for (ordnum, grouppers_vals) in enumerate(table_groups.keys()):
            group_entries = table_groups[grouppers_vals]
            
            grouppers_vals_dict = dict(grouppers_vals)
            
            values = dict(map(lambda fn: (fn, self.groupper_value( \
                    group_entries, grouppers_vals_dict, grouppers_names, fn)), \
                schema))
            
            entry = Entry.create_new(new_schema, ordnum, COMPUTED, values)
            result += entry
            
        return result.to_table()
    
    def schema_of_groupped(self, schema, grouppers_names):
       
        group_names_typed = dict(map(lambda vn: (vn, \
                (schema[vn] if (vn in grouppers_names) else "SubTable")), \
            grouppers_names))
        return Schema(group_names_typed)

    def groupper_value(self, group_entries, grouppers_vals_dict, \
                       grouppers_names, groupper_name):
        
        if groupper_name in grouppers_names:
            return grouppers_vals_dict[groupper_name]
        else:
            return list(map(lambda e: e[groupper_name], group_entries))
            
################################################################################
    def agregate(self, groupped, groups):
        schema = self.schema_of_agregated(groupped.schema, groups)
        result = RowsMutableTable(schema)
        
        for entry in groupped:
            new_entry = self.compute_agregated_entry(schema, entry, groups)
            result += new_entry

        return result.to_table()

    def schema_of_agregated(self, schema, groups):
        return schema #TODO schema
    
    def compute_agregated_entry(self, schema, entry, groups):
        values = dict(map(lambda fn: \
            (fn, self.compute_agregated_value(fn, entry[fn], groups)),
            schema))
    
        return Entry.create(schema, values)
    
    def compute_agregated_value(self, field_name, field_value, groups):
        if field_name not in groups.keys():
            return field_value
        
        agregator = groups[field_name]
        if agregator is None:
            return field_value
         
        return self.apply_agregator(agregator, field_value)
        
    def apply_agregator(self, agregator, values):
        if agregator in ("first", "any"):
            return values[0]

        if agregator in ("max", "maximum"):
            return max(values)
        
        if agregator in ("min", "minimum"):
            return min(values)
        
        if agregator in ("avg", "average"):
            return math.fsum(values) / len(values)
        
        if agregator in ("count"):
            return len(values)
        
        raise ValueError("Unsupprted aggregator: " + agregator)

################################################################################
    
#     
#     def _agregate(self, query, schema, x_axis_field, groupped, new_table):
#         """ Agreggates the values of the subtables. """
#         
#         result = ColsMutableTable(new_table)
#         for y_axis_name in query.y_axis_specifiers.keys():
#             y_axis_agrexp = query.y_axis_specifiers[y_axis_name]
#             self.add_y(result, schema, x_axis_field, y_axis_name, y_axis_agrexp, groupped)
#         
#         return result.to_table() 
# 
#     def add_y(self, result, schema, x_axis, y_axis_name, y_axis_agrexp, groupped):
#         """ Computes and adds new y_axis_name with value computed by 
#         y_axis_agrexp on the groupped data to the result table """
#         
#         y_axis_type = y_axis_agrexp.result_type
# 
#         y_axis_values = list(map(
#             lambda g_v: self.compute_y(g_v, groupped, y_axis_name, y_axis_agrexp),
#             groupped.keys()))
#         result.add_field_with_values(y_axis_name, y_axis_type, y_axis_values)
#         
#     def compute_y(self, group_value, groupped, y_axis_name, y_axis_agrexp):
#         """ Computes the y_axis_value of given group by given expression """
#         
#         group = groupped[group_value]
#         y_axis_enexp = y_axis_agrexp.expression
#         agregator = y_axis_agrexp.aggregator
#         
#         y_values = list(map(lambda e: self.evaluate(e, y_axis_enexp), group))
#         return self.agregate(y_values, agregator)
#         
#     def evaluate(self, entry, y_axis_enexp):
#         """ Evaluates the given entry expression entry for given entry """
#         
#         python_expr = self.renderer.to_native(y_axis_enexp, self, "_entry_")
#         return eval(python_expr, globals(),  {"_entry_": entry} )
#     
#     def _agregate(self, values, aggregator):
#         """ Calls the specified agregator on the given values """
#         
#         if aggregator is None:
#             if len(values) == 1:
#                 return values[0]
#             else:
#                 raise ValueError("Only single-valued can have no aggregator")
#         
#         if aggregator in ("first", "any"):
#             return values[0]
# 
#         if aggregator in ("max", "maximum"):
#             return max(values)
#         
#         if aggregator in ("min", "minimum"):
#             return min(values)
#         
#         if aggregator in ("avg", "average"):
#             return math.fsum(values) / len(values)
#         
#         if aggregator in ("count"):
#             return len(values)
#         
#         raise ValueError("Unsupprted aggregator: " + aggregator)
#     
################################################################################
        
