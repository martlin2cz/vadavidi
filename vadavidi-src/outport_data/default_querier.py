import math

from common.datas import Table, Schema, Entry, ID, SOURCE
from common.datas_util import RowsMutableTable, DatasUtil
from outport_data.base_queriers import BaseQuerier
from outport_data.base_query import BaseExpressionNativeRenderer, Query


################################################################################
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
        
        for ordernum, entry in enumerate(groupped):
            new_entry = self.compute_agregated_entry(schema, ordernum, entry, groups)
            result += new_entry

        return result.to_table()

    def schema_of_agregated(self, schema, groups):
        grouppers_names = self.create_grouppers_names(groups)
        fields = dict(map(lambda vn: (vn, \
                (schema[vn] if (vn in grouppers_names) else "(Agregated)")), \
            schema))
        return Schema(fields)
    
    def compute_agregated_entry(self, schema, ordernum, entry, groups):
        values = dict(map(lambda fn: \
            (fn, self.compute_agregated_value(fn, entry[fn], ordernum, groups)),
            schema))
    
        return Entry.create(schema, values)
    
    def compute_agregated_value(self, field_name, field_value, ordernum, groups):
        if field_name not in groups.keys():
            return field_value

        if field_name is ID:
            return ordernum
        
        if field_name is SOURCE:
            return COMPUTED
        
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