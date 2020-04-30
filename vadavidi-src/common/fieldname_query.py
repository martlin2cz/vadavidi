""" The query which just simply picks value of the input table. """

from dataclasses import dataclass

from outport_data.base_query import EntryExpression, \
    BaseExpressionNativeRenderer
from outport_data.default_querier import DefaultQuerier
from outport_data.sqllite_querier import SQLLiteQuerier


################################################################################
@dataclass
class FieldRefExpression(EntryExpression):
    """ The entry expression referencing the field of that entry. """

    # the field name
    field_name: str
    
################################################################################
class FieldRefNativeRenderer(BaseExpressionNativeRenderer):
    """ The expression native renderer for the elang expressions """
    
    def supports(self, expression, querier):
        return isinstance(expression, FieldRefExpression) \
               and (isinstance(querier, DefaultQuerier) \
                or isinstance(querier, SQLLiteQuerier)) 
    
    def to_native(self, expression, querier, dataset_identifier, entry_identifier):
        if not isinstance(expression, FieldRefExpression):
            raise ValueError("Not fieldref expression")
        
        if isinstance(querier, DefaultQuerier):
            return self.to_python_native(expression, entry_identifier)
 
        if isinstance(querier, SQLLiteQuerier):
            return self.to_sqllite_native(expression, dataset_identifier, entry_identifier)
        
        raise ValueError("Unsupported querier")

    def to_python_native(self, expression,  entry_identifier):
        """ Converts the expression to pyhon native expression """
        
        return "{0}['{1}']".format(entry_identifier, expression.field_name)
        
    def to_sqllite_native(self, expression,  dataset_identifier, entry_expressions):
        """ Converts the expression to sqllite native expression """
        
        return expression.field_name
    