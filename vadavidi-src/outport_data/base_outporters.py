"""
The base outporter module. Runs the query and displays the result.
"""

from abc import ABC, abstractmethod

################################################################################
class BaseOutporter(ABC):
    """ The outporter. It it responsible of executing and displaing the queries.
    """

    @abstractmethod
    def run(self, dataset_name, schema, query_name):
        """ Runs the query. """
        yield Exception("Implement me!")
        
################################################################################
