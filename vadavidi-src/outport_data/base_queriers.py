"""
The base queriers module. The querier executes the query on the specific table.
"""
from abc import ABC, abstractmethod

from dataclasses import dataclass
from builtins import str
from typing import Mapping, Callable

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
    """ The query is in fact just mapping from x-axis field to one or more 
    y-axises, which are just general named expressions. """
    
    # the x-axis field
    x_axis: str
    # the y-axis specifiers (mapping of the y_axis_names to y_axis_agrexps)
    y_axis_specifiers: Mapping[str, AggregatingExpression]
    
    # just __str__
    def __str__(self):
        return "Query: " + self.x_axis + " -> " + str(self.y_axis_specifiers)

################################################################################
class BaseQuerier(ABC):
    """ The (base) querier. """
    
    def query(self, table, query):
        """ Runs the query on the table """
        
        yield Exception("Implement Me!")
        
################################################################################
class BaseExpressionNativeRenderer(ABC):
    """ The renderer of the entry expression to native language expression """
    
    @abstractmethod
    def to_native(self, expression, querier, entry_identifier):
        """ Renders the given expression to native, specified by the querier """
        
        yield Exception("Implement me!")

################################################################################