"""
The base queriers module. The querier executes the query on the specific table.
"""
from abc import ABC

################################################################################
class BaseQuerier(ABC):
    """ The (base) querier. """
    
    def query(self, table, query):
        """ Runs the query on the table """
        
        yield Exception("Implement Me!")
        
################################################################################
        