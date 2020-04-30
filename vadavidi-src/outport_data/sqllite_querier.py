""" The sqllite querier. The query is "compiled" to SQL query and then simply
executed on the sqllite dumped database. """

from common.datas import Table, ID, SOURCE, Schema
from common.sqlite_db import SQL_LITE_POOL, SQLLite
from outport_data.base_queriers import BaseQuerier
from outport_data.base_query import BaseExpressionNativeRenderer, Query

################################################################################ 

COMPUTED = "(Computed)"
################################################################################ 
class SQLLiteQuerier(BaseQuerier):
    """
    The sqllite querier. The query is converted to SQLLite query and executed 
    directly on the database table.
    """
    
    # the renderer of the expressions
    renderer: BaseExpressionNativeRenderer
    
    def query(self, dataset_name:str, table:Table, query:Query):
        schema = table.schema
        
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
        new_schema = self.create_schema(query.values_map)
        
        metas_generate = self.metas_generate(query.values_map, query.groups_map)
        return sqll.load_better(new_schema, metas_generate, fields, where, group, having, order)


    def add_to_where(self, where, condition):
        if where is None:
            return condition
        else:
            return "({0}) AND ({1})".format(where, condition)
        
    def metas_generate(self, values_map, groups_map):
        values_names = values_map.keys()
        if (ID not in values_names) or (SOURCE not in values_names):
            return True
        
        if (groups_map):
            grouppers_names = BaseQuerier.create_grouppers_names(groups_map)
            
            if (ID in grouppers_names) or (SOURCE in grouppers_names):
                return True
        
        return False
        
        
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
            values_map_str = self.render_values(dataset_name, values_map)
            return self.renderer.to_native(condition_expr, self, None, values_map_str)


    def render_values(self, dataset_name, values_map):
        return self.generate_fields(dataset_name, values_map, None)
################################################################################

    def generate_fields(self, dataset_name, values_map, groups_map):
        return dict(map(lambda vn: \
            (vn, self.generate_field(dataset_name, vn, values_map[vn], \
                         groups_map[vn] if groups_map else None)),
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
