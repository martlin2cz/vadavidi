# the base outporter module
from abc import ABC, abstractmethod
from dataclasses import dataclass
from builtins import str
from typing import Mapping

################################################################################
@dataclass
class Query:
    xAxisSpecifier: str
    yAxisSpecifiers: Mapping[str,str]
    
        
    # just __str__
    def __str__(self):
        return "Query: " + self.xAxisSpecifier + " -> " + self.yAxisSpecifier

################################################################################
class BaseOutporter(ABC):

    @abstractmethod
    def run(self, datasetName, schema, query):
        yield Exception("Implement me!")
        
################################################################################
