"""
The base outporter module. Runs the query on the dataset and displays the 
result somehow.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from builtins import str
from typing import Mapping

################################################################################
@dataclass
class Query:
    x_axis_specifier: str
    y_axis_specifiers: Mapping[str,str]
    
        
    # just __str__
    def __str__(self):
        return "Query: " + self.x_axis_specifier + " -> " + self.y_axis_specifiers

################################################################################
class BaseOutporter(ABC):

    @abstractmethod
    def run(self, dataset_name, schema, query):
        yield Exception("Implement me!")
        
################################################################################
