from builtins import str
from dataclasses import dataclass
import re
from typing import List, Any

from common.datas import Schema


################################################################################
@dataclass
class XLangExpression:
    items: List[Any]

    def __str__(self):
        return "XLang[" + " ".join(map(str, self.items)) + "]"

################################################################################  
@dataclass
class XLangField:
    fieldName: str
    operation: str

    def __str__(self):
        return "XLF[{0}.{1}]".format(self.fieldName, self.operation)
################################################################################    
class XLangParser:
        
    def parse(self, schema, expr):
        tokens = re.split("\\s+", expr)
        result = []
        for token in tokens:
            if (token.startswith("$")):
                item = self.parseToken(schema, token)
                result.append(item)
            else:
                result.append(token)
        
        return XLangExpression(result)

    def parseToken(self, schema, token):
        withoutDolar = token[1:]
        parts = withoutDolar.split('.')
        fieldName = parts[0]
        if len(parts) < 2:
            raise ValueError(token + " not valid, no operation after " + fieldName)
        
        if fieldName not in schema.listFieldNames():
            raise ValueError(token + " not valid, " + fieldName + " not known")

        operation = parts[1]
        return XLangField(fieldName, operation)

################################################################################    
if __name__ == '__main__':
    parser = XLangParser()
    schema = Schema({"karel": "string"})
    
    xle = parser.parse(schema, "abc   $karel.randomize jitka + 45")
    print(xle)
