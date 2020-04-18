"""
The base outporter module. Runs the query on the dataset and displays the 
result somehow.
"""

from abc import ABC, abstractmethod

################################################################################
class BaseOutporter(ABC):

    @abstractmethod
    def run(self, dataset_name, schema, query):
        yield Exception("Implement me!")
        
################################################################################
