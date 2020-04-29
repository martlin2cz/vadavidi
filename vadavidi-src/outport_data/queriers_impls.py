"""
The implementations of the queriers.
"""
from common.sqlite_db import SQLLite, SQL_LITE_POOL

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

    def query(self, dataset_name:str, table:Table, query:Query):
        
        if query.before_values_filter is not None:
            table = self.filter(table, query.before_values_filter)
        
        if query.values_map is not None:
            table = self.compute(table, query.values_map)
        
        if query.after_values_filter is not None:
            table = self.filter(table, query.after_values_filter)
        
        if query.groups_map is not None:
            if list(query.groups_map.keys()) != list(table.schema):
                raise ValueError("Group fields mismatch")
            
            table = self.group(table, query.groups_map)
            table = self.agregate(table, query.groups_map)
            
        if query.after_groupped_filter is not None:
            table = self.filter(table, query.after_groupped_filter)
        
        if query.order_by is not None:
            table = self.order(table, query.order_by)
    
        return table

################################################################################       
    def filter(self, table, filter_expr):
        schema = table.schema
        result = RowsMutableTable(schema)
        
        for entry in table:
            value = self.compute_value(entry, filter_expr)
            if value:
                result += entry
                
        return result.to_table()

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
                          (vn, self.compute_value(entry, values_map[vn])), \
                          values_map.keys()))
        
        return Entry.create_new(schema, entry[ID], entry[SOURCE], values)
    
        
################################################################################       
    def group(self, table, groups_map):
        """ Groups the table, based on the grouppers to map 
        (grouppers) -> list of entries with that groupper_value """
        
        grouppers_names = self.create_grouppers_names(groups_map)
        schema = table.schema
         
        table_groups = self.compute_groups(table, grouppers_names)
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
                (schema[vn] if (vn in grouppers_names) else "(SubTable)")), \
            schema))
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
        grouppers_names = self.create_grouppers_names(groups)
        fields = dict(map(lambda vn: (vn, \
                (schema[vn] if (vn in grouppers_names) else "(Agregated)")), \
            schema))
        return Schema(fields)
    
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

    def order(self, table, order_by):
        entries = list(table)
        entries.sort(key = lambda e: tuple(DatasUtil.extract(e, order_by).values()))
        
        schema = table.schema
        return Table(schema, entries)

################################################################################
    def compute_value(self, entry, value_expression):
        ENTRY_IDENTIFIER = "_entry_"
        python_expr = self.renderer.to_native(value_expression, self, None, ENTRY_IDENTIFIER)
        
        try:
            return eval(python_expr, globals(),  { ENTRY_IDENTIFIER: entry } )
        except Exception as ex:
            print("The " + str(value_expression) + " of " + str(entry) \
                  + " ( " + python_expr + " ) evaluation failed: " + str(ex))

            #TODO handle error properly
            return None

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
################################################################################
class SQLLiteQuerier(BaseQuerier):
    """
    The sqllite querier. The query is converted to SQLLite query and executed 
    directly on the database table.
    """
    
    # the renderer of the expressions
    renderer: BaseExpressionNativeRenderer
    
    def query(self, dataset_name:str, table:Table, query:Query):
        
        fields = None
        if query.values_map:
            fields = self.generate_fields(dataset_name, query.values_map, query.groups_map)
        
        where = None
        if query.before_values_filter:
            before_value_condition = self.generate_condition(dataset_name, query.before_values_filter, None)
            where = self.add_to_where(where, before_value_condition)
            
        if query.after_values_filter:
            after_value_condition = self.generate_condition(dataset_name, query.after_values_filter, query.values_map)
            where = self.add_to_where(where, after_value_condition)
        
        group = None
        if query.groups_map:
            grouppers_names = BaseQuerier.create_grouppers_names(query.groups_map)
            group = self.generate_groups(grouppers_names)
        
        having = None
        if query.after_groupped_filter:
            after_groupped_condition = self.generate_condition(dataset_name, query.after_groupped_filter, query.values_map)
            if query.groups_map:
                having = after_groupped_condition
            else:
                where = self.add_to_where(where, after_groupped_condition)
        
        order = None
        if query.order_by:
            order = query.order_by

        sqll = SQL_LITE_POOL.get(dataset_name)
        schema = self.create_schema(query.values_map)
        return sqll.load_better(schema, fields, where, group, having, order)


    def add_to_where(self, where, condition):
        if where is None:
            return condition
        else:
            return "({0}) AND ({1})".format(where, condition)
            
################################################################################

    def create_schema(self, values_map):
        fields = dict(map(lambda vn: (vn, COMPUTED), values_map.keys()))
        return Schema(fields)

################################################################################        
    
    def generate_condition(self, dataset_name, condition_expr, values_map):
        if values_map is None:
            table_name = SQLLite.table_name(dataset_name)
            return self.renderer.to_native(condition_expr, self, table_name, None)
        else:
            return self.renderer.to_native(condition_expr, self, None, values_map)

################################################################################

    def generate_fields(self, dataset_name, values_map, groups_map):
        return dict(map(lambda vn: \
            (vn, self.generate_field(dataset_name, vn, 
                                     values_map[vn], groups_map[vn])),
            values_map.keys()))

    def generate_field(self, dataset_name, value_name, value_expr, agregator):
        table_name = SQLLite.table_name(dataset_name)
        sql_expr = self.renderer.to_native(value_expr, self, table_name, None)
        
        if agregator is None:
            return "{0}".format(sql_expr)
        else:
            return "{1}({0})".format(sql_expr, agregator)
    
        
################################################################################        

    def generate_groups(self, grouppers_names):
        return grouppers_names
    
################################################################################
