"""
The xlang expressions parser.
"""

from builtins import str
from dataclasses import dataclass
import re
from typing import List, Any

from common.datas import Schema
from outport_data.base_queriers import EntryExpression, \
    BaseExpressionNativeRenderer
from outport_data.queriers_impls import DefaultQuerier


################################################################################
@dataclass
class XLangExpression(EntryExpression):
    """ The simple dataclass holding the list of items, plain strs or
     XLangFieldReferences. """
     
    # the items itself
    items: List[Any]
    

    def __str__(self):
        return "XLang[" + " ".join(map(str, self.items)) + "]"


################################################################################
@dataclass
class XLangFieldReference:
    """ Just one item of the XLangExpression, which references the field """
    
    field_name: str

    def __str__(self):
        return "Field[" + self.field_name + "]"

################################################################################
class XLangNativeRenderer(BaseExpressionNativeRenderer):
    """ The expression native renderer for the XLang expressions """
    
    def to_native(self, expression, querier, entry_identifier):
        if not isinstance(expression, XLangExpression):
            raise ValueError("Not XLang expression")
        
        if isinstance(querier, DefaultQuerier):
            return self.to_python_native(expression, entry_identifier)
 
# FIXME SQLiteQuerier        
#        if isinstance(querier, SQLiteQuerier):
#            return self.to_sqllite_native(expression, entry_identifier)
        
        raise ValueError("Unsupported querier")

    def to_python_native(self, expression, entry_identifier):
        """ Converts the expression to pyhon native expression """
        
        return " ".join(list(map(
            lambda i: ("{0}['{1}']".format(entry_identifier, i.field_name) \
                        if isinstance(i, XLangFieldReference) else i),
            expression.items)))
    
    def to_sqllite_native(self, expression, entry_identifier):
        """ Converts the expression to sql native expression """
        
        raise Exception("TODO")
            
        
################################################################################    
class XLangParser:
    """ The parser of the xlang expression strings. """
    
    def parse(self, schema, expr):
        """ Parses the expression """
        
        tokens = re.split("\\s+", expr)
        result = []
        for token in tokens:
            if (token.startswith("€")):
                item = self.parse_token(schema, token)
                result.append(item)
            else:
                result.append(token)
        
        return XLangExpression(result)

    def parse_token(self, schema, token):
        """ Parses one single token (with xlang field) of the expression """
        
        without_euro = token[1:]
        
        if without_euro not in schema:
            raise ValueError("No such field " + without_euro) 
        
        field_name = without_euro
        return XLangFieldReference(field_name)


################################################################################    
if __name__ == '__main__':
    parser = XLangParser()
    schema = Schema({"karel": "string"})
    
    xle = parser.parse(schema, "abc -  €karel * jitka + 45")
    print(xle)
    
    renderer = XLangNativeRenderer()
    print(renderer.to_python_native(xle, "eee"))
    print(renderer.to_sqllite_native(xle, "eee"))
