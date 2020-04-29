"""
The base queriers module. The querier executes the query on the specific table.
"""
from abc import ABC, abstractmethod
from builtins import str, staticmethod
from dataclasses import dataclass
from typing import Mapping, Callable, List

from common.datas import Table


################################################################################
@dataclass
class EntryExpression:
    """ The expression working with the entry. """
    
################################################################################
@dataclass
class AggregatingExpression:  
    """ The expression, which performs some entry_expression on some set of 
    entries and then invokes the aggregator. """
    
    # the final aggretor function identifier (vararg function returning the 
    # result_type)
    aggregator: str
    
    # the result_type of the aggregation
    result_type: str
    
    # the expression to be applied to each entry before aggregated
    expression: EntryExpression
    
    def __str__(self):
        return "AE:{0}->{1}:{2}".format(
            self.aggregator, self.result_type, self.expression)

################################################################################
@dataclass
class Query:
    """ The plain query is in fact just list of named expressions and some other
    stuff, like groupping or ordering. """
    
    # the filter to be applied before the values are computed
    before_values_filter: EntryExpression
    
    # the values specifiers (mapping of the values_names to values_entryexprs)
    values_map: Mapping[str, EntryExpression]

    # the filter to be applied after the values have been computed, but before
    # the groupping
    after_values_filter: EntryExpression
    
    # the groupping specifiers (mapping of the value_names to either None (group
    # by this name or the aggregator action), for subset of values
    groups_map: Mapping[str, str]

    # the filter to be applied after the values have been groupped and aggregated
    after_groupped_filter: EntryExpression
    
    # the fields to be the table ordered by
    order_by: List[str]
    
#    def __init__(self, before_values_filter = None, values_map = None, \
#                 after_values_filter = None, groups_map = None, \
#                 after_groupped_filter = None, order_by = None):
#        
#        self.before_values_filter = before_values_filter
#        self.values_map = values_map
#        self.after_values_filter = after_values_filter
#        self.groups_map = groups_map
#        self.after_groupped_filter = after_groupped_filter
#        self.order_by = order_by
        

################################################################################
class BaseQuerier(ABC):
    """ The (base) querier. """
    
    def query(self, dataset_name:str, table:Table, query:Query):
        """ Runs the query on the table """
        
        yield Exception("Implement Me!")
        
    @staticmethod    
    def create_grouppers_names(groups_map):
        return list(filter(lambda gn: (groups_map[gn] is None), \
                           groups_map.keys()))
        
################################################################################
class BaseExpressionNativeRenderer(ABC):
    """ The renderer of the entry expression to native language expression """
    
    @abstractmethod
    def to_native(self, expression, querier, dataset_identifier, entry_identifier):
        """ Renders the given expression to native, specified by the querier """
        
        yield Exception("Implement me!")

################################################################################