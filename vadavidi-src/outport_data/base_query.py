""" The query base module. Specifies the abstract queries. """

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Mapping, List


################################################################################
@dataclass
class EntryExpression:
    """ The expression working with the entry. """
    
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
class BaseExpressionNativeRenderer(ABC):
    """ The renderer of the entry expression to native language expression """
    
    @abstractmethod
    def supports(self, expression, querier):
        """ Returns true if supports given expression and querier """
        
        yield Exception("Implement me!")

    
    @abstractmethod
    def to_native(self, expression, querier, dataset_identifier, entry_identifier):
        """ Renders the given expression to native, specified by the querier """
        
        yield Exception("Implement me!")


################################################################################
@dataclass
class ExpressionRenderers(BaseExpressionNativeRenderer):
    """ An simplifier for the more native renderers. Combines support of many 
    of the renderers. """
    
    # the renderers itself
    renderers: List[BaseExpressionNativeRenderer]
    
    def supports(self, expression, querier):
        return True
    
    def to_native(self, expression, querier, dataset_identifier, entry_identifier):
        renderers = list(filter(lambda r: r.supports(expression, querier), \
                                self.renderers))
        
        if len(renderers) < 1:
            raise ValueError("No renderer for " + expression)
        
        if len(renderers) > 1:
            print("Warning, found more than one matching renderers for " + str(expression))

        renderer = renderers[0];
        return renderer.to_native(expression, querier, dataset_identifier, entry_identifier)
    
        