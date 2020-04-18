"""
The xlang expressions parser.
"""

from builtins import str
from dataclasses import dataclass
import re
from typing import List, Any

from common.datas import Schema


################################################################################
@dataclass
class XLangExpression:
    """ The simple dataclass holding the list of items, plain strs or
     XLangFields."""
     
    # the items itself
    items: List[Any]
    # TODO agregator
    agregator: str 
    
    def to_python_str(self, entry_var_name):
        return " ".join(list(map(
            lambda i: ("{0}['{1}']".format(entry_var_name, i.field_name) \
                        if isinstance(i, XLangField) else i), 
            self.items)))

    def __str__(self):
        return "XLang[" + " ".join(map(str, self.items)) + "]"

################################################################################  
@dataclass
class XLangField:
    """ The vadavidi field of the xlang expression. Has a field name and 
    operation to do with that field. """
    
    # field name
    field_name: str
    # operation
    operation: str

    def __str__(self):
        return "XLF[{0}.{1}]".format(self.field_name, self.operation)
################################################################################    
class XLangParser:
    """ The parser of the xlang expression strings. """
    
    def parse(self, schema, expr):
        """ Parses the expression """
        
        tokens = re.split("\\s+", expr)
        result = []
        for token in tokens:
            if (token.startswith("$")):
                item = self.parse_token(schema, token)
                result.append(item)
                agregator = item.operation # FIXME HACK agregator
            else:
                result.append(token)
        
        return XLangExpression(result, agregator)

    def parse_token(self, schema, token):
        """ Parses one single token (with xlang field) of the expression """
        
        without_dolar = token[1:]
        parts = without_dolar.split('.')
        field_name = parts[0]
        if len(parts) < 2:
            raise ValueError(token + " not valid, no operation after " + field_name)
        
        if field_name not in schema:
            raise ValueError(token + " not valid, " + field_name + " not known")

        operation = parts[1]
        return XLangField(field_name, operation)

################################################################################    
if __name__ == '__main__':
    parser = XLangParser()
    schema = Schema({"karel": "string"})
    
    xle = parser.parse(schema, "abc -  $karel.randomize * jitka + 45")
    print(xle)
    print(xle.to_python_str("eee"))
