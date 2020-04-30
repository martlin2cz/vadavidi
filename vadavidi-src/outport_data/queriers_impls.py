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
from common.sqlite_db import SQLLite, SQL_LITE_POOL
from outport_data.base_queriers import BaseQuerier
from outport_data.base_query import BaseExpressionNativeRenderer, Query


COMPUTED = "(Computed)"


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
